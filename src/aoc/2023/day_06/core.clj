(ns day-6.core
  (:require
   [clojure.java.io :as io]
   [clojure.string :as str]
   [utils :refer [get-local-fname]]))


(defn get-lines [fname]
  (vec (line-seq (io/reader (get-local-fname fname)))))

(defn parse
  "Parse file into a list of "
  [fname]
  (let [lines (get-lines fname)
        times (mapv parse-long (re-seq #"\d+" (first lines)))
        distances (mapv parse-long (re-seq #"\d+" (second lines)))
        time-dist-tuples (map vector times distances)]
    (map #(zipmap [:time :dist] %) time-dist-tuples)))

(parse "input-sample.txt")
;; => ({:time 7, :dist 9} {:time 15, :dist 40} {:time 30, :dist 200})


(defn calc-dist
  "Calculate the distance traveled given total time t, and time button held tb"
  [t tb]
  (when (and (<= tb t)
             (not (neg? t))
             (not (neg? tb)))
    (* (- t tb) tb)))

(calc-dist 7 3)

(defn calc-distances
  "Calculate all possible distances for a time."
  [time]
  (map #(calc-dist time %) (range time)))

(calc-distances 7)
;; => (0 6 10 12 12 10 6)

(defn calc-extreme-distances
  "Calculate the distances that are greater then :dist in the input."
  [{:keys [time dist]}]  ; Destructure input dict, pulling keys :time and :dist
  (->> time
       calc-distances
       (filter #(< dist %))))

(calc-extreme-distances {:time 7 :dist 10})

(defn task1 [fname]
  (->> fname
       parse
       (mapv calc-extreme-distances)
       (mapv count)
       (apply *)))

(task1 "input-sample.txt")
;; => 288
;; => [4 8 9]
;; => [(10 12 12 10)
;;     (44 50 54 56 56 54 50 44)
;;     (209 216 221 224 225 224 221 216 209)]
;; => ((10 12 12 10)
;;     (44 50 54 56 56 54 50 44)
;;     (209 216 221 224 225 224 221 216 209))


(task1 "input.txt")
;; => 1084752

;;;;; task 2

(defn parse2
  "Parse file into a list of "
  [fname]
  (->> (get-lines fname)
       (map (fn [line] (-> (str/split line #":")
                           second
                           (str/replace #"\s*" "")
                           parse-long)))
       (zipmap [:time :dist])))

(parse2 "input-sample.txt")
;; => {:time 71530, :dist 940200}

(parse2 "input.txt")
;; => {:time 40709879, :dist 215105121471005}

(defn task2 [fname]
  (->> fname
       parse2
       calc-extreme-distances
       count))

(task2 "input-sample.txt")
;; => 71503

(task2 "input.txt")
;; => 28228952
