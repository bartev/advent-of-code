(ns aoc.string-util
  (:refer-clojure :exclude [ints])
  (:require
   [clojure.set :as set]
   [clojure.string :as str]))

;; Shameless coped from
;; https://github.com/tschady/advent-of-code/blob/main/src/aoc/string_util.clj

(def alphabet-lower "abcdefghijklmnopqrstuvwxyz")
(def alphabet-upper "ABCDEFGHIJKLMNOPQRSTUVWXYZ")

(defn ints
  "Return a collection of integers found in a string.  Integers may be negative."
  [s]
  (map read-string (re-seq #"-?\d+" s)))

(defn rotate-left [s n]
  (let [i (mod n (count s))]
    (concat (drop i s) (take i s))))

(defn rotate-right [s n]
  (let [i (mod n (count s))]
    (concat (take-last i s) (drop-last i s))))
