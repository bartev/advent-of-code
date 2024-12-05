(ns day-3.core
  (:require
   [utils :refer [read-lines-io-slurp]]
   [clojure.string :as str]
   [clojure.edn :as edn]))

;; Goal: Add up all the part numbers.
;; Input: Engine schematic

;; Any number adjacent to a symbol, even diagonally, is a "part number"
;; and should be included in your sum

;; Here is an example engine schematic:

;; 467..114..
;; ...*......
;; ..35..633.
;; ......#...
;; 617*......
;; .....+.58.
;; ..592.....
;; ......755.
;; ...$.*....
;; .664.598..

(defn read-input [fname]
  (read-file-lines-slurp fname))

(def fname-sample "input-sample.txt")

(read-input fname-sample)
;; => ["467..114.."
;;     "...*......"
;;     "..35..633."
;;     "......#..."
;;     "617*......"
;;     ".....+.58."
;;     "..592....."
;;     "......755."
;;     "...$.*...."
;;     ".664.598.."]

(def regex-symbol #"[^0-9.]")
(def regex-number #"\d+")

(defn find-start-indices [s regex]
  (let [matcher (re-matcher regex s)] ; matcher finds all matches
    (loop [indices []]
      (if (.find matcher) ; .find advances through the matches
        (recur (conj indices (.start matcher)))
        indices))))

(defn find-start-end-indices [s regex]
  "Return a list of dicts for each match containing the match, start and end +1 indices."
  (let [matcher (re-matcher regex s)] ; matcher finds all matches
    (loop [result []]
      (if (.find matcher) ; .find advances through the matches
        (recur (conj result {:match (.group matcher)
                             :start (.start matcher)
                             :end (.end matcher)}))
        result))))

(defn mapify-row
  "Process each line of the list"
  [row]
  {:numbers (find-start-end-indices row regex-number)
   :symbols (find-start-indices row regex-symbol)})

(defn combine-sort-vectors [& vectors]
  (->> vectors
       (apply concat)
       set
       sort
       vec))

(defn combine-before-after-symbol-indices
  "Combine lists of symbol indices from prev, current and next row for each row"
  [row-maps]
  (map-indexed
   (fn [idx row]
     (let [before (get row-maps (dec idx))
           after (get row-maps (inc idx))
           before-idx (:symbols before)
           after-idx (:symbols after)
           cur-idx (:symbols row)
           all-idx (vec (combine-sort-vectors cur-idx before-idx after-idx))]
       (merge row {:indices all-idx})))
   row-maps))

(defn get-number-if-overlap [number-map indices]
  (let [start (dec (:start number-map))
        end (:end number-map)]
    (when (-> (mapv #(<= start % end) indices)
              (#(some true? %)))
      (parse-long (:match number-map)))))

(defn check-for-overlaps
  "Check each number in :numbers for an overlap in :indices"
  [row-map]
  (let [numbers (:numbers row-map)
        indices (:indices row-map)]
    (->> numbers
         (map #(get-number-if-overlap % indices))
         (remove nil?)
         vec)))

;; Don't really need `map-indexed`
(defn part1 [fname]
  (->> (read-input fname) ; Read input file into a vec of strings.
       (map-indexed (fn [idx row] (merge {:row-idx idx} (mapify-row row))))  ; Mapfify each row (find numbers, symbols and indices of each)
       vec
       combine-before-after-symbol-indices
       (map check-for-overlaps)
       flatten
       (apply +)
       ))

(part1 fname-sample)
;; => 4361

(part1 "input.txt")
;; => 532331





;;;;; Part 2

;; Gears are `*` that are adjacent to exactly 2 part numbers.
;; Gear ratio is the product of those 2 numbers.

(defn mapify-row-star
  "Process each line of the list"
  [row]
  {:numbers (find-start-end-indices row regex-number)
   :stars (find-start-indices row #"\*")})

(defn combine-before-after-numbers
  "Combine lists of :numbers from prev, current and next row for each row"
  [row-maps]
  (map-indexed
   (fn [idx row]
     (let [before (get row-maps (dec idx))
           after (get row-maps (inc idx))
           before-nums (:numbers before)
           after-nums (:numbers after)
           cur-nums (:numbers row)
           all-nums (concat cur-nums before-nums after-nums)]
       (merge row {:all-numbers all-nums})
       {:stars (:stars row)
        :numbers all-nums}))
   row-maps))

(defn get-overlapping-numbers
  "Get all numbers from :numbers that overlap with idx."
  [numbers idx]
  (vec (remove nil? (map #(get-number-if-overlap % [idx]) numbers))))

(defn create-gear-map [star-index numbers]
  (let [overlaps (get-overlapping-numbers numbers star-index)]
    (when (= 2 (count overlaps))
      {:gear star-index
       :product-numbers overlaps
       :gear-ratio (apply * overlaps)})))

(defn ->gear-maps
  "Convert row-map to gear maps to the row-map"
  [row-map]
  (let [star-indices (:stars row-map)
        numbers (:numbers row-map)]
    (map #(create-gear-map % numbers) star-indices)))

(defn part2 [fname]
  (->> (read-input fname)
       (mapv mapify-row-star)
       combine-before-after-numbers
       (map ->gear-maps)
       flatten
       (remove nil?)
       (map :gear-ratio)
       (reduce +)
       ))

(part2 fname-sample)
(part2 "input.txt")
;; => 82301120
