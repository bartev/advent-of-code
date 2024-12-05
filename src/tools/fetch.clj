;; These tools are from my solutions to 2023 days 1-7, before I
;; started automatically downloading and populating stub files.

(ns tools.fetch
  (:require
   [clj-http.client :as client]
   [clojure.edn :as edn]
   [clojure.string :as str]))


;; Copied from https://clojurians.slack.com/archives/C0GLTDB2T/p1701776494128219?thread_ts=1701762545.148749&cid=C0GLTDB2T

;; Need to have the session cookie.
;; See
;; https://github.com/wimglenn/advent-of-code-wim/issues/1
;; And image at screenshot-get-session-cookie

(defn- fetch-input' [day]
  (try
    (let [cookie (slurp ".aoc-session")]
      (:body (client/get
              (str "https://adventofcode.com/2023/day/" day "/input")
              {:cookies {"session" {:value cookie}}
               :headers {"User-Agent"
                         "Bartev's AOC, https://github.com/bartev bartev@gmail.com"}})))
    (catch Exception e
      (println "Ho, ho, ho! Did you forget to populate `.aoc-session` with your AOC session cookie?")
      (throw e))))

(def fetch-input
  (memoize fetch-input'))
