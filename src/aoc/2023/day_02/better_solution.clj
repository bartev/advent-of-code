(ns day-2.better-solution
  (:require [clojure.string :as str]
            [clojure.java.io :as io]
            [babashka.fs :as fs]))


;;;; 1st person (Norman Richards)
;; Not too far from what I did.
;; https://gitlab.com/maximoburrito/advent2023/-/blob/main/src/day02/main.clj

;; This function does my parse-draw and count-colors in 1 step
(defn parse-roll [roll]
  (let [draws (str/split roll #", ")]
    (into {:red 0
           :blue 0
           :green 0}
          (for [draw draws
                :let [[n color] (str/split draw #" ")]]
            [(keyword color) (parse-long n)]))))

(parse-roll "3 blue, 4 red, 7 green")
;; => {:red 4, :blue 3, :green 7}

(defn parse-line [line]
  (let [[_ n games] (re-matches #"Game (.*): (.*)" line)
        rolls (str/split games #"; ")]
    {:n (parse-long n)
     :rolls (mapv parse-roll rolls)}))

(parse-line "Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green")
;; => {:n 1,
;;     :rolls
;;     [{:red 4, :blue 3, :green 0}
;;      {:red 1, :blue 6, :green 2}
;;      {:red 0, :blue 0, :green 2}]}

(defn read-input [fname]
  (->> (slurp fname)
       str/split-lines
       (map parse-line)))

(read-input "./src/day_2/input-sample-1.txt")

;; => ({:n 1,
;;      :rolls
;;      [{:red 4, :blue 3, :green 0}
;;       {:red 1, :blue 6, :green 2}
;;       {:red 0, :blue 0, :green 2}]}
;;     {:n 2,
;;      :rolls
;;      [{:red 0, :blue 1, :green 2}
;;       {:red 1, :blue 4, :green 3}
;;       {:red 0, :blue 1, :green 1}]}
;;     {:n 3,
;;      :rolls
;;      [{:red 20, :blue 6, :green 8}
;;       {:red 4, :blue 5, :green 13}
;;       {:red 1, :blue 0, :green 5}]}
;;     {:n 4,
;;      :rolls
;;      [{:red 3, :blue 6, :green 1}
;;       {:red 6, :blue 0, :green 3}
;;       {:red 14, :blue 15, :green 3}]}
;;     {:n 5,
;;      :rolls [{:red 6, :blue 1, :green 3} {:red 1, :blue 2, :green 2}]})


;; Understanding how he got the maxes

(def one-roll {:n 1,
               :rolls
               [{:red 4, :blue 3, :green 0}
                {:red 1, :blue 6, :green 2}
                {:red 0, :blue 0, :green 2}]})

;; This is MUCH simpler than my solution
(reduce (partial merge-with max) (:rolls one-roll))
;; => {:red 4, :blue 6, :green 2}
