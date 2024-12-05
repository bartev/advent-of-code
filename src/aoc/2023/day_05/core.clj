(ns day-5.core
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

(defn gen-range
  "Use start/length instead of start/end."
  [start len]
  (range start (+ start len)))

(defn gen-one-mapping
  "Create a mapping of src->dest for a single row."
  [dest source len]
  (zipmap (gen-range source len)
          (gen-range dest len)))

(defn str->one-mapping [s]
  "Convert a string with `dest`, `src`, `rng` to a mapping.
  Inputs should look like
  '49 53 8'"
  (let [[dest src len] (extract-digits-as-nums s)]
    (gen-one-mapping dest src len)))

(def pat-seeds #"seeds:\s*([\d\s]+).*")
(def pat-map #"(\w+)-to-(\w+)\s+map:\s*([\d\s]+).*")
(def pat-is-map #"\w+-to-\w+")

(defn gen-mapping
  "Generate a mapping from an x-to-y string."
  [input]
  (let [[_ source dest ranges] (re-matches pat-map input)]
    {:source source
     :dest dest
     :ranges (->> (str/split ranges #"\n")
                  (map str->one-mapping)
                  (apply merge) ; Combine all the mappings into a single, sorted map
                  (into (sorted-map))
                  ;; combine-mappings
                  )}))

(defn process-map-lines [lines]
  (->> lines
       (filter #(re-find pat-is-map %))
       (map gen-mapping)))

(defn parse-file [fname]
  (let [input (utils/read-local-file fname)
        str-vec (str/split input #"\n\n")
        seeds-str (first str-vec)
        seeds-match (re-matches pat-seeds seeds-str)
        seeds-vec (extract-digits-as-nums (nth seeds-match 1))
        mappings (process-map-lines str-vec)]
    {:input input
     :seeds seeds-vec
     :mappings mappings}))

(defn filter-by-source
  "Select the element where the :source field is 'source'."
  [dicts src]
  (->> (filter #(= src (:source %)) dicts)
       first))

(defn src->dest
  "Get a destination number given a source"
  [src-name src-num mappings]

  (let [cur-mapping (filter-by-source mappings src-name)
        dest (:dest cur-mapping)
        ranges (:ranges cur-mapping)
        dest-val (get ranges src-num src-num)]
    {(keyword dest) dest-val}))

;; (def tmp-mappings (process-map-lines str-vec))

;; (filter-by-source tmp-mappings "seed")

;; (src->dest "seed" 57 tmp-mappings)
;; =>
;; => {:dest "soil", :value 59}
;; => {:dest "soil", :value 57, :ranges nil}

;; => {:dest "soil", :value 57}

(defn seed->all
  "Map a seed number through all mappings.
  Mappings are from source (seed, etc) to dest (soil, etc)"
  [seed mappings]
  (let [soil (src->dest "seed" seed mappings)
        fertilizer (src->dest "soil" (:soil soil) mappings)
        water (src->dest "fertilizer" (:fertilizer fertilizer) mappings)
        light (src->dest "water" (:water water) mappings)
        temperature (src->dest "light" (:light light) mappings)
        humidity (src->dest "temperature" (:temperature temperature) mappings)
        location (src->dest "humidity" (:humidity humidity) mappings)]
    (merge {:seed seed} soil fertilizer water light temperature humidity location)))

(defn seeds->destinations
  "Map all seeds to their various destinations"
  [seeds mappings]
  (mapv #(seed->all % mappings) seeds))

(defn part1
  "Get lowest location"
  [fname]
  (let [parsed (parse-file fname)
        seeds (:seeds parsed)
        mappings (:mappings parsed)]
    (->> (seeds->destinations seeds mappings)
         (map #(get % :location))
         (apply min))))

(part1 "input-sample.txt")
;; => 35
;; => clojure.lang.LazySeq
;; => (82 43 86 35)
;; => #function[clojure.core/min]
;; => (82 43 86 35)


(part1 "input.txt")
;; => Execution error (OutOfMemoryError) at java.lang.Long/valueOf (Long.java:1204).
;;    Java heap space
