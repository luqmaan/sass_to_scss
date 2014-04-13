import argparse
from pprint import pprint
import re


def count_leading_spaces(line):
    return len(line) - len(line.lstrip(' '))


def sass_to_scss(sass_lines, spaces=4):
    outlines = []
    cleaned = []

    re_css_rule = re.compile(r'[\w\-\d]+:')
    re_import = re.compile(r'@import')
    re_sass_mixin = re.compile(r'\=\w+')
    re_sass_include = re.compile(r'\+\w+')

    for line in sass_lines:
        line = line.replace('\n', '')

        if re_import.match(line):
            line = line.replace('@import ', '@import "')
            line += '";'

        if re_sass_mixin.search(line):
            line = line.replace('=', '@mixin ')

        if re_sass_include.search(line):
            line = line.replace('+', '@include ')
            line += ';'

        if re_css_rule.search(line):
            line += ';'

        cleaned.append(line)

    # add an extra element in case we get to the end and
    # we need one more iteration to figure out the }
    # because we need to get next_indent
    cleaned.append('')

    for i, line in enumerate(cleaned):
        indent = count_leading_spaces(cleaned[i])
        try:
            next_indent = count_leading_spaces(cleaned[i + 1])
        except IndexError:
            next_indent = 0
        try:
            prev_indent = count_leading_spaces(cleaned[i - 1])
        except IndexError:
            prev_indent = 0

        print i, "next_indent", next_indent, "indent", indent, "prev_indent", prev_indent, line

        if indent < next_indent:
            line = line + ' ' + '{'
            print '{'

        if indent < prev_indent:
            print i
            closed_indent = prev_indent
            while closed_indent >= next_indent and closed_indent != 0:
                print '} : ', closed_indent, '- ', next_indent, '=', closed_indent - next_indent
                insert = ' ' * (closed_indent - spaces) + '}'
                outlines.append(insert)
                closed_indent -= spaces

        outlines.append(line)

    # remove that extra line we added
    outlines.pop()
    return '\n'.join(outlines)
