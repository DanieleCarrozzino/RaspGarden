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

##To control raspberry pins view link

https://www.google.com/search?q=raspberry+pi+zero+2w+pin&rlz=1C1CHBF_itIT971IT971&oq=pin+raspberry+pi+2W&gs_lcrp=EgZjaHJvbWUqCAgBEAAYFhgeMgYIABBFGDkyCAgBEAAYFhgeMggIAhAAGBYYHjIKCAMQABiABBiiBDIKCAQQABiABBiiBDIKCAUQABiABBiiBDIKCAYQABiABBiiBDIKCAcQABiABBiiBNIBCDYzODVqMGoxqAIAsAIA&sourceid=chrome&ie=UTF-8#vhid=Eg1IkrMJmHBw5M&vssid=l

5V Supply 
Ground
Thermometer GPIO4
Soil moisture sensor GPIO2 serial data & GPIO3 serial clock
