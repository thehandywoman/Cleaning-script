import ctypes
import os
import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta
from functools import partial
from send2trash import send2trash
import platform


def delete_old_files_and_show_popup(folder_path, days=14):
    files_in_folder = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

    if not files_in_folder:
        show_popup("Folder jest pusty. Brak plików do usunięcia.")
    else:
        deleted_files = 0
        current_time = datetime.now()
        for filename in files_in_folder:
            file_path = os.path.join(folder_path, filename)

            if os.path.isfile(file_path):
                try:
                    modification_time = datetime.fromtimestamp(os.path.getmtime(file_path))

                    if current_time - modification_time > timedelta(days=days):
                        send2trash(file_path)
                        deleted_files += 1
                        print(f'Przeniesiono do kosza (starszy niż {days} dni): {filename}')
                except Exception as e:
                    print(f'Błąd podczas przenoszenia pliku {filename} do kosza: {e}')

        if deleted_files > 0:
            show_popup(f"Przeniesiono {deleted_files} plik(i/ów) starszych niż 14 dni do kosza.")
        else:
            show_popup("Brak plików starszych niż 14 dni do przeniesienia do kosza.")


def empty_trash_and_show_popup():
    system_name = platform.system()

    if system_name == "Windows":
        try:

            ctypes.windll.shell32.SHEmptyRecycleBinW(None, None, 0)
            show_popup("Kosz został wyczyszczony.")
        except Exception as e:
            show_popup(f"Błąd podczas opróżniania kosza: {e}")
    else:
        trash_path = get_trash_path()

        try:
            os.system(f"rm -rf {trash_path}/*")
            show_popup("Kosz został wyczyszczony.")
        except Exception as e:
            show_popup(f"Błąd podczas opróżniania kosza: {e}")


def get_trash_path():
    system_name = platform.system()

    if system_name == "Darwin" or system_name == "Linux":
        return os.path.join(os.path.expanduser("~"), ".Trash")
    elif system_name == "Windows":
        return os.path.join(os.path.expanduser("~"), "Recycle Bin")
    else:
        raise NotImplementedError(f"System operacyjny {system_name} nie jest obsługiwany.")


def empty_trash_and_show_popup():
    system_name = platform.system()

    if system_name == "Darwin":  # macOS
        os.system("rm -rf ~/.Trash/*")
        show_popup("Kosz został wyczyszczony.")
    elif system_name == "Linux":
        os.system("rm -rf ~/.local/share/Trash/*")
        show_popup("Kosz został wyczyszczony.")
    elif system_name == "Windows":
        try:

            ctypes.windll.shell32.SHEmptyRecycleBinW(None, None, 0)
            show_popup("Kosz został wyczyszczony.")
        except Exception as e:
            show_popup(f"Błąd podczas opróżniania kosza: {e}")
    else:
        show_popup("System operacyjny nie jest obsługiwany.")


def is_trash_empty():
    system_name = platform.system()

    if system_name == "Darwin" or system_name == "Linux":
        trash_path = os.path.join(os.path.expanduser("~"), ".Trash")
    elif system_name == "Windows":
        trash_path = os.path.join(os.path.expanduser("~"), "Recycle Bin")
    else:
        raise NotImplementedError(f"System operacyjny {system_name} nie jest obsługiwany.")

    try:
        file_count = len(os.listdir(trash_path))
        return file_count == 0
    except FileNotFoundError:
        return True


def show_popup(message):
    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo("Informacja", message)
    root.destroy()


def main():
    folder_path = "D:\\Test"  

    root = tk.Tk()
    root.title("Akcje na folderze")

    btn_empty_trash = tk.Button(root, text="Opróżnij kosz", command=empty_trash_and_show_popup)
    btn_empty_trash.pack(pady=10)

    btn_clear_folder = tk.Button(root, text="Wyczyść folder", command=partial(delete_old_files_and_show_popup, folder_path))
    btn_clear_folder.pack(pady=10)

    root.mainloop()


if __name__ == "__main__":
    main()
