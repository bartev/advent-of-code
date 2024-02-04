(ns aoc.2023.day-09.core
  (:require
   [aoc.file-util :as f]
   [aoc.string-util :as s]))

(def input (f/read-int-vectors "2023/d09.txt"))
(def input-sample (f/read-int-vectors "aoc/2023/day_09/sample.txt"))

(defn input-size [input]
  {:rows (count input)
   :cols (->> input
              (map count)
              first)})


;; Explore the data

input-sample
;; => [[0 3 6 9 12 15] [1 3 6 10 15 21] [10 13 16 21 30 45]]


(input-size input-sample)
;; => {:rows 3, :cols 6}

(input-size input)
;; => {:rows 200, :cols 21}


;; Structure for a single row


(defn ->deltas [row] (mapv - (rest row) row))

(defn <-deltas [row deltas]
  (let [delta+ (conj deltas (last deltas))]
    (mapv + row delta+)))

(<-deltas [0 3 6 9] [3 3 3 3])

(def xs [1 2 3 4])
(last xs)
(conj xs (last xs))

(defn inc-prev
  "Add the last value of ys to the last value of xs, and append to end of xs"
  [xs ys]
  (conj xs (+ (last xs) (last ys))))

(defn inc-next
  "Add the last value of xs to the last value of ys, and append to end of ys"
  [xs ys]
  (conj ys (+ (last ys) (last xs))))

(inc-prev [0 3 6 9] [3 3 3 3])

(defn reduce-reverse
  "reduce function applied to reverse of a collection"
  [f coll]
  (reduce f (reverse coll)))

(reduce-reverse inc-next [[0 3 6 9 12 15] [3 3 3 3 3] [0 0 0 0]])


(defn process-row
  "process a row of data"
  [row reduce-fn]
  (loop [data [row]
         deltas (->deltas row)]
    (if (every? zero? deltas)
      (->> deltas
           (conj data)
           (reduce-reverse reduce-fn))
      (do #_(println deltas)
          (recur (conj data deltas)
                 (->deltas deltas))))))

(process-row (first input-sample) inc-next)
;; => [0 3 6 9 12 15 18]

(process-row (second input-sample) inc-next)
;; => [1 3 6 10 15 21 28]

(process-row (nth input-sample 2) inc-next)
;; => [10 13 16 21 30 45 68]


(defn part-1 [input]
  (->> input
       (map #(last (process-row % inc-next)))
       (apply +)))

(part-1 input-sample)
;; => 114
(part-1 input)
;; => 1834108701


;; Part 2
;; This time work BACKWARDS.
;; Note, you'll need to subtract instead of add.

(defn dec-next
  "Add the last value of xs to the last value of ys, and append to end of ys"
  [xs ys]
  (cons (- (first ys) (first xs)) ys))

(defn part-2 [input]
  (->> input
       (map #(first (process-row % dec-next)))
       (apply +)))

(part-2 input-sample)
;; => 2

(part-2 input)
;; => 993
