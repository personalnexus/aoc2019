# Advent of Code 2019

My solutions in Python to the [Advent of Code 2019](https://adventofcode.com/2019) problems.

I have built them as one class for each day in the test package. Base classes handle file I/O and provide two methods to override:
* `process()` receives the contents of the input file (either one line at a time or all lines at once depending on the chosen test base class) and returns the output which is then saved to the output file.
* `test()` can be used to verify the workings of `process()` using standard unit test mechanisms with the example inputs and outputs given in the puzzle.

Functionality that is shared across days is in separate packages at the root level, e.g. intcode.

I have decided to code in Python, because I want to get more proficient in that language. Hence, this code does not aim to be the most compact or Pythonic, but should be readable by someone with a basic understanding of Python. I also aim for the same clean code principles I use in my day-job, e.g. by limiting the number of nested function calls, introducing variables with descriptive names for intermediate results, placing related functionality in small, well-named and easy to understand classes and so on.  