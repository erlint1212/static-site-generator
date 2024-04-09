class TextNode:
    def __init__(self, TEXT, TEXT_TYPE, URL=None):
        self.text = TEXT
        self.text_type = TEXT_TYPE
        self.url = URL
    
    def __eq__(self, other):
        return self.__dict__ == other.__dict__
            
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})" 

     
        



