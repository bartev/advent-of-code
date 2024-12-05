;; These tools are from my solutions to 2023 days 1-7, before I
;; started automatically downloading and populating stub files.

(ns tools.utils
  (:require
   [babashka.fs :as fs]
   [clojure.edn :as edn]
   [clojure.java.io :as io]
   [clojure.string :as str]))

;;;; File io
(defn get-local-fname
  "Get the full filename when in same dir as this file."
  [fname]
  (-> (fs/parent *file*)
      (fs/path fname)
      str))

(defn read-local-file
  "Read an entire file file in the current directory"
  [fname]
  (let [path (get-local-fname fname)]
    (slurp path)))

;; Duplicate of `read-local-file`
#_ (defn read-file
     "Read an entire file in the current directory"
     [fname]
     (let [path (-> (fs/parent *file*)
                    (fs/path fname)
                    str)]
       (slurp path)))


;; line-seq works on a reader object (not string)
;; str/split-lines works on a string (not reader)
(defn read-lines-io
  "Read a file line-by-line"
  [fname]
  (with-open [reader (io/reader fname)]
    (doall (line-seq reader))))

;; Not sure what the difference is here
(defn read-lines-io-local
  "Same as `read-lines`, but uses io instead of slurp"
  [fname]
  (let [lfname (get-local-fname fname)]
    (vec (line-seq (io/reader lfname)))))

;; Could also do this with `slurp`
(defn read-lines-local
  "Read a file into a vec of lines.
  Same result as `read-lines-io`"
  [fname]
  (let [lfname (get-local-fname fname)]
    (str/split-lines (slurp lfname))))





;;;; Reading numbers

(defn extract-digits
  "Extract the digits from a string (as strings)
  (extract-digits '1a2b3cx')
  => ['1' '2' '3']
  "
  [x]
  (vec (re-seq #"\d+" x)))

(defn extract-digits-as-nums
  "Extract the digits from a string, and convert to vec of numbers.
  (extract-digits-as-nums '1x2y3z')
  => [1 2 3]
  "
  [x]
  (mapv parse-long (re-seq #"\d+" x)))

(defn extract-combine-numbers
  "Extract all numbers from a string, concatenate them and read as a single number
  (extract-combine-numbers '1a2b3cx')
  => 123
  "
  [s]
  (->> s
       (re-seq #"\d")
       (apply str)
       parse-long))
