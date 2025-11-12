"""Jinja2 template linter.

This script checks all Jinja2 templates in the templates directory
for syntax errors and provides detailed error messages.
"""

from pathlib import Path
from jinja2 import Environment, FileSystemLoader, TemplateSyntaxError


def lint_template(template_path: Path, env: Environment) -> tuple[bool, str | None]:
    """Lint a single Jinja2 template.

    Args:
        template_path: Path to template file
        env: Jinja2 environment

    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        template_name = template_path.name
        template = env.get_template(template_name)
        return True, None
    except TemplateSyntaxError as e:
        error_msg = f"Line {e.lineno}: {e.message}"
        if hasattr(e, 'source'):
            # Show context around the error
            lines = e.source.splitlines()
            start = max(0, e.lineno - 3)
            end = min(len(lines), e.lineno + 2)
            context = "\n".join(f"{i+1:4d}: {lines[i]}" for i in range(start, end))
            error_msg += f"\n\nContext:\n{context}"
        return False, error_msg
    except Exception as e:
        return False, f"Unexpected error: {e}"


def main():
    """Lint all templates in the templates directory."""
    project_root = Path(__file__).parent.parent
    template_dir = project_root / "templates"

    if not template_dir.exists():
        print(f"✗ Template directory not found: {template_dir}")
        return 1

    # Setup Jinja2 environment
    env = Environment(
        loader=FileSystemLoader(str(template_dir)),
        trim_blocks=True,
        lstrip_blocks=True,
        keep_trailing_newline=True
    )

    # Find all .j2 files
    template_files = list(template_dir.glob("*.j2"))

    if not template_files:
        print(f"✗ No .j2 files found in {template_dir}")
        return 1

    print(f"Linting {len(template_files)} template(s)...\n")

    all_valid = True
    for template_path in sorted(template_files):
        is_valid, error_msg = lint_template(template_path, env)

        if is_valid:
            print(f"✓ {template_path.name}")
        else:
            print(f"✗ {template_path.name}")
            print(f"  {error_msg}\n")
            all_valid = False

    print("\n" + "=" * 60)
    if all_valid:
        print(f"✓ All {len(template_files)} template(s) passed!")
        return 0
    else:
        print("✗ Some templates have errors")
        return 1


if __name__ == "__main__":
    exit(main())
