(ns test-runner
  (:require
   [clojure.test :as t]
   [babashka.classpath :as cp]))

(cp/add-classpath "src:test")

(require 'day-1.core-test
         'day-3.core-test
         'day-5.core-test)

(def test-results
  (t/run-tests 'day-1.core-test
               'day-3.core-test
               'day-5.core-test))

(println ">>>>>>>>>> BV test results")
(println test-results)

#_
(let [{:keys [fail error]} test-results]
  (when (pos? (+ fail error))
    (System/exit 1)))
