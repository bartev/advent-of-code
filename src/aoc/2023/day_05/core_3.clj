(ns day-5.core-3
  (:require
   [clojure.java.io :as io]
   [utils :refer [get-local-fname]]))

;; Copy from https://gist.github.com/alexander-yakushev/7f10ec2b18b504533447af0438179507

(def lines (vec (line-seq (io/reader (get-local-fname "input-sample.txt")))))
(def lines (vec (line-seq (io/reader (get-local-fname "input.txt")))))

(defn parse [task]
  (let [seeds (mapv parse-long (re-seq #"\d+" (first lines)))
        seeds (case task
                1 seeds
                2 (->> (partition 2 seeds)
                       (mapv (fn [[a b]] [a (+ a b)]))))
        maps (->> (partition-by empty? (rest lines))
                  (keep (fn [lines]
                          (->> lines
                               ;; drops the name line <src>-to-<dest>
                               ;; returns a list of [start end delta]
                               (keep #(when-let [[dst src n] (re-seq #"\d+" %)]
                                        (let [src (parse-long src)]
                                          [src
                                           (+ src (parse-long n))
                                           (- (parse-long dst) src)])))
                               (sort-by first)
                               seq))))]
    [seeds maps]))

;; (parse 1)
;; ;; => [[79 14 55 13]
;; ;;     (([50 98 2] [98 100 -48])
;; ;;      ([0 15 39] [15 52 -15] [52 54 -15])
;; ;;      ([0 7 42] [7 11 50] [11 53 -11] [53 61 -4])
;; ;;      ([18 25 70] [25 95 -7])
;; ;;      ([45 64 36] [64 77 4] [77 100 -32])
;; ;;      ([0 69 1] [69 70 -69])
;; ;;      ([56 93 4] [93 97 -37]))]

;; NIFTY!
;; At the partition-by empty? stage
;; ;; => (("")
;; ;;     ("seed-to-soil map:" "50 98 2" "52 50 48")
;; ;;     ("")
;; ;;     ("soil-to-fertilizer map:" "0 15 37" "37 52 2" "39 0 15")
;; ;;     ("")
;; ;;     ("fertilizer-to-water map:" "49 53 8" "0 11 42" "42 0 7" "57 7 4")
;; ;;     ("")
;; ;;     ("water-to-light map:" "88 18 7" "18 25 70")
;; ;;     ("")
;; ;;     ("light-to-temperature map:" "45 77 23" "81 45 19" "68 64 13")
;; ;;     ("")
;; ;;     ("temperature-to-humidity map:" "0 69 1" "1 0 69")
;; ;;     ("")
;; ;;     ("humidity-to-location map:" "60 56 37" "56 93 4"))
;; ;; => [79 14 55 13]

;; Only differece is the first element -- seeds
;; (parse 2)
;; ;; => [((79 14) (55 13))
;; ;;     (([50 98 2] [98 100 -48])
;; ;;      ([0 15 39] [15 52 -15] [52 54 -15])
;; ;;      ([0 7 42] [7 11 50] [11 53 -11] [53 61 -4])
;; ;;      ([18 25 70] [25 95 -7])
;; ;;      ([45 64 36] [64 77 4] [77 100 -32])
;; ;;      ([0 69 1] [69 70 -69])
;; ;;      ([56 93 4] [93 97 -37]))]

(defn convert [seed maps]
  (reduce
   (fn [seed m]
     (or (some (fn [[from to delta]]
                 (when (and (>= seed from) (< seed to))
                   (+ seed delta)))
               m)
         seed))
   seed maps))

;; (defn redfn
;;   "The function for reduce"
;;   [seed m]
;;   (or
;;    (some (fn [[from to delta]]
;;            (when (and (>= seed from)
;;                       (< seed to))
;;              (+ seed delta)))
;;          m)
;;    seed))

;; (defn convert2 [seed maps]
;;   (reduce redfn seed maps))

;; (let [[seeds maps] (parse 1)]
;;   (->> seeds
;;        (map #(convert2 % maps))
;;        (apply min)))

(defn task1 []
  (let [[seeds maps] (parse 1)]
    (->> seeds
         (map #(convert % maps))
         (apply min))))


(task1)
;; => 35
;; => 35
;; => 424490994
;; => 35

;;;

(defn transform-range [[from to] amap]
  (loop [start from, amap amap, res []]
    (if (>= start to)
      res ;; exit

      (let [amap (drop-while #(>= start (second %)) amap)
            [mfrom mto delta] (first amap)]
        (cond (or (nil? mfrom) (<= to mfrom))
              (recur to amap (conj res [start to]))

              (< start mfrom)
              (recur mfrom amap (conj res [start mfrom]))

              :else
              (let [to (min to mto)]
                (recur to amap (conj res [(+ start delta) (+ to delta)]))))))))

(defn task2 []
  (let [[seeds maps] (parse 2)]
    (ffirst
     (reduce (fn [ranges amap]
               (->> (mapcat #(transform-range % amap) ranges)
                    (sort-by first)))
             seeds
             maps))))

;; This version works super fast.
;; Why?
(task2)
;; => 46
;; => 15290096

;; Figure out `transform-range`

;; Each range (from to) is converted to a new range or ranges.
;; If the entire range is within the first mapping, it is mapped directly.
;; If not, the part that is in the first mapping is mapped, then the
;; first mapping is dropped and the next mapping is used and a 2nd range is
;; created.
;; this goes on until all the ranges are exhausted.

(let [[seeds maps] (parse 2)]
  seeds)
;; => [[79 93] [55 68]]

;; maps are [start end delta]
;; delta = (dest - start)
(let [[seeds maps] (parse 2)]
  seeds)
;; => [[79 93] [55 68]]
;; => (([50 98 2] [98 100 -48])
;;     ([0 15 39] [15 52 -15] [52 54 -15])
;;     ([0 7 42] [7 11 50] [11 53 -11] [53 61 -4])
;;     ([18 25 70] [25 95 -7])
;;     ([45 64 36] [64 77 4] [77 100 -32])
;;     ([0 69 1] [69 70 -69])
;;     ([56 93 4] [93 97 -37]))

(let [[seeds maps] (parse 2)]
  (ffirst maps)) ;; (first (first maps))
;; => [50 98 2]

(defn red-fn-2 [ranges amap]
  (->> (mapcat #(transform-range % amap) ranges)
       (sort-by first)))

(let [[seeds maps] (parse 2)]
  (ffirst
   (reduce red-fn-2 seeds maps)))

(transform-range [55 68] [[50 98 2] [98 100 -48]])
;; => [[57 70]]
(transform-range [45 68] [[50 98 2] [98 100 -48]])
;; => [[45 50] [52 70]]

(loop [x 10]
  (when (> x 0)
    (print x "")
    (recur (- x 2))))

(defn xform [[from to] amap]
  (loop [start from
         amap amap
         res []]
    (if (>= start to)
      ;; then exit
      res
      ;; else
      (do
        (println "start" start)
        (println "amap" amap)
        (println)
        (recur (+ start 4) amap (cons start res))))))



(defn xform
  "Transform a single range given a single map"
  [[from to] amap]
  (loop [start from
         amap amap
         res []]
    (if (>= start to)
      ;; then exit
      res
      ;; else
      (let [amap (drop-while #(>= start (second %)) amap)
            [mfrom mto delta] (first amap)]
        (println "start" start "mfrom" mfrom)
        (println "to" to "mto" mto)
        (println "delta" delta)
        (println "amap" amap)
        (println)
        (cond
          (or (nil? mfrom) (<= to mfrom))
          (do
            (print "case 1")
            (recur to amap (conj res [start to])))

          (< start mfrom)
          (do
            (print "case 2")
            (recur mfrom amap (conj res [start mfrom])))

          :else
          (let [to (min to mto)]
            (print "case 3")
            (recur to amap (conj res [(+ start delta)
                                      (+ to delta)])))
          )))))

(def my-map [[50 98 2] [98 100 -48]])
(xform [0 1000] my-map)
;; => [[0 50] [52 100] [50 52] [100 1000]]


(reduce (fn [ranges amap]
          (->> (mapcat #(transform-range % amap) ranges)
               (sort-by first)))
        [[79 93] [55 68]]
        [my-map
         [[0 15 39] [15 52 -15] [52 54 -15]]
         [[0 7 42] [7 11 50] [11 53 -11] [53 61 -4]]
         [[18 25 70] [25 95 -7]]
         [[45 64 36] [64 77 4] [77 100 -32]]
         [[0 69 1] [69 70 -69]]
         [[0 69 1] [69 70 -69]]
         [[56 93 4] [93 97 -37]]]
        )
;; => ([47 56] [56 60] [60 62] [82 85] [86 90] [94 97] [97 99])
;; => ([46 57] [78 81] [82 86] [90 99])
