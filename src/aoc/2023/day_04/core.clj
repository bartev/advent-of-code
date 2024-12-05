(ns day-4.core
  (:require
   [utils :refer [read-lines-io-slurp]]
   [clojure.string :as str]
   [clojure.edn :as edn]))

;; Scorecards on Island Island

(defn extract-digits [x]
  (vec (re-seq #"\d+" x)))

(defn ->lists [[winners my-nums]]
  {:winners (vec winners)
   :my-nums (vec my-nums)})

;; Different from `parse-card` below.
(defn parse-cards [fname]
  (->> (read-lines-io-slurp fname)
       ;; (#(map (fn [line] (str/split line #":")) %))
       (map (fn [x] (-> x
                        (str/split #":")
                        second
                        (str/split #"\|")
                        (#(mapv extract-digits %))
                        ->lists)))))

(defn common-items-card
  "Get the set of items that are common to both winners and my-nums"
  [{:keys [winners my-nums]}]
  (set (clojure.set/intersection (set winners) (set my-nums))))


(def card {:winners ["41" "48" "83" "86" "17"],
           :my-nums ["83" "86" "6" "31" "17" "9" "48" "53"]})

(defn ->winnings
  "Calculate how much you won by taking 2^num-matches if num-matches > 0."
  [num-matches]
  (if (pos? num-matches)
    (Math/pow 2 (dec num-matches))
    0))

(defn part1 [fname]
  (->> (parse-cards fname)
       (map common-items-card)
       (map count)
       (mapv ->winnings) ; Calculate winnings for each card.
       (apply +) ; Sum up the winnings.
       ))

(part1 "input-sample.txt")
;; => 13.0
(part1 "input.txt")
;; => 25010.0


;;; Part 2

(defn common-items [lst1 lst2]
  (set (clojure.set/intersection (set lst1) (set lst2))))

;; Different from `parse-cards` above.
(defn parse-card
  "Parse out the card index, winners and my numbers.
  Watch out for different number of spaces after `Card`
  between the sample and real data."
  [input-string]
  (let [regex #"(?i)Card\s*(\d+): (.+?) \| (.+)$"
        match (re-matches regex input-string)
        card (parse-long (second match))
        winners (extract-digits (nth match 2))
        my-nums (extract-digits (nth match 3))
        common-items (common-items winners my-nums)
        num-winners (count common-items)
        ]
    {:card card
     ;; :winners winners
     ;; :my-nums my-nums
     :num-winners num-winners
     :num-copies 1}))

(parse-card "Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53")
;; => {:card 1, :num-winners 4, :num-copies 1}
(parse-card "Card   1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53")
;; => {:card 1, :num-winners 4, :num-copies 1}


;; How does `re-matches` work?
;; 0: Complete string that matched.
;; 1, 2, ...: Each matching group

;; Note how only the <alpha><digits><alpha> part matched
;; (re-seq #"[^\d]*(\d+)[^\d]*" "abc123def456")
;; => (["abc123def" "123"] ["456" "456"])

;; (let [input-string "Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53"
;;       regex #"(?i)Card (\d+): (.+?) \| (.+)$"
;;       match (re-matches regex input-string)]
;;   match)
;; => ["Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53"
;;     "1"
;;     "41 48 83 86 17"
;;     "83 86  6 31 17  9 48 53"]

;; (re-seq #"[^\d]*(\d+)[^\d]*" "abc123def456")
;; => (["abc123def" "123"] ["456" "456"])

(defn parse-cards-idx [fname]
  (->> (read-file-lines-slurp fname)
       ;; (#(map (fn [line] (str/split line #":")) %))
       ;; (map parse-card)
       ))

(defn update-cards
  "Increment the :num-copies of the next :num-winners cards by the
  number of copies of the current card.
  E.g. You have 4 copies of the current card (card 3).
  It has 2 winners.
  Add 4 to the :num-copies field of the next 2 cards."
  [cards card-num]
  (let [cur-card (nth cards (dec card-num))
        num-copies (:num-copies cur-card)
        num-winners (:num-winners cur-card)]
    (map-indexed
     (fn [idx item]
       (if (and (>= idx card-num) ; Start AFTER current card
                (< idx (+ card-num num-winners))) ; Modify `num-winners` cards
         (update item :num-copies (fnil + 0) num-copies) ; (fnil + 0) replaces nil with 0 if value is missing.
         item))
     cards)))

(def cards-sample [{:card 1, :num-winners 4, :num-copies 1}
                   {:card 2, :num-winners 2, :num-copies 1}
                   {:card 3, :num-winners 2, :num-copies 1}
                   {:card 4, :num-winners 1, :num-copies 1}
                   {:card 5, :num-winners 0, :num-copies 1}
                   {:card 6, :num-winners 0, :num-copies 1}])

(update-cards cards-sample 1)
;; => ({:card 1, :num-winners 4, :num-copies 1}
;;     {:card 2, :num-winners 2, :num-copies 2}
;;     {:card 3, :num-winners 2, :num-copies 2}
;;     {:card 4, :num-winners 1, :num-copies 2}
;;     {:card 5, :num-winners 0, :num-copies 2}
;;     {:card 6, :num-winners 0, :num-copies 1})

(let [cards cards-sample
      after-1 (update-cards cards-sample 1)
      after-2 (update-cards after-1 2)
      after-3 (update-cards after-2 3)
      after-4 (update-cards after-3 4)]
  {:after-1 after-1
   :after-2 after-2
   :after-3 after-3
   :after-4 after-4})
;; => {:after-1
;;     ({:card 1, :num-winners 4, :num-copies 1}
;;      {:card 2, :num-winners 2, :num-copies 2}
;;      {:card 3, :num-winners 2, :num-copies 2}
;;      {:card 4, :num-winners 1, :num-copies 2}
;;      {:card 5, :num-winners 0, :num-copies 2}
;;      {:card 6, :num-winners 0, :num-copies 1}),
;;     :after-2
;;     ({:card 1, :num-winners 4, :num-copies 1}
;;      {:card 2, :num-winners 2, :num-copies 2}
;;      {:card 3, :num-winners 2, :num-copies 4}
;;      {:card 4, :num-winners 1, :num-copies 4}
;;      {:card 5, :num-winners 0, :num-copies 2}
;;      {:card 6, :num-winners 0, :num-copies 1}),
;;     :after-3
;;     ({:card 1, :num-winners 4, :num-copies 1}
;;      {:card 2, :num-winners 2, :num-copies 2}
;;      {:card 3, :num-winners 2, :num-copies 4}
;;      {:card 4, :num-winners 1, :num-copies 8}
;;      {:card 5, :num-winners 0, :num-copies 6}
;;      {:card 6, :num-winners 0, :num-copies 1}),
;;     :after-4
;;     ({:card 1, :num-winners 4, :num-copies 1}
;;      {:card 2, :num-winners 2, :num-copies 2}
;;      {:card 3, :num-winners 2, :num-copies 4}
;;      {:card 4, :num-winners 1, :num-copies 8}
;;      {:card 5, :num-winners 0, :num-copies 14}
;;      {:card 6, :num-winners 0, :num-copies 1})}

;; (update {:a 1} :a (fnil + 0) 3)
;; => {:a 4}

;; How `fnil` works. Replaces FIRST argument if `nil`.
;; ((fnil + 0) nil 4)
;; ;; => 4

;; ((fnil + 0) 1 4)
;; ;; => 5

;; ((fnil + 0) 1 nil)
;; ;; => Execution error (NullPointerException) at day-4.core/eval13794 (REPL:197).
;; ;;    Cannot invoke "Object.getClass()" because "x" is null

;; (update {:name "jammes" :age 26} :foo + 10)

;; (def items [:a :b :c :d])
;; (nth items 3)

(defn process-cards [cards]
  (let [num-cards (count cards)]
    (loop [cur-idx 1 ; index 1 corresponds to card 1.
           cur-cards cards]
      (if (<= num-cards cur-idx)
        cur-cards
        (recur (inc cur-idx)
               (update-cards cur-cards cur-idx))))))

(defn part2 [fname]
  (->> (parse-cards-idx fname)
       process-cards
       (mapv :num-copies)
       (apply +)
       ))

(part2 "input-sample.txt")
;; => 30

(part2 "input.txt")
;; => 9924412
