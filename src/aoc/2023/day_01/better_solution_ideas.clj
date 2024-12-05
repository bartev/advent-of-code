(ns day-1.better-solution-ideas
  (:require
   [clojure.string :as str]
   [utils :refer [get-local-fname
                  read-lines-io]]
   [clojure.java.io :as io]))

;; This solution is much simpler (at least for part 2)
;; https://github.com/nbardiuk/adventofcode/blob/master/2023/src/day01.clj

(def fname-sample-1 (get-local-fname "sample-input.txt"))
(def inputs-sample-1 (read-lines-io fname-sample-1))

(def fname-sample-2 (get-local-fname "sample-input-pt-2.txt"))
(def inputs-sample-2 (read-lines-io fname-sample-2))

inputs-sample-1
;; => ("1abc2" "pqr3stu8vwx" "a1b2c3d4e5f" "treb7uchet")

(defn part1 [input]
  (apply +
         (for [line input]
           (let [digits (re-seq #"\d" line)
                 number (str (first digits) (last digits))]
             (clojure.edn/read-string number)))))

(part1 inputs-sample-1)
;; => 142

(defn part2 [input]
  (apply +
         (for [line input]
           (let [num (->> (re-seq #"(?=(\d|one|two|three|four|five|six|seven|eight|nine))" line)
                          (mapv (fn [[_ digit]] (name->digit digit digit)))
                          (map str)
                          (#(str (first %) (last %)))
                          clojure.edn/read-string)]
             num))))

(part2 inputs-sample-1)
;; => 142

(part2 inputs-sample-2)
;; => 281


;; Another solution
;; https://github.com/samcf/advent-of-code/blob/main/2023-01-trebuchet.clj

(def fname-sample-1 (get-local-fname "sample-input.txt"))
(->> (slurp (get-local-fname "sample-input.txt"))
     str/split-lines)
;; => ["1abc2" "pqr3stu8vwx" "a1b2c3d4e5f" "treb7uchet"]

(with-open [reader (io/reader fname-sample-1)]
  (doall (line-seq reader)))

;; Really nice!
;; https://github.com/vollcheck/aoc/blob/master/src/y23/day01.clj
(defn parse-line [line]
  (->> (re-seq #"\d" line)
       ((juxt first last))
       (apply str)
       parse-long))

(parse-line "1eightwone3four56")


;; More solutions
;; https://github.com/potetm/advent-of-code/blob/b77255eb3e3111274c5438189ba0a2ccbbe6eee4/src/advent_2023/day_1.clj

;; Nice word-hack
;; https://github.com/tschady/advent-of-code/blob/main/src/aoc/2023/d01.clj
