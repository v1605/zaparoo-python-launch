# zaparoo-python-launch
An example utility script to launch Zaparoo scripts via python

## Setup
Recommended to setup a python virtual environement to run the script but not required. Download all .py files from the repository and place them into the environment/working directory. After that step is complete, install the "websocket-client" library.

## Running the Script
The main.py script takes two parameters. The first is the websocket url to the Zaparoo service (eg. ws://mister.local:7497) and the second is the [ZapSript](https://wiki.zaparoo.org/ZapScript#Generic_Launch_(launch)) to run. The main_hardcoded.py requires you to update the url in the script file, which is more convient to update if this will be called in many places. It only takes the script argument.

````
python main.py ws://mister.local:7497 **launch.random:snes
python main_hardcoded.py **launch.random:snes
````
