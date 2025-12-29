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

all_buttons = []
windows_buttons = []
installer_buttons = [] 



def load_distros():
    if os.path.exists("distros.json"):
        with open("distros.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def load_windows():
    if os.path.exists("windows.json"):
        with open("windows.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def load_installers():
    if os.path.exists("downloaders.json"):
        with open("downloaders.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return []

distro_data = load_distros()
windows_data = load_windows()
installer_data = load_installers()


def show_details(item):
    tabview.pack_forget()
    for widget in details_frame.winfo_children():
        widget.destroy()
    
    back_btn = ctk.CTkButton(details_frame, text="← Назад", width=80, fg_color="transparent", 
                             border_width=1, command=hide_details)
    back_btn.pack(anchor="w", padx=10, pady=10)

    banner_path = item.get("full_banner", "")
    if banner_path and os.path.exists(banner_path):
        img = Image.open(banner_path)
        w, h = img.size
        

        new_width = 250 
        new_height = int(h * (new_width / w))
        
        banner_img = ctk.CTkImage(light_image=img, dark_image=img, size=(new_width, new_height))
        ctk.CTkLabel(details_frame, image=banner_img, text="").pack(pady=5)

    ctk.CTkLabel(details_frame, text=item.get("name"), font=("Arial", 22, "bold")).pack()
    
    desc_text = item.get("description", "Description were here soon...")
    ctk.CTkLabel(details_frame, text=desc_text, wraplength=350, font=("Arial", 13)).pack(pady=15, padx=20)

    ctk.CTkButton(details_frame, text="Скачать", height=40, font=("Arial", 14, "bold"),
                  command=lambda: webbrowser.open(item.get("link", "#"))).pack(pady=10)

    versions = item.get("versions", [])
    if versions:
        ctk.CTkLabel(details_frame, text="Другие редакции:", font=("Arial", 11, "bold"), text_color="gray").pack(pady=5)
        v_scroll = ctk.CTkScrollableFrame(details_frame, height=150)
        v_scroll.pack(fill="x", padx=30)
        
        for v in versions:
            v_btn = ctk.CTkButton(v_scroll, text=v.get("label"), fg_color="#2c3e50",
                                  command=lambda l=v.get("link"): webbrowser.open(l))
            v_btn.pack(fill="x", pady=2)

    details_frame.pack(fill="both", expand=True)

def hide_details():
    details_frame.pack_forget()
    tabview.pack(padx=10, pady=5, fill="both", expand=True)



def update_list(*args):
    for btn in all_buttons:
        btn.destroy()
    all_buttons.clear()
    search_text = search_var.get().lower()
    for item in distro_data:
        if search_text in item.get("name", "").lower():
            logo_path = item.get("logo", "")
            icon = None
            if logo_path and os.path.exists(logo_path):
                try:
                    img = Image.open(logo_path)
                    icon = ctk.CTkImage(light_image=img, dark_image=img, size=(24, 24))
                except: icon = None
            new_btn = ctk.CTkButton(scroll_frame, text=item.get("name"), image=icon, compound="left",
                                    command=lambda i=item: show_details(i), height=40,
                                    fg_color="#2c3e50", hover_color="#033ca5", anchor="w")
            new_btn.pack(fill="x", pady=2, padx=5)
            all_buttons.append(new_btn)

def update_windows_list():
    for btn in windows_buttons:
        btn.destroy()
    windows_buttons.clear()
    for item in windows_data:
        logo_path = item.get("logo", "")
        icon = None
        if logo_path and os.path.exists(logo_path):
            try:
                img = Image.open(logo_path)
                icon = ctk.CTkImage(light_image=img, dark_image=img, size=(24, 24))
            except: icon = None
        new_btn = ctk.CTkButton(windows_scroll_frame, text=item.get("name"), image=icon, compound="left",
                                command=lambda i=item: show_details(i), height=40,
                                fg_color="#2c3e50", hover_color="#033ca5", anchor="w")
        new_btn.pack(fill="x", pady=2, padx=5)
        windows_buttons.append(new_btn)

def update_installer_list():
    for btn in installer_buttons:
        btn.destroy()
    installer_buttons.clear()
    for item in installer_data:
        logo_path = item.get("logo", "")
        icon = None
        if logo_path and os.path.exists(logo_path):
            try:
                img = Image.open(logo_path)
                icon = ctk.CTkImage(light_image=img, dark_image=img, size=(24, 24))
            except: icon = None
        new_btn = ctk.CTkButton(installer_scroll_frame, text=item.get("name"), image=icon, compound="left",
                                command=lambda i=item: show_details(i), height=40,
                                fg_color="#2c3e50", hover_color="#033ca5", anchor="w")
        new_btn.pack(fill="x", pady=2, padx=5)
        installer_buttons.append(new_btn)



details_frame = ctk.CTkFrame(window, fg_color="transparent")

tabview = ctk.CTkTabview(window)
tabview.pack(padx=10, pady=5, fill="both", expand=True)

tab_search = tabview.add("Linux")
tab_windows = tabview.add("Windows")
tab_installers = tabview.add("Downloaders") 
tab_info = tabview.add("Info")


search_var = ctk.StringVar()
search_var.trace_add("write", update_list) 
search_entry = ctk.CTkEntry(tab_search, placeholder_text="Поиск системы...", textvariable=search_var, height=35)
search_entry.pack(pady=5, padx=10, fill="x")
scroll_frame = ctk.CTkScrollableFrame(tab_search, label_text="Linux")
scroll_frame.pack(pady=5, padx=5, fill="both", expand=True)


windows_scroll_frame = ctk.CTkScrollableFrame(tab_windows, label_text="Windows Versions")
windows_scroll_frame.pack(pady=5, padx=5, fill="both", expand=True)


installer_scroll_frame = ctk.CTkScrollableFrame(tab_installers, label_text="Available Installers")
installer_scroll_frame.pack(pady=5, padx=5, fill="both", expand=True)


ctk.CTkLabel(tab_info, text="SystemNest", font=("Arial", 16, "bold")).pack(pady=10)
ctk.CTkLabel(tab_info, text="Compact bible\n all of systems", font=("Arial", 12)).pack()
ctk.CTkLabel(tab_info, text="\nVersion: 1.10.0", font=("Arial", 15)).pack()


update_list()
update_windows_list()
update_installer_list()

window.mainloop()