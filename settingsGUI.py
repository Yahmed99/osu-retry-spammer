from tkinter import *
import requests
import pyperclip

hitDict = {"300": 0, "100": 0, "50": 0, "0": 0, "Mods": 0}



# create root window
def start_gui():

    root = Tk()
    global pp_var 
    pp_var = StringVar()

    root.title("Osu Retry Spammer")
    root.geometry("350x300")

    # Set up labels and placement
    lb300 = Label(root, text="Max # of 300s: ")
    lb300.grid(row=0, column=0, sticky=W, pady=2)
    lb100 = Label(root, text="Max # of 100s: ")
    lb100.grid(row=1, column=0, sticky=W, pady=2)
    lb50 = Label(root, text="Max # of 50s: ")
    lb50.grid(row=2, column=0, sticky=W, pady=2)
    lb0 = Label(root, text="Max # of Misses: ")
    lb0.grid(row=3, column=0, sticky=W, pady=2)

    pp_var.set(f"PP: {get_pp_from_input()}")

    lbpp = Label(root, textvariable=pp_var)
    lbpp.grid(row=4, column=1, sticky=W, pady=2)
    
    # Entry Fields
    h300 = Entry(root)
    h300.grid(row=0, column=1, sticky=W, pady=2)
    h100 = Entry(root)
    h100.grid(row=1, column=1, sticky=W, pady=2)
    h50 = Entry(root)
    h50.grid(row=2, column=1, sticky=W, pady=2)
    h0 = Entry(root)
    h0.grid(row=3, column=1, sticky=W, pady=2)

    # function to set the parameters in hitDict from user input
    def clicked():
        try:
            hitDict["300"] = int(h300.get()) if h300.get().strip() else 0
            hitDict["100"] = int(h100.get()) if h100.get().strip() else 0
            hitDict["50"] = int(h50.get()) if h50.get().strip() else 0
            hitDict["0"] = int(h0.get()) if h0.get().strip() else 0
        except ValueError:
            show_error_window("Please enter valid numbers.")
        update_pp_label()
        # lbpp.config(text=f"PP: {get_pp_from_input()}")

    def reset():
        global hitDict
        for entry in [h300, h100, h50, h0]:
            entry.delete(0, END)
        hitDict = {"300": 0, "100": 0, "50": 0, "0": 0, "Mods" : 0}
        # lbpp.config(text=f"PP: {get_pp_from_input()}")

    # button widget for apply and reset
    btnApply = Button(root, text="Apply", fg="black", command=clicked)
    btnReset = Button(root, text="Reset", fg="red", command=reset)
    btnApply.grid(row=5, column=0, sticky="se", padx=5, pady=5)
    btnReset.grid(row=5, column=1, sticky="sw", padx=5, pady=5)

    # Execute Tkinter
    root.mainloop()

def update_pp_label():
    pp_var.set(f"PP: {get_pp_from_input()}")

def get_pp_from_input():
    pp_url = f"http://127.0.0.1:24050/api/calculate/pp?n100={hitDict['100']}&n50={hitDict['50']}&nMisses={hitDict['0']}&mods={hitDict['Mods']}"
    
    try:
        response = requests.get(pp_url)
        responseData = response.json()
        
        if "error" in responseData:
            show_error_window(responseData["error"])
            return 0  
        else:
            pp_value = int(round(responseData["pp"]))
            return pp_value
    except Exception as e:
        show_error_window(str(e))
        pass

#dont think its even possible to have a null keybind in osu but better safe than sorry
def key_error():
    show_error_window("Please set a reset key in osu!.")
    
#error window for reporting
def show_error_window(error_message):
    error_window = Toplevel()
    error_window.title("Error")
    error_window.geometry("600x450")
    # print(error_message)
    label = Label(error_window, text=error_message, fg="red", wraplength=500)
    label.pack(pady=20)

    button_frame = Frame(error_window)
    button_frame.pack(pady=10)

    ok_button = Button(button_frame, text="OK", command=error_window.destroy)
    copy_button = Button(button_frame, text="Copy", command=lambda: pyperclip.copy(error_message))

    copy_button.pack(side="left", padx=10)
    ok_button.pack(side="left", padx=10)