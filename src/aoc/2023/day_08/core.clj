(ns aoc.2023.day-08.core
  (:require
   [aoc.file-util :as f]
   [aoc.string-util :as s]
   [clojure.string :as str]))

(def input (f/read-lines "2023/d08.txt"))
(def input-sample (f/read-lines "2023/d08-sample.txt"))
(def input-sample-2 (f/read-lines "2023/d08-sample-2.txt"))

;; (f/read-chunks "2023/d08-sample.txt")




(defn get-instructions [input] (-> input first (str/split #"" )))

(defn str->node-map
  "Convert a string to a map, key : {:left :right}"
  [x]
  (let [pat #"(\w{3}) = \((\w{3}), (\w{3})\)"
        [_ k l r] (re-matches pat x)]
    {k {:left l :right r}}))

(defn create-network
  "Create a network map from a list of network strings"
  [ns]
  (apply merge (map str->node-map ns)))

#_((comp #(map str->node-map %) rest rest) input-sample)

(defn get-nwk [input] (-> input rest rest create-network))

(defn follow-instructions
  "Follow the instructions (left/right) given the input map.
  Track how many steps to finish."
  [instructions nwk]
  (loop [steps 0            ; Track steps
         instr instructions ; will rotate each step so always take first elem
         from "AAA"         ; Ending key of last step
         ]
    (if (= "ZZZ" from)
      steps
      (let [direction (first instr)
            choices (get nwk from)
            ;; condp will raise an exception if no matching clause
            to (condp = direction
                 "R" (:right choices)
                 "L" (:left choices)
                 )]
        (recur (inc steps)
               (s/rotate-left instr 1)
               to)))))

(defn part-1 [input]
  (let [instructions (get-instructions input)
        nwk (get-nwk input)]
    (follow-instructions instructions nwk)
    ))

(part-1 input-sample)
;; => 2
(part-1 input-sample-2)
;; => 6
(part-1 input)
;; => 11911

(defn part-2 [input] false)
