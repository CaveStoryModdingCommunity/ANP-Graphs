# Guidelines

## Naming
- All entities start with the state labeled "Init"
- File names must follow the format:
	- `XXXX_YYY_-_NAME_GOES_HERE`
	- `X` is either the string `Npc` for regular entities, or `Boss` for bosses
	- `Y` is a 0-padded integer (`000`-`999`)
- Entities go in the ANP directory, Bosses go in the BOA directory

## Graphing
- Solid lines -> Npc sets its act_no, then breaks from that case
- Dashed lines -> Npc sets its act_no to the next case, then falls through into that case
- Dotted lines -> Npc falls through into the next case
