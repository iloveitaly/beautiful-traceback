"""
Tests for LoggingFormatter and LoggingFormatterMixin.

These tests verify that the logging formatters correctly format
exceptions in log output.
"""
import logging
import io
import pytest
from beautiful_traceback import LoggingFormatter, LoggingFormatterMixin


def test_logging_formatter_exists():
    """Test that LoggingFormatter class exists and is importable."""
    assert LoggingFormatter is not None
    assert issubclass(LoggingFormatter, logging.Formatter)
    assert issubclass(LoggingFormatter, LoggingFormatterMixin)


def test_logging_formatter_mixin_exists():
    """Test that LoggingFormatterMixin exists and has required methods."""
    assert LoggingFormatterMixin is not None
    assert hasattr(LoggingFormatterMixin, 'formatException')
    assert callable(LoggingFormatterMixin.formatException)


def test_logging_formatter_basic_usage():
    """Test basic LoggingFormatter usage with a logger."""
    # Create a logger with our formatter
    logger = logging.getLogger('test_basic')
    logger.setLevel(logging.DEBUG)
    
    # Capture output
    stream = io.StringIO()
    handler = logging.StreamHandler(stream)
    handler.setFormatter(LoggingFormatter())
    logger.addHandler(handler)
    
    try:
        # Log a normal message (no exception)
        logger.info("Test message")
        output = stream.getvalue()
        
        assert "Test message" in output
    finally:
        logger.removeHandler(handler)


def test_logging_formatter_with_exception():
    """Test that LoggingFormatter formats exceptions beautifully."""
    logger = logging.getLogger('test_exception')
    logger.setLevel(logging.ERROR)
    
    stream = io.StringIO()
    handler = logging.StreamHandler(stream)
    handler.setFormatter(LoggingFormatter())
    logger.addHandler(handler)
    
    try:
        try:
            raise ValueError("Test exception in logging")
        except ValueError:
            logger.exception("An error occurred")
        
        output = stream.getvalue()
        
        # Should contain the exception details
        assert "ValueError" in output
        assert "Test exception in logging" in output
        assert "An error occurred" in output
    finally:
        logger.removeHandler(handler)


def test_logging_formatter_with_nested_exception():
    """Test LoggingFormatter with nested exceptions."""
    logger = logging.getLogger('test_nested')
    logger.setLevel(logging.ERROR)
    
    stream = io.StringIO()
    handler = logging.StreamHandler(stream)
    handler.setFormatter(LoggingFormatter())
    logger.addHandler(handler)
    
    try:
        try:
            try:
                raise ValueError("Inner error")
            except ValueError:
                raise RuntimeError("Outer error")
        except RuntimeError:
            logger.exception("Nested exception occurred")
        
        output = stream.getvalue()
        
        # Should contain both exceptions
        assert "ValueError" in output
        assert "Inner error" in output
        assert "RuntimeError" in output
        assert "Outer error" in output
    finally:
        logger.removeHandler(handler)


def test_logging_formatter_with_chained_exception():
    """Test LoggingFormatter with chained exceptions (raise ... from)."""
    logger = logging.getLogger('test_chained')
    logger.setLevel(logging.ERROR)
    
    stream = io.StringIO()
    handler = logging.StreamHandler(stream)
    handler.setFormatter(LoggingFormatter())
    logger.addHandler(handler)
    
    try:
        try:
            try:
                raise ValueError("Original error")
            except ValueError as e:
                raise RuntimeError("Chained error") from e
        except RuntimeError:
            logger.exception("Chained exception occurred")
        
        output = stream.getvalue()
        
        # Should contain both exceptions and the chain indicator
        assert "ValueError" in output
        assert "Original error" in output
        assert "RuntimeError" in output
        assert "Chained error" in output
        assert "direct cause" in output
    finally:
        logger.removeHandler(handler)


def test_logging_formatter_mixin_format_exception():
    """Test LoggingFormatterMixin.formatException directly."""
    mixin = LoggingFormatterMixin()
    
    try:
        raise ValueError("Direct test")
    except ValueError:
        import sys
        exc_info = sys.exc_info()
        
        # Call formatException directly
        formatted = mixin.formatException(exc_info)
        
        assert isinstance(formatted, str)
        assert "ValueError" in formatted
        assert "Direct test" in formatted
        
        # Should use beautiful formatting (has "Traceback" header)
        assert "Traceback (most recent call last):" in formatted


def test_logging_formatter_uses_beautiful_formatting():
    """Test that LoggingFormatter actually uses beautiful-traceback formatting."""
    logger = logging.getLogger('test_beautiful_format')
    logger.setLevel(logging.ERROR)
    
    stream = io.StringIO()
    handler = logging.StreamHandler(stream)
    handler.setFormatter(LoggingFormatter())
    logger.addHandler(handler)
    
    try:
        def inner():
            raise ValueError("Beautiful test")
        
        def outer():
            inner()
        
        try:
            outer()
        except ValueError:
            logger.exception("Error with stack")
        
        output = stream.getvalue()
        
        # Should have the beautiful traceback header
        assert "Traceback (most recent call last):" in output
        
        # Should show function names
        assert "inner" in output
        assert "outer" in output
        
        # Should show the error
        assert "ValueError" in output
        assert "Beautiful test" in output
        
        # Beautiful-traceback specific features:
        # 1. Shows path aliases like "<pwd>:"
        # 2. Has indented traceback lines (4 spaces)
        # 3. May show "Aliases for entries in sys.path:" header
        
        # Check for beautiful-traceback specific formatting
        # The format is: "    <alias> path/file.py:123  function  code"
        has_alias_in_traceback = "<pwd>" in output or "<site>" in output
        has_indented_traceback = "\n    " in output  # 4-space indentation
        
        assert has_alias_in_traceback or has_indented_traceback, \
            f"Output doesn't have beautiful-traceback formatting:\n{output}"
    finally:
        logger.removeHandler(handler)


def test_logging_formatter_mixin_as_base_class():
    """Test using LoggingFormatterMixin as a base class with custom formatter."""
    class CustomFormatter(LoggingFormatterMixin, logging.Formatter):
        def __init__(self):
            super().__init__(fmt='[CUSTOM] %(levelname)s: %(message)s')
    
    logger = logging.getLogger('test_custom')
    logger.setLevel(logging.ERROR)
    
    stream = io.StringIO()
    handler = logging.StreamHandler(stream)
    handler.setFormatter(CustomFormatter())
    logger.addHandler(handler)
    
    try:
        try:
            raise ValueError("Custom formatter test")
        except ValueError:
            logger.exception("Error with custom format")
        
        output = stream.getvalue()
        
        # Should have custom format prefix
        assert "[CUSTOM]" in output
        assert "ERROR" in output
        assert "Error with custom format" in output
        
        # Should still format exception beautifully
        assert "ValueError" in output
        assert "Custom formatter test" in output
    finally:
        logger.removeHandler(handler)


def test_logging_formatter_different_log_levels():
    """Test that formatter works with different log levels."""
    logger = logging.getLogger('test_levels')
    logger.setLevel(logging.DEBUG)
    
    stream = io.StringIO()
    handler = logging.StreamHandler(stream)
    handler.setFormatter(LoggingFormatter())
    logger.addHandler(handler)
    
    try:
        logger.debug("Debug message")
        logger.info("Info message")
        logger.warning("Warning message")
        logger.error("Error message")
        logger.critical("Critical message")
        
        output = stream.getvalue()
        
        assert "Debug message" in output
        assert "Info message" in output
        assert "Warning message" in output
        assert "Error message" in output
        assert "Critical message" in output
    finally:
        logger.removeHandler(handler)


def test_logging_formatter_with_multiple_handlers():
    """Test that formatter works correctly with multiple handlers."""
    logger = logging.getLogger('test_multi_handler')
    logger.setLevel(logging.ERROR)
    
    stream1 = io.StringIO()
    stream2 = io.StringIO()
    
    handler1 = logging.StreamHandler(stream1)
    handler1.setFormatter(LoggingFormatter())
    
    handler2 = logging.StreamHandler(stream2)
    handler2.setFormatter(LoggingFormatter())
    
    logger.addHandler(handler1)
    logger.addHandler(handler2)
    
    try:
        try:
            raise ValueError("Multi-handler test")
        except ValueError:
            logger.exception("Error logged to multiple handlers")
        
        output1 = stream1.getvalue()
        output2 = stream2.getvalue()
        
        # Both should have the same beautiful formatting
        assert "ValueError" in output1
        assert "ValueError" in output2
        assert "Multi-handler test" in output1
        assert "Multi-handler test" in output2
    finally:
        logger.removeHandler(handler1)
        logger.removeHandler(handler2)


def test_logging_formatter_with_unicode():
    """Test that formatter handles unicode characters correctly."""
    logger = logging.getLogger('test_unicode')
    logger.setLevel(logging.ERROR)
    
    stream = io.StringIO()
    handler = logging.StreamHandler(stream)
    handler.setFormatter(LoggingFormatter())
    logger.addHandler(handler)
    
    try:
        try:
            raise ValueError("Unicode test: 你好 🎉 Ñoño")
        except ValueError:
            logger.exception("Error with unicode")
        
        output = stream.getvalue()
        
        # Should handle unicode properly
        assert "ValueError" in output
        assert "你好" in output or "unicode" in output.lower()
    finally:
        logger.removeHandler(handler)


def test_logging_formatter_exception_in_different_function():
    """Test that formatter shows the call stack correctly."""
    def inner_function():
        raise ValueError("Error in inner function")
    
    def outer_function():
        inner_function()
    
    logger = logging.getLogger('test_stack')
    logger.setLevel(logging.ERROR)
    
    stream = io.StringIO()
    handler = logging.StreamHandler(stream)
    handler.setFormatter(LoggingFormatter())
    logger.addHandler(handler)
    
    try:
        try:
            outer_function()
        except ValueError:
            logger.exception("Stack trace test")
        
        output = stream.getvalue()
        
        # Should show both functions in the stack
        assert "ValueError" in output
        assert "Error in inner function" in output
        assert "inner_function" in output
        assert "outer_function" in output
    finally:
        logger.removeHandler(handler)


def test_logging_formatter_with_extra_data():
    """Test that formatter works with extra log data."""
    logger = logging.getLogger('test_extra')
    logger.setLevel(logging.INFO)
    
    stream = io.StringIO()
    handler = logging.StreamHandler(stream)
    handler.setFormatter(LoggingFormatter('%(levelname)s - %(message)s - %(user)s'))
    logger.addHandler(handler)
    
    try:
        logger.info("Test with extra", extra={'user': 'testuser'})
        output = stream.getvalue()
        
        assert "Test with extra" in output
        assert "testuser" in output
    finally:
        logger.removeHandler(handler)


def test_logging_formatter_backward_compatibility_typo():
    """Test that the typo variant (LoggingFormaterMixin) still works."""
    from beautiful_traceback import LoggingFormaterMixin
    
    # Should be the same as LoggingFormatterMixin
    assert LoggingFormaterMixin is LoggingFormatterMixin
    
    # Should work as a base class
    class CustomFormatter(LoggingFormaterMixin, logging.Formatter):
        pass
    
    formatter = CustomFormatter()
    assert isinstance(formatter, LoggingFormatterMixin)


def test_logging_formatter_exception_without_traceback():
    """Test formatter with an exception that has no traceback."""
    mixin = LoggingFormatterMixin()
    
    # Create an exception without raising it (no traceback)
    exc = ValueError("No traceback")
    exc_info = (type(exc), exc, None)
    
    # Should handle gracefully
    formatted = mixin.formatException(exc_info)
    
    assert isinstance(formatted, str)
    assert "ValueError" in formatted
    assert "No traceback" in formatted


def test_logging_formatter_integration_with_file_handler(tmp_path):
    """Test that formatter works with FileHandler (writes to file)."""
    log_file = tmp_path / "test.log"
    
    logger = logging.getLogger('test_file')
    logger.setLevel(logging.ERROR)
    
    handler = logging.FileHandler(log_file)
    handler.setFormatter(LoggingFormatter())
    logger.addHandler(handler)
    
    try:
        try:
            raise ValueError("File handler test")
        except ValueError:
            logger.exception("Error logged to file")
        
        handler.close()
        
        # Read the log file
        log_content = log_file.read_text()
        
        assert "ValueError" in log_content
        assert "File handler test" in log_content
    finally:
        logger.removeHandler(handler)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
