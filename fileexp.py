import tkinter as tk
from tkinter import ttk
import os

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
    tree = event.widget
    node = tree.focus()
    if tree.set(node, "type") == "directory":
        # Очистить временные узлы
        if tree.get_children(node):
            tree.delete(*tree.get_children(node))
        # Добавить настоящие узлы
        path = tree.set(node, "fullpath")
        populate_tree(tree, node, path)

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

# Размещаем дерево на окне
tree.pack(fill='both', expand=True)

# Запускаем основное приложение
root.mainloop()