## 🔥 Critical Issues (Must Fix)

- [x] **Remove debug print statement in pytest plugin**
  - File: `beautiful_traceback/pytest_plugin.py:55-58`
  - Issue: `print("hello this is the value", ...)` left in production code
  - Impact: HIGH - Pollutes test output
  - Priority: 🔥🔥🔥 IMMEDIATE
  - ✅ **COMPLETED: 2025-10-31** - Removed debug print, all tests passing

- [ ] **Investigate and fix infinite loop bug**
  - File: See `TODO` file
  - Issue: `raise httpx.ConnectError("Connection failed")` causes infinite loop
  - Impact: CRITICAL - Can hang applications
  - Action: Add recursion protection in exception handling
  - Priority: 🔥🔥 HIGH

---

## ⚠️ Code Quality Issues

- [x] **Fix pytest plugin option descriptions**
  - File: `beautiful_traceback/pytest_plugin.py:25, 32`
  - Issue: Says "pretty traceback plugin" instead of "beautiful"
  - Issue: Second option has wrong/duplicate description
  - Impact: MEDIUM - Confusing documentation
  - Priority: ⚠️ MEDIUM
  - ✅ **COMPLETED: 2025-10-31** - Updated descriptions to be accurate and clear

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



## 📚 Documentation Improvements

- [ ] **Document LoggingFormatterMixin usage**
  - Add examples beyond basic LoggingFormatter
  - Show mixin pattern use cases
  - Document when to use Formatter vs Mixin
  - Priority: 💡 LOW
