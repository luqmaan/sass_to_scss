import argparse
import re
import logging

DEFAULT_INDENTATION = 4


class SassToSCSS(object):

    def __init__(self, loglevel=None, spaces=DEFAULT_INDENTATION):

        self.spaces = spaces
        self.logger = logging.getLogger()
        self.logger.setLevel(loglevel or logging.WARNING)

    @classmethod
    def count_leading_spaces(cls, line):
        return len(line) - len(line.lstrip(' '))

    def convert(self, sass_lines):
        outlines = []
        cleaned = []

        re_css_rule = re.compile(r'\s*[\w\-\d]+:')
        re_import = re.compile(r'@import')
        re_sass_mixin = re.compile(r'\=\w+')
        re_sass_include = re.compile(r'\+\w+')
        re_sass_variable = re.compile(r'\s*\$')

        for line in sass_lines:
            line = line.replace('\n', '')

            if re_import.match(line):
                if not '@import "' in line:
                    line = line.replace('@import ', '@import "')
                    line += '"'
                line += ';'
            elif re_sass_mixin.search(line):
                line = line.replace('=', '@mixin ')
            elif re_sass_include.search(line):
                line = line.replace('+', '@include ')
                line += ';'
            elif re_css_rule.match(line):
                line += ';'
            elif re_sass_variable.match(line):
                line += ';'

            # an empty line resets the indent back to zero, skipping them solves that problem
            if line == '':
                continue

            cleaned.append(line)

        # add an extra element in case we get to the end and
        # we need one more iteration to figure out the }
        # because we need to get next_indent
        cleaned.append('')

        for i, line in enumerate(cleaned):
            indent = self.count_leading_spaces(cleaned[i])
            try:
                next_indent = self.count_leading_spaces(cleaned[i + 1])
            except IndexError:
                next_indent = 0
            try:
                prev_indent = self.count_leading_spaces(cleaned[i - 1])
            except IndexError:
                prev_indent = 0

            logging.debug('{} next_indent {}, indent {}, prev_indent {}, {}'.format(i, next_indent, indent, prev_indent, line))

            if indent < next_indent:
                line = line + ' ' + '{'
                logging.debug('{')

            if indent < prev_indent:
                closed_indent = prev_indent
                while closed_indent >= next_indent and closed_indent != 0:
                    logging.debug('}} : {}-{}={}'.format(closed_indent, next_indent, closed_indent - next_indent))
                    insert = ' ' * (closed_indent - self.spaces) + '}'
                    outlines.append(insert)
                    closed_indent -= self.spaces

            outlines.append(line)

        # remove that extra line we added
        outlines.pop()

        result = '\n'.join(outlines)
        self.logger.debug(result)

        return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert a Sass file to SCSS.')
    parser.add_argument('file', type=argparse.FileType('r'))
    parser.add_argument('--spaces', help="Number of spaces used for indentation", default=DEFAULT_INDENTATION)
    parser.add_argument('--debug', help="Output debug information", dest='debug', action='store_true')
    args = parser.parse_args()

    sassy = SassToSCSS(loglevel=args.debug or logging.INFO, spaces=args.spaces)

    lines = args.file.readlines()
    print sassy.convert(lines)
