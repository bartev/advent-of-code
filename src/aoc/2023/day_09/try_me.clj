(ns aoc.2023.day-09.try-me
  (:require
   [aoc.file-util :as f]))

(def input (f/read-int-vectors "2023/d09.txt"))


;; Understanding transducers

(def xform (map inc))

(transduce xform conj [1 2 3])
;; => [2 3 4]

(transduce xform + [1 2 3]) ;; => 9
(transduce xform * [1 2 3]) ;; => 24

;; Transducer to produce the first 10 odd numbers.
(def xf (comp (filter odd?)
              (take 10)))

;; Apply the transducer.

;; Get numbers as a seq
(transduce xf conj (range))
;; => [1 3 5 7 9 11 13 15 17 19]

(transduce xf + (range))
;; => 100

;; with an initializer
(transduce xf + 17 (range))
;; => 117

;; concat to a string
(transduce xf str (range))
;; => "135791113151719"

(transduce xform conj [1 2 3])
