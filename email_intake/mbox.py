from itertools import chain

def group_lines_as_headers(lines):
    current_header = []
    for line in lines:
        if not line.startswith(' ') and not line.startswith('\t') and current_header:
            yield current_header
            current_header = []
        current_header.append(line)

    yield current_header


def header_as_tuple(headers):
    line = next(headers)
    name, line = line.split(":", 1)
    return (name, chain([line.lstrip()], headers))


def collect_headers(lines):
    line = next(lines)
    while line != '\n':
        yield line
        line = next(lines)
