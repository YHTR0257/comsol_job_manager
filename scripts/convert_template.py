"""Convert reference Java file to Jinja2 template.

This script reads tmp/ref/hosoda_ref.java and converts it to a proper
Jinja2 template in templates/simulation.java.j2.
"""

from pathlib import Path
import re


def convert_to_jinja2_template(reference_path: Path, output_path: Path):
    """Convert reference Java file to Jinja2 template.

    Args:
        reference_path: Path to reference Java file
        output_path: Path to output Jinja2 template
    """
    # Read reference file
    with open(reference_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Define placeholder replacements - only replace VALUES, not variable names
    # Format: (pattern, replacement, description)
    replacements = [
        # Class name
        (r'public class \w+', 'public class {{ class_name }}', 'class name'),

        # String literals
        (r'String file = "rve_.*?";', 'String file = "{{ file_name }}";', 'file name'),
        (r'String path = ".*?";', 'String path = "{{ output_path }}";', 'output path'),
        (r'String stlfile = ".*?";', 'String stlfile = "{{ stl_path }}";', 'stl path'),

        # Value assignments (right-hand side only)
        (r'double lconst = OOO\.;', 'double lconst = {{ lattice_constant }};', 'lattice constant'),
        (r'double pratio = POISSON\./100\.;', 'double pratio = {{ poisson_ratio }}/100.;', 'poisson ratio'),
        (r'double delta_ = 0\.001;', 'double delta_ = {{ delta }};', 'delta value'),
        (r'rs = AAA\./100\.;', 'rs = {{ sphere_radius_ratio }}/100.;', 'sphere radius'),
        (r'rb = BBB\./100\.;', 'rb = {{ bond_radius_ratio }}/100.;', 'bond radius'),
        (r'double dpos = 0\.SHIFT;', 'double dpos = {{ shift }};', 'shift value'),
        (r'int nnn = NNN;', 'int nnn = {{ num_cells }};', 'num cells'),

        # String literals in conditionals
        (r'which_lattice == "LATTICE"', 'which_lattice == "{{ lattice_type }}"', 'lattice type'),
        (r'String which_lattice = "LATTICE";', 'String which_lattice = "{{ lattice_type }}";', 'lattice type var'),

        # dstep array - special handling (note the space to avoid {{{ syntax error)
        (r'String\[\] dstep = new String\[\]\{"0, 1"\};', 'String[] dstep = new String[]{ {{ dstep }} };', 'dstep array'),

        # References to variables (use in expressions)
        (r'\bd_min = 0 \* lconst;', 'd_min = {{ d_min }};', 'd_min init'),
        (r'\bd_max = 1 \* lconst;', 'd_max = {{ d_max }};', 'd_max init'),

        # In conditionals for lattice types
        (r'd_min = \.7 \* lconst;', 'd_min = 0.7 * lconst;', 'fcc d_min'),
        (r'd_max = \.71 \* lconst;', 'd_max = 0.71 * lconst;', 'fcc d_max'),
    ]

    # Apply replacements
    modified_content = content

    for pattern, replacement, description in replacements:
        count = len(re.findall(pattern, modified_content))
        modified_content = re.sub(pattern, replacement, modified_content)
        if count > 0:
            print(f"  - {description}: {count} replacement(s)")



    # Escape Java array literals {{ }} for Jinja2
    # Pattern: new Type[][]{{...}, {...}, {...}}
    # These need to be wrapped in {% raw %}{% endraw %}

    # Match nested braces properly
    # Pattern: new Type[][]{{ ... }}  where ... can contain nested {}
    def escape_java_arrays(content):
        # Find all "new Type[][]{{" and escape until matching "}}"
        result = []
        i = 0
        while i < len(content):
            # Look for "new Type[][]{{" pattern
            match = re.match(r'(new \w+\[\]\[\])\{\{', content[i:])
            if match:
                prefix = match.group(1)
                result.append(prefix)
                i += len(match.group(0))

                # Now find the matching }}
                brace_count = 2  # We've seen {{
                array_content = []
                while i < len(content) and brace_count > 0:
                    char = content[i]
                    if char == '{':
                        brace_count += 1
                    elif char == '}':
                        brace_count -= 1
                    array_content.append(char)
                    i += 1

                # Wrap in raw tags
                inner = ''.join(array_content)
                result.append('{% raw %}{{' + inner[:-2] + '}}{% endraw %}')
            else:
                result.append(content[i])
                i += 1

        return ''.join(result)

    modified_content = escape_java_arrays(modified_content)

    print(f"\n  Applied array literal escaping")

    # Write output
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(modified_content)

    print(f"✓ Converted {reference_path} to {output_path}")
    print(f"  Total replacements: {len(replacements)}")


def main():
    project_root = Path(__file__).parent.parent
    reference_path = project_root / "tmp" / "ref" / "hosoda_ref.java"
    output_path = project_root / "templates" / "simulation.java.j2"

    if not reference_path.exists():
        print(f"✗ Reference file not found: {reference_path}")
        return 1

    convert_to_jinja2_template(reference_path, output_path)

    print(f"\n✓ Template conversion completed successfully!")
    return 0


if __name__ == "__main__":
    exit(main())
