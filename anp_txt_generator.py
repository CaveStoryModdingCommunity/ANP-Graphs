from typing import List
from plantuml import state_diagram
from pathlib import Path
import argparse, re

NAME = re.compile(r'\D+(\d+)\s+-\s+(.+)')

def id_extractor(diagram: state_diagram) -> int:
    n = NAME.match(diagram.name)
    if n == None:
        raise ValueError('Invalid name: ' + diagram.name)
    return int(n.group(1))

def read_input(path: Path) -> List[state_diagram]:
    if path.is_dir:
        res = []
        for d in path.iterdir():
            if d.is_dir():
                continue
            with open(d,'r') as f:
                res.append(state_diagram(f))
        return res
    else:
        with open(path, 'r') as f:
            return [state_diagram(f)]

def to_txt(input: List[state_diagram], output: Path):
    with open(output, 'w') as o:
        for d in input:
            name = NAME.match(d.name)
            if name == None:
                raise ValueError('Invalid name: ' + d.name)
            o.write('    \t' + name.group(2) + ' [' + name.group(1) + ']' + '\n')

            for node in d.nodes:
                if node.name.isdigit():
                    o.write(node.name + '\t' + node.description + '\n')

            o.write('\n\n')

if __name__ == '__main__':
    parser = argparse.ArgumentParser('ANP.txt Generator', description='Generates an ANP.txt file from the given plantuml state diagrams')
    parser.add_argument('input', type=Path, help='The file/folder to read')
    parser.add_argument('output', type=Path, help='The destination to write to')

    args = parser.parse_args()

    input = read_input(args.input)
    if len(input) > 1:
        input.sort(key=id_extractor)

    to_txt(input, args.output)