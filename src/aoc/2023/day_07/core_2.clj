(ns day-7.core-2
  (:require
   [clojure.string :as str]
   [day-7.core :as d7]))

;; Trying other peoples' solutions
;; Nothing crazy better than I did.

;; ideas to use
;; zipmap with (range)
;; (zipmap "23456789TJQK" (range))

(def hnd "KTJJT")

(frequencies hnd)

((comp sort vals frequencies) "KTJJT")
;; => (1 2 2)

((comp sort vals frequencies) "JTTJT")
;; => (2 3)

(def hand-strength (zipmap [[1 1 1 1 1]
                            [2 1 1 1]
                            [2 2 1]
                            [3 1 1]
                            [3 2]
                            [4 1]
                            [5]]
                           (range)))
hand-strength
;; => {[1 1 1 1 1] 0,
;;     [2 1 1 1] 1,
;;     [2 2 1] 2,
;;     [3 1 1] 3,
;;     [3 2] 4,
;;     [4 1] 5,
;;     [5] 6}

(defn hand->type [hand]
  (->> hand
       frequencies
       vals
       (sort >)))

(hand->type "JTTJT")
;; => (3 2)

(defn hand->type-2 [hand]
  ((comp #(sort > %) vals frequencies) hand))

(hand->type-2 "JTTJT")
;; => (3 2)

(def card-strength (zipmap "23456789TJQK" (range)))
card-strength
;; => {\J 9,
;;     \K 11,
;;     \Q 10,
;;     \2 0,
;;     \3 1,
;;     \4 2,
;;     \T 8,
;;     \5 3,
;;     \6 4,
;;     \7 5,
;;     \8 6,
;;     \9 7}

(zipmap (str/split "23456789TJQK" #"") (range))
;; => {"T" 8,
;;     "9" 7,
;;     "K" 11,
;;     "3" 1,
;;     "4" 2,
;;     "8" 6,
;;     "Q" 10,
;;     "J" 9,
;;     "7" 5,
;;     "5" 3,
;;     "6" 4,
;;     "2" 0}
(defn score [hand]
  {:hand-strength (hand-strength (sort-by - (vals (frequencies hand))))
   :card-strengths (mapv card-strength hand)})

(score "JTTJT")
;; => [4 [9 8 8 9 8]]
;; => [9 8 8 9 8]
;; => [4]

(defn parse-line [score-fn line]
  (let [[hand bid] (str/split line #" ")
        score (score-fn hand)]
    (merge
     {:hand hand
      :bid (parse-long bid)}
     score)))

(->> (d7/get-sample "input-sample.txt")
     (map (fn [line] (parse-line score line))))
