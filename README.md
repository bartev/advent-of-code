# Table of Contents

1.  [Introduction](#orgdd99be6)
2.  [Structure](#org6324024)
    1.  [Babashka scripts](#org5a605b3)
    2.  [Clojure](#orgd0f8925)
        1.  [Basic setup](#org7e54cdd)
        2.  [Tests](#orga25334a)
3.  [Running code](#orgdef063a)
    1.  [Clojure](#orgf6b1c9f)
    2.  [Python](#org791d946)
        1.  [I'm using `uv` to manage the environment.](#orgc7f367a)
        2.  [To add more dependencies,](#org31bf348)
4.  [Learnings](#org0d1dfca)
    1.  [Clojure](#org04cb310)
        1.  [Transducers](#org603b0e5)
    2.  [Python](#org3f1d583)
        1.  [I always forget the collections package](#org569ad8d)
        2.  [Remember regex syntax](#org85e7dea)
        3.  [Use profiling to see what's taking so long (see 2024 day 11)](#org9f2da87)

I'm basing the structure of this repo (`*.edn` files, etc) off of [tschady's repo](https://github.com/tschady/advent-of-code/tree/main).


<a id="orgdd99be6"></a>

# Introduction

-   2024-12-01 This year I'm using python.
    I'm still using the clojure scripts (babashka) to download the data and setup initial files.

-   2023 My Clojure solutions to the [Advent of Code](https://adventofcode.com) challenge (to be reused over multiple years).


<a id="org6324024"></a>

# Structure


<a id="org5a605b3"></a>

## Clojure


<a id="org7e54cdd"></a>

### Basic setup

Use `deps.edn` to define dependencies and paths.

Files in `src` and `resources` can be found during runtime.

Tests use file in `test`.


<a id="orga25334a"></a>

### Tests

Tests are under `tests`.

Tests use `kaocha` (not sure how this works yet).

`kaocha` recommends setting up test configs in `tests.edn`.

Run with

    bb test


<a id="orgdef063a"></a>

## Babashka scripts

Handy scripts (thanks tschady) are in `script`.

`bb.edn` defines tasks that call them.

e.g. To create stub files for 2023 day 7, download the data to `resources/day07.txt` and open the websites for the problem and data, run:

    bb go -y 2023 -d 7

or, if you want to use the current date, just run

    bb go

-   Make sure to update the `AOC_SESSION` cookie annually (expires after ~1 month)

<https://github.com/wimglenn/advent-of-code-wim/issues/1>


<a id="orgd0f8925"></a>

# Running code


<a id="orgf6b1c9f"></a>

## Python


<a id="orgc7f367a"></a>

### I'm using `uv` to manage the environment.

    uv venv
    source .venv/bin/activate


<a id="org31bf348"></a>

### To add more dependencies,

    uv add new_package
    uv add --dev dev_package
    uv sync

### Caching ###

It's really easy to cache function results. Useful for recursive functions.

`cache` or `lru_cache` (least recently used)

See 2024-12-19
```python
from functools import cache

@cache
def my_recursive_function(x):
    ...
```

<a id="org0d1dfca"></a>

## Clojure


<a id="org791d946"></a>

# Learnings


<a id="org04cb310"></a>

## Python


<a id="org569ad8d"></a>

### I always forget the collections package

-   2024 day 1, to make a `Counter` from a list

```
        from collections import Counter

        xs = [1, 2, 1, 3, 1, 4]
        counts = Counter(xs)

        # Counter({1: 3, 2: 1, 3: 1, 4: 1})
```


<a id="org85e7dea"></a>

### Remember regex syntax

-   2024 day 3, to find all matches and groups


<a id="org9f2da87"></a>

### Use profiling to see what's taking so long (see 2024 day 11)

### Transpose list of tuples, matrices, etc ###

Seen 2024-12-14, part 2.

Use `zip(*xs)` to unpack and reorganize data.

```
xs = [(43, 88), (18, 3), (39, 70), (68, 43)]

first_elements, second_elements = zip(*xs)
print(first_elements)  # Output: (43, 18, 39, 68)
print(second_elements) # Output: (88, 3, 70, 43)
```

### Walrus operator `:=` (assignment expression) ###

The expression `(xvar := variance(xs))` means:
Compute `variance(xs)` (call the `variance` function with `xs`).
Assign the result to the variable `xvar`.
Return the value of `xvar` for use in the rest of the condition.

Reduces redundancy, only call `variance(xs)` 1 time.

Example
```
if (xvar := variance(xs)) < bxvar:
    bx, bxvar = t, xvar
```

### Reading text from a file ###

#### Deconstruct: Read line 1 into a list, skip line 2, read line 3+ into a list ####

This is a nice snipped of code (2024-12-19)

```python
P, _, *D = open('test_data.txt').read().splitlines()
```

With test data like this:

```
r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb
```

The result is
```python
>>> P
'r, wr, b, g, bwu, rb, gb, br'
>>> _
''
>>> D
['brwrr', 'bggr', 'gbbr', 'rrbgbr', 'ubwu', 'bwurrg', 'brgr', 'bbrgwb']
```

### Using generators and itertools.product ###

Not sure if this is better, but ChatGPT suggested this change.

original, nested for-loops
```python
    def find_char_old(self, char: str = "S"):
        """Find the Point that contains `char`"""
        for row in range(self.rows):
            for col in range(self.cols):
                if self.get((row, col)) == char:
                    return (row, col)
```

after, using `itertools.product` and a generator function
```python
    def find_char(self, char: str = "S"):
        """GPT suggested improvements
        This is also marginally faster than my original double
        for-loop method
        """
        return next(
            (
                (row, col)
                for row, col in product(range(self.rows), range(self.cols))
                if self.get((row, col)) == char
            ),
            None,
        )
```

## Clojure


<a id="org603b0e5"></a>

### Transducers

<https://clojure.org/reference/transducers>

1.  Reducing function

    The kind of function you'd pass to `reduce`
    Takes an accumulated result and a new input and returns a new accumulated result.

2.  Transducer (`xform` or `xf`)

    A transformation from one reducing function to another.

    Examples

        (filter odd?) ;; returns a transducer that filters odd
        (map inc)     ;; returns a mapping transducer for incrementing
        (take 5)      ;; returns a transducer that will take the first 5 values

3.  Compose with `comp`

    Use the existing `comp` function.
    `comp` applies the rightmost function to the parameters, then the next rightmost function to the result, and so on.

        (def xf
          (comp
           (filter odd?)
           (map inc)
           (take 5)))

    The transformation above is equivalent to the sequence transformation

        (->> coll
             (filter odd?)
             (map inc)
             (take 5))


<a id="org3f1d583"></a>

## Math ##

### Chinese Remainder Theorem ###

[Chines Remainder Theorem Wiki](https://en.wikipedia.org/wiki/Chinese_remainder_theorem)

In mathematics, the Chinese remainder theorem states that if one knows
the remainders of the Euclidean division of an integer n by several
integers, then one can determine uniquely the remainder of the
division of n by the product of these integers, under the condition
that the divisors are pairwise coprime (no two divisors share a common
factor other than 1)
