Convert Sass to SCSS [![Build Status](https://travis-ci.org/luqmaan/sass_to_scss.svg?branch=master)](https://travis-ci.org/luqmaan/sass_to_scss)
==

libsass/sassc require SCSS. This is an experiment at writing a really barebones Sass to SCSS converter. Hopefully if this experiment works out, I can rewrite it in C and use it in a patch to libsass.

Supports
--

- automatic semicolon `;` insertion
- automatic opening and closing curly brace `{}` insertion
- `@import bourbon/bourbon` => `@import "bourbon/bourbon"`
- `=` => `mixin`
- `+` => `include`

Usage
--

Convert asdf.sass to asdf.scss: `python sass_to_scss.py asdf.sass`

Options:

```
usage: sass_to_scss.py [-h] [--spaces SPACES] 9[--debug] file

Convert a Sass file to SCSS.

positional arguments:
  file

optional arguments:
  -h, --help       show this help message and exit
  --spaces SPACES  number of spaces used for indentation
  --debug          output debug information
```


Example
--

Turn this beautiful Sass:

```sass
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
```

into this less beautiful SCSS:

```scss
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
```
