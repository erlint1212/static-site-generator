from textnode import TextNode

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
        if self.tag not in ["img", "code"]:
            return f"<{self.tag}" + props_html + ">" + self.value + f"</{self.tag}>"
        match self.tag:
            case "img":
                return f"<img" + props_html + ">"
            case "code":
                return f"```{self.value}```"
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
            output += child.TO_HTML() 

        self.value = output

        props_html = ""
        if self.props != None:
            props_html = " " + child.PROPS_TO_HTML()

        return self._TO_HTML_CONVERTER(props_html)

def text_node_to_html_node(text_node):
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
        case _:
            raise Exception(f"Text type \"{text_node.text_type}\" not supported")



