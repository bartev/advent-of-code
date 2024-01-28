(ns aoc.2023.core
  (:require
   [environ.core :refer [env]]
   [environ.core :as e]
   [clojure.edn :as edn]
   [clojure.string :as str]
   [clojure.java.io :as io]))

(env "PIP_REQUIRE_VIRTUALENV")
;; => nil
;; => nil

(env :foo)
;; => nil

(->> "PIP_REQUIRE_VIRTUALENV"
     (System/getenv))

(System/env)
;; => Syntax error (NoSuchFieldException) compiling . at (src/aoc/2023/core.clj:15:1).
;;    env

(defn load-env-from-file-?
  "Load environment variables from a file."
  [file]
  (when (.exists (java.io.File. file))
    (-> (slurp file)
        str/split-lines
        (map #(str/split % #"="))
        (filter (comp not empty? first))
        (into {}))))

(defn load-env-from-edn
  "Load environment variables from edn file"
  [file]
  (-> (slurp efname)
      edn/read-string))

(let [private-env (load-env-from-edn "private.env")]
  (environ.core/env private-env))


(def fname "private.env")

(load-env-from-file "private.env")

(when (.exists (java.io.File. fname))
  (->> (slurp fname)
       str/split-lines
       (map #(str/split % #"="))
       (filter (comp not empty? first))
       (into {})))
;; => {"AOC-SESSION-COOKIE"
;;     "53616c7465645f5fcaac3c8d7dd82127a79416c1df6e391f6ce21e9735e0a4fc050e27d958676894ce5852a5e9f79cb298cba0983a57856ad0cd4c0042ad1726"}
;; => (["AOC-SESSION-COOKIE"
;;      "53616c7465645f5fcaac3c8d7dd82127a79416c1df6e391f6ce21e9735e0a4fc050e27d958676894ce5852a5e9f79cb298cba0983a57856ad0cd4c0042ad1726"])
;; => (["AOC-SESSION-COOKIE"
;;      "53616c7465645f5fcaac3c8d7dd82127a79416c1df6e391f6ce21e9735e0a4fc050e27d958676894ce5852a5e9f79cb298cba0983a57856ad0cd4c0042ad1726"]
;;     ["FOO"])

(def efname "private.edn")
(when (.exists (java.io.File. efname))
  (edn/read {:eof :thread} (io/reader efname)))


(with-open [in (java.io.PushbackReader. (clojure.java.io/reader efname))]
  (let [edn-seq (repeatedly (partial edn/read {:eof :theend} in))]
    (dorun (map println (take-while (partial not= :theend) edn-seq)))))
;; => nil


(e/keywordize "foo")

(def cur-env-defs (System/getenv))
cur-env-defs
;; => {"HOMEBREW_PREFIX" "/opt/homebrew",
;;     "COMMAND_MODE" "unix2003",
;;     "DEV_HOME" "/Users/bartev/dev",
;;     "DISPLAY" "BV-Home-Mac.attlocal.net",
;;     "DOT_FILES" "/Users/bartev/dev/github/sam-adams",
;;     "GITHUBPERS_HOME" "/Users/bartev/dev/github",
;;     "HOME" "/Users/bartev",
;;     "HOMEBREW_CELLAR" "/opt/homebrew/Cellar",
;;     "HOMEBREW_REPOSITORY" "/opt/homebrew",
;;     "INFOPATH" "/opt/homebrew/share/info:",
;;     "LANG" "en_US.UTF-8",
;;     "LOGNAME" "bartev",
;;     "LaunchInstanceID" "7AC0D734-9829-4AAC-B980-5FC1DB6667A5",
;;     "MANPATH" "/opt/homebrew/share/man::",
;;     "PATH" "/opt/homebrew/bin:/opt/homebrew/sbin:/usr/local/bin:/System/Cryptexes/App/usr/bin:/usr/bin:/bin:/usr/sbin:/sbin:/var/run/com.apple.security.cryptexd/codex.system/bootstrap/usr/local/bin:/var/run/com.apple.security.cryptexd/codex.system/bootstrap/usr/bin:/var/run/com.apple.security.cryptexd/codex.system/bootstrap/usr/appleinternal/bin:/Library/TeX/texbin:/opt/homebrew/bin:/opt/homebrew/sbin:/Users/bartev/bin:/Users/bartev/bin",
;;     "PWD" "/Users/bartev/dev/github/advent-of-code-repos/advent-of-code"
;;     "SECURITYSESSIONID" "186b2",
;;     "SHELL" "/bin/zsh",
;;     "SHLVL" "0",
;;     "SSH_AUTH_SOCK" "/private/tmp/com.apple.launchd.JcFg5fxbpS/Listeners",
;;     "TERM" "dumb",
;;     "TMPDIR" "/var/folders/zc/tbdf79nj7m1_jkn65fr8tj3m0000gn/T/",
;;     "USER" "bartev",
;;     "XPC_FLAGS" "0x0",
;;     "XPC_SERVICE_NAME" "application.org.gnu.Emacs.2413776.2413781",
;;     "ZDOTDIR" "/Users/bartev/.config/zsh",
;;     "ZSH_PRIVATE_HOME" "/Users/bartev/.config/.zshenv-private",
;;     "__CFBundleIdentifier" "org.gnu.Emacs",
;;     "__CF_USER_TEXT_ENCODING" "0x1F5:0x0:0x0",
;; }

(env :shell)
;; => "/bin/zsh"

env

(apply sorted-map env)

(System/getProperties)
