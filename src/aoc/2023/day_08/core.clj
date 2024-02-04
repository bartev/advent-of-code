(ns aoc.2023.day-08.core
  (:require
   [aoc.file-util :as f]
   [aoc.math :refer [lcm]]
   [aoc.string-util :as s]
   [clojure.string :as str]))

;; Things I learned
;; Brute force is often just bad. Look at the size of the problem first.

;; cond->

;; (cond-> 1
;;   true inc
;;   true (* 3)
;;   false (* 4))
;; ;; => 6
;; ;; => 6

;; lcm, gcd, numeric-tower

;; Use `re-seq` to get ALL instance that match a regex from a string.
;; (re-seq #"\w{3}" x)

;; Got more comfortable with `loop...recur`.
;; Got more comfortable with `reduce`.
;; Got more comfortable with passing functions as parameters.

;; Use `bb test` and `kaocha` to run tests

;; fizz-buzz in 6 lines
;; Use `for` loop with `:when` (see `part-2`)

;; `cycle` function (even though I still used `rotate-left`) to create a lazy infinite seq.
;; Could've used characters as keys (instead of strings or keywords).
;; `take-upto` -- didn't use
;; `for-map` -- didn't use

;; `medley.core` library https://github.com/weavejester/medley
;; Look here for useful functions missing from clojure.core

;; `plumbing.core` library http://plumatic.github.io/plumbing/plumbing.core.html
;; Look here for useful functions missing from clojure.core

;; I could do this with f/read-chunks, but didn't.
(def input (f/read-lines "2023/d08.txt"))
(def input-sample (f/read-lines "aoc/2023/day_08/sample.txt"))
(def input-sample-2 (f/read-lines "aoc/2023/day_08/sample-2.txt"))
(def input-sample-3 (f/read-lines "aoc/2023/day_08/sample-3.txt"))


(defn get-instructions [input] (-> input first (str/split #"" )))

(defn str->node-map
  "Convert a string to a map, key : {:left :right}"
  [x]
  (let [[k l r] (re-seq #"\w{3}" x)]
    {k {:left l :right r}}))

(defn create-network
  "Create a network map from a list of network strings"
  [ns]
  (apply merge (map str->node-map ns)))

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

#_(get-instructions input-sample)
;; => ["R" "L"]

#_(get-nwk input-sample)

;; => {"AAA" {:left "BBB", :right "CCC"},
;;     "BBB" {:left "DDD", :right "EEE"},
;;     "CCC" {:left "ZZZ", :right "GGG"},
;;     "DDD" {:left "DDD", :right "DDD"},
;;     "EEE" {:left "EEE", :right "EEE"},
;;     "GGG" {:left "GGG", :right "GGG"},
;;     "ZZZ" {:left "ZZZ", :right "ZZZ"}}

(defn part-1 [input]
  (let [instructions (get-instructions input)
        nwk (get-nwk input)]
    (follow-instructions instructions nwk)
    ))


;;; Part 2
;; Brute force does NOT work.

;; Explore the data. There is a pattern. Starting from each valid
;; starting point, it cycles regularly.

;; So, if we find the size of the cycles for each starting point, we
;; can get the lowest common multiple (LCM) to find when they'll ALL
;; end up at a valid end point.




(defn find-to-state
  "Get the next state given the input and a left/right instruction."
  [tree from-state l-or-r]
  (let [lr-key (condp = l-or-r
                 "L" :left
                 "R" :right)]
    (get-in tree [from-state lr-key])))

(find-to-state (get-nwk input-sample) "AAA" "L")

;; (find-to-state (get-nwk input-sample) "AAA" :left)
;; ;; => "BBB"

;; (find-to-state (get-nwk input-sample) "GGG" :left)
;; ;; => "GGG"

(defn start-state? [s] (str/ends-with? s "A"))
(defn goal-state? [s] (str/ends-with? s "Z"))

;; (s/rotate-left instr 1)
(defn try-explore
  [input from-state]
  (let [instructions (get-instructions input)
        tree (get-nwk input)]
    {:instr instructions :state from-state}

    #_(println "Starting try-explore")

    (-> (loop [instr instructions
               n 0
               state from-state
               seen #{}]

          #_(when (goal-state? state) (println "*" n state seen))

          (if
              ;; Continue looping until we've seen the goal state twice.
              (not (and
                    (goal-state? state)
                    (seen state))) ; Inverse of exit condition

            (recur (s/rotate-left instr 1)
                   (inc n)
                   (find-to-state tree state (first instr))
                   (cond-> seen
                     (goal-state? state) (conj state)))
            ;; Exit
            {:n n
             :state state
             :seen seen}
            )))))

#_(try-explore input-sample "AAA")
;; => {:n 3, :state "ZZZ", :seen #{"ZZZ"}}
#_(try-explore input-sample-2 "AAA")
;; => {:n 7, :state "ZZZ", :seen #{"ZZZ"}}

(defn find-start-states [input start-fn]
  (let [tree (get-nwk input)
        start-nodes (keys tree)]
    (filter start-fn start-nodes)))

#_(find-start-states input-sample-3 start-state?)
;; => ("11A" "22A")

#_(try-explore input-sample-3 "11A")
;; => {:instr ("L" "R"), :n 4, :state "11Z", :seen #{"11Z"}, :cycle-size 3}
#_(try-explore input-sample-3 "22A")
;; => {:instr ("L" "R"), :n 6, :state "22Z", :seen #{"22Z"}, :cycle-size 5}

#_(find-start-states input start-state?)
;; ;; => ("RMA" "PLA" "QLA" "NXA" "AAA" "GDA")

#_(try-explore input "RMA")
;; => {:n 43766, :state "FQZ", :seen #{"FQZ"}, :cycle-size 43765}
;; => {:n 43766, :state "FQZ", :seen #{"FQZ"}, :cycle-size 43765}

#_(try-explore input "PLA")
;; => {:n 33794, :state "MQZ", :seen #{"MQZ"}, :cycle-size 33793}


(defn solve
  "Solve any puzzle to goal state"
  [input start-state]
  (let [instructions (get-instructions input)
        tree (get-nwk input)]
    (loop [instr instructions
           n 0 ; Track how many iterations
           state start-state]
      (if (goal-state? state)
        n  ; If we reach the goal state, return the number of steps it took
        (recur (s/rotate-left instr 1)
               (inc n)
               (find-to-state tree state (first instr)))))))

(solve input-sample-3 "11A")
;; => 2
(solve input-sample-3 "22A")
;; => 3
(solve input "RMA")
;; => 21883

(defn part-2
  "Solve part 2"
  [input]
  (let [instructions (get-instructions input)
        tree (get-nwk input)
        distances (for [state (keys tree)
                        :when (start-state? state)]
                    (solve input state))]
    (reduce lcm distances)))

(part-2 input-sample-3)
;; => 6

(part-2 input)
;; 10+ trillion! brute force would not have been happy.
;; => 10,151,663,816,849

#_(defn fizz-buzz [n]
    (let [div-by? (fn [divisor number] (zero? (mod number divisor)))]
      (cond-> nil
        (div-by? 3 n) (str "Fizz")
        (div-by? 5 n) (str "Buzz")
        :always (or (str n)))))

#_(mapv fizz-buzz (range 20))


;; Brute force - doesn't work - heap error
;; (defn move-many
;;   "Make a move from many starting points.
;;   Return the number of steps until all current nodes end in Z."
;;   [instructions nwk]
;;   ;; nwk doesn't change
;;   ;; instructions keeps rotating (take 1st, place at end).
;;   (loop [steps 0
;;          instr instructions
;;          start-keys (filterv ends-in-a? (keys nwk))]
;;     (if (every? ends-in-z? start-keys)
;;       {:steps steps
;;        :nodes start-keys}
;;       (recur (inc steps)
;;              (s/rotate-left instr 1)
;;              (map #(take-step % instr nwk) start-keys)))))

;; ;; Brute force is NOT going to work
;; #_(defn part-2 [input]
;;     (let [instructions (get-instructions input)
;;           nwk (get-nwk input)]
;;       (move-many instructions nwk)))

;; #_(defn part-3 [input]
;;     (let [instructions (get-instructions input)
;;           nwk (get-nwk input)]
;;       (loop [steps 0
;;              start-keys (filterv ends-in-a? (keys nwk))]
;;         (if (some not-ends-in-z? start-keys)
;;           (let [direction (first (s/rotate-left instructions steps))
;;                 choices (map #(get nwk %) start-keys)
;;                 end-keys (condp = direction
;;                            "R" (map :right choices)
;;                            "L" (map :left choices))]
;;             (recur (inc steps)
;;                    end-keys))
;;           {:steps steps
;;            :nodes start-keys}))))



;; ;;;;; tschady's solution

;; ;; Regex parsing is nicer
;; ;; Parse file in chunks
;; ;; Use `cycle` instead of `rotate-left`
;; ;; Learned about `plumbing` and `clojure.math.numeric-tower`

;; (def input-c (f/read-chunks "2023/d08.txt"))
;; (def input-c-sample (f/read-chunks "aoc/2023/day_08/sample.txt"))
;; (def input-c-sample-2 (f/read-lines "aoc/2023/day_08/sample-2.txt"))
;; (def input-c-sample-3 (f/read-lines "aoc/2023/day_08/sample-3.txt"))

;; ;; Keys are chars, not strings or keywords
;; #_(defn parse-net [s]
;;     (for-map [node (str/split-lines s)
;;               :let [[loc l r] (re-seq #"\w{3}" node)]]
;;              loc {\L l \R r}))

;; #_(defn next-loc [net [start dir]]
;;     [(get-in net [start (first dir)]) (rest dir)])

;; #_(defn steps-to-end [net end-fn inst start]
;;     (->> [start inst]
;;          (iterate (partial next-loc net))
;;          (map first)
;;          (take-upto end-fn)
;;          count
;;          dec))

;; #_(defn solve [input start-fn end-fn]
;;     (let [inst (cycle (first input))
;;           net (parse-net (second input))]
;;       (->> (start-fn net)
;;            (map (partial steps-to-end net end-fn inst))
;;            (reduce lcm))))

;; #_(defn starts [net] (filter #(str/ends-with? % "A") (keys net)))

;; #_(defn tschady-part-1 [input]
;;     (solve input (constantly ["AAA"]) #{"ZZZ"}))


;; #_(tschady-part-1 input-c-sample)
;; ;; => 2
