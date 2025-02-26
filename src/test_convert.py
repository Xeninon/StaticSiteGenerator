import unittest

from convert import *

class Test_text_node_to_html_node(unittest.TestCase):
    def test(self):
        test_inputs = [
            TextNode("hello world", TextType.TEXT),
            TextNode("hello world", TextType.BOLD),
            TextNode("hello world", TextType.ITALIC),
            TextNode("hello world", TextType.CODE),
            TextNode("hello world", TextType.LINK, url="url"),
            TextNode("hello world", TextType.IMAGE, url="url")
        ]

        correct_outputs = [
            LeafNode(None, "hello world"),
            LeafNode("b", "hello world"),
            LeafNode("i", "hello world"),
            LeafNode("code", "hello world"),
            LeafNode("a", "hello world", {"href": "url"}),
            LeafNode("img", "", {"src": "url", "alt": "hello world"})
        ]

        answer_key = zip(test_inputs, correct_outputs)
        for key in answer_key:
            self.assertEqual(text_node_to_html_node(key[0]).__repr__(), key[1].__repr__())

class Test_split_nodes_delimiter(unittest.TestCase):
    def test(self):
        test_inputs = [
            ([TextNode("**hello** world", TextType.TEXT),TextNode("hello world", TextType.BOLD)], "**", TextType.BOLD),
            ([TextNode("**hello world**", TextType.TEXT)], "**", TextType.BOLD),
        ]

        correct_outputs = [
            [TextNode("hello", TextType.BOLD), TextNode(" world", TextType.TEXT), TextNode("hello world", TextType.BOLD)],
            [TextNode("hello world", TextType.BOLD)],
        ]

        answer_key = zip(test_inputs, correct_outputs)
        for key in answer_key:
            self.assertEqual(split_nodes_delimiter(*key[0]), key[1])

class Test_markdown_extractions(unittest.TestCase):
    def test(self):
        image_test_key = {
            "this is an image ![text](link)" : [("text", "link")],
            "and this has two images ![text](link) ![more text](more link)" : [("text", "link"), ("more text", "more link")]
        }

        link_test_key = {
            "this is a link [text](link)" : [("text", "link")],
            "and this has two links [text](link) [more text](more link)" : [("text", "link"), ("more text", "more link")]
        }

        for test in image_test_key:
            self.assertEqual(extract_markdown_images(test), image_test_key[test])

        for test in link_test_key:
            self.assertEqual(extract_markdown_links(test), link_test_key[test])

class Test_split_node_functions(unittest.TestCase):
    def test(self):
        text_node_images = TextNode(
            "This is text with an image ![to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
            )
        
        text_node_links = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
            )

        image_test_key = [([text_node_images],
            [
            TextNode("This is text with an image ", TextType.TEXT),
            TextNode("to boot dev", TextType.IMAGE, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode("to youtube", TextType.IMAGE, "https://www.youtube.com/@bootdotdev")
            ]
        )]

        link_test_key = [([text_node_links],
            [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev")
            ]
        )]

        for test in image_test_key:
            self.assertEqual(split_nodes_image(test[0]), test[1])

        for test in link_test_key:
            self.assertEqual(split_nodes_link(test[0]), test[1])

class Test_text_to_textnodes(unittest.TestCase):
    def test(self):
        key = [(
            "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)",
            [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
            ]
        )]

        for test in key:
            self.assertEqual(text_to_textnodes(test[0]), test[1])

class Test_markdown_to_blocks(unittest.TestCase):
    def test(self):
        key = [(
            "# This is a heading\n\n\n\nThis is a paragraph of text. It has some **bold** and *italic* words inside of it. \n\n* This is the first list item in a list block\n* This is a list item\n* This is another list item",
            [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            "* This is the first list item in a list block\n* This is a list item\n* This is another list item"
            ]
        )]

        for test, answer in key:
            self.assertEqual(markdown_to_blocks(test), answer)

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
            "This is **bolded** paragraph",
            "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
            "- This is a list\n- with items",
        ],
    )

class Test_block_to_blocktype(unittest.TestCase):
    def test(self):
        key = [("paragrapgh", BlockType.PARAGRAPH),
               ("###### heading", BlockType.HEADING),
               ("```code```", BlockType.CODE),
               (">quote\n>block", BlockType.QUOTE),
               ("* unordered\n* list", BlockType.UNORDERED_LIST),
               ("1. ordered\n2. list", BlockType.ORDERED_LIST)]

        for test in key:
            self.assertEqual(block_to_blocktype(test[0]), test[1])

class Test_markdown_to_html_node(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )
    
    def test_ordered_lists(self):
        md = """
1. I am **cool**
2. I am **awesome**
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>I am <b>cool</b></li><li>I am <b>awesome</b></li></ol></div>",
        )
    
    def test__code(self):
        md = """
```<p>I'm in the club straight up blocking it</p>```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code><p>I'm in the club straight up blocking it</p></code></pre></div>",
        )

if __name__ == "__main__":
    unittest.main()