import re
valid_text_types = ("text", "bold", "italic", "code", "link", "image")
# Why use this system? Seems ineficent, see later on i course to see it usage.
text_type_text = "text"
text_type_bold = "bold"
text_type_italic = "italic"
text_type_code = "code"
text_type_link = "link"
text_type_image = "image"


class TextNode:
    def __init__(self, TEXT, TEXT_TYPE, URL=None):
        self.text = TEXT
        self.text_type = TEXT_TYPE
        self.url = URL
    
    def __eq__(self, other):
        return self.__dict__ == other.__dict__
            
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})" 

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    if text_type not in valid_text_types:
        raise ValueError(f"{text_type} is not a valid text type")
    output_nodes = ""
    for node in old_nodes:
        if not isinstance(node, TextNode):
            if type(node) == str:
                output_nodes += node
            continue
        output_nodes += node.text
    
    text_list = output_nodes.split(delimiter)
    # If prime then missing one, works?
    if len(text_list) % 2 == 0:
        raise Exception(f"Missing matching closing delimiter: {delimiter}")
    output_list = []
    for i, text in enumerate(text_list):
        if i % 2 != 0:
            output_list.append(TextNode(text, text_type))
        else:
            output_list.append(TextNode(text, "text"))
    return output_list

def extract_markdown_images(text):
    matches = re.findall(r"\!\[.*?\]\(.*?\)", text)
    if matches == []:
        return ""
    output = []
    for img in matches:
        text = re.findall(r"\[[^\]]*", img)
        link = re.findall(r"\([^\)]*", img)
        output.append((text[0][1:], link[0][1:]))
    return output

def extract_markdown_links(text):
    matches = re.findall(r"[^\!]\[.*?\]\(.*?\)", text)
    if matches == []:
        return ""
    output = []
    for img in matches:
        text = re.findall(r"\[[^\]]*", img)
        link = re.findall(r"\([^\)]*", img)
        output.append((text[0][1:], link[0][1:]))
    return output

def split_nodes_image(old_nodes):
    if old_nodes == [] or type(old_nodes) != list:
        return []
    
    new_textnodes = []
    for old_textnode in old_nodes:
        # Inefficent? Make new func to check if empty?
        if repr(old_textnode) == "TextNode(None, None, None)":
            continue
        image_list = extract_markdown_images(old_textnode.text)
        if image_list == []:
            new_textnodes.append(old_textnode)
            continue
        original_text = old_textnode.text
        for image_tup in image_list:
            if type(original_text) != list:
                original_text = original_text.split(f"![{image_tup[0]}]({image_tup[1]})", 1)
            else:
                new_split = original_text[-1].split(f"![{image_tup[0]}]({image_tup[1]})", 1)
                original_text.pop()
                original_text += new_split
        if original_text[-1] == "":
            original_text.pop()
        for i, chunk in enumerate(original_text):
            new_text_node = TextNode(chunk, text_type_text) 
            new_textnodes.append(new_text_node)
            if i < len(image_list):
                new_image_node = TextNode(image_list[i][0], text_type_image,image_list[i][1]) 
                new_textnodes.append(new_image_node)
    return new_textnodes


def split_nodes_link(old_nodes):
    if old_nodes == [] or type(old_nodes) != list:
        return []
    
    new_textnodes = []
    for old_textnode in old_nodes:
        # Inefficent? Make new func to check if empty?
        if repr(old_textnode) == "TextNode(None, None, None)":
            continue
        link_list = extract_markdown_links(old_textnode.text)
        if link_list == []:
            new_textnodes.append(old_textnode)
            continue
        original_text = old_textnode.text
        for link_tup in link_list:
            if type(original_text) != list:
                original_text = original_text.split(f"[{link_tup[0]}]({link_tup[1]})", 1)
            else:
                new_split = original_text[-1].split(f"[{link_tup[0]}]({link_tup[1]})", 1)
                original_text.pop()
                original_text += new_split
        if original_text[-1] == "":
            original_text.pop()
        for i, chunk in enumerate(original_text):
            new_text_node = TextNode(chunk, text_type_text) 
            new_textnodes.append(new_text_node)
            if i < len(link_list):
                new_image_node = TextNode(link_list[i][0], text_type_link,link_list[i][1]) 
                new_textnodes.append(new_image_node)
    print(new_textnodes)
    return new_textnodes
    



