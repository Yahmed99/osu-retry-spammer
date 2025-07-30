# Osu Retry Spammer
- Are you a chronic retry spammer whenever you farm performance points in [osu!](https://osu.ppy.sh)?
- Are you a going for a leaderboard score on your favorite map but dont want to wate time on scores that dont qualify?

Well this is the program for you!

**Osu Retry Spammer** is a Python executable that automatically restarts osu! maps based on customizable hit conditions (number of 300s, 100s, 50s, or misses). It connects to the game using [Tosu](https://github.com/tosuapp/tosu) and provides a simple GUI to configure retry thresholds.

---

##  Features

-  Auto-retries maps when specified hit conditions are met
-  GUI to set thresholds for 300s, 100s, 50s, and misses
-  Displays live PP estimates
-  Runs locally — no osu! API key required

---
##  Requirements

- Currently only Windows is supported
- [Tosu](https://github.com/limjeck/tosu)
---

## Setup
1. Download [tosu](https://github.com/tosuapp/tosu/releases/latest)
2. Download [Osu Retry Spammer](https://github.com/Yahmed99/osu-retry-spammer/releases/latest)
2. Extract tosu.exe to a `Folder`
3. run `osu!`
4. Run `tosu.exe`
5. Run `osu retry spammer.exe`
6. Have fun!
---


##  Usage

1. Set your desired thresholds in the GUI (e.g. "Retry if I get more than 1 miss").
    - These threshholds are **inclusive**. This means if you set 5 `100`s, it will restart on the 6th `100` hit.
2. Click **Apply**.
3. The tool will automatically retry the map when your hit results exceed the set values.

You can reset the thresholds with the **Reset** button.

---

##  FAQ

-  **HTTP Error on startup:** Make sure Tosu is running before you launch `osu retry spammer.exe`
-  **Running outside of osu!:** The app won't work properly unless you're actively in-game with tosu running.

---

## Running The Script 
You can run the script by itself if you don't want to use the executable in releases.

You will need:
 - `main.py`
 - `settingsGUI.py`
 - `requirements.txt`
 - Python 3.8+ installed on your system

1. Put all files in a new folder
2. **(Optional, but recommended)** create a virtual environment
3. Open a terminal, run `pip install -r requirements.txt`
4. Run main.py 

##  License

MIT — you can do whatever you want, just star the project before you do 😉

---

##  Contributions

Pull requests welcome! If you have an idea or improvement, feel free to open an issue or PR.



