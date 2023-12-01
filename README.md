## advent-of-code-2023

Solutions to all of the problems in

https://adventofcode.com/2023

for anyone interested.

The solutions are written in Python following a specific template. Reuse of this code as well as suggestions are strongly encouraged. Since the tasks themselves come out at around 5AM for me, my focus is on writing the most optimal solutions for the problems (time-complexity wise), hence the abstractions.

## Structure

Each day of AoC is solved within the respectable `Days/Day X` directory.

In each one of these, you will have a `Problem 1` and `Problem 2` directory, which contain the two parts of each problem.

In each of the problem directories, you will have the following files:

- `input.txt` (used for the actual test case of the problem)
- `input_test.txt` (used as a custom test case, mainly for testing or containing the example test case in each problem)
- `input_test_expected.txt` (containing a single line, the solution to the case in `input_test.txt`)
- `solution.py` (the engine running and printing the solution for both inputs)

In other words, the structure would look something like this for each day:

```
Days/
├─ ...
├─ Day <X>/
|  ├── Problem 1/
|  │   ├── input.txt
|  │   ├── input_test.txt
|  │   ├── input_test_expected.txt
|  │   └── solution.py
|  └── Problem 2/
|      ├── input.txt
|      ├── input_test.txt
|      ├── input_test_expected.txt
|      └── solution.py
└─ ...
```

## Prerequisites

Make sure you have Python 3.x installed on your local machine before running the solutions. Alternatively, you can also have Anaconda3 installed and it should work fine as well.

## Running the solutions

To run each one of the daily problem solutions, go in the adequate folder (something along the lines of `Day X/Problem X`), execute

```
python solution.py
```

and it should work out of the box.

If you wish to run the solutions with your own test cases, you can refer to the [Structure section](#structure) to know where to add them.

## Adding your own solutions / Using in future AoC competitions

The repo comes with some core libraries used for testing the solutions or reusing already written algorithms. If you find it useful and want to use it in future AoC competitions, you may do that freely.

Amongst other things, there is the `/Template` directory. This directory is essentially a pre-set "AoC Day". Adding another day to the repo is as simple as copying contents of `/Template` into another directory (for example `Day 12`) and after copying over the test cases you should be good to go.
