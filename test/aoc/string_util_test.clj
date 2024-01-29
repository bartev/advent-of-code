(ns aoc.string-util-test
  (:require [aoc.string-util :as sut]
            [clojure.test :refer :all]))

(deftest rotate-left-test
  (is (= ["b" "c" "a"]
         (sut/rotate-left ["a" "b" "c"] 1)))

  (is (= ["c" "a" "b"]
         (sut/rotate-left ["a" "b" "c"] 2))))

(deftest rotate-right-test
  (is (= ["c" "a" "b"]
         (sut/rotate-right ["a" "b" "c"] 1)))
  (is (= ["b" "c" "a"]
         (sut/rotate-right ["a" "b" "c"] 2))))
