import os
import json
import jinja2
from jinja2 import Environment, FileSystemLoader
import webbrowser
import base64
import re

def escape_latex(text):
    """Escape special LaTeX characters in a string."""
    if not isinstance(text, str):
        return text
    replacements = {
        '%': r'\%',
        '_': r'\_',
        '&': r'\&',
        '#': r'\#',
        '{': r'\{',
        '}': r'\}',
        '$': r'\$',
    }
    # Use regex to replace special characters
    return re.sub(r'([%_&#{}$])', lambda match: replacements[match.group()], text)

def escape_context(context):
    """Recursively escape special LaTeX characters in the context dictionary."""
    if isinstance(context, dict):
        return {key: escape_context(value) for key, value in context.items()}
    elif isinstance(context, list):
        return [escape_context(item) for item in context]
    else:
        return escape_latex(context)


# Base directories
TEMPLATES_DIR = "templates"
OUTPUT_DIR = "output"

def get_available_templates():
    """Fetch the list of available LaTeX templates."""
    return [f for f in os.listdir(TEMPLATES_DIR) if f.endswith(".tex")]

def load_data(file_path):
    """
    Load resume data from a JSON file.

    Args:
        file_path (str): Path to the JSON file.

    Returns:
        dict: Loaded data as a dictionary.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return {}
    except json.JSONDecodeError:
        print(f"Error: Failed to parse JSON file '{file_path}'.")
        return {}

def render_template(template_name, context, output_file):
    """
    Render the selected LaTeX template with the provided context.

    Args:
        template_name (str): Name of the LaTeX template file.
        context (dict): Dictionary containing placeholder values.
        output_file (str): Path to save the rendered LaTeX file.
    """
    # Load the template with custom delimiters
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(TEMPLATES_DIR),
        block_start_string='<<%',
        block_end_string='%>>',
        variable_start_string='<<',
        variable_end_string='>>'
    )
    template = env.get_template(template_name)

    # Render the template with context
    rendered_content = template.render(context)

    # Save to output file
    with open(output_file, "w") as f:
        f.write(rendered_content)
    print(f"Generated LaTeX file: {output_file}")


def open_in_overleaf(file_path):
    """
    Open the LaTeX file in Overleaf using a browser-based snippet.

    Args:
        file_path (str): Path to the generated LaTeX file.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        tex_content = file.read()
    encoded_content = base64.b64encode(tex_content.encode("utf-8")).decode("utf-8")

    overleaf_url = (
        f"https://www.overleaf.com/docs?snip_uri=data:application/x-tex;base64,{encoded_content}&snip_name=resume.tex"
    )
    webbrowser.open(overleaf_url)
    print(f"LaTeX file uploaded! Open in Overleaf: {overleaf_url}")

def main():
    # Load data from JSON
    input_file = "data/sample.json"
    data = load_data(input_file)
    if not data:
        print("Error: Failed to load resume data. Exiting.")
        return
    # Escape LaTeX special characters
    data = escape_context(data)

    # Display available templates
    templates = get_available_templates()
    if not templates:
        print("No templates found in the 'templates' folder.")
        return

    print("Available Templates:")
    for idx, template in enumerate(templates, start=1):
        print(f"{idx}. {template}")

    # Ask the user to select a template
    choice = int(input("Select a template by number: ")) - 1
    if choice < 0 or choice >= len(templates):
        print("Invalid selection. Exiting.")
        return

    selected_template = templates[choice]
    print(f"Selected template: {selected_template}")

    # Render the template
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_file = os.path.join(OUTPUT_DIR, "generated_resume.tex")
    render_template(selected_template, data, output_file)

    print(f"Generated LaTeX file: {output_file}")

    # Open in Overleaf
    open_in_overleaf(output_file)

if __name__ == "__main__":
    main()
