# Advent of Code 2019

My solutions to the [Advent of Code 2019](https://adventofcode.com/2019) problems.

I have built them as one class for each day in the test package. Base classes handle file I/O and provide two methods to override:
* `process()` receives the contents of the input file (either one line at a time or all lines at once depending on chosen the test base class) and returns the output which is then saved to the output file.
* `test()` can be used to verify the workings of `process()` using standard unit test mechanisms.

Functionality that is shared across days is in separate packages at the root level, e.g. intcode. 