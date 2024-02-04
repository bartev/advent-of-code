(ns aoc.2023.day-08.core-richards
  (:require [clojure.string :as str]
            [clojure.java.io :as io]))

;; This solution is from Norman Richards
;; https://gitlab.com/maximoburrito/advent2023/-/blob/main/src/day08/main.clj

(defn parse-line
  ""
  [text]
  (let [[_ a b c] (re-matches #"(... = \((...), (...)\))"text)]
    [a {:l b :r c}]))

(defn read-input
  ""
  [filename]
  (let [lines (str/split-lines (slurp (io/resource filename)))]
    {:steps (map #(keyword (str/lower-case (str %))) (first lines))
     :tree (into {} (map parse-line (drop 2 lines)))}))

(def full-input  (read-input "2023/d08.txt"))
(def sample1 (read-input "aoc/2023/day_08/sample.txt"))
(def sample2 (read-input "aoc/2023/day_08/sample-2.txt"))
(def sample3 (read-input "aoc/2023/day_08/sample-3.txt"))

(defn sum [ns] (reduce + 0 ns))

(sum [1 2 3 4])
;; => 10

(defn part1 [input]
  (loop [steps (cycle (:steps input))
         n 0
         state "AAA"]
    (if (= state "ZZZ")
      n
      (recur (rest steps)
             (inc n)
             (get-in input [:tree state (first steps)])))))

(part1 sample1)

(defn goal-state? [state] (str/ends-with? state "Z"))

(defn start-state? [state] (str/ends-with? stata "A"))

;; Explore what the paths look like
(defn explore [input state]
  (let [take-step (fn [state step]
                    (get-in input [:tree state step]))]
    (loop [steps (cycle (:steps input))
           n 0
           state state
           seen #{}]
      (when (goal-state? state)
        (println "*" n state))
      (if (and (goal-state? state)
               (seen state))
        :repeat
        (recur (rest steps)
               (inc n)
               (take-step state (first steps))
               (cond-> seen
                 (goal-state? state) (conj state)))))))

(explore sample1 "AAA")
