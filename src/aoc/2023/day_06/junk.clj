(ns day-6.junk
  (:require
   [clojure.java.io :as io]
   [tools.utils :refer (get-local-fname)]
   [clojure.string :as str]))

(defn get-lines [fname]
  (vec (line-seq (io/reader (get-local-fname fname)))))

(def fname "input-sample.txt")
(def lfname "src/day_6/input-sample.txt")

(get-lines fname)
;; => ["Time:      7  15   30" "Distance:  9  40  200"]



(defn read-file-lines
  "Read a file line-by-line"
  [fname]
  (with-open [reader (io/reader fname)]
    (doall (line-seq reader))))

(get-local-fname fname)
;; => "/Users/bartev/dev/github/aoc-23/src/day_6/input-sample.txt"

(read-file-lines "src/day_6/input-sample.txt")
;; => ("Time:      7  15   30" "Distance:  9  40  200")

(read-file-lines (get-local-fname fname))
;; => ("Time:      7  15   30" "Distance:  9  40  200")

(defn read-file-lines-slurp
  "Read a file using slurp
  Split into a vec of strings (by line)"
  [fname]
  (->> (slurp (get-local-fname fname))
       str/split-lines))

(read-file-lines-slurp fname)
;; => ["Time:      7  15   30" "Distance:  9  40  200"]

(->> (slurp lfname) str/split-lines)
;; => ["Time:      7  15   30" "Distance:  9  40  200"]

(->> (io/reader lfname) line-seq)
;; => ("Time:      7  15   30" "Distance:  9  40  200")
(->> (io/reader lfname) line-seq doall)
;; => ("Time:      7  15   30" "Distance:  9  40  200")
(->> (io/reader lfname) line-seq vec)
;; => ["Time:      7  15   30" "Distance:  9  40  200"]
(->> (io/reader lfname) str/split-lines)
;; => Execution error (ClassCastException) at day-6.junk/eval18871 (REPL:48).
;;    class java.io.BufferedReader cannot be cast to class java.lang.CharSequence (java.io.BufferedReader and java.lang.CharSequence are in module java.base of loader 'bootstrap')

(->> (slurp lfname) line-seq)
;; => Execution error (ClassCastException) at day-6.junk/eval18873 (REPL:52).
;;    class java.lang.String cannot be cast to class java.io.BufferedReader (java.lang.String and java.io.BufferedReader are in module java.base of loader 'bootstrap')

(->> (slurp lfname) str/split-lines)
;; => ["Time:      7  15   30" "Distance:  9  40  200"]
(->> (io/reader lfname) line-seq vec)
;; => ["Time:      7  15   30" "Distance:  9  40  200"]
