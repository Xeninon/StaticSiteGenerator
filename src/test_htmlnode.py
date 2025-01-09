import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(props={"this": "that", "triangle": "square hole"})
        self.assertEqual(node.props_to_html(), ' this="that" triangle="square hole"')

class TestLeafNode(unittest.TestCase):
    def test_to_html(self):
        node = LeafNode(None, "raw.txt")
        node2 = LeafNode("b", "I am valued", props={"coconut": "lime"})
        self.assertEqual(node.to_html(), "raw.txt")
        self.assertEqual(node2.to_html(), '<b coconut="lime">I am valued</b>')

class TestParentNode(unittest.TestCase):
    def test_to_html(self):
        node = ParentNode("p", [LeafNode("b", "I am valued", props={"coconut": "lime"})], props={"coconut": "lime"})
        node2 = ParentNode("p", [LeafNode(None, "raw.txt"), LeafNode("b", "I am valued", props={"coconut": "lime"})])
        node3 = ParentNode("p", [ParentNode("p", [LeafNode("b", "I am valued", props={"coconut": "lime"})], props={"coconut": "lime"})])
        node4 = ParentNode("p", [])
        self.assertEqual(node.to_html(), '<p coconut="lime"><b coconut="lime">I am valued</b></p>')
        self.assertEqual(node2.to_html(), '<p>raw.txt<b coconut="lime">I am valued</b></p>')
        self.assertEqual(node3.to_html(), '<p><p coconut="lime"><b coconut="lime">I am valued</b></p></p>')
        self.assertEqual(node4.to_html(), "<p></p>")


if __name__ == "__main__":
    unittest.main()