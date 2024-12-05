(ns day-7.core
  (:require
   [clojure.edn :as edn]
   [clojure.java.io :as io]
   [clojure.string :as str]
   [tools.fetch :refer [fetch-input]]
   [utils :refer [get-local-fname]]))

(defn get-sample [fname]
  (vec (line-seq (io/reader (get-local-fname fname)))))

(get-sample "input-sample.txt")
;; => ["32T3K 765" "T55J5 684" "KK677 28" "KTJJT 220" "QQQJA 483"]

(defn get-lines [day]
  (-> (fetch-input day)
      str/split-lines))

(defn parse
  "live = 0 is sample, 1 = real data."
  [live]
  (let [lines (condp = live
                0 (get-sample "input-sample.txt")
                1 (get-lines 7))] ; Get day 7 data from web
    (->> lines
         (map #(str/split % #"\s+"))
         (map (fn [[hand bid]] {:hand hand :bid (parse-long bid)})))))

(def cards ["A" "K" "Q" "J" "T"
            "9" "8" "7" "6"
            "5" "4" "3" "2"])

(defn create-card-maps [cards]
  (zipmap cards (range (count cards) 0 -1)))

(def card-ranks (create-card-maps cards))
card-ranks
;; => {"T" 9,
;;     "9" 8,
;;     "K" 12,
;;     "3" 2,
;;     "4" 3,
;;     "8" 7,
;;     "Q" 11,
;;     "J" 10,
;;     "7" 6,
;;     "5" 4,
;;     "6" 5,
;;     "A" 13,
;;     "2" 1}

(parse 1)

(defn hand->type
  "Get the hand type (5 of a kind, 4 of a kind, etc).
  A `hand` is a string of 5 cards, e.g. `QQQJA`"
  [hand]
  (let [freqs (frequencies (str/split hand #""))
        values (sort > (vals freqs))]
    (condp = values
      [5] 50         ; 5 of a kind
      [4 1] 40       ; 4 of a kind
      [3 2] 32       ; Full house
      [3 1 1] 30     ; 3 of a kind
      [2 2 1] 22     ; 2 pair
      [2 1 1 1] 20   ; 1 pair
      [1 1 1 1 1] 10 ; High card
      )))

;; (hand->type "32T3K")

(defn process-hand
  "Add vector of chars, hand type to hand map"
  [hand-map]
  (let [char-vec (str/split (:hand hand-map) #"")
        char-ranks (mapv #(get card-ranks %) char-vec)
        tipe (hand->type (:hand hand-map))]
    (merge hand-map
           {:chars char-vec}
           {:ranks char-ranks}
           {:type tipe})))

(defn compare-hands
  "Sort by :type (desc) then :ranks (desc)"
  [x y]
  (compare [(:type y) (:ranks y) (:bid y) y]  ; Switching x & y causes descending sort
           [(:type x) (:ranks x) (:bid x) x]))

(defn create-ranked-maps
  "Add :hand-rank (index) starting at cnt, and working down to 1"
  [maps]
  (let [cnt (count maps)]
    (map-indexed (fn [index map]
                   (assoc map :hand-rank (- cnt index)))
                 maps)))

(defn add-winnings
  "Winnings = :bid * :hand-rank"
  [hand-map]
  (let [bid (:bid hand-map)
        rnk (:hand-rank hand-map)
        win (* bid rnk)])
  (assoc hand-map :win (* (:bid hand-map) (:hand-rank hand-map))))

(defn task1 [live]
  (->> (parse live)
       (mapv process-hand)
       (sort compare-hands)
       create-ranked-maps
       (map add-winnings)
       (map :win)
       (apply +)))

(task1 0)
;; => 6440

(task1 1)
;; => 253638586


;; Task 2
;; J cards are jokers

(def cards-j ["A" "K" "Q" "T"
              "9" "8" "7" "6"
              "5" "4" "3" "2"
              "J"])

(def card-ranks-j (create-card-maps cards-j))
card-ranks-j

(def ex-hand "KTJJT")

(defn hand->type-j
  "Get the hand type (5 of a kind, 4 of a kind, etc) when J is a wild card.
  A `hand` is a string of 5 cards, e.g. `QQQJA`"
  [hand]
  (let [tmp-hand (if (= "JJJJJ" hand)
                   hand
                   (str/replace hand #"J" ""))
        replace-with (->> (frequencies (str/split tmp-hand #""))
                          (apply max-key val)
                          key)
        new-hand (str/replace hand #"J" replace-with)]
    (hand->type new-hand)))

(hand->type-j ex-hand)
;; => 40

(hand->type ex-hand)
;; => 22

(hand->type-j "JJJJJ")
;; => 50

(defn process-hand-j
  "Add vector of chars, hand type to hand map"
  [hand-map]
  (let [char-vec (str/split (:hand hand-map) #"")
        char-ranks (mapv #(get card-ranks-j %) char-vec)
        tipe (hand->type-j (:hand hand-map))]
    (merge hand-map
           {:chars char-vec}
           {:ranks char-ranks}
           {:type tipe})))

(defn task2 [live]
  (->> (parse live)
       (mapv process-hand-j)
       (sort compare-hands)
       create-ranked-maps
       (map add-winnings)
       (map :win)
       (apply +)))

(task2 0)
;; => 5905

(task2 1)
;; => 253253225
