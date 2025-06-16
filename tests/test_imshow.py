
import unittest
from definitions.imshow import imshow

class TestImshow(unittest.TestCase):

    def test_valid_input(self):
        data = [[1.0, 2.0], [3.0, 4.0]]
        text_auto = True
        title = "Test Heatmap"
        try:
            imshow(data, text_auto, title)
        except TypeError:
            self.fail("imshow() raised TypeError unexpectedly!")

    def test_invalid_data_type(self):
        with self.assertRaises(TypeError):
            imshow("invalid", True, "Test Heatmap")

    def test_invalid_row_type(self):
        with self.assertRaises(TypeError):
            imshow([1, "invalid"], True, "Test Heatmap")

    def test_invalid_element_type(self):
        with self.assertRaises(TypeError):
            imshow([[1, "invalid"], [3, 4]], True, "Test Heatmap")

    def test_invalid_text_auto_type(self):
        with self.assertRaises(TypeError):
            imshow([[1, 2], [3, 4]], "invalid", "Test Heatmap")

    def test_invalid_title_type(self):
        with self.assertRaises(TypeError):
            imshow([[1, 2], [3, 4]], True, 123)

    def test_empty_data(self):
        data = [[]]  # Empty data, but valid structure
        text_auto = True
        title = "Empty Heatmap"
        try:
            imshow(data, text_auto, title)
        except TypeError:
            self.fail("imshow() raised TypeError unexpectedly!")
