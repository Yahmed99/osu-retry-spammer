import websockets
import json
import pyautogui
import time
import threading
import settingsGUI
import asyncio

uri = "ws://127.0.0.1:24050/websocket/v2"

# Function to retry using keybind
def retry(key):
    if key:
        #tosu reports all 0s for stats until the map is reset, causing my code loop to retry twice
        #resetting the hit dict here to prevent a double retry
        settingsGUI.hitDict = {"300": 0, "100": 0, "50": 0, "0": 0, "Mods": 0}
        pyautogui.keyDown(key)
        time.sleep(0.25)
        pyautogui.keyUp(key)
    else:
        settingsGUI.key_error()


async def listen():

    async with websockets.connect(uri) as websocket:
        (f"Connected to {uri}")

        while True:
            try:
                # get data from tosu websocket
                message = await websocket.recv()
                data = json.loads(message)
                #extract hits
                newhits = data.get("play", {}).get("hits", {})
                # Extract mods for pp calculation
                mods = int(data.get("play", {}).get("mods", {}).get("number", 0))
                
                settingsGUI.update_pp_label()
                settingsGUI.hitDict["Mods"] = mods
                # get the retry keybind
                retryKey = (
                    data.get("settings", {}).get("keybinds", {}).get("quickRetry", "")
                )

                # logic for restarting when parameters met
                for key in settingsGUI.hitDict:
                    if (
                        newhits.get(key, 0) >= settingsGUI.hitDict[key] + 1
                        and settingsGUI.hitDict[key] != 0
                    ):
                        retry(retryKey)
                        break

            except Exception as e:
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
