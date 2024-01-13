# Raspberry pi 2 W
## Structure
Left Part 3.3V - right part 5V

## Run command
### Running script
tmux a -t name_session 
to attach to the old running script
to get the list of running script
tmux list-sessions 

### Launching a new run
cd Project
source garden/bin/activate
cd RaspGarden
python3 main.py

### Launching a new run on tmux
tmux new -s name_session
- new run


