Convert Sass to SCSS
==

libsass/sassc require SCSS. This is an experiment at writing a really barebones Sass to SCSS converter. Hopefully if this experiment works out, I can rewrite it in C and use it in a patch to libsass.

Supports
-

- automatic semicolon (;) insertion
- automatic opening and closing curly brance ({}) insertion
- @import bourbon/bourbon > @import "bourbon/bourbon"
- = > mixin
- + > include


Demo
--

Turn this beautiful Sass:

```sass
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
```

into this less beautiful SCSS:

```scss
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
```
