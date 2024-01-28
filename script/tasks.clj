(ns tasks
  (:require
   ;; [clj-http.client :as client]
   ;; [babashka.pods :as pods]
   [clojure.edn :as edn]
   [babashka.curl :as curl]
   [babashka.fs :as fs]
   [clojure.java.io :as io]
   [clojure.java.shell :refer [sh]]
   [selmer.parser :refer [render-file]]))


;; Babashka pods are programs that can be used as Clojure libraries by babashka
;; https://github.com/babashka/pods

;; https://github.com/retrogradeorbit/bootleg
;; Static website generation made simple. A powerful, fast, clojure
;; html templating solution

;; TODO: [2024-01-27] I can specify pods in `bb.edn`
;; Leave it here until I know things work
#_(pods/load-pod 'retrogradeorbit/bootleg "0.1.9")

#_(require '[pod.retrogradeorbit.bootleg.utils :refer [convert-to]]
           '[pod.retrogradeorbit.hickory.select :as s])

(def now (java.time.LocalDate/now (java.time.ZoneId/of "US/Eastern")))
(def current-day (str (.getDayOfMonth now)))
(def current-year (str (if (= 12 (.getMonthValue now))
                         (.getYear now)
                         (dec (.getYear now)))))

(def aoc-url "https://adventofcode.com")
(def badge-url "http://img.shields.io/static/v1")
(def icon-path "img/aoc-favicon-base64")

(def private-env-file "private.edn")
(defn load-sys-properties-from-edn
  "Load system properties from edn file and setProperty"
  [file]
  (let [env-vars (-> (slurp file)
                     edn/read-string)]
    (map (fn [[k v]] (System/setProperty k v))
         env-vars)))
(load-sys-properties-from-edn private-env-file)

(def headers
  {:headers
   {"Cookie"    (str "session=" (System/getProperty "AOC_SESSION"))
    "UserAgent" (str (System/getProperty "AOC_REPO")
                     " by "
                     (System/getProperty "AOC_EMAIL"))}})
(def badge-style
  {"color"      "00cc00" ; right side
   "labelColor" "0a0e25" ; left side
   "style"      "flat"
   "logo"       (str "data:image/png;base64," (slurp icon-path))})

(defn- zero-pad-str [s] (format "%02d" (Long/valueOf s)))

;; Get urls
(defn- problem-url [y d] (str aoc-url "/" y "/day/" d))
(defn- input-url   [y d] (str (problem-url y d) "/input"))
(defn- answer-url  [y d] (str (problem-url y d) "/answer"))

;; Get file locations in this repo
(defn- source-path [y d] (format "src/aoc/%s/day_%s/core.clj"       y (zero-pad-str d)))
(defn- test-path   [y d] (format "test/aoc/%s/day_%s/core_test.clj" y (zero-pad-str d)))
;; (defn- source-path [y d] (format "src/aoc/%s/d%s.clj"       y (zero-pad-str d)))
;; (defn- test-path   [y d] (format "test/aoc/%s/d%s_test.clj" y (zero-pad-str d)))
(defn- input-path  [y d] (format "resources/%s/d%s.txt"     y (zero-pad-str d)))

;; => "src/aoc/2023/d07.clj"
(source-path 2023 7)
;; => "src/aoc/2023/day_07/core.clj"


(defn create-new-file
  "Create the file and parent directories"
  [template-type year day]
  (let [d0 (zero-pad-str day)
        template (condp = template-type
                   :src "templates/src.clj"
                   :test "templates/test.clj")
        file-function (condp = template-type
                        :src source-path
                        :test test-path)
        fname (file-function year day)]
    (println "Create new file using template:" template "for year:" year "and day:" day)
    (if (fs/exists? fname)
      (println (format "Create '%s' failed, file already exists." fname))
      (doall
       (io/make-parents fname)
       (spit fname (render-file template {:year year :day d0}))))))

(defn template-day
  "Create stubs
  E.g.
  (template-day {:y 2023 :d 3})"
  [{:keys [y d] :or {y current-year d current-day}}]
  (do
    (println "Creating templates: inputs year:" y "day:" d)
    (map #(create-new-file % y d) [:src :test])))

;; Header is slightly different. Does this matter?
#_(defn download-input-bb
    "Download the problem input for the given day, and save to correct path."
    [{:keys [y d] :or {y current-year d current-day}}]
    (let [fname (input-path y d)]
      (if (fs/exists? fname)
        (println (format "Create '%s' failed, file already exists." fname))
        (doall
         (io/make-parents fname)
         (spit fname (:body (curl/get (input-url y d) headers)))))))

;; this is working with clj-http.client, but not babashka.curl
(defn- download-input
  [{:keys [y d] :or {y current-year d current-day}}]
  (try
    (doall
     (load-sys-properties-from-edn private-env-file)
     (let [cookie (System/getProperty "AOC_SESSION")
           fname (input-path y d)
           url (input-url y d)
           repo-url (System/getProperty "AOC_REPO")
           email (System/getProperty "AOC_EMAIL")
           headers {"UserAgent" (str repo-url " by " email)}
           body (:body (curl/get url {:cookies {"session" {:value cookie}}
                                      :headers headers}))]
       (if (fs/exists? fname)
         (println (format "Create '%s' failed, file already exists." fname))
         (doall
          (io/make-parents fname)
          (spit fname body)))))
    (catch Exception e
      (println "Ho, ho, ho! Did you forget to populate `session-cookie` with your AOC session cookie?")
      (throw e))))

(defn- save-badge
  "Create badge with year label and star count, and save to file."
  [[label stars]]
  (let [path (str "img/" label ".svg")
        params (merge {"label" label
                       "message" stars}
                      badge-style)
        badge (:body (curl/get badge-url {:query-params params}))]
    (doall
     (io/make-parents path)
     (spit path "badge"))))

;; Requires pods (2024-01-27 not working)
#_(defn update-badges [arg]
    (let [parsed (-> (str aoc-url "/events")
                     (curl/get headers)
                     :body
                     #_(convert-to :hickory)
                     )
          stars (->> parsed
                     (s/select (s/class "star-count")))]
      stars))

;; (update-badges :foo)

(defn open-apps
  "Fire up all apps required to solve the problem"
  [{:keys [y d] :or {y current-year d current-day}}]
  (sh "open" (input-url y d))
  (sh "open" (problem-url y d)))

#_(defn submit
    ""
    []
    )
