import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)

        self.assertEqual(node, node2)

    def test_not_eq(self):
        node3 = TextNode("This is a italic node", TextType.ITALIC)
        node4 = TextNode("This is a bold node", TextType.BOLD)

        self.assertNotEqual(node3, node4)

    def test_urlmismatch(self):
        node5 = TextNode(
            "This is a bold, with url", TextType.BOLD, url="www.google.com"
        )
        node6 = TextNode("This is a bold, without url", TextType.BOLD)

        self.assertNotEqual(node5, node6)

class TestTextToLeaf(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node1 = TextNode("This is a bold node", TextType.BOLD)
        html_node1 = text_node_to_html_node(node1)
        self.assertEqual(html_node1.tag, "b")
        self.assertEqual(html_node1.value, "This is a bold node")

    def test_link(self):
        node2 = TextNode("This is link node", TextType.LINK)
        html_node2 = text_node_to_html_node(node2)
        self.assertEqual(html_node2.tag, "a")
        self.assertEqual(html_node2.props, "href")





if __name__ == "__main__":
    unittest.main()
