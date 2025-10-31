"""
Test for infinite loop bug with httpx.ConnectError and circular exception chains.
"""
import pytest
import beautiful_traceback


def test_httpx_connect_error_reproduction():
    """
    Try to reproduce the infinite loop with httpx.ConnectError.
    
    Note: We'll mock httpx since it's not a dependency.
    """
    # Mock httpx.ConnectError
    class MockConnectError(Exception):
        """Mock of httpx.ConnectError"""
        pass
    
    # Install beautiful traceback
    beautiful_traceback.install()
    
    try:
        # This should not cause an infinite loop
        raise MockConnectError("Connection failed")
    except MockConnectError as e:
        # Get the formatted traceback
        tb_str = beautiful_traceback.formatting.exc_to_traceback_str(
            e, 
            e.__traceback__, 
            color=False
        )
        assert "MockConnectError" in tb_str
        assert "Connection failed" in tb_str


def test_circular_exception_chain():
    """
    Test that circular exception chains don't cause infinite loops.
    
    This is the real potential issue - if __cause__ or __context__ 
    creates a circular reference.
    """
    # Create two exceptions
    exc1 = ValueError("First error")
    exc2 = RuntimeError("Second error")
    
    # Create a circular reference via __cause__
    # This is technically possible (though weird) in Python
    try:
        raise exc1
    except ValueError:
        pass
    
    try:
        raise exc2
    except RuntimeError:
        pass
    
    # Manually create circular reference
    exc1.__cause__ = exc2
    exc2.__cause__ = exc1
    
    # This should not infinite loop
    
    # Set a timeout to catch infinite loops
    import signal
    
    def timeout_handler(signum, frame):
        raise TimeoutError("Infinite loop detected!")
    
    # Only set alarm on Unix systems
    if hasattr(signal, 'SIGALRM'):
        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(2)  # 2 second timeout
    
    try:
        tb_str = beautiful_traceback.formatting.exc_to_traceback_str(
            exc1,
            exc1.__traceback__,
            color=False
        )
        # Should complete without hanging
        assert isinstance(tb_str, str)
    finally:
        if hasattr(signal, 'SIGALRM'):
            signal.alarm(0)  # Cancel alarm


def test_self_referencing_exception():
    """
    Test exception that references itself.
    """
    exc = ValueError("Self-referencing error")
    
    try:
        raise exc
    except ValueError:
        pass
    
    # Make exception reference itself
    exc.__cause__ = exc
    
    # This should not infinite loop
    import signal
    
    def timeout_handler(signum, frame):
        raise TimeoutError("Infinite loop detected!")
    
    if hasattr(signal, 'SIGALRM'):
        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(2)
    
    try:
        tb_str = beautiful_traceback.formatting.exc_to_traceback_str(
            exc,
            exc.__traceback__,
            color=False
        )
        # Should complete without hanging
        assert isinstance(tb_str, str)
    finally:
        if hasattr(signal, 'SIGALRM'):
            signal.alarm(0)


def test_deeply_nested_exception_chain():
    """
    Test a very deep (but not circular) exception chain.
    """
    # Create a chain of 100 exceptions
    exc = ValueError("Base error")
    try:
        raise exc
    except:
        pass
    
    for i in range(100):
        new_exc = RuntimeError(f"Error {i}")
        try:
            raise new_exc from exc
        except:
            pass
        exc = new_exc
    
    # This should handle deep chains without issues
    tb_str = beautiful_traceback.formatting.exc_to_traceback_str(
        exc,
        exc.__traceback__,
        color=False
    )
    
    assert isinstance(tb_str, str)
    assert len(tb_str) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
