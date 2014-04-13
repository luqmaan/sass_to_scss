import logging
from unittest import TestCase
from sass_to_scss import SassToSCSS


class TestSassToSCSS(TestCase):

    def setUp(self):
        self.sassy = SassToSCSS(loglevel=logging.DEBUG)

    def trim_docstring(self, docstring):
        return '\n'.join(docstring.split('\n')[1:-1])

    def test_double_spaces(self):
        self.sassy.spaces = 2
        sass = """
body
  background: red
  header
    background: blue
"""
        scss = """
body {
  background: red;
  header {
    background: blue;
  }
}
"""
        actual = self.sassy.convert(self.trim_docstring(sass).split('\n'))
        expected = self.trim_docstring(scss)

        self.assertEquals(expected, actual)

    def test_triple_nested_class(self):
        sass = """
@import bourbon/bourbon
@import "http://fonts.googleapis.com/css?family=PT+Serif:400,700,400italic,700italic|Oswald:400,300,700|Droid+Sans:400,700"

$teal: #00917d
$serif: 'PT Serif', serif

=red-text
    color: red
    background-color: $teal

=rounded($amount, $background_color)
    -moz-border-radius: $amount
    -webkit-border-radius: $amount
    border-radius: $amount
    background-color: saturate(lighten($background_color, 30%), 100%)

.error
    +red-text
    .details
        border: 3px solid #777
        +rounded(0.5em, desaturate(#5336a2, 10%))

.container
    position: absolute
    top: 0
    color: green
    bottom: 0

    .right, .row:hover, &.touch .row
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
@import "bourbon/bourbon";
@import "http://fonts.googleapis.com/css?family=PT+Serif:400,700,400italic,700italic|Oswald:400,300,700|Droid+Sans:400,700";
$teal: #00917d;
$serif: 'PT Serif', serif;
@mixin red-text {
    color: red;
    background-color: $teal;
}
@mixin rounded($amount, $background_color) {
    -moz-border-radius: $amount;
    -webkit-border-radius: $amount;
    border-radius: $amount;
    background-color: saturate(lighten($background_color, 30%), 100%);
}
.error {
    @include red-text;
    .details {
        border: 3px solid #777;
        @include rounded(0.5em, desaturate(#5336a2, 10%));
    }
}
.container {
    position: absolute;
    top: 0;
    color: green;
    bottom: 0;
    .right, .row:hover, &.touch .row {
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

        actual = self.sassy.convert(self.trim_docstring(sass).split('\n'))
        expected = self.trim_docstring(scss)

        self.assertEquals(expected, actual)
