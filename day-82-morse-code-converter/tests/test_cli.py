from io import StringIO
import unittest
from unittest.mock import patch

from pymorse import cli, __version__


class TestParseArgs(unittest.TestCase):
    def test_parse_args(self):
        args = cli.parse_args(["Hello"])
        self.assertEqual(args.message, "Hello")


@patch("sys.stderr", new_callable=StringIO)
@patch("sys.stdout", new_callable=StringIO)
class TestMain(unittest.TestCase):
    def test_no_arguments(self, mock_stdout, mock_stderr):
        with self.assertRaises(SystemExit) as e:
            cli.main([])
        self.assertEqual(e.exception.code, 2)
        self.assertIn("required: message", mock_stderr.getvalue())

    def test_simple_input(self, mock_stdout, mock_stderr):
        cli.main(["Hello World!"])
        self.assertEqual(
            ".... . .-.. .-.. ---   .-- --- .-. .-.. -.. -.-.--\n",
            mock_stdout.getvalue(),
        )

    def test_message_with_invalid_character(self, mock_stdout, mock_stderr):
        with self.assertRaises(SystemExit) as e:
            cli.main(["a*"])
        self.assertEqual(e.exception.code, 100)
        self.assertEqual("Invalid character: *", mock_stderr.getvalue())

    def test_print_version_short_arg(self, mock_stdout, mock_stderr):
        with self.assertRaises(SystemExit) as e:
            cli.main(["-v"])
        self.assertEqual(e.exception.code, 0)
        self.assertEqual(f"pymorse {__version__}\n", mock_stdout.getvalue())

    def test_print_version_long_arg(self, mock_stdout, mock_stderr):
        with self.assertRaises(SystemExit) as e:
            cli.main(["--version"])
        self.assertEqual(e.exception.code, 0)
        self.assertEqual(f"pymorse {__version__}\n", mock_stdout.getvalue())
