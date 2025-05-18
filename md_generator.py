from typing import List
from pathlib import Path
import argparse, re, urllib.parse

NAME = re.compile(r'\D+(\d+)\s+-\s+(.+)\..+')
DEFAULT_SERVER = 'http://www.plantuml.com/plantuml/proxy'
DEFAULT_CONTENT = 'https://raw.githubusercontent.com/CaveStoryModdingCommunity/ANP-Graphs/main'

class Diagram:
    def __init__(self, path: Path):
        n = path.name.replace('_',' ')
        m = NAME.match(n)
        if m == None:
            raise ValueError('Invalid name: ' + path.name)

        self.id = int(m.group(1))
        self.name = m.group(2)
        self.title = f'{self.id} - {self.name}'
        self.filename = path.name

def get_files(input: Path) -> List[Diagram]:
    if not input.is_dir():
        raise ValueError('Input must be a directory')
    res = []
    for f in input.iterdir():
        if f.is_dir():
            continue
        res.append(Diagram(f))
        
    res.sort(key=lambda d: d.id)
    return res


def make_md(input: List[Diagram], output: Path, server: str, cache: str, content: str):
    with open(output, 'w') as o:
        for d in input:
            o.write(f'# {d.title}\n')
            
            content_path = '/'.join([content, d.filename])

            url = server + '?' + urllib.parse.urlencode({ 'cache': cache, 'src': content_path })
            
            o.write(f'![{d.name}]({url})\n\n')

if __name__ == '__main__':
    parser = argparse.ArgumentParser('Markdown Generator', description='Generates the markdown files found in this repo')
    parser.add_argument('input', type=Path, help='The folder to convert')
    parser.add_argument('--plantuml_server', default=DEFAULT_SERVER, help='The url of the plantuml server that will render the diagrams')
    parser.add_argument('--plantuml_cache', choices=['yes','no'], default='no', help='The caching method the links should use')
    parser.add_argument('--content_url', default=DEFAULT_CONTENT, help='The url of the folder on the server containing the diagrams')
    parser.add_argument('output', type=Path, help='The destination to write to')

    args = parser.parse_args()

    diagrams = get_files(args.input)
    content_path = '/'.join([args.content_url, args.input.name])

    make_md(diagrams, args.output, args.plantuml_server, args.plantuml_cache, content_path)
