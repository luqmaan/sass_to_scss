import argparse
from pprint import pprint
import re


def count_leading_spaces(line):
    return len(line) - len(line.lstrip(' '))


def to_blocks(lines):
    outlines = []
    cleaned = []

    css_rule = re.compile(r'\s+\w+:')

    for line in lines:
        if line.isspace():
            continue
        cleaned.append(line.replace('\n', ''))

    for i, line in enumerate(cleaned):
        indent = count_leading_spaces(lines[i])
        try:
            next_indent = count_leading_spaces(lines[i + 1])
        except IndexError:
            continue
        try:
            prev_indent = count_leading_spaces(lines[i - 1])
        except IndexError:
            prev_indent = 0

        if css_rule.match(line) is not None:
            line += ';'

        if indent < next_indent:
            outlines.append(line + ' ' + '{')

        elif indent > prev_indent and indent != next_indent:
            outlines.append(line)
            closed_indent = indent
            spaces = indent - prev_indent
            while closed_indent != next_indent:
                insert = ' ' * (closed_indent - spaces) + '}'
                outlines.append(insert)
                closed_indent -= spaces

        else:
            outlines.append(line)

    return '\n'.join(outlines)


def main(args):
    lines = args.file.readlines()
    blocks = to_blocks(lines)
    for block in blocks:
        pprint(block)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert a SASS file to SCSS.')
    parser.add_argument('file', type=argparse.FileType('r'))
    parser.add_argument('--spaces', help="number of spaces for indentation", default=4)
    args = parser.parse_args()
    main(args)
