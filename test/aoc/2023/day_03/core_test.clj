(ns aoc.2023.day-03.core-test
    (:require
     [aoc.2023.day-03.core :as sut]
     [clojure.test :refer :all]))

(deftest challenges
  (is (= false (sut/part-1 sut/input)))
  (is (= false (sut/part-2 sut/input))))