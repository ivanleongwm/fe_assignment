# fe_assignment

rays = ['C7+','C5+','R5-']

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

python array is a linkedlist so indexing is O(n) -> so power of array is numpy

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




# how code is organised
# Skip to end of mirror (jumping to end)

# Length very big (skipping ahead)

# Alot of mirror position (optimise of on seomthing else)

# alot of rays (optimise on something else)


# caching

# Switch case