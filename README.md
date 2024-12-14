
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
        3.  [For an editable install of the current package](#org8c70886)
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

# Running code


<a id="orgf6b1c9f"></a>

## Clojure


<a id="org791d946"></a>

## Python


<a id="orgc7f367a"></a>

### I'm using `uv` to manage the environment.

    uv venv
    source .venv/bin/activate


<a id="org31bf348"></a>

### To add more dependencies,

    uv add new_package
    uv sync


<a id="org8c70886"></a>

### For an editable install of the current package

(to add utility functions)

    uv pip install -e .


<a id="org0d1dfca"></a>

# Learnings


<a id="org04cb310"></a>

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

## Python


<a id="org569ad8d"></a>

### I always forget the collections package

-   2024 day 1, to make a `Counter` from a list
    
        from collections import Counter
        
        xs = [1, 2, 1, 3, 1, 4]
        counts = Counter(xs)
        
        # Counter({1: 3, 2: 1, 3: 1, 4: 1})


<a id="org85e7dea"></a>

### Remember regex syntax

-   2024 day 3, to find all matches and groups


<a id="org9f2da87"></a>

### Use profiling to see what's taking so long (see 2024 day 11)

