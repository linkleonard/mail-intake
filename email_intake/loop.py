#!/usr/bin/env python
from email_intake import mbox
import os

folder = "/Users/leonard/Documents/output/"

def main():
    headers = set()
    for fname in os.listdir(folder):
        with open(folder + fname) as fp:
            # Consume the From_ line
            # See: http://www.qmail.org/man/man5/mbox.html
            next(fp)

            header_lines = mbox.collect_headers(fp)
            grouped_header_lines = mbox.group_lines_as_headers(header_lines)
            for header_lines in grouped_header_lines:
                header = mbox.header_as_tuple(iter(header_lines))
                headers.add(header[0])


if __name__ == '__main__':
    main()
