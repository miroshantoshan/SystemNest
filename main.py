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

def load_distros():
    if os.path.exists("distros.json"):
        with open("distros.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return []

distro_data = load_distros()

# --- Логика переключения экранов ---

def show_details(item):
    # Скрываем основное меню
    tabview.pack_forget()
    
    # Очищаем фрейм деталей перед отрисовкой (если там что-то было)
    for widget in details_frame.winfo_children():
        widget.destroy()
    
    # Кнопка НАЗАД
    back_btn = ctk.CTkButton(details_frame, text="← Назад", width=80, fg_color="transparent", 
                             border_width=1, command=hide_details)
    back_btn.pack(anchor="w", padx=10, pady=10)

    # Логотип/Баннер
    banner_path = item.get("full_banner", "")
    if banner_path and os.path.exists(banner_path):
        img = Image.open(banner_path)
        banner_img = ctk.CTkImage(light_image=img, dark_image=img, size=(200, 200))
        ctk.CTkLabel(details_frame, image=banner_img, text="").pack(pady=5)

    # Название и описание
    ctk.CTkLabel(details_frame, text=item.get("name"), font=("Arial", 22, "bold")).pack()
    
    desc_text = item.get("description", "Описание скоро появится...")
    ctk.CTkLabel(details_frame, text=desc_text, wraplength=350, font=("Arial", 13)).pack(pady=15, padx=20)

    # Кнопка скачать (основная)
    ctk.CTkButton(details_frame, text="Скачать дистрибутив", height=40, font=("Arial", 14, "bold"),
                  command=lambda: webbrowser.open(item.get("link", "#"))).pack(pady=10)

    # Дополнительные версии (если есть в JSON)
    versions = item.get("versions", [])
    if versions:
        ctk.CTkLabel(details_frame, text="Другие редакции:", font=("Arial", 11, "bold"), text_color="gray").pack(pady=5)
        v_scroll = ctk.CTkScrollableFrame(details_frame, height=150)
        v_scroll.pack(fill="x", padx=30)
        
        for v in versions:
            v_btn = ctk.CTkButton(v_scroll, text=v.get("label"), fg_color="#2c3e50",
                                  command=lambda l=v.get("link"): webbrowser.open(l))
            v_btn.pack(fill="x", pady=2)

    # Показываем фрейм
    details_frame.pack(fill="both", expand=True)

def hide_details():
    details_frame.pack_forget()
    tabview.pack(padx=10, pady=5, fill="both", expand=True)

# --- Основной интерфейс ---

# Фрейм для деталей (изначально скрыт)
details_frame = ctk.CTkFrame(window, fg_color="transparent")

tabview = ctk.CTkTabview(window)
tabview.pack(padx=10, pady=5, fill="both", expand=True)

tab_search = tabview.add("Search")
tab_info = tabview.add("Info")

def update_list(*args):
    for btn in all_buttons:
        btn.destroy()
    all_buttons.clear()

    search_text = search_var.get().lower()
    found_count = 0

    for item in distro_data:
        name = item.get("name", "???")
        logo_path = item.get("logo", "")

        if search_text in name.lower():
            icon = None
            if logo_path and os.path.exists(logo_path):
                try:
                    img = Image.open(logo_path)
                    icon = ctk.CTkImage(light_image=img, dark_image=img, size=(24, 24))
                except: icon = None

            new_btn = ctk.CTkButton(
                scroll_frame,
                text=name,
                image=icon,
                compound="left",
                command=lambda i=item: show_details(i), # Переход к деталям
                height=40,
                fg_color="#2c3e50",
                hover_color="#033ca5",
                anchor="w"
            )
            new_btn.pack(fill="x", pady=2, padx=5)
            all_buttons.append(new_btn)
            found_count += 1

    counter_label.configure(text=f"Found: {found_count}")

# Поле поиска
search_var = ctk.StringVar()
search_var.trace_add("write", update_list) 
search_entry = ctk.CTkEntry(tab_search, placeholder_text="Поиск системы...", textvariable=search_var, height=35)
search_entry.pack(pady=5, padx=10, fill="x")

counter_label = ctk.CTkLabel(tab_search, text="", font=("Arial", 10), text_color="gray")
counter_label.pack()

scroll_frame = ctk.CTkScrollableFrame(tab_search, label_text="Результаты")
scroll_frame.pack(pady=5, padx=5, fill="both", expand=True)

# Вкладка Info
ctk.CTkLabel(tab_info, text="SystemNest", font=("Arial", 16, "bold")).pack(pady=10)
ctk.CTkLabel(tab_info, text="Compact bible\n all of systems", font=("Arial", 12)).pack()
ctk.CTkLabel(tab_info, text="\nVersion: 0.20.0 Beta", font=("Arial", 15)).pack()

update_list()
window.mainloop()