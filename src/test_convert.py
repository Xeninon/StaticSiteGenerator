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