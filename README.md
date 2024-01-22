## advent-of-code

Solutions to all of the problems in

https://adventofcode.com/events

for anyone interested.

The solutions are written in Python following a specific template. [Reuse of this code](#adding-your-own-solutions--using-in-future-aoc-competitions) as well as suggestions are strongly encouraged. Since the tasks themselves come out at around 5AM for me, my focus is on writing the as optimal solutions as I can for the problems (time-complexity wise), hence the abstractions.

Solutions for all days can be found in the repository for the following years:

- [2015](https://adventofcode.com/2015)
- [2016](https://adventofcode.com/2016)
- [2023](https://adventofcode.com/2023)

## Prerequisites

Make sure you have Python 3.x installed on your local machine before running the solutions. Alternatively, you can also have Anaconda3 installed and it should work fine as well.

The solutions mostly utilize "vanilla" Python features, meaning we won't heavily rely on new(er) features from the more recent versions. Feel free to open an issue if this is not the case though and I'll gladly fix the solutions.

## Structure

Each day of AoC is solved within the respectable `<year>/Day <x>` directory. The year represents the `year` of the event taking place (for example, for 2023 it would refer to [this event](https://adventofcode.com/2023)), while `x` represents the solution for the respectable day of that year.

Typically, in the folder of each day you will have the following files:

- `input.txt` (used for the actual test case of the problem)
- `input_test.txt` (used as a custom test case, mainly for testing or containing the example test case in each problem)
- `p1.py` (the engine running and printing the solution for both inputs for part 1 of the puzzle)
- `p2.py` (the engine running and printing the solution for both inputs for part 2 of the puzzle)

This of course assumes that the inputs for part 1 and part 2 of the puzzle are the same. In case they are not, you will likely find something along the lines of the same names but suffixed by `_p1` and `_p2` for the different parts (for example, if the test input for each part is different we would find `input_test_p1.txt` and `input_test_p2.txt`).

In other words, the structure would look something like this for each day:

```
<year>/
├─ ...
├─ Day <x>/
|  ├── input.txt
|  ├── input_test.txt
|  ├── p1.py
|  └── p2.py
|
├─ Day <x + 1>/   
|  ├── input.txt
|  ├── input_test_p1.txt
|  ├── input_test_p2.txt
|  ├── p1.py
|  └── p2.py
└─ ...
```

In this example, for day `x` we have the same input for both parts. For day `x + 1` on the other hand, we have a different test input for both parts (but the same real input).

## `SolverCore`

The `SolverCore` class is responsible for running the solutions for the actual problems. It takes the following arguments:

| argument               | required | description                                                                                                                                                              |
|------------------------|----------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `expected_answer`      | yes      | This is the expected answer of the test samples, which is going to be checked against the result your program outputs.                                                   |
| `input_types_override` | no       | This is an override of the names of the input files that are going to be used as the problem input for your solution. If omitted, it will simply be an empty dictionary. |

### Example

To use the `SolverCore` class, we need to create our own `Solver` class and implement the `_solve` method. After this, whenever we instantiate our new solver we can simply call `solver.solve()` and the class will take care of the rest.

For example:

```python
class Solver(SolverCore):
    def _solve(self, problem_input):
        return sum([int(line) for line in problem_input])

solver = Solver(15)
solver.solve()
```
is something we would use to find the sum of each line in the input, assuming our input file looks like this:

```text
1
2
3
4
5
```
By default, the `SolverCore` class will try to read the test input from `input_test.txt` and the real one from `input.txt`. If needed, you can [override this behaviour](#overriding-the-input_types) for each problem easily.

#### Overriding the `input_types`

The second argument, `input_types_override` is responsible for overriding the names of the files used for both test cases. The following input types are supported:

- `test` - the input type used for the test sample (its default value is `input_test.txt`)
- `real` - the input type used for the real sample (your actual problem input, whose default value is `input.txt`)

This means that if we want to override the files from which we read the test samples for example, we would need to have

```
solver = Solver(25, { 'test': 'my_test_input.txt' })
```
which would make sure that we read the actual test input from `my_test_input.txt` and compare it against the expected value, which in this case is `25`.

## Running the solutions

To run each one of the daily problem solutions, go in the adequate folder (something along the lines of `<year>/Day <x>`), execute

```
python p1.py
```
or
```
python p2.py
```

and it should work out of the box.

Optionally, the repo comes with an `.idea` preset for `PyCharm` so if you're using this you can simply run each solution and it should also work.

If you wish to run the solutions with your own test cases, you can refer to the [structure section](#structure) as well [`SolverCore`](#solvercore) as to know where and how to add them.

#### Optional arguments

If you wish to run only a specific input, the core solver class comes with that functionality.

The currently supported arguments are:

| argument | required | description                                                                                                                                                              |
| -------- |----------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `-t`     | no       | Runs only the `input_test.txt` test case (or whichever one was specified as the `test` input) and compares it with the result passed to the `Solver` factory constructor |
| `-r`     | no       | Runs only the `input.txt` test case (or whichever one was specified as the `real` input)                                                                                 |
| `-a`     | no       | Runs both of the test cases (as specified)                                                                                                                               |

As an example, if we only wanted to run our custom test case (for debugging purposes or similar) on part 1 of a certain day, we would run:

```
python p1.py -t
```
If no arguments are passed, **the program will default to `-a` as an argument** and will run both.

## Adding your own solutions / Using in future AoC competitions

The repo comes with some core libraries used for testing the solutions or reusing already written algorithms. If you find it useful and want to use it in future AoC competitions, you may do that freely.

Amongst other things, there is the `/Example/Template` directory. This directory is essentially a pre-set "AoC Day". Adding another day to the repo is as simple as copying contents of `/Template` into another directory (for example `Day 12`) and after copying over the test cases you should be good to go. Make sure you don't forget adding the expected input for the test samples as well, as [explained before](#solvercore).

From that point on, you can simply implement the `_solve(self, problem_input)` method of whichever class inherits from `SolverCore` and run the solutions.
