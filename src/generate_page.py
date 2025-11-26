from block_markdown import markdown_to_html_node
from extract_title import extract_title
import os

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    #
    with open(from_path, "r") as file:
        md_contents = file.read()
        file.close()

    with open(template_path, "r") as file1:
        template = file1.read()
        file1.close()

    node = markdown_to_html_node(md_contents)
    html = node.to_html()
    title = extract_title(md_contents)
    output = template.replace("{{ Title }}", title ).replace("{{ Content }}", html)

    directory = os.path.dirname(dest_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(dest_path, 'w') as f:
        f.write(output)





    def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
        pass



