(ns aoc.math-test
  (:require [aoc.math :as sut]
            [clojure.test :refer :all]))


(deftest gcd-test
  (is (= 7 (sut/gcd 7 28)))
  (is (= 5 (sut/gcd 25 115))))

(deftest lcm-test
  (is (= 0 (sut/lcm 0 1)))
  (is (= 2 (sut/lcm 1 2)))
  (is (= 6 (sut/lcm 2 3))))
