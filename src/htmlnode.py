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
            raise ValueError("Must input props, currently None")
        if type(self.props) != dict:
            raise ValueError("Props must be dictionary")
        output = ""
        for key in self.props.keys():
            output += f"{key}=\"{self.props[key]}\" "
        return output[:-1]

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
