import customtkinter as ctk
import webbrowser
import json
import os
from PIL import Image

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

window = ctk.CTk()
window.title("SystemNest")
window.geometry("400x550")
window.resizable(False, False)
window.iconbitmap("images/logo.ico")

all_buttons = []

def load_distros():
    if os.path.exists("distros.json"):
        with open("distros.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return []

distro_data = load_distros() 

def update_list(*args):
    for btn in all_buttons:
        btn.destroy()
    all_buttons.clear()

    search_text = search_var.get().lower()
    found_count = 0

    for item in distro_data:
        name = item.get("name", "???")
        link = item.get("link", "#")
        logo_path = item.get("logo", "") # Читаем путь из ключа "logo"

        if search_text in name.lower():
            # Загрузка иконки
            icon = None
            if logo_path and os.path.exists(logo_path):
                try:
                    img = Image.open(logo_path)
                    icon = ctk.CTkImage(light_image=img, dark_image=img, size=(24, 24))
                except:
                    icon = None

            new_btn = ctk.CTkButton(
                scroll_frame,
                text=name,
                image=icon,         # Установка иконки
                compound="left",    # Картинка слева от текста
                command=lambda l=link: webbrowser.open(l),
                height=40,
                fg_color="#2c3e50",
                hover_color="#033ca5",
                anchor="w"
            )
            new_btn.pack(fill="x", pady=2, padx=5)
            all_buttons.append(new_btn)
            found_count += 1

    counter_label.configure(text=f"Found: {found_count}")

def open_json():
    if os.path.exists("distros.json"):
        os.startfile("distros.json")

tabview = ctk.CTkTabview(window)
tabview.pack(padx=10, pady=5, fill="both", expand=True)

tab_search = tabview.add("Search")
tab_info = tabview.add("Info")

search_var = ctk.StringVar()
search_var.trace_add("write", update_list) 

search_entry = ctk.CTkEntry(
    tab_search, 
    placeholder_text="Find a system...", 
    textvariable=search_var,
    height=35
)
search_entry.pack(pady=5, padx=10, fill="x")

counter_label = ctk.CTkLabel(tab_search, text="", font=("Arial", 10), text_color="gray")
counter_label.pack()

scroll_frame = ctk.CTkScrollableFrame(tab_search, label_text="Results")
scroll_frame.pack(pady=5, padx=5, fill="both", expand=True)

ctk.CTkLabel(tab_info, text="SystemNest", font=("Arial", 16, "bold")).pack(pady=10)
ctk.CTkLabel(tab_info, text="Compact bible\n all of systems", font=("Arial", 12)).pack()
ctk.CTkLabel(tab_info, text='''
             
Version: 0.10.0 Beta''', font=("Arial", 15)).pack()

update_list()

window.mainloop()