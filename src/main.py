from textnode import TextNode
from static_to_public import *
from generate_page import *
import os

def main():
    path = os.getcwd() 
    #dummy_node = TextNode("This is a text node", "bold", "hrrrps://www.boot.dev")
    #print(repr(dummy_node)) 
    static_to_public()
    generate_page(f"{path}/content/index.md", f"{path}/template.html", f"{path}/public")

if __name__ == "__main__":
    main()
