from textnode import *

class HTMLNode():
    def __init__(self, TAG=None, VALUE=None, CHILDREN=None, PROPS=None):
        self.tag = TAG
        self.value = VALUE
        self.children = CHILDREN
        self.props = PROPS

    def TO_HTML(self):
        raise NotImplementedError("TODO")

    def PROPS_TO_HTML(self):
        if self.props == None:
            return None
            #raise ValueError("Must input props, currently None")
        if type(self.props) != dict:
            raise ValueError("Props must be dictionary")
        output = ""
        for key in self.props.keys():
            output += f"{key}=\"{self.props[key]}\" "
        return output[:-1]

    def _TO_HTML_CONVERTER(self, props_html):
        if self.tag not in ["img"]:
            if isinstance(self.value, list):
                output = ""
                for item in self.value:
                    output += item._TO_HTML_CONVERTER(props_html)

                #return output 
                return f"<{self.tag}" + props_html + ">" + output + f"</{self.tag}>"
            if self.tag == None:
                return self.value 
            return f"<{self.tag}" + props_html + ">" + self.value + f"</{self.tag}>"
        match self.tag:
            case "img":
                return f"<img" + props_html + ">"
            case _:
                raise Exception("Tag not supported")

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

class LeafNode(HTMLNode):
    def __init__(self, TAG=None, VALUE=None, PROPS=None):
        if VALUE == None:
            raise ValueError("Value is None, LeafNode requires a valid value")
        super().__init__(TAG=TAG, VALUE=VALUE, PROPS=PROPS)
    
    def TO_HTML(self):
        if self.value == None:
            raise ValueError("Value is None, LeafNode requires a valid value")
        if self.tag == None:
            return self.value

        
        props_html = ""
        if self.props != None:
            props_html = " " + self.PROPS_TO_HTML()
        
        return self._TO_HTML_CONVERTER(props_html)


class ParentNode(HTMLNode):
    def __init__(self, TAG=None, CHILDREN=None, PROPS=None):
        if CHILDREN == None:
            raise ValueError("CHILDREN are mandatory in ParentNode")
        if type(CHILDREN) != list:
            raise ValueError("CHILDREN must be a list")
        if CHILDREN == []:
            raise ValueError("There are no children in CHILDREN")
        super().__init__(TAG=TAG, CHILDREN=CHILDREN, PROPS=PROPS)
        self.value = None
    
    def TO_HTML(self):
        output = ""
        for child in self.children:
            if isinstance(child, ParentNode):
                output += child.TO_HTML()
                continue
            """
            if isinstance(child, list):
                for item in child:
                    output += item.TO_HTML()
            """
            output += child.TO_HTML() 

        self.value = output

        props_html = ""
        if self.props != None:
            props_html = " " + child.PROPS_TO_HTML()

        return self._TO_HTML_CONVERTER(props_html)

def text_node_to_html_node(text_node):
    if isinstance(text_node, list):
        text_node_list = []
        for item in text_node:
            text_node_list.append(text_node_to_html_node(item))
        return text_node_list
    if not isinstance(text_node, TextNode):
        raise ValueError("Input must be a TextNode")
    match text_node.text_type:
        case "text":
            return LeafNode(None, text_node.text)
        case "bold":
            return LeafNode("b", text_node.text)
        case "italic":
            return LeafNode("i", text_node.text)
        case "code":
            return LeafNode("code", text_node.text)
        case "link":
            return LeafNode("a", text_node.text, {"href":text_node.url})
        case "image":
            return LeafNode("img", "", {"src":text_node.url , "alt":text_node.text})
        case "li":
            return LeafNode("li", textnode.text)
        case _:
            raise Exception(f"Text type \"{text_node.text_type}\" not supported")

def block_paragraph_to_html_node(block):
    return ParentNode(block_type_paragraph, text_node_to_html_node(text_to_textnodes(block))) 

def block_heading_to_html_node(block):
    heading_number = len(re.findall(r"^#{1,6}", block)[0]) 
    return ParentNode(block_type_heading + f"{heading_number}", text_node_to_html_node(text_to_textnodes(block.lstrip("# ")))) 

def block_code_to_html_node(block):
    return ParentNode(block_type_code, text_node_to_html_node(text_to_textnodes(block.strip("`"))))
        
def block_quote_to_html_node(block):
    split_list = block.splitlines()
    output = "\n".join([x.lstrip(">").strip() for x in split_list])
    return ParentNode(block_type_quote, text_node_to_html_node(text_to_textnodes(output)))

# ul and ol are horribly writen, rewrite later (textnode never needs to be called as i only need the text, and I'm breaking function)
# convention making a leafnode outside the make leafnode funckit, breaking the fuctional programing paragrim ?

def block_unordered_list_to_html_node(block):
    split_list = block.splitlines()
    output = [text_node_to_html_node(text_to_textnodes(x[2:])) for x in split_list]
    output_2 = [LeafNode("li", x) for x in output]#[LeafNode("li", x) for x in output] # LeafNode("li", output) [LeafNode("li", x) for x in output]
    return ParentNode(block_type_unordered_list, output_2)

def block_ordered_list_to_html_node(block):
    split_list = block.splitlines()
    output = [text_node_to_html_node(text_to_textnodes(x[3:])) for x in split_list]
    output_2 = [LeafNode("li", x) for x in output]#[LeafNode("li", x) for x in output] # LeafNode("li", output) [LeafNode("li", x) for x in output]
    
    return ParentNode(block_type_ordered_list, output_2)


def markdown_to_html_node(markdown):
    children = []
    text_blocks = markdown_to_blocks(markdown)
    text_blocks_type = [block_to_block_type(x) for x in text_blocks]
    for i, block in enumerate(text_blocks):
        html_block = None
        # Tried to make it into match case, but requires blocky types to be enum, so if tree it is :(
        if text_blocks_type[i] == block_type_paragraph: 
            html_block = block_paragraph_to_html_node(block) 
        elif text_blocks_type[i] ==  block_type_heading:
            html_block = block_heading_to_html_node(block)
        elif text_blocks_type[i] ==  block_type_code:
            html_block = block_code_to_html_node(block)
        elif text_blocks_type[i] == block_type_quote:
            html_block = block_quote_to_html_node(block)
        elif text_blocks_type[i] == block_type_unordered_list:
            html_block = block_unordered_list_to_html_node(block)
        elif text_blocks_type[i] == block_type_ordered_list:
            html_block = block_ordered_list_to_html_node(block)

        if html_block != None:
            children.append(html_block)

    return ParentNode("div", children)
