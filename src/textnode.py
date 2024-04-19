import re
valid_text_types = ("text", "bold", "italic", "code", "link", "image")
# Why use this system? Seems ineficent, see later on i course to see it usage.
text_type_text = "text"
text_type_bold = "bold"
text_type_italic = "italic"
text_type_code = "code"
text_type_link = "link"
text_type_image = "image"

block_type_paragraph = "p"#"paragraph"
block_type_heading = "h"#"heading"
block_type_code = "code"
block_type_quote = "blockquote"#"quote"
block_type_unordered_list = "ul" #"unordered_list"
block_type_ordered_list = "ol"#"ordered_list"

valid_delims = {"**" : text_type_bold, "*" : text_type_italic, "`" : text_type_code, "```" : text_type_code}


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
        if old_textnode.text in [None, "", " "]:
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
        if type(original_text) == str:
            new_textnodes.append(old_textnode)
            continue

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
        if old_textnode.text in [None, "", " "]:
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

        if type(original_text) == str:
            new_textnodes.append(old_textnode)
            continue
        
        for i, chunk in enumerate(original_text):
            new_text_node = TextNode(chunk, text_type_text) 
            new_textnodes.append(new_text_node)
            if i < len(link_list):
                new_image_node = TextNode(link_list[i][0], text_type_link,link_list[i][1]) 
                new_textnodes.append(new_image_node)
    return new_textnodes
    
def text_to_textnodes(text):
    split_list = []
    for delim in valid_delims.keys():
        if split_list == []:
            split_list = split_nodes_delimiter(text, delim, valid_delims[delim])
            continue
        new_list = []
        for i, node in enumerate(split_list):
            if node.text_type != text_type_text:
                new_list.append(node)
                continue
            current_node_split = split_nodes_delimiter(node.text, delim, valid_delims[delim])
            if len(current_node_split) == 1:
                new_list.append(node)
                continue
            for new_node in current_node_split:
                new_list.append(new_node)
        split_list = new_list
    split_list = split_nodes_image(split_list) 
    split_list = split_nodes_link(split_list)
    return split_list

    lines = doc_content.split("\n")
    return "\n".join(new_lines)


def remove_asterisks_from_words(line):
    words = line.split()

    def clean_word(word):
        return word.strip("*") if len(word) > 1 else word

    cleaned_words = filter(lambda word: len(word) > 0, map(clean_word, words))
    return " ".join(cleaned_words)

def markdown_to_blocks(markdown):
    initial_split = markdown.split("\n\n")
    split_extra_newlines = [x.strip().split("\n") for x in initial_split]
    flatten_split = [x[0] if len(x)==1 else x for x in split_extra_newlines]
    for i, block in enumerate(flatten_split):
        if type(block) == str:
            flatten_split[i] = block.strip() 
            continue
        for k, line in enumerate(block):
            flatten_split[i][k] = line.strip() 
        flatten_split[i] = "\n".join(flatten_split[i])    
    return flatten_split

def block_to_block_type(markdown_block):
    if re.findall(r"^#{1,6}\s", markdown_block) != []:
        #heading_number = len(re.findall(r"^#{1,6}", markdown_block)[0]) 
        return block_type_heading #+ f"{heading_number}"
    if markdown_block[:3] == "```" and markdown_block[-3:] == "```":
        return block_type_code
    if any([False if x[0] == ">" else True for x in markdown_block.splitlines()]) == False:
        return block_type_quote
    if any([False if x[:2] in ["* ", "- "] else True for x in markdown_block.splitlines()]) == False:
        return block_type_unordered_list
    if any([False if x[:3] == f"{i+1}. "  else True for i, x in enumerate(markdown_block.splitlines())]) == False:
        return block_type_ordered_list

    return block_type_paragraph


    
