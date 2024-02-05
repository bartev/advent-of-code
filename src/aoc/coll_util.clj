(ns aoc.coll-util)

;; Copied from tschady
;; https://github.com/tschady/advent-of-code/blob/main/src/aoc/coll_util.clj#L43
;; Very similar to the ->deltas function I wrote 2023 day 9.
(defn intervals
  "Returns the seq of intervals between each element of `xs`, step `n` (default 1)"
  ([xs] (intervals 1 xs))
  ([n xs] (map - (drop n xs) xs)))
