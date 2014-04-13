from unittest import TestCase

import sass_to_scss


class TestSassToSCSS(TestCase):

    def trim_docstring(self, docstring):
        return '\n'.join(docstring.split('\n')[1:-1])

    def test_triple_nested_class(self):
        sass = """
@import bourbon/bourbon

=red-text
    color: red

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
@import "bourbon/bourbon";

@mixin red-text {
    color: red;
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
