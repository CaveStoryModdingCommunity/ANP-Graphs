from typing import TextIO, List, Tuple
import re

class state_diagram:
    HEADER = re.compile(r'\@startuml(?: (.+))?')
    STATE = re.compile(r'state +(\S+)(?: <<\w+>>)?')
    NODE = re.compile(r'(\S+)(?: *: *(.+))?')
    EDGE = re.compile(r'(\S+) *-+(\S+)?(?:\[(\S+)\])?-*> *(\S+)(?: *: *(.+))?')
    TAIL = r'@enduml'

    BACKSLASH = '\\'
    COMMENT = '\''

    NOTE = r'note'
    NOTE_DIR = re.compile(NOTE + r' +(?:right|left|top|bottom)(?: +of +(.+))?(?: *: *(.+))?')
    NOTE_ON = re.compile(NOTE + r' +on +link(?: *: *(.+))?')
    NOTE_END = re.compile(r'end +' + NOTE)

    class node:
        def __init__(self, name: str, description: str = '', note: str = ''):
            self.name : str = name
            self.description : str = description
            self.note : str
    
    class edge:
        def __init__(self, start: str, end: str, description: str = '', note: str = ''):
            self.start : str
            self.end : str
            self.description : str
            self.note : str

    def __init__(self, stream: TextIO):
        self.nodes: List[state_diagram.node] = []
        self.edges: List[state_diagram.edge] = []
    
        #find the header
        header = ''
        while header == '':
            header = stream.readline().strip()
        header_match = state_diagram.HEADER.fullmatch(header)
        if header_match == None:
            raise ValueError('Invalid header')
        
        self.name = header_match.group(1)
        if self.name == None:
            self.name = ''

        #read the graph
        while True:
            line = stream.readline().strip()

            #skip whitespace and comments
            if line == None or line == '' or line.startswith(state_diagram.COMMENT):
                continue

            #stop at the end
            if line == state_diagram.TAIL:
                break
            
            #notes
            if line.startswith(state_diagram.NOTE):
                def read_note() -> str:
                    n = ''
                    l = stream.readline().strip()
                    while state_diagram.NOTE_END.fullmatch(l) == None:
                        if len(n) > 0:
                            n += ' '
                        n += l
                        l = stream.readline().strip()
                    return n
                def set_note(name:str, note:str, list: List) -> bool:
                    for i in list:
                        if i.name == name:
                            i.note = note
                            return True
                    return False

                #note on node
                m = state_diagram.NOTE_DIR.fullmatch(line)
                if not m == None:
                    name = m.group(1) or self.nodes[-1].name
                    note = m.group(2) or read_note()
                    while note.endswith(state_diagram.BACKSLASH):
                        note += ' ' + stream.readline().strip()
                    if not set_note(name, note, self.nodes):
                        self.nodes.append(state_diagram.node(name,note=note))
                    continue
                
                #note on edge
                m = state_diagram.NOTE_ON.fullmatch(line)
                if not m == None:
                    note = m.group(1) or read_note()
                    while note.endswith(state_diagram.BACKSLASH):
                        note += ' ' + stream.readline().strip()
                    self.edges[-1].note = note
                    continue

                raise ValueError('Invalid note: ' + line)

            #basic state declaration
            m = state_diagram.STATE.fullmatch(line)
            if not m == None:
                self.nodes.append(state_diagram.node(m.group(1)))
                continue

            #regular nodes
            m = state_diagram.NODE.fullmatch(line)
            if not m == None:
                n = state_diagram.node(m.group(1))
                if not m.group(2) == None:
                    n.description = m.group(2)
                    while n.description.endswith(state_diagram.BACKSLASH):
                        n.description += ' ' + stream.readline().strip()
                self.nodes.append(n)
                continue

            #edges
            m = state_diagram.EDGE.fullmatch(line)
            if not m == None:
                e = state_diagram.edge(m.group(1), m.group(4))
                if not m.group(5) == None:
                    e.description = m.group(5)
                    while e.description.endswith(state_diagram.BACKSLASH):
                        e.description += ' ' + stream.readline().strip()
                self.edges.append(e)
                continue

            raise ValueError('Unknown line: ' + line)
            

