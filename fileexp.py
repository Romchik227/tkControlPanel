import tkinter as tk
from tkinter import ttk
import os

# Глобальная переменная для хранения истории путей
path_history = []

# Функция для заполнения дерева файлов и папок
def populate_tree(tree, parent, path):
    for p in os.listdir(path):
        abs_path = os.path.join(path, p)
        isdir = os.path.isdir(abs_path)
        oid = tree.insert(parent, 'end', text=p, open=False, values=[abs_path, 'directory' if isdir else 'file'])
        if isdir:
            tree.insert(oid, 'end')

# Функция для обработки раскрытия узла
def on_open(event):
    global path_history
    tree = event.widget
    node = tree.focus()
    if tree.set(node, "type") == "directory":
        # Очистить временные узлы
        if tree.get_children(node):
            tree.delete(*tree.get_children(node))
        # Добавить настоящие узлы
        path = tree.set(node, "fullpath")
        path_history.append(path)
        populate_tree(tree, node, path)

# Функция для возврата назад
def go_back():
    global path_history
    if len(path_history) > 1:
        # Удаляем текущий путь из истории
        path_history.pop()
        # Получаем предыдущий путь
        previous_path = path_history.pop()
        # Очищаем дерево
        for item in tree.get_children():
            tree.delete(item)
        # Заполняем дерево предыдущим путем
        root_node = tree.insert('', 'end', text=previous_path, open=True, values=[previous_path, 'directory'])
        populate_tree(tree, root_node, previous_path)
        path_history.append(previous_path)

# Создаем основное окно
root = tk.Tk()
root.title("Файловый проводник")

# Создаем дерево
tree = ttk.Treeview(root, columns=("fullpath", "type"), displaycolumns="")

# Создаем корневой узел
root_node = tree.insert('', 'end', text='/', open=True, values=['/', 'directory'])
populate_tree(tree, root_node, '/')

# Привязываем обработчик для раскрытия узла
tree.bind('<<TreeviewOpen>>', on_open)

# Создаем кнопку "Назад"
back_button = tk.Button(root, text="Назад", command=go_back)
back_button.pack()

# Размещаем дерево на окне
tree.pack(fill='both', expand=True)

# Запускаем основное приложение
root.mainloop()
