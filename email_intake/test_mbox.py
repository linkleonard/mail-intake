from email_intake import mbox
from unittest import TestCase


class TestHeaderAsTuple(TestCase):
    def test(self):
        lines = [
            "HeaderName: my value\n",
        ]
        result = mbox.header_as_tuple(iter(lines))
        self.assertEqual(2, len(result))
        (name, value) = result
        self.assertEqual("HeaderName", name)

        value = ''.join(value)
        self.assertEqual("my value\n", value)

    def test_multiple_lines(self):
        lines = [
            "HeaderName: my value\n",
            " continued\n",
        ]
        result = mbox.header_as_tuple(iter(lines))
        self.assertEqual(2, len(result))
        (name, value) = result
        self.assertEqual("HeaderName", name)

        value = ''.join(value)
        self.assertEqual("my value\n continued\n", value)


class TestCollectHeader(TestCase):
    def test(self):
        lines = [
            "Something\n",
            "\n",
            "Other\n",
        ]
        headers = tuple(mbox.collect_headers(iter(lines)))
        expected = ('Something\n',)
        self.assertEqual(expected, headers)
