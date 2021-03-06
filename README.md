This repository contains files for my master thesis at University of Wroclaw. Title of thesis is: "Gra "zgadnij automat"" and it is written in Polish language. Project is in progress.

# Project aim:
Aim of this project is to create a game in which player will have to guess an automata (https://en.wikipedia.org/wiki/Finite-state_machine) using some hints for this automaton. The game will be a mobile app written in the Python language (https://www.python.org/) using Kivy framework (https://kivy.org/#home).

# Launching the project:
First you need to install Python. Then you need to install all required packages:
```
pip install kivy
pip install matplotlib
pip install networkx
```

You will also need to install library kivy.garden.matplotlib. The method of installation depends on the operating system you are working on.
#### For Windows users:
Just type
```
pip install Kivy-Garden
garden install matplotlib --kivy
```
in the command line.
#### For Linux users:
Download the repo https://github.com/kivy-garden/garden. Go to directory garden/bin and execute command:
```
python3 garden install matplotlib --kivy
```

Also for linux users it is recommended to install two additional packages:
```
sudo apt-get install xclip
sudo apt-get install xsel
``` 

#### Starting the program
After installing packages you can start the application by running the command:
```
python Game.py
```

#### Important Note:
If you ever enounter error:  
```
ImportError: cannot import name '_png' from 'matplotlib'
```
just go to the file in which error occurs and comment out the line causing the error

# Project structure:
Files DFA.py, VPA.py and WFA.py contain definition of automatas. File DFA.py contatins definition of Deterministic finite automaton (https://en.wikipedia.org/wiki/Deterministic_finite_automaton) and Nondeterministic finite automaton (https://en.wikipedia.org/wiki/Nondeterministic_finite_automaton). File VPA.py contains definition of Deterministic visibly pushdown automaton (https://www.csa.iisc.ac.in/~deepakd/atc-common/vpa-stoc04.pdf). File WFA.py contains definitions of weighted automaton (https://en.wikipedia.org/wiki/Weighted_automaton). Files Game.py and Game.kv contain definition of application interface. File automata_generator.py contains functions that can generate random automata. 
