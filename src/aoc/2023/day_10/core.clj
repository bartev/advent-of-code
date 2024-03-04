(ns aoc.2023.day-10.core
  (:require
   [aoc.file-util :as f]
   [aoc.string-util :as s]
   [clojure.string :as str]))


;; The pipes are arranged in a two-dimensional grid of tiles:
;;
;; | is a vertical pipe connecting north and south.
;; - is a horizontal pipe connecting east and west.
;; L is a 90-degree bend connecting north and east.
;; J is a 90-degree bend connecting north and west.
;; 7 is a 90-degree bend connecting south and west.
;; F is a 90-degree bend connecting south and east.
;; . is ground; there is no pipe in this tile.
;; S is the starting position of the animal; there is a pipe on this tile, but your sketch doesn't show what shape the pipe has.


* Find starting point.
* Find possible moves (there will be 2 possible moves)

(str/split "|UG" #"")
;; => ["|" "U" "G"]

(str/includes? "|7F" "g")



;; (valid-move? :south "F")
;; (valid-move? :south "J")

(def input (f/read-lines "2023/d10.txt"))
(def input-sample-1 (f/read-lines "aoc/2023/day_10/sample-1.txt"))

(def input-sample-2 (f/read-lines "aoc/2023/day_10/sample-2.txt"))
input-sample-1
;; => ["....." ".F-7." ".|.|." ".L-J." "....."]

(def input-sample-2 (f/read-lines "aoc/2023/day_10/sample-2.txt"))
input-sample-2
;; => ["....." ".S-7." ".|.|." ".L-J." "....."]

(defn find-start
  "Find the row/col that contains 'S'
  Positions are 0-indexed"
  [input]
  (->> input
       (map #(str/index-of % "S"))
       ;; Only keep the index and row/col of the position of "S"
       (keep-indexed (fn [idx x]
                       (when (some? x)
                         {:row idx
                          :col x
                          :steps 0
                          :pipe "S"})))
       first))

(find-start input-sample-2)
;; => {:row 1, :col 1, :steps 0, :pipe "S"}

(find-start input)
;; => {:row 90, :col 62, :steps 0, :pipe "S"}

(defn coord->pipe
  "Return the character found at (row, col)"
  [field row col]
  (str (get (nth field row) col)))

(def valid-moves
  {:north "|7F"
   :south "|JL"
   :east "-J7"
   :west "-LF"})

(defn valid-move?
  "True if the move is valid.
  to-dir should be a keyword :north, :south, :east or :west"
  [m]
  (let [to-dir (first (keys m))
        pipe (first (vals m))
        valid-moves {:north "|7F"
                     :south "|JL"
                     :east "-J7"
                     :west "-LF"}]
    (when (str/includes? (to-dir valid-moves) pipe)
      m)))

(valid-move? {:north "|"})

(valid-move? {:north "S"})

(defn pipes-nsew
  "Get the valid pipes north, south, east, west of current position (row, col).
  row, col are 0-indexed"
  [field row col]
  (let [nrows (count field)
        ncols (count (first field))
        north (when (pos? row) (coord->pipe field (dec row) col))
        south (when (< row nrows) (coord->pipe field (inc row) col))
        east (when (pos? col) (coord->pipe field row (inc col)))
        west (when (< col ncols) (coord->pipe field row (dec col)))]
    (merge (valid-move? {:north north})
           (valid-move? {:south south})
           (valid-move? {:east east})
           (valid-move? {:west west}))))

(defn get-from-dir
  "Get the direction from which the previous cell came."
  [m-cur m-prev]
  (let [delta-ns (- (:row m-cur) (:row m-prev))
        delta-ew (- (:col m-cur) (:col m-prev))]
    (cond
      (pos? delta-ns) :south
      (neg? delta-ns) :north
      (pos? delta-ew) :west
      (neg? delta-ew) :east)))

#_(get-from-dir {:row 3 :col 1}
                {:row 3 :col 2})

(defn get-next-cell
  "Given the current cell (m-cur) and the previous cell (m-prev), What is the next cell?"
  ([field m-cur]
   ;; if no previous direction, then pick next direction at random
   (let [surroundings (pipes-nsew field (:row m-cur) (:col m-cur))]
     (first surroundings)))

  ([field m-cur m-prev]
   (let [surroundings (pipes-nsew field (:row m-cur) (:col m-cur))
         from-dir (get-from-dir m-cur m-prev)]
     from-dir)))

(get-next-cell input-sample-2 (find-start input-sample-2))



(let [start-vec (find-start input-sample-2)
      row (:row start-vec)
      col (:col start-vec)]
  (pipes-nsew input-sample-2 row col))


(nth input-sample-2 3)

(defn process-step
  "Get valid moves, previous direction and return the map for the next cell."
  ([field m-cur] (get-next-cell field m-cur))
  ([field m-cur m-prev] (get-next-cell field m-cur m-prev)))

(defn is-start? [m] (= "S" (:pipe m)))

(defn part-1 [input]
  (let [start (find-start input)]
    (loop [dist 0
           tunnel-locs [start]
           m-cur start
           m-prev nil]
      (if (and (pos? dist) (is-start? m-cur)) ;; Stop when get back to "S"
        tunnel-locs
        (recur (inc dist)
               (conj tunnel-locs (process-step input m-cur ))
               (if m-prev
                 (process-step input m-cur m-prev)
                 (process-step input m-cur))
               m-cur)
        ))))


(part-1 input-sample-2)
;; => Execution error (NullPointerException) at aoc.2023.day-10.core/pipes-nsew (REPL:99).
;;    Cannot invoke "Object.getClass()" because "x" is null
;; => {:row 1, :col 1, :steps 0, :pipe "S"}

(get-next-cell input-sample-2 {:row 1, :col 1, :dist 0, :pipe "S"})

(defn part-2 [input] true)
