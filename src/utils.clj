(ns utils
  (:require
   [babashka.fs :as fs]
   [clojure.edn :as edn]
   [clojure.java.io :as io]
   [clojure.string :as str]))

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

;; (read-file "sample-input.txt")

(defn read-lines-io
  "Read a file line-by-line"
  [fname]
  (with-open [reader (io/reader fname)]
    (doall (line-seq reader))))

;; Could also do this with `slurp`
(defn read-file-lines-slurp
  "Read a file using slurp"
  [fname]
  (->> (slurp (get-local-fname fname))
       str/split-lines))

;; (defn get-local-fname
;;   "Get fname relative to source file."
;;   [fname]
;;   (-> (fs/parent *file*)
;;       (fs/path fname)
;;       str))

;; Probably won't use this.
(defn read-file
  "Read an entire file file in the current directory"
  [fname]
  (let [path (-> (fs/parent *file*)
                 (fs/path fname)
                 str)]
    (slurp path)))

(defn extract-digits-as-nums
  "Extract the digits from a string, and convert to vec of numbers."
  [x]
  (->> x
       (re-seq #"\d+")
       vec
       (map edn/read-string)))
