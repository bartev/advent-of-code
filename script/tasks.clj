(ns tasks
  (:require
   ;; [clj-http.client :as client]
   [babashka.curl :as curl]
   [babashka.fs :as fs]
   [babashka.http-client :as http]
   [babashka.pods :as pods]
   [clojure.edn :as edn]
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
#_(load-sys-properties-from-edn private-env-file)

(defn- get-private-configs
  "Read a config value from an edn file.
  Use for private data."
  [file]
  (let [m (-> (slurp file)
              edn/read-string)]
    m))

(defn- get-private-val [k] (-> (get-private-configs private-env-file) (get k)))
(defn- get-aoc-session [] (-> (get-private-val "AOC_SESSION")))
(defn- get-aoc-repo [] (get-private-val "AOC_REPO"))
(defn- get-aoc-email [] (get-private-val "AOC_EMAIL"))

#_(get-aoc-session)
#_(get-aoc-repo)

;; Can't get System/getenv to read the the private info
#_(def headers
    {:headers
     {"Cookie"    (str "session=" (System/getenv "AOC_SESSION"))
      "UserAgent" (str (System/getenv "AOC_REPO")
                       " by "
                       (System/getenv "AOC_EMAIL"))}})
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

(defn- source-py-path [y d] (format "src/aoc/yr_%s/day_%s/puzzle.py"      y (zero-pad-str d)))
(defn- test-py-path   [y d] (format "src/aoc/yr_%s/day_%s/puzzle_test.py" y (zero-pad-str d)))
(defn- readme-path    [y d] (format "src/aoc/yr_%s/day_%s/readme.org"     y (zero-pad-str d)))
(defn- test-data-path [y d] (format "src/aoc/yr_%s/day_%s/test_data.txt"  y (zero-pad-str d)))
(defn- init-py-path   [y d] (format "src/aoc/yr_%s/day_%s/__init__.py"    y (zero-pad-str d)))

;; => "src/aoc/2023/d07.clj"
#_(source-path 2023 7)
;; => "src/aoc/2023/day_07/core.clj"


(defn create-new-file
  "Create the file and parent directories"
  [template-type year day]
  (let [d0 (zero-pad-str day)
        template (condp = template-type
                   :src "templates/src.clj"
                   :test "templates/test.clj"
                   :src-py "templates/src.py"
                   :test-py "templates/test.py"
                   :readme "templates/readme.org"
                   :test-data "templates/test_data.txt"
                   :init-py "templates/__init__.py"
                   )
        file-function (condp = template-type
                        :src source-path
                        :test test-path
                        :src-py source-py-path
                        :test-py test-py-path
                        :readme readme-path
                        :test-data test-data-path
                        :init-py init-py-path)
        fname (file-function year day)]
    (do
      (if (fs/exists? fname)
        (println (format "Create '%s' failed, file already exists." fname))
        (do
          (println "Create new file" fname "using template:" template "for year:" year "and day:" day)
          (io/make-parents fname)
          (spit fname (render-file template {:year year :day d0})))))))

(defn template-day
  "Create stubs
  E.g.
  (template-day {:y 2023 :d 3})"
  [{:keys [y d] :or {y current-year d current-day}}]
  (do
    (println "Creating stubs from templates template: year:" y "day:" d)
    ;; (create-new-file :src y d)
    ;; (create-new-file :test y d)
    (create-new-file :src-py y d)
    (create-new-file :readme y d)
    (create-new-file :test-data y d)
    (create-new-file :test-py y d)
    (create-new-file :init-py y d)
    ))

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

#_(download-input-bb {:y 2023 :d 2})

;; ;; this is working with clj-http.client, but not babashka.curl
;; (defn download-input
;;   [{:keys [y d] :or {y current-year d current-day}}]
;;   (load-sys-properties-from-edn private-env-file)
;;   (try
;;     (let [cookie (get-aoc-session)
;;           fname (input-path y d)
;;           url (input-url y d)
;;           repo-url (get-aoc-repo)
;;           email (get-aoc-email)
;;           headers {"UserAgent" (str repo-url " by " email)}
;;           body (:body (http/get url {:cookies {"session" {:value cookie}}
;;                                      :headers headers}))]
;;       (if (fs/exists? fname)
;;         (println (format "Create '%s' failed, file already exists." fname))
;;         (doall
;;          (io/make-parents fname)
;;          (spit fname body))))
;;     (catch Exception e
;;       (println "Ho, ho, ho! Did you forget to populate `session-cookie` with your AOC session cookie?")
;;       (throw e))))

;; Not working
#_(download-input {:y 2023 :d 1})


(def headers-curl {:headers
                   {"Cookie"    (str "session=" (get-aoc-session))
                    "UserAgent" (str (get-aoc-repo) " by " (get-aoc-email))}})

(defn download-input-curl
  "Download the problem input for given day, and save to correct path."
  [{:keys [y d] :or {y current-year d current-day}}]
  (let [fname (input-path y d)
        body (:body (curl/get (input-url y d) headers-curl))]
    (if (fs/exists? fname)
      (println (format "Create '%s' failed, file already exists." fname))
      (do
        (io/make-parents fname)
        (spit fname body)))))

(defn try-me
  "Try some code"
  [{:keys [y d] :or {y current-year d current-day}}]
  (println (format "year '%s' day '%s'" y d)))

#_(download-input-curl {:y 2023 :d 2})

;; Comment out because of `client`
#_(defn fetch-input
    [{:keys [y d] :or {y current-year d current-day}}]
    (try
      (let [cookie (get-aoc-session)]
        (:body (client/get
                (input-url y d)
                {:cookies {"session" {:value cookie}}
                 :headers {"User-Agent"
                           "Bartev's AOC, https://github.com/bartev bartev@gmail.com"}})))
      (catch Exception e
        (println "Ho, ho, ho! Did you forget to populate `.aoc-session` with your AOC session cookie?")
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
  (sh "open" (problem-url y d))
  (download-input-curl {:y y :d d})
  (template-day {:y y :d d}))
