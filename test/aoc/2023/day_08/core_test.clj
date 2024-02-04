(ns aoc.2023.day-08.core-test
    (:require
     [aoc.2023.day-08.core :as sut]
     [clojure.test :refer :all]))

(deftest challenges
  (is (= 11911 (sut/part-1 sut/input)))
  (is (= 2 (sut/part-1 sut/input-sample)))
  (is (= 6 (sut/part-1 sut/input-sample-2))))


(deftest try-explore-test
  (is (= 3 (:n (sut/try-explore sut/input-sample "AAA"))))
  (is (= 7 (:n (sut/try-explore sut/input-sample-2 "AAA"))))
  (is (= 43766 (:n (sut/try-explore sut/input "RMA")))))

(deftest find-start-states-test
  (is (= ["RMA" "PLA" "QLA" "NXA" "AAA" "GDA"]
         (sut/find-start-states sut/input sut/start-state?))))

(deftest solve-test
  (is (= 2 (sut/solve sut/input-sample-3 "11A")))
  (is (= 3 (sut/solve sut/input-sample-3 "22A")))
  (is (= 21883 (sut/solve sut/input "RMA"))))

(deftest part-2-test
  (is (= 6 (sut/part-2 sut/input-sample-3)))
  (is (= 10151663816849 (sut/part-2 sut/input))))
