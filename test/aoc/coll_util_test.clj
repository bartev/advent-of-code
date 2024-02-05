(ns aoc.coll-util-test
  (:require [aoc.coll-util :as sut]
            [clojure.test :refer :all]))

(deftest intervals-test
  (let [data [1 2 3 5 8 13 21]]
    (is (= [1 1 2 3 5 8] (sut/intervals data)))
    (is (= [2 3 5 8 13] (sut/intervals 2 data)))
    (is (= [4 6 10 16] (sut/intervals 3 data)))))
