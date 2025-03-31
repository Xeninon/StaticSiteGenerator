from textnode import TextNode, TextType

from htmlnode import *

import re

from enum import Enum

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise Exception("invalid text type")
        
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            text_split = node.text.split(delimiter)
            if len(text_split) % 2 < 0:
                raise Exception("invalid_syntax")
            for text in text_split:
                if len(text) != 0:
                    if text_split.index(text) % 2 == 1:
                            new_nodes.append(TextNode(text, text_type))
                    else:
                            new_nodes.append(TextNode(text, TextType.TEXT))
        else:
            new_nodes.append(node)
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            text_list = [node.text]
            images = extract_markdown_images(node.text)
            for image in images:
                alt, link = image
                text_list = text_list[-1].split(f"![{alt}]({link})", 1)
                if len(text_list[-2]) != 0:
                    new_nodes.append(TextNode(text_list[-2], TextType.TEXT))
                new_nodes.append(TextNode(alt, TextType.IMAGE, link))
            if len(text_list[-1]) != 0:
                new_nodes.append(TextNode(text_list[-1], TextType.TEXT))
        else:
            new_nodes.append(node)
    return new_nodes
        
def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            text_list = [node.text]
            links = extract_markdown_links(node.text)
            for link in links:
                alt, link = link
                text_list = text_list[-1].split(f"[{alt}]({link})", 1)
                if len(text_list[-2]) != 0:
                    new_nodes.append(TextNode(text_list[-2], TextType.TEXT))
                new_nodes.append(TextNode(alt, TextType.LINK, link))
            if len(text_list[-1]) != 0:
                new_nodes.append(TextNode(text_list[-1], TextType.TEXT))
        else:
            new_nodes.append(node)
    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def markdown_to_blocks(markdown):
    blocks = markdown.split('\n\n')
    for i in range(len(blocks)):
        blocks[i] = blocks[i].strip()
    blocks = list(filter(None, blocks))
    return blocks

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_blocktype(block):
    for i in range(7):
        if block[i] == " ":
            return BlockType.HEADING
        if block[i] != "#":
            break
    if block[:3] == "```" and block[-3:] == "```":
        return BlockType.CODE
    split_lines = block.split("\n")
    quote = True
    ulist = True
    olist = True
    for i in range(len(split_lines)):
        if split_lines[i][0] != ">":
            quote = False
        if split_lines[i][:2] != "* " and split_lines[i][:2] != "- ":
            ulist = False
        if split_lines[i][:3] != f"{i + 1}. ":
            olist = False
    if quote:
        return BlockType.QUOTE
    if ulist:
        return BlockType.UNORDERED_LIST
    if olist:
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

def text_to_children(blocktype, block):
    text = remove_block_syntax(blocktype, block)
    oneline = text.replace("\n", " ")
    if blocktype == BlockType.ORDERED_LIST or blocktype == BlockType.UNORDERED_LIST:
        children = []
        lines = text.split("\n")
        for line in lines:
            listnode = ParentNode("li", text_to_children_helper(line))
            children.append(listnode)
        return children
    elif blocktype == BlockType.CODE:
        return [LeafNode("code", text)]
    else:
        return text_to_children_helper(oneline)

def text_to_children_helper(text):
    children = []
    textnodes = text_to_textnodes(text)
    for textnode in textnodes:
        children.append(text_node_to_html_node(textnode))
    return children

def remove_block_syntax(blocktype, block):
    lines = block.split("\n")
    match blocktype:
        case BlockType.QUOTE:
            for i in range(len(lines)):
                lines[i] = lines[i][2:]
            return "\n".join(lines)
        case BlockType.UNORDERED_LIST:
            for i in range(len(lines)):
                lines[i] = lines[i][2:]
            return "\n".join(lines)
        case BlockType.ORDERED_LIST:
            for i in range(len(lines)):
                lines[i] = lines[i][3:]
            return "\n".join(lines)
        case BlockType.CODE:
            return block[4:-3]
        case BlockType.HEADING:
            return block.lstrip("#")[1:]
        case BlockType.PARAGRAPH:
            return block
        case _:
            return block
        
def get_blocktag(blocktype, block):
    match blocktype:
        case BlockType.QUOTE:
            return "blockquote"
        case BlockType.UNORDERED_LIST:
            return "ul"
        case BlockType.ORDERED_LIST:
            return "ol"
        case BlockType.CODE:
            return "pre"
        case BlockType.HEADING:
            for i in range(7):
                if block[i] == " ":
                    return f"h{i}"
        case BlockType.PARAGRAPH:
            return "p"

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    blocknodes = []
    for block in blocks:
        blocktype = block_to_blocktype(block)
        blocknode = ParentNode(get_blocktag(blocktype, block), text_to_children(blocktype, block))
        blocknodes.append(blocknode)
    return ParentNode("div", blocknodes)
