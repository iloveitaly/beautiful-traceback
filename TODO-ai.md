# Beautiful Traceback - AI-Generated TODO List

*Generated: 2025-10-31*

This document contains improvements and fixes identified through codebase analysis.

---

## 🔥 Critical Issues (Must Fix)

- [ ] **Remove debug print statement in pytest plugin**
  - File: `beautiful_traceback/pytest_plugin.py:55-58`
  - Issue: `print("hello this is the value", ...)` left in production code
  - Impact: HIGH - Pollutes test output
  - Priority: 🔥🔥🔥 IMMEDIATE

- [ ] **Investigate and fix infinite loop bug**
  - File: See `TODO` file
  - Issue: `raise httpx.ConnectError("Connection failed")` causes infinite loop
  - Impact: CRITICAL - Can hang applications
  - Action: Add recursion protection in exception handling
  - Priority: 🔥🔥 HIGH

---

## ⚠️ Code Quality Issues

- [ ] **Fix pytest plugin option descriptions**
  - File: `beautiful_traceback/pytest_plugin.py:25, 32`
  - Issue: Says "pretty traceback plugin" instead of "beautiful"
  - Issue: Second option has wrong/duplicate description
  - Impact: MEDIUM - Confusing documentation
  - Priority: ⚠️ MEDIUM

- [ ] **Set up linting and formatting tools**
  - Add `ruff` configuration to `pyproject.toml`
  - Add pre-commit hooks (optional)
  - Set up CI/CD for automated checks
  - Impact: MEDIUM - Code quality can drift
  - Priority: ⚠️ MEDIUM

- [ ] **Add type checking configuration**
  - Add `mypy` to dev dependencies
  - Configure `pyproject.toml` with mypy settings
  - Add type checking to development workflow
  - Impact: MEDIUM - Better code reliability
  - Priority: ⚠️ MEDIUM

- [ ] **Decide on CLI command functionality**
  - File: `pyproject.toml:14` + `beautiful_traceback/__init__.py:main()`
  - Current: Only prints "Beautiful Traceback installed!"
  - Options: (1) Remove script entry point, (2) Make it useful (demo, tests, etc.)
  - Impact: LOW - Wasted potential
  - Priority: 💡 LOW

- [ ] **Clean up old TODO comments**
  - File: `beautiful_traceback/parsing.py:12` - "TODO (mb 2020-08-12)"
  - File: `tests/test_formatting.py` - "TODO (mb 2020-08-14)"
  - Action: Either fix, remove, or update comments
  - Impact: LOW - Technical debt
  - Priority: 💡 LOW

---

## 📝 Missing Features

- [ ] **Add option to disable path aliases in traceback**
  - File: See `TODO` file
  - Feature: Add `show_aliases=True` parameter to `install()`
  - Impact: MEDIUM - Some users may prefer full paths always
  - Priority: ⚠️ MEDIUM

- [ ] **Filter pytest internal frames from tracebacks**
  - File: See `TODO` file
  - Issue: Stack traces include too much pytest internal code
  - Solution: Implement `_is_purely_internal_error()` logic suggested in TODO
  - Impact: MEDIUM - Makes test failures harder to read
  - Priority: ⚠️ MEDIUM

- [ ] **Improve IPython integration**
  - File: See `TODO` file reference to Rich's approach
  - Issue: IPython extension may not work optimally
  - Action: Review https://github.com/Textualize/rich/.../traceback.py#L45
  - Impact: MEDIUM - IPython is a major use case
  - Priority: ⚠️ MEDIUM

---

## 🧪 Testing

- [ ] **Add pytest plugin tests**
  - Test automatic activation
  - Test configuration options
  - Test with failing tests
  - Test with collection errors
  - Priority: ⚠️ MEDIUM

- [ ] **Add IPython extension tests**
  - Test load_ipython_extension
  - Test unload_ipython_extension
  - Test behavior in notebook environment
  - Priority: ⚠️ MEDIUM

- [ ] **Add LoggingFormatter tests**
  - Test LoggingFormatter class
  - Test LoggingFormatterMixin class
  - Test with various log levels
  - Test exception formatting in logs
  - Priority: ⚠️ MEDIUM

- [ ] **Add configuration option tests**
  - Test color=True/False
  - Test only_tty=True/False
  - Test local_stack_only=True/False
  - Test envvar parameter
  - Test NO_COLOR environment variable
  - Priority: ⚠️ MEDIUM

- [ ] **Add error condition tests**
  - Test with various exception types
  - Test with chained exceptions
  - Test with nested exceptions
  - Test edge cases
  - Priority: ⚠️ MEDIUM

---

## 🧹 Code Organization

- [ ] **Add useful Justfile recipes**
  - `test` - Run tests with pytest
  - `lint` - Run ruff check
  - `fmt` - Format code with ruff
  - `demo` - Run interactive demo
  - `build` - Build package
  - `typecheck` - Run mypy (if added)
  - Priority: 💡 LOW-MEDIUM

- [ ] **Organize documentation files**
  - Consider moving `AGENT.md`, `CLAUDE.md`, `GEMINI.md` to `docs/` or `.github/`
  - Convert `TODO` to `TODO.md` with proper markdown
  - Add project documentation structure
  - Priority: 💡 LOW

- [ ] **Update .gitignore**
  - Add `README_original.md` (if it exists)
  - Add `*.md~` (backup files)
  - Add `.DS_Store` (macOS)
  - Add `.ruff_cache/` (already present)
  - Add `.cursor/` (already present)
  - Consider: `AGENT.md`, `CLAUDE.md`, `GEMINI.md`
  - Priority: 💡 LOW

---

## 📦 Package Configuration

- [ ] **Add ruff configuration to pyproject.toml**
  ```toml
  [tool.ruff]
  line-length = 100
  target-version = "py39"
  
  [tool.ruff.lint]
  select = ["E", "F", "I", "N", "W", "UP"]
  ```
  - Priority: ⚠️ MEDIUM

- [ ] **Add mypy configuration to pyproject.toml**
  ```toml
  [tool.mypy]
  python_version = "3.9"
  warn_return_any = true
  warn_unused_configs = true
  disallow_untyped_defs = false  # Start lenient
  ```
  - Priority: ⚠️ MEDIUM

- [ ] **Add pytest configuration to pyproject.toml**
  ```toml
  [tool.pytest.ini_options]
  testpaths = ["tests"]
  python_files = ["test_*.py"]
  addopts = "-v --tb=short"
  ```
  - Priority: 💡 LOW

- [ ] **Update dev dependencies in pyproject.toml**
  ```toml
  [dependency-groups]
  dev = [
      "pytest>=8.3.3",
      "ruff>=0.1.0",
      "mypy>=1.0",
  ]
  ```
  - Priority: ⚠️ MEDIUM

---

## 📚 Documentation Improvements

- [ ] **Document LoggingFormatterMixin usage**
  - Add examples beyond basic LoggingFormatter
  - Show mixin pattern use cases
  - Document when to use Formatter vs Mixin
  - Priority: 💡 LOW

- [ ] **Add CONTRIBUTING.md**
  - Development setup instructions
  - Code style guidelines
  - Testing requirements
  - PR process
  - Priority: 💡 LOW

- [ ] **Add CHANGELOG.md**
  - Track version changes
  - Document breaking changes
  - List new features and fixes
  - Priority: 💡 LOW

---

## 🎯 Priority Summary

### Immediate (Do Today):
1. Remove debug print statement
2. Investigate infinite loop bug

### High Priority (This Week):
3. Fix pytest plugin descriptions
4. Set up linting/formatting
5. Add type checking
6. Update dev dependencies

### Medium Priority (This Month):
7. Implement path aliases toggle
8. Filter pytest internals
9. Improve IPython integration
10. Expand test coverage
11. Add configuration to pyproject.toml

### Low Priority (When Time Permits):
12. Enhance or remove CLI command
13. Clean up TODO comments
14. Add Justfile recipes
15. Organize project files
16. Update .gitignore
17. Add documentation files

---

## 📋 Implementation Notes

**Guidelines from project instructions:**
- Make **minimal changes** - only change what's necessary
- **Don't break working code** - all fixes should be surgical
- **Test before/after** - run tests to ensure nothing breaks
- **Focus on task** - don't get distracted by unrelated issues

**Critical takeaway:** The debug print statement is the only thing that MUST be fixed immediately. Everything else is enhancement territory that should be carefully considered.

---

## 🔗 Related Files

- Original TODO: `TODO`
- Project README: `README.md`
- Build config: `pyproject.toml`
- Dev tasks: `Justfile`
- Main module: `beautiful_traceback/__init__.py`
- Pytest plugin: `beautiful_traceback/pytest_plugin.py`
