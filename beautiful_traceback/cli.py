"""CLI commands for beautiful-traceback installation and configuration."""

import sys
from pathlib import Path


def inject_pth() -> None:
    """
    Inject beautiful-traceback into the current Python environment via .pth file.

    Creates a .pth file in site-packages that automatically imports beautiful_traceback
    on interpreter startup. Only works within virtual environments.
    """
    if not _is_in_venv():
        print("Error: Not running in a virtual environment", file=sys.stderr)
        print(
            "Beautiful traceback pth injection only works in virtual environments",
            file=sys.stderr,
        )
        sys.exit(1)

    site_packages = _get_site_packages()
    pth_file = site_packages / "beautiful_traceback_injection.pth"
    py_file = site_packages / "_beautiful_traceback_injection.py"

    _create_injection_files(py_file, pth_file)

    print(f"Beautiful traceback injection installed: {pth_file}")


def _is_in_venv() -> bool:
    """Check if running in a virtual environment."""
    return hasattr(sys, "real_prefix") or (
        hasattr(sys, "base_prefix") and sys.base_prefix != sys.prefix
    )


def _get_site_packages() -> Path:
    """Get the site-packages directory for the current Python environment."""
    import site

    site_packages_list = site.getsitepackages()

    if not site_packages_list:
        print("Error: Could not find site-packages directory", file=sys.stderr)
        sys.exit(1)

    return Path(site_packages_list[0])


def _create_injection_files(py_file: Path, pth_file: Path) -> None:
    """Create the Python injection file and .pth file."""
    py_content = """def run_startup_script():
  try:
    import beautiful_traceback
    beautiful_traceback.install(only_tty=False)
  except ImportError:
    pass

run_startup_script()
"""

    py_file.write_text(py_content)
    pth_file.write_text("import _beautiful_traceback_injection\n")


def main() -> None:
    """Main CLI entrypoint."""
    inject_pth()


if __name__ == "__main__":
    main()
