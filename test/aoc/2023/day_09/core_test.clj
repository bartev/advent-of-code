(ns aoc.2023.day-09.core-test
    (:require
     [aoc.2023.day-09.core :as sut]
     [clojure.test :refer :all]))

(deftest challenges
  (is (= 114 (sut/part-1 sut/input-sample)))
  (is (= 1834108701 (sut/part-1 sut/input)))
  #_(is (= false (sut/part-2 sut/input))))
