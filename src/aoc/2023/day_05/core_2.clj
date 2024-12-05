(ns day-5.core-2
  (:require
   [clojure.edn :as edn]
   [clojure.string :as str]
   [utils :refer [extract-digits-as-nums
                  read-file-lines-slurp]]
   [utils]))

;; Input map has 3 numbers

;; * destination range start
;; * source range start
;; * range length

;; Ranges can be long, so don't brute force it!

(def pat-seeds #"seeds:\s*([\d\s]+).*")
(def pat-map #"(\w+)-to-(\w+)\s+map:\s*([\d\s]+).*")
(def pat-is-map #"\w+-to-\w+")

(defn range-str->map
  "Convert a range string to a map
  Input:  ('50 98 2')
  Output:
  {:src-start 98
   :dest-start 50
   :len 2}"
  [s]
  (let [[dest-start src-start len] (extract-digits-as-nums s)]
    {:src-start src-start
     :src-end (+ src-start len)
     :dest-start dest-start
     :dest-end (+ dest-start len)
     :len len}))

(defn process-map-str
  "Process a map string to generate a dict containing src, dest, ranges
  Input:
  'seed-to-soil map:\n50 98 2\n52 50 48'
  Output:
  {:source 'seed'
   :dest 'soil'
   :ranges [{:dest-start 50
             :src-start 92
             :len 2}
            {:dest-start 52
             :src-start 50
             :len 48}]}"
  [input]
  (let [[_ src dest ranges] (re-matches pat-map input)]
    {:source src
     :dest dest
     :ranges (->> (str/split-lines ranges)
                  (mapv range-str->map)
                  (sort-by :src-start))}))

;; (process-map-str "seed-to-soil map:\n50 98 2\n52 50 48")
;; => {:source "seed",
;;     :dest "soil",
;;     :ranges
;;     ({:src-start 50, :src-end 98, :dest-start 52, :len 48}
;;      {:src-start 98, :src-end 100, :dest-start 50, :len 2})}

(defn process-map-lines [lines]
  (->> lines
       (filter #(re-find pat-is-map %))
       (map process-map-str)
       ;; (map gen-mapping)
       ))

(defn parse-file [fname]
  (let [input (utils/read-local-file fname)
        str-vec (str/split input #"\n\n")
        seeds-str (first str-vec)
        seeds-match (re-matches pat-seeds seeds-str)
        seeds-vec (extract-digits-as-nums (nth seeds-match 1))
        mappings (process-map-lines str-vec)
        ]
    { ; :input input
     :seeds seeds-vec
     :mappings mappings
     }))

(parse-file "input-sample.txt")
;; => {:seeds (79 14 55 13),
;;     :mappings
;;     ({:source "seed",
;;       :dest "soil",
;;       :ranges
;;       ({:src-start 50, :src-end 98, :dest-start 52, :len 48}
;;        {:src-start 98, :src-end 100, :dest-start 50, :len 2})}
;;      {:source "soil",
;;       :dest "fertilizer",
;;       :ranges
;;       ({:src-start 0, :src-end 15, :dest-start 39, :len 15}
;;        {:src-start 15, :src-end 52, :dest-start 0, :len 37}
;;        {:src-start 52, :src-end 54, :dest-start 37, :len 2})}
;;      {:source "fertilizer",
;;       :dest "water",
;;       :ranges
;;       ({:src-start 0, :src-end 7, :dest-start 42, :len 7}
;;        {:src-start 7, :src-end 11, :dest-start 57, :len 4}
;;        {:src-start 11, :src-end 53, :dest-start 0, :len 42}
;;        {:src-start 53, :src-end 61, :dest-start 49, :len 8})}
;;      {:source "water",
;;       :dest "light",
;;       :ranges
;;       ({:src-start 18, :src-end 25, :dest-start 88, :len 7}
;;        {:src-start 25, :src-end 95, :dest-start 18, :len 70})}
;;      {:source "light",
;;       :dest "temperature",
;;       :ranges
;;       ({:src-start 45, :src-end 64, :dest-start 81, :len 19}
;;        {:src-start 64, :src-end 77, :dest-start 68, :len 13}
;;        {:src-start 77, :src-end 100, :dest-start 45, :len 23})}
;;      {:source "temperature",
;;       :dest "humidity",
;;       :ranges
;;       ({:src-start 0, :src-end 69, :dest-start 1, :len 69}
;;        {:src-start 69, :src-end 70, :dest-start 0, :len 1})}
;;      {:source "humidity",
;;       :dest "location",
;;       :ranges
;;       ({:src-start 56, :src-end 93, :dest-start 60, :len 37}
;;        {:src-start 93, :src-end 97, :dest-start 56, :len 4})})}

(defn filter-by-source
  "Select the element where the :source field is 'source'."
  [dicts src]
  (->> (filter #(= src (:source %)) dicts)
       first))

(defn filter-by-dest
  "Select the element where the :source field is 'source'."
  [dicts dest]
  (->> (filter #(= dest (:dest %)) dicts)
       first))

(def tmp-mappings [{:source "seed",
                    :dest "soil",
                    :ranges
                    [{:src-start 50, :src-end 98, :dest-start 52, :len 48}
                     {:src-start 98, :src-end 100, :dest-start 50, :len 2}]}
                   {:source "soil",
                    :dest "fertilizer",
                    :ranges
                    [{:src-start 0, :src-end 15, :dest-start 39, :len 15}
                     {:src-start 15, :src-end 52, :dest-start 0, :len 37}
                     {:src-start 52, :src-end 54, :dest-start 37, :len 2}]}
                   {:source "fertilizer",
                    :dest "water",
                    :ranges
                    [{:src-start 0, :src-end 7, :dest-start 42, :len 7}
                     {:src-start 7, :src-end 11, :dest-start 57, :len 4}
                     {:src-start 11, :src-end 53, :dest-start 0, :len 42}
                     {:src-start 53, :src-end 61, :dest-start 49, :len 8}]}
                   {:source "water",
                    :dest "light",
                    :ranges
                    [{:src-start 18, :src-end 25, :dest-start 88, :len 7}
                     {:src-start 25, :src-end 95, :dest-start 18, :len 70}]}
                   {:source "light",
                    :dest "temperature",
                    :ranges
                    [{:src-start 45, :src-end 64, :dest-start 81, :len 19}
                     {:src-start 64, :src-end 77, :dest-start 68, :len 13}
                     {:src-start 77, :src-end 100, :dest-start 45, :len 23}]}
                   {:source "temperature",
                    :dest "humidity",
                    :ranges
                    [{:src-start 0, :src-end 69, :dest-start 1, :len 69}
                     {:src-start 69, :src-end 70, :dest-start 0, :len 1}]}
                   {:source "humidity",
                    :dest "location",
                    :ranges
                    [{:src-start 56, :src-end 93, :dest-start 60, :len 37}
                     {:src-start 93, :src-end 97, :dest-start 56, :len 4}]}])

;; Moved into src->dest
#_(defn src->dest-from-range
    "Given a range and src-val, get a dest val"
    [rng src-val]
    (if (nil? rng)
      src-val
      (let [src-start (:src-start rng)
            delta (- src-val src-start)
            dest-start (:dest-start rng)]
        (+ dest-start delta))))

(defn src->dest
  "Given a source value, find the destination value and name.
  Output:
  {:soil 55}"
  [mappings src-name src-val]
  (let [cur-mapping (filter-by-source mappings src-name)
        dest (:dest cur-mapping)
        ranges (:ranges cur-mapping)
        cur-range (first
                   (filter #(and (<= (:src-start %) src-val)
                                 (< src-val (:src-end %)))
                           ranges))
        dest-val (if (nil? cur-range)
                   src-val
                   (let [src-start (:src-start cur-range)
                         delta (- src-val src-start)
                         dest-start (:dest-start cur-range)]
                     (+ dest-start delta)))
        ]
    ;; dest-val
    {(keyword dest) dest-val}
    ))

#_(src->dest tmp-mappings "seed" 1)

#_(parse-file "input-sample.txt")

(defn seed->all
  "Map a seed number through all mappings.
  Mappings are from source (seed, etc) to dest (soil, etc)"
  [mappings seed]
  (let [soil (src->dest mappings "seed" seed)
        fertilizer (src->dest mappings "soil" (:soil soil))
        water (src->dest mappings "fertilizer" (:fertilizer fertilizer))
        light (src->dest mappings "water" (:water water))
        temperature (src->dest mappings "light" (:light light))
        humidity (src->dest mappings "temperature" (:temperature temperature))
        location (src->dest mappings "humidity" (:humidity humidity))
        ]
    (merge {:seed seed} soil fertilizer water light temperature humidity location)
    ;; (merge {:seed seed} soil fertilizer water light temperature)
    ))

(seed->all tmp-mappings 79)
;; => {:seed 79,
;;     :soil 81,
;;     :fertilizer 81,
;;     :water 81,
;;     :light 74,
;;     :temperature 78,
;;     :humidity 78,
;;     :location 82}
;; (seed->all tmp-mappings 14)

(defn part1
  "Process the whole file"
  [fname]
  (let [parsed (parse-file fname)
        seeds (:seeds parsed)
        mappings (:mappings parsed)]
    (->> (map #(seed->all mappings %) seeds)
         (map #(get % :location))
         (apply min))))

(part1 "input-sample.txt")

(part1 "input.txt")
;; => 424490994

(def seeds [79 14 55 13])
;; (partition 2 seeds)

(defn create-range [[start len]]
  {:start start
   :end (+ start len)
   :len len})

;; (create-range [1 7])
;; => {:start 1, :len 7}

(defn create-seed-ranges
  "Use the same `seeds` value as before (vec of ints).
  This time interpret them as starting point + len"
  [seeds]
  (let [pairs (partition 2 seeds)
        ranges (map create-range pairs)]
    (sort-by :start ranges)))

(create-seed-ranges seeds)
;; => ({:start 55, :end 68, :len 13} {:start 79, :end 93, :len 14})
;; => ({:start 55, :len 13} {:start 79, :len 14})
;; => nil

;; loop over all seed locations in seed range

(defn min-loc-in-range
  "Get the min :location for seeds in `seed-range`"
  [mappings seed-range]
  (let [seed-start (:start seed-range)
        seed-end (:end seed-range)]
    (loop [seed seed-start
           min-loc nil
           counter 1]
      (if (>= seed seed-end)
        min-loc
        (let [new-loc (:location (seed->all mappings seed))]
          (when (or (= 1 counter)
                    (zero? (mod counter 50)))
            (println "iter:" counter "seed:" seed
                     "new-loc:" new-loc " min-loc:" min-loc))
          (recur (inc seed)
                 (min (or min-loc new-loc) new-loc)
                 (inc counter)))))))

(min-loc-in-range tmp-mappings {:start 55, :end 68, :len 13})
;; => 56
;; => 56

;; REALLY BAD! Iterates over billions(?) of values
(defn part2
  "Treat seeds as ranges"
  [fname]
  (let [parsed (parse-file fname)
        seeds (:seeds parsed)
        seed-ranges (create-seed-ranges seeds)
        mappings (:mappings parsed)]
    (->> seed-ranges ; Start with the seed ranges
         (map #(min-loc-in-range mappings %)) ; Get min loc for a single range
         (apply min) ; Get min loc of all ranges
         )))

(part2 "input-sample.txt")
;; => 46

(part2 "input.txt")

str/split-lines

(defn get-loc-ranges
  "Get the loc ranges from the mappings. (for working backwards)"
  [mappings]
  (let [loc-vec (mappings)])
  )

(defn part2-backwards
  "Work backwards through locations - find first loc that maps to a seed"
  [fname]
  (let [parsed (parse-file fname)
        seeds (:seeds parsed)
        seed-ranges (create-seed-ranges seeds)
        mappings (:mappings parsed)
        loc-maps (filter-by-dest mappings "location")
        ;; loc-ranges (get-loc-ranges mappings)
        ]
    loc-maps
    ))

(defn dest->src
  "Given a dest value, find the source value and name.
  Output:
  {:soil 55}"
  [mappings src-name src-val]
  (let [cur-mapping (filter-by-source mappings src-name)
        dest (:dest cur-mapping)
        ranges (:ranges cur-mapping)
        cur-range (first
                   (filter #(and (<= (:src-start %) src-val)
                                 (< src-val (:src-end %)))
                           ranges))
        dest-val (if (nil? cur-range)
                   src-val
                   (let [src-start (:src-start cur-range)
                         delta (- src-val src-start)
                         dest-start (:dest-start cur-range)]
                     (+ dest-start delta)))
        ]
    ;; dest-val
    {(keyword dest) dest-val}
    ))

(defn seed->all-backwards
  "Map a seed number through all mappings.
  Mappings are from source (seed, etc) to dest (soil, etc)"
  [mappings loc]
  (let [humid (dest->src mappings "location" loc)]

    [soil (src->dest mappings "seed" seed)
     fertilizer (src->dest mappings "soil" (:soil soil))
     water (src->dest mappings "fertilizer" (:fertilizer fertilizer))
     light (src->dest mappings "water" (:water water))
     temperature (src->dest mappings "light" (:light light))
     humidity (src->dest mappings "temperature" (:temperature temperature))
     location (src->dest mappings "humidity" (:humidity humidity))
     ]
    (merge {:seed seed} soil fertilizer water light temperature humidity location)
    ;; (merge {:seed seed} soil fertilizer water light temperature)
    ))

(part2-backwards "input-sample.txt")
;; => {:source "humidity",
;;     :dest "location",
;;     :ranges
;;     ({:src-start 56, :src-end 93, :dest-start 60, :len 37}
;;      {:src-start 93, :src-end 97, :dest-start 56, :len 4})}
;; => Execution error (ArityException) at day-5.core-2/part2-backwards (REPL:342).
;;    Wrong number of args (1) passed to: day-5.core-2/filter-by-dest
