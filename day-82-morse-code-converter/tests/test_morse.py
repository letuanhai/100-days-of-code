import unittest

import pymorse.morse as morse


class TestMorseEncode(unittest.TestCase):
    def test_encode_hello_world(self):
        self.assertEqual(
            morse.encode("Hello World!"),
            ".... . .-.. .-.. ---   .-- --- .-. .-.. -.. -.-.--",
        )

    def test_encode_empty_string(self):
        self.assertEqual(morse.encode(""), "")

    def test_encode_numbers(self):
        self.assertEqual(morse.encode("123"), ".---- ..--- ...--")

    def test_encode_invalid_character(self):
        with self.assertRaisesRegex(ValueError, "^Invalid character"):
            morse.encode("*")

    def test_encode_string_with_invalid_character(self):
        with self.assertRaisesRegex(ValueError, "^Invalid character"):
            morse.encode("a*")


if __name__ == "__main__":
    unittest.main()
