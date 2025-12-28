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

def open_details(item):
    """Создает отдельное окно с детальной информацией о дистрибутиве."""
    details_window = ctk.CTkToplevel(window)
    details_window.title(item.get("name", "Details"))
    details_window.geometry("350x500")
    details_window.attributes("-topmost", True)  # Окно поверх основного
    
    # 1. Баннер/Лого сверху
    banner_path = item.get("full_banner", item.get("logo", ""))
    if banner_path and os.path.exists(banner_path):
        img = Image.open(banner_path)
        # Масштабируем картинку под ширину окна
        banner_img = ctk.CTkImage(light_image=img, dark_image=img, size=(300, 150))
        banner_label = ctk.CTkLabel(details_window, image=banner_img, text="")
        banner_label.pack(pady=10)

    # 2. Название и описание
    ctk.CTkLabel(details_window, text=item.get("name"), font=("Arial", 20, "bold")).pack()
    
    desc_text = item.get("description", "Описание отсутствует.")
    desc_label = ctk.CTkLabel(details_window, text=desc_text, wraplength=300, font=("Arial", 12))
    desc_label.pack(pady=10, padx=15)

    # 3. Кнопка "Скачать основной"
    main_btn = ctk.CTkButton(
        details_window, 
        text="Скачать дистрибутив", 
        fg_color="#1f6aa5",
        command=lambda: webbrowser.open(item.get("main_link", "#"))
    )
    main_btn.pack(pady=10)

    # 4. Список версий (если есть)
    versions = item.get("versions", [])
    if versions:
        ctk.CTkLabel(details_window, text="Другие версии:", font=("Arial", 10, "bold")).pack(pady=5)
        v_frame = ctk.CTkScrollableFrame(details_window, height=120)
        v_frame.pack(fill="x", padx=20, pady=5)
        
        for v in versions:
            v_btn = ctk.CTkButton(
                v_frame, 
                text=v.get("label"), 
                height=28,
                fg_color="transparent",
                border_width=1,
                command=lambda l=v.get("link"): webbrowser.open(l)
            )
            v_btn.pack(fill="x", pady=2)

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
                except:
                    icon = None

            # Теперь кнопка открывает окно с описанием, а не сразу ссылку
            new_btn = ctk.CTkButton(
                scroll_frame,
                text=name,
                image=icon,
                compound="left",
                command=lambda i=item: open_details(i), # Передаем весь объект данных
                height=40,
                fg_color="#2c3e50",
                hover_color="#033ca5",
                anchor="w"
            )
            new_btn.pack(fill="x", pady=2, padx=5)
            all_buttons.append(new_btn)
            found_count += 1

    counter_label.configure(text=f"Found: {found_count}")

# --- Интерфейс (без изменений) ---
tabview = ctk.CTkTabview(window)
tabview.pack(padx=10, pady=5, fill="both", expand=True)

tab_search = tabview.add("Search")
tab_info = tabview.add("Info")

search_var = ctk.StringVar()
search_var.trace_add("write", update_list) 

search_entry = ctk.CTkEntry(tab_search, placeholder_text="Find a system...", textvariable=search_var, height=35)
search_entry.pack(pady=5, padx=10, fill="x")

counter_label = ctk.CTkLabel(tab_search, text="", font=("Arial", 10), text_color="gray")
counter_label.pack()

scroll_frame = ctk.CTkScrollableFrame(tab_search, label_text="Results")
scroll_frame.pack(pady=5, padx=5, fill="both", expand=True)

ctk.CTkLabel(tab_info, text="SystemNest", font=("Arial", 16, "bold")).pack(pady=10)
ctk.CTkLabel(tab_info, text="Compact bible\n all of systems", font=("Arial", 12)).pack()
ctk.CTkLabel(tab_info, text="\nVersion: 0.10.0 Beta", font=("Arial", 15)).pack()

update_list()
window.mainloop()