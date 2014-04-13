from unittest import TestCase

import sass_to_scss


class TestSassToSCSS(TestCase):

    def trim_docstring(self, docstring):
        return '\n'.join(docstring.split('\n')[1:-1])

    def test_triple_nested_class(self):
        sass = """
.container
    position: absolute
    top: 0
    color: green
    bottom: 0
    .right
        right: 0
        border: 1px solid #fff
        h1
            color: blue
    .left
        left: 0
        h1
            color: red
        """

        scss = """
.container {
    position: absolute;
    top: 0;
    color: green;
    bottom: 0;
    .right {
        right: 0;
        border: 1px solid #fff;
        h1 {
            color: blue;
        }
    }
    .left {
        left: 0;
        h1 {
            color: red;
        }
    }
}
        """

        input = self.trim_docstring(sass).split('\n')
        actual = sass_to_scss.sass_to_scss(input)
        expected = self.trim_docstring(scss)
        print actual

        self.assertEquals(expected, actual)
