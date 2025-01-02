import tkinter as tk
from tkinter import ttk
import os

# Глобальная переменная для хранения истории путей
path_history = []

# Функция для заполнения списка файлов и папок
def populate_listbox(listbox, path):
    listbox.delete(0, tk.END)
    for p in os.listdir(path):
        abs_path = os.path.join(path, p)
        isdir = os.path.isdir(abs_path)
        listbox.insert(tk.END, p + ("/" if isdir else ""))

# Функция для обработки двойного щелчка на элементе списка
def on_double_click(event):
    global path_history
    widget = event.widget
    selection = widget.curselection()
    if selection:
        index = selection[0]
        file_name = widget.get(index)
        abs_path = os.path.join(path_history[-1], file_name)
        if os.path.isdir(abs_path):
            path_history.append(abs_path)
            populate_listbox(widget, abs_path)

# Функция для возврата назад
def go_back():
    global path_history
    if len(path_history) > 1:
        path_history.pop()
        previous_path = path_history[-1]
        populate_listbox(listbox, previous_path)

# Создаем основное окно
root = tk.Tk()
root.title("Файловый проводник")
root.geometry("800x600")  # Увеличиваем размер окна

# Создаем список
listbox = tk.Listbox(root)
listbox.pack(fill='both', expand=True)

# Привязываем обработчик для двойного щелчка
listbox.bind('<Double-1>', on_double_click)

# Создаем кнопку "Назад"
back_button = tk.Button(root, text="Назад", command=go_back)
back_button.pack()

# Заполняем список корневым узлом
path_history.append('/')
populate_listbox(listbox, '/')

# Запускаем основное приложение
root.mainloop()
