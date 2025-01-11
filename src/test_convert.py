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
            [TextNode("", TextType.TEXT), TextNode("hello", TextType.BOLD), TextNode(" world", TextType.TEXT), TextNode("hello world", TextType.BOLD)],
            [TextNode("", TextType.TEXT), TextNode("hello world", TextType.BOLD), TextNode("", TextType.TEXT)],
        ]

        answer_key = zip(test_inputs, correct_outputs)
        for key in answer_key:
            self.assertEqual(split_nodes_delimiter(*key[0]), key[1])