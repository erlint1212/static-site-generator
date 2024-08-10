from htmlnode import markdown_to_html_node 
from title_extractor import * 
import os
import pathlib


def generate_page(from_path, template_path, dest_path):

    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    markdown_content = open(from_path, "r").read()
    template_content = open(template_path, "r").read()
    markdown_content_to_html = markdown_to_html_node(markdown_content).TO_HTML()
    markdown_content_title = extract_title(markdown_content)
    
    html_output = template_content.replace("{{ Title }}", markdown_content_title)
    html_output = html_output.replace("{{ Content }}", markdown_content_to_html)
    
    new_file_name = from_path.split("/")[-1][:-3]
    dest_path_short = "/".join(dest_path.split("/")[:-1])
    if not os.path.exists(f"{dest_path}/{new_file_name}.html"):
        output = open(f"{dest_path_short}/{new_file_name}.html", "a+")
    else:
        output = open(f"{dest_path_short}/{new_file_name}.html", "w")
    output.write(html_output)
    output.close()

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    content_dir_crawl_md_found = []

    def recursive_crawl(prev_dir_path):
        current_dir_path_content = os.listdir(prev_dir_path)
        if current_dir_path_content != []:
            for item in current_dir_path_content:
                if "." not in item:
                    recursive_crawl(prev_dir_path+"/"+item) 
                if item[-3:] == ".md":
                    content_dir_crawl_md_found.append(prev_dir_path[len(dir_path_content):] +"/"+item)
    recursive_crawl(dir_path_content)
    # make dirs that don't exist in public
    for item in content_dir_crawl_md_found:
        split_item = item.split("/")
        if len(split_item) != 2: 
            for i in range(1,len(split_item)-1):
                if not os.path.isdir(dest_dir_path + "/".join(split_item[:i+1])):
                    os.mkdir(dest_dir_path +"/".join(split_item[:i+1]))

    for item in content_dir_crawl_md_found:
        print(dir_path_content+item, "|", dest_dir_path+item)
        generate_page(dir_path_content+item, template_path, dest_dir_path+item)

    print(content_dir_crawl_md_found)


    
