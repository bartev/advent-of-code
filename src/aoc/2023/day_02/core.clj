(ns day-2.core
  (:require
   [clojure.edn :as edn]
   [clojure.string :as str]
   [utils :refer [get-local-fname
                  read-lines-io]]))


;; Parse data to look like


;; 1. parse data into map
;; {:game 1
;;  :draws [{:red r
;;           :green g
;;           :blue b}]}

;; 2. Filter by applying assertion over all draws in a game
;; (and (<= max-red (:red draw))
;;      (<= max-green (:green draw))
;;      (<= max-blue (:blue draw)))

;; 3. Sum up the remaining `:game` numbers.

(def input-sample-1 "input-sample-1.txt")

(defn parse-draw
  "Input looks like
  '3 blue, 4 red, 7 green'"
  [draw]
  (let [items (map str/trim (str/split draw #","))]
    items))

(parse-draw "3 blue, 4 red, 7 green") ;; => ("3 blue" "4 red" "7 green")

(def items ["3 blue" " 4 red" " 7 green"])

;; This could've been done more easily by splitting the string into [n color]
(defn count-colors [color items]
  (let [col-count (some->> (filter #(str/includes? % color) items)
                           first
                           str/trim
                           (#(str/split % #" "))
                           first
                           edn/read-string)]
    (when col-count
      {(keyword color) col-count})))

(count-colors "red" items)

(def count-blues (partial count-colors "blue"))
(def count-greens (partial count-colors "green"))
(def count-reds (partial count-colors "red"))

items ;; => ["3 blue" " 4 red" " 7 green"]
(count-blues items) ;; => {:blue 3}
(count-reds items) ;; => {:red 4}
(count-greens items) ;; => {:green 7}

(def draw-str "3 blue, 4 red, 7 green")
(defn create-color-counts-map
  [draw-str]
  (let [draw (parse-draw draw-str)
        blues (count-blues draw)
        greens (count-greens draw)
        reds (count-reds draw)]
    (when (or blues greens reds)
      (merge blues greens reds))))

(create-color-counts-map draw-str) ;; => {:blue 3, :green 7, :red 4}

(defn parse-file [fname]
  (let [lines (->> (slurp (get-local-fname fname))
                   str/split-lines)]
    (for [line lines]
      (let [[game raw-draws] (str/split line #":")
            id (last (str/split game #"\s"))
            draws (map str/trim (str/split raw-draws #";"))
            draw-maps (map create-color-counts-map draws)
            ]
        {:id id
         :draws draw-maps}))))


(def res-1 (parse-file input-sample-1))
res-1
;; => ({:id "1",
;;      :draws ({:blue 3, :red 4} {:blue 6, :green 2, :red 1} {:green 2})}
;;     {:id "2",
;;      :draws
;;      ({:blue 1, :green 2}
;;       {:blue 4, :green 3, :red 1}
;;       {:blue 1, :green 1})}
;;     {:id "3",
;;      :draws
;;      ({:blue 6, :green 8, :red 20}
;;       {:blue 5, :green 13, :red 4}
;;       {:green 5, :red 1})}
;;     {:id "4",
;;      :draws
;;      ({:blue 6, :green 1, :red 3}
;;       {:green 3, :red 6}
;;       {:blue 15, :green 3, :red 14})}
;;     {:id "5",
;;      :draws ({:blue 1, :green 3, :red 6} {:blue 2, :green 2, :red 1})})


(defn has-color-gt-n
  "True if any dict in the list has a key `:color` whose value is > n."
  [color n coll]
  (let [draws (:draws coll)
        values (remove nil? (map color draws))
        max-val (apply max values)]
    (when max-val
      (> max-val n))))

(first res-1)
;; => {:id "1",
;;     :draws ({:blue 3, :red 4} {:blue 6, :green 2, :red 1} {:green 2})}

(for [n (range 3 7)]
  {n (has-color-gt-n :red n (first res-1))})
;; => ({3 true} {4 false} {5 false} {6 false})

(defn part1 [fname]
  (let [draw-maps (parse-file fname)]
    (->> draw-maps
         (remove (fn [draw-item] (has-color-gt-n :red 12 draw-item)))
         (remove (fn [draw-item] (has-color-gt-n :green 13 draw-item)))
         (remove (fn [draw-item] (has-color-gt-n :blue 14 draw-item)))
         (map :id)
         (map edn/read-string)
         (apply +)
         )))

(part1 "input-sample-1.txt")
;; => 8


(part1 "input.txt")
;; => 2439

;;; Part 2

;; What is the fewest number of cubes of each color for each game?

(defn max-color
  "Get the max number of cubes of a color for the draw."
  [color coll]
  (let [draws (:draws coll)
        values (remove nil? (map color draws))
        max-val (apply max values)]
    {color (or max-val 0)}))

;; Could've been done more simply using
;; (reduce (partial merge-with max) draws)
;; => {:red 4, :blue 6, :green 2}
(defn get-min-cubes
  "For a given set of draws, get the minimum number of cubes of each color"
  [draws]
  (let [red (max-color :red draws)
        green (max-color :green draws)
        blue (max-color :blue draws)
        min-cubes (merge red green blue)
        power (* (:red red) (:green green) (:blue blue))]
    (merge min-cubes {:power power})))

(defn part2 [fname]
  (let [draw-maps (parse-file fname)
        first-draw (get-min-cubes (first draw-maps))
        min-maps-by-draw (map get-min-cubes draw-maps)]
    (->> min-maps-by-draw
         (map :power)
         (apply +))))

(part2 "input-sample-1.txt")
;; => 2286
;; => (48 12 1560 630 36)
;; => ({:red 4, :green 2, :blue 6, :power 48}
;;     {:red 1, :green 3, :blue 4, :power 12}
;;     {:red 20, :green 13, :blue 6, :power 1560}
;;     {:red 14, :green 3, :blue 15, :power 630}
;;     {:red 6, :green 3, :blue 2, :power 36})

(part2 "input.txt")
;; => 63711


(def a-draw (first res-1))
a-draw
;; => {:id "1",
;;     :draws ({:blue 3, :red 4} {:blue 6, :green 2, :red 1} {:green 2})}

(get-min-cubes a-draw)
;; => {:red 4, :green 2, :blue 6, :power 48}

(defn get-min-cubes-simpler
  "For a given set of draws, get the minimum number of cubes of each color"
  [draws]
  (let [min-cubes (reduce (partial merge-with max) (:draws draws))
        power (* (:red min-cubes) (:green min-cubes) (:blue min-cubes))
        ;; power ((fn [{:keys [red green blue]}] (* red green blue)) min-cubes)
        ]
    (merge min-cubes {:power power})))

(get-min-cubes-simpler a-draw)
;; => {:blue 6, :red 4, :green 2, :power 48}
;; => [4 2 6]
;; => {:blue 6, :red 4, :green 2, :power 48}

;; Destructuring!
(defn minima [{:keys [red green blue]}]
  [red green blue])

(get-min-cubes-simpler a-draw)
;; => {:blue 6, :red 4, :green 2, :power 48}
(minima (get-min-cubes-simpler a-draw))
;; => [4 2 6]
