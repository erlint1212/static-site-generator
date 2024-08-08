from htmlnode import markdown_to_html_node 
from title_extractor import * 
import os


def generate_page(from_path, template_path, dest_path):

    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    markdown_content = open(from_path, "r").read()
    template_content = open(template_path, "r").read()
    markdown_content_to_html = markdown_to_html_node(markdown_content).TO_HTML()
    markdown_content_title = extract_title(markdown_content)
    
    html_output = template_content.replace("{{ Title }}", markdown_content_title)
    html_output = html_output.replace("{{ Content }}", markdown_content_to_html)
    

    if not os.path.exists(f"{dest_path}/index.html"):
        output = open(f"{dest_path}/index.html", "a")
    else:
        output = open(f"{dest_path}/index.html", "w")
    output.write(html_output)
    output.close()


