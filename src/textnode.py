import re
valid_text_types = ("text", "bold", "italic", "code", "link", "image")

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
    matches = re.findall(r"\!\[\w+\]\([^\)]*\)", text)
    if matches == []:
        return ""
    output = []
    for img in matches:
        text = re.findall(r"\[[^\]]*", img)
        link = re.findall(r"\([^\)]*", img)
        output.append((text[0][1:], link[0][1:]))
    return output

def extract_markdown_links(text):
    matches = re.findall(r"(?!\!)\[\w+\]\([^\)]*\)", text)
    if matches == []:
        return ""
    output = []
    for img in matches:
        text = re.findall(r"\[[^\]]*", img)
        link = re.findall(r"\([^\)]*", img)
        output.append((text[0][1:], link[0][1:]))
    return output

     
        



