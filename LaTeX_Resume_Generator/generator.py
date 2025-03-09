import os
import json
from jinja2 import Environment, FileSystemLoader
import shutil
import webbrowser
import base64
# import jinja2

# # Base directory for templates
# TEMPLATES_DIR = "templates"
# OUTPUT_DIR = "output"

# def get_available_templates():
#     """Fetch the list of available templates."""
#     return [f for f in os.listdir(TEMPLATES_DIR) if f.endswith(".tex")]

# def render_template(template_name, context, output_file):
#     """
#     Render the selected LaTeX template with the provided context.

#     Args:
#         template_name (str): Name of the LaTeX template file.
#         context (dict): Dictionary containing placeholder values.
#         output_file (str): Path to save the rendered LaTeX file.
#     """
#     # Load the template
#     env = jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATES_DIR))
#     template = env.get_template(template_name)

#     # Render the template with context
#     rendered_content = template.render(context)

#     # Save to output file
#     with open(output_file, "w") as f:
#         f.write(rendered_content)
#     print(f"Generated LaTeX file: {output_file}")

# def main():
#     # Display available templates
#     templates = get_available_templates()
#     if not templates:
#         print("No templates found in the 'templates' folder.")
#         return

#     print("Available Templates:")
#     for idx, template in enumerate(templates, start=1):
#         print(f"{idx}. {template}")

#     # Ask the user to select a template
#     choice = int(input("Select a template by number: ")) - 1
#     if choice < 0 or choice >= len(templates):
#         print("Invalid selection. Exiting.")
#         return

#     selected_template = templates[choice]
#     print(f"Selected template: {selected_template}")

#     # Define the context for placeholders
#     context = {
#         "name": "Agnel M S",
#         "email": "agnelms27@gmail.com",
#         "phone": "+91 9037193079",
#         "linkedin": "www.linkedin.com/in/agnel-m-s-7a2774280",
#         "github": "AGNELMS",
#         "career_objective": (
#             "Aspiring software engineer with expertise in Python automation, "
#             "LaTeX development, and IoT systems. Passionate about solving real-world "
#             "challenges through innovation and efficiency."
#         ),
#         "education": [
#             {"duration": "Dec 2021 -- Present", "degree": "B.Tech in Electronics and Communication Engineering", "institute": "NIT Calicut, Kerala", "details": "CGPA: 7.33"},
#             {"duration": "Jun 2018 -- Mar 2020", "degree": "CBSE Stream, Computer Science", "institute": "St. Antony's Public School, Anakkal, Kerala", "details": "Percentage: 94.4%"}
#         ],
#         "skills": [
#             {"name": "Programming Languages", "details": "C, C++, Python, Javascript"},
#             {"name": "Development Tools", "details": "LaTeX, Visual Studio Code, MATLAB"},
#             {"name": "Soft Skills", "details": "Team Collaboration, Stakeholder Management"}
#         ],
#         "projects": [
#             {
#                 "title": "LaTeX Resume Generator (Dec 2024)",
#                 "details": "Automated the creation of professional resumes using Python, achieving a 70% reduction in manual formatting efforts."
#             },
#             {
#                 "title": "Flood Prediction System (Nov 2024)",
#                 "details": "Developed a wireless sensor network achieving 90% accuracy in early flood detection."
#             }
#         ]
#     }

#     # Render the template
#     os.makedirs(OUTPUT_DIR, exist_ok=True)
#     output_file = os.path.join(OUTPUT_DIR, "generated_resume.tex")
#     render_template(selected_template, context, output_file)

#     print("\nLaTeX file generated. Upload this file to Overleaf for preview.")



def open_in_overleaf(file_path, file_name="project.tex"):
    # Read and encode the LaTeX file
    with open(file_path, "r", encoding="utf-8") as file:
        tex_content = file.read()
    encoded_content = base64.b64encode(tex_content.encode("utf-8")).decode("utf-8")

    # Construct the Overleaf URL
    overleaf_url = (
        f"https://www.overleaf.com/docs?snip_uri=data:application/x-tex;base64,{encoded_content}&snip_name={file_name}"
    )

    # Open the URL in the default web browser
    webbrowser.open(overleaf_url)
    print(f"LaTeX file uploaded! Open in Overleaf: {overleaf_url}")


# Load data from JSON
def load_data(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

# Render the LaTeX template
def render_template(template_name, data):
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template(template_name)
    return template.render(data)

# Create a .zip archive for Overleaf
def create_zip(tex_file, zip_name='overleaf_project.zip'):
    # Ensure the .zip only includes the required files
    files_to_include = [tex_file]
    if not os.path.exists('output'):
        os.makedirs('output')
    for file in files_to_include:
        shutil.copy(file, 'output')
    shutil.make_archive('overleaf_project', 'zip', 'output')
    print(f"Created {zip_name} for Overleaf.")
    shutil.rmtree('output')  # Clean up temporary folder

if __name__ == "__main__":
    input_file = 'data/sample.json'
    data = load_data(input_file)

    tex_content = render_template('Minimalist.tex', data)

    tex_file = 'resume.tex'
    with open(tex_file, 'w', encoding='utf-8') as f:
        f.write(tex_content)

    # Open the file in Overleaf
    open_in_overleaf(tex_file)

