import websockets
import json
import pyautogui
import time
import threading
import settingsGUI
import asyncio

uri = "ws://127.0.0.1:24050/websocket/v2"
retryCooldown = False


# Function to retry using keybind
def retry(key):
    global retryCooldown
    if key and not retryCooldown:
        pyautogui.keyDown(key)
        time.sleep(0.25)
        pyautogui.keyUp(key)
        retryCooldown = True
    elif retryCooldown:
        pass
    else:
        settingsGUI.key_error()


async def listen():

    async with websockets.connect(uri) as websocket:
        while True:
            try:
                global retryCooldown
                # get data from tosu websocket
                message = await websocket.recv()
                data = json.loads(message)
                # extract necessary info
                liveHits = data.get("play", {}).get("hits", {})
                liveTime = int(data.get("beatmap", {}).get("time", {}).get("live", {}))
                firstObject = int(
                    data.get("beatmap", {}).get("time", {}).get("firstObject", {})
                )
                if liveTime <= firstObject:
                    retryCooldown = False

                # Extract mods for pp calculation
                mods = int(data.get("play", {}).get("mods", {}).get("number", 0))
                settingsGUI.update_pp_label()
                settingsGUI.hitDict["Mods"] = mods

                # get the retry keybind
                """ TODO: I recently found out Lazer does not have an api for keybinds, so this entire feature is more or less useless for you guys.
                 I initially hoped that using tosu would make the code the same for both clients but upon testing i was completely wrong :p
                 anyways, if you are running this program with lazer you are gonna get spammed with errors, sorry """
                retryKey = (
                    data.get("settings", {}).get("keybinds", {}).get("quickRetry", "`")
                )

                # logic for restarting when parameters met
                for key in settingsGUI.hitDict:
                    if (
                        liveHits.get(key, 0) >= settingsGUI.hitDict[key] + 1
                        and settingsGUI.hitDict[key] != 0
                    ):

                        retry(retryKey)

            except Exception as e:
                # settingsGUI.show_error_window(f"Error: {e}")
                # print(f"Error: {e}")
                pass


# Run the WebSocket listener
def start_tosu_websocket():
    asyncio.run(listen())


# Start Tkinter GUI in a separate thread
stop_event = threading.Event()
gui_thread = threading.Thread(target=settingsGUI.start_gui, daemon=True)
gui_thread.start()
ws_thread = threading.Thread(target=start_tosu_websocket)
ws_thread.start()

# Keep the main thread alive
ws_thread.join()
gui_thread.join()
