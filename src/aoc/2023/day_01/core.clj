;; #!/usr/bin/env bb

(ns day-1.core
  (:require
   [clojure.string :as str]
   [utils :refer [get-local-fname
                  read-lines-io]]))

;; I made this extra complicated!

;; https://adventofcode.com/2023/day/1

;; The newly-improved calibration document consists of lines of text;
;; each line originally contained a specific calibration value that
;; the Elves now need to recover. On each line, the calibration value
;; can be found by combining the first digit and the last digit (in
;; that order) to form a single two-digit number.

;; For example:

;; 1abc2
;; pqr3stu8vwx
;; a1b2c3d4e5f
;; treb7uchet

;; In this example, the calibration values of these four lines are 12,
;; 38, 15, and 77. Adding these together produces 142.

;; Consider your entire calibration document. What is the sum of all of the calibration values?

;; => "/Users/bartev/dev/github/aoc-23/src/day_1/sample-input.txt"


;; => #object[sun.nio.fs.UnixPath 0x57e6807a "/Users/bartev/dev/github/aoc-23/src/day_1"]


;; Define this here so I can use it in the tests.
(def fname-sample-1 (get-local-fname "sample-input.txt"))
;; fname-sample-1
;; => "/Users/bartev/dev/github/aoc-23/src/day_1/sample-input.txt"
(def fname-live (get-local-fname "input.txt"))

;; fname
;; => "/Users/bartev/dev/github/aoc-23/src/day_1/sample-input.txt"

(def inputs-sample-1 (read-lines-io fname-sample-1))

(def inputs-live (read-lines-io fname-live))

;; sample-input
;; => ("1abc2" "pqr3stu8vwx" "a1b2c3d4e5f" "treb7uchet")

(defn extract-numbers [s]
  "Extract all numbers from a string, concatenate them and read as a single number"
  (->> s
       (re-seq #"\d")
       ;; vec
       ;; (#(conj [(first %) (last %)]))
       (apply str)
       ;; clojure.edn/read-string
       parse-long))

;; (extract-numbers "abc2de")
;; => 22

;; Should use `(range 1 10)`
(def digits-as-strings (map #(-> % inc str) (range 9)))
(def digit-names ["one" "two" "three" "four" "five" "six" "seven" "eight" "nine"])
(def number-string-map
  (zipmap digit-names digits-as-strings))
(def number-name-digit-map (zipmap digit-names (map inc (range 9))))

(defn sum-calib-data
  "Sum the calibration data (part 1)."
  [fname]
  (let [data (read-lines-io fname)
        data-nums (mapv extract-numbers data)]
    (apply + data-nums)))

;; Check part 1 calibration data
(sum-calib-data fname-sample-1)
;; => 142

;; This is the answer.
(sum-calib-data fname-live)
;; => 54877

;;; Part 2

(def fname-sample-2 (get-local-fname "sample-input-pt-2.txt"))
(def sample-input-2 (read-lines-io fname-sample-2))

;; search-for

(defn find-all-sub-indices
  "Find all the indices of `needle` in `haystack`"
  [haystack needle]
  (loop [positions []
         start (str/index-of haystack needle)]
    (if (nil? start)
      positions
      (recur (conj positions start)
             (str/index-of haystack needle (inc start))))))

(defn indices->map [xs value]
  (when (not (empty? xs))
    (mapv (fn [x] {:index x :value value}) xs)))

(def search-for
  (interleave digits-as-strings digit-names))

(defn strings->sub-index-maps
  "Convert a string to a map of index [indices]"
  [s]
  (->> search-for
       (map #(find-all-sub-indices s %))
       (zipmap search-for)
       (mapv (fn [[xs value]] (indices->map value xs)))
       (remove nil?)
       flatten
       (sort-by :index)))

(defn value->num-str [{:keys [index value]}]
  {:index index
   :value (or (number-string-map value) value)})

(defn put-it-together [s]
  (let [idx-map (-> s
                    strings->sub-index-maps
                    (#(map value->num-str %)))
        f-str (:value (first idx-map))
        l-str (:value (last idx-map))
        first-last-str (str f-str l-str)]
    (clojure.edn/read-string first-last-str)))

(put-it-together "twone3one")

(defn sum-calib-data-pt-2
  "Sum the calibration data (part 1)."
  [fname]
  (let [data (read-lines-io fname)
        data-nums (mapv put-it-together data)]
    (apply + data-nums)))

(sum-calib-data-pt-2 fname-live)
;; => 54100
