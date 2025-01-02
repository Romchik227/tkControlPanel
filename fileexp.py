import tkinter as tk
from tkinter import ttk
import os

# Глобальная переменная для хранения истории путей и текущей позиции в истории
path_history = []
current_position = -1

# Функция для заполнения списка файлов и папок
def populate_listbox(listbox, path):
    listbox.delete(0, tk.END)
    for p in os.listdir(path):
        abs_path = os.path.join(path, p)
        isdir = os.path.isdir(abs_path)
        listbox.insert(tk.END, p + ("/" if isdir else ""))

# Функция для обработки двойного щелчка на элементе списка
def on_double_click(event):
    global path_history, current_position
    widget = event.widget
    selection = widget.curselection()
    if selection:
        index = selection[0]
        file_name = widget.get(index)
        abs_path = os.path.join(path_history[current_position], file_name)
        if os.path.isdir(abs_path):
            current_position += 1
            path_history = path_history[:current_position]
            path_history.append(abs_path)
            populate_listbox(widget, abs_path)
            update_buttons()

# Функция для возврата назад
def go_back():
    global current_position
    if current_position > 0:
        current_position -= 1
        populate_listbox(listbox, path_history[current_position])
        update_buttons()

# Функция для перехода вперед
def go_forward():
    global current_position
    if current_position < len(path_history) - 1:
        current_position += 1
        populate_listbox(listbox, path_history[current_position])
        update_buttons()

# Функция для обновления состояния кнопок
def update_buttons():
    back_button.config(state=tk.NORMAL if current_position > 0 else tk.DISABLED)
    forward_button.config(state=tk.NORMAL if current_position < len(path_history) - 1 else tk.DISABLED)

# Создаем основное окно
root = tk.Tk()
root.title("Файловый проводник")
root.geometry("800x600")  # Увеличиваем размер окна

# Создаем фрейм для кнопок "Назад" и "Вперед"
button_frame = tk.Frame(root)
button_frame.pack(side=tk.TOP, fill=tk.X)

# Создаем кнопки "Назад" и "Вперед"
back_button = tk.Button(button_frame, text="<-", command=go_back, state=tk.DISABLED)
back_button.pack(side=tk.LEFT)
forward_button = tk.Button(button_frame, text="->", command=go_forward, state=tk.DISABLED)
forward_button.pack(side=tk.LEFT)

# Создаем список
listbox = tk.Listbox(root)
listbox.pack(fill='both', expand=True)

# Привязываем обработчик для двойного щелчка
listbox.bind('<Double-1>', on_double_click)

# Заполняем список корневым узлом
path_history.append('/')
current_position += 1
populate_listbox(listbox, '/')

# Запускаем основное приложение
root.mainloop()
