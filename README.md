# fe_assignment

rays = ['C2+','C3+','C5+','C6-','R4+','R5+','C7+','R5-']
mirror_positions = [(3,2),(3,7),(6,4),(8,7,10)] 

1. If hits directly, its absorbed
2. If pass diagonally, its redirected
3. If two diagonals, redirected twice
4. If mirror is diagonal while entering, reflect out immediately
5. Once life span gone, disappear
6. Pass through if no obstruction

**make sure all test cases pass

input validation <- what if input is invalid
stateful <- grid needs to keep track mirror (schema for state)
list of dictionary, each dictionary is mirror

-> so power of array is numpy

numpy array, representing each mirror with -1 or 1–

clarifications:
- how is the file run is it command line? 
- does it exit after execution

Express the class Cell() as a numpy array


Each test session is distinct from each other. Each session has a unique variable to refer to.

test session as a class:
 - python representation of the grid
 - tests that have been run, have not been run
 - results
 - methods all the function

main : every time a new user input comes in, instantiate a new instance of that class (arg parse) -> pass arguments to new instance, gather and print results back.

# use default logger library. loguru can be configured by color


threading. -> turning into async can be done later.


** make it robust, and error handling very verbose. (file paths incomplete, ), exception handling, file format (which line has unexpected character JSON parsing error message)

** test cases -> check for logical error. (shooting from column 9 when the grid is only 8x8)

Use type hints


# how code is organised
# Skip to end of mirror (jumping to end)

# Length very big (skipping ahead)

# Alot of mirror position (optimise of on seomthing else)

# alot of rays (optimise on something else)


# caching

# Switch case


Take home project tips
1. set up virtual environment (with dependencies installed)
2. triple check code to submit (instructions to set everything up)
3. Focus on solving the code problem first and optimise later
4. Add additional features if time permits
5. If you have any questions please clarify instead of being instantly rejected when it fails the test case
6. Small write up on design decisions, and potential improvements



Malformed inputs
1. R or C out of range
2. invalid characters in test
3. invalid file format


*** make sure its able to run on linux

Questions:
1. is -> separated by space " "
2. input files are .txt