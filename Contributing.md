# Guidelines

## Language Of These Guidelines

SHOULD = strong suggestion in order to make these graphs clear

MUST = your PR won't be accepted if this isn't followed

## File Organization
- File names MUST follow the format: `X_Y_-_NAME_GOES_HERE`
	- `X` is either the string `Npc` for regular entities, or `Boss` for bosses
	- `Y` is the npc/boss's number as an integer
- Regular entities MUST go in the `ANP` directory, while room/map bosses MUST go in the `BOA` directory

## Graphing

### Nodes/States
- Node names MUST be 4 digit (0 padded) integers
	- Just imagine that you were typing in an `<ANP` or `<BOA` command.
- Node descriptions SHOULD be a high-level/modder-oriented description of  the state
	- Don't go into detail about any internal actions taking place, such as timers being set, etc., those should be placed in a note instead
- Any node/state that has special conditions outside the npc/boss's switch statement to reach it MUST have a note explaining what conditions must be met

### Connections
- Node connections MUST follow this format:
	- Solid lines (`-->`) = Npc sets its act_no, then breaks from that case
	- Dashed lines (`-[dashed]->`) = Npc sets its act_no to the next case, then falls through into that case
	- Dotted lines (`-[dotted]->`) = Npc falls through into the next case
- The condition for taking a transition MUST be used as its label
	- If it is not obvious why the condition wouldn't *always* be met (such as an entity being grounded vs airborne), an extra transition SHOULD be added

### Notes
- Notes SHOULD be used to describe any internal actions being taken
	- Things like wait times being set, becoming invulnerable, picking a new target, etc.
- Notes MUST describe one action per line
	- This includes the source code (don't write `\n`)
- Notes MUST be attached to the most relevant part in the entity's logic
	- Actions taken during a transition should be tied to the transition arrow
	- Actions taken at any other time in that state should be tied to that node