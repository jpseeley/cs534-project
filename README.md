# cs534-project
CS534 Project

Justin Seeley<br/>
jpseeley@wpi.edu<br/>
Alex Stylos<br/>
acstylos@wpi.edu<br/>

Project<br/>
Language: Python<br/>

During execution there will be trace printouts to the terminal. 
For the backtracking search they include:
1. Variable selection using MRV heuristic and degree heuristic
2. Value ordering using LCV heuristic
3. Consistency checking and value assignment
4. Backtracking notification

For the AC-3 algorithm they include:
1. Arc popping from queue
2. Domain revisions made, if any

Part 1<br/>
Instructions:<br/>
Python is an interpreted language and thus scripts can be run from the commmand line if Python is installed.<br/>
1. Navigate to the project directory<br/>
2. Use the given CSP text files or copy your own into the directory<br/>

To run the project type:<br/>

python part1.py [input.txt]<br/>

Notes:
1. The input.txt is the input text file you wish to use<br/>
2. If no file is specified, the program will exit and ask you to specify a file<br/>
   a. If the specified file cannot be found, the program will show an error
3. This will run the CSP algorithm for part 1 on the file<br/>
4. Sample output for input_sample1.txt and input_australia.txt is in the part 1 report<br/>