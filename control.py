import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import ctypes
from PIL import Image, ImageTk

class ClassicWin95App:
    def __init__(self, root):
        self.root = root
        self.root.title("Моя Программа")
        self.root.geometry("500x250")

        # Добавляем уголок для изменения размера
        resize_grip = ttk.Sizegrip(root)
        resize_grip.pack(side="right", anchor="se")

        # Установка классической темы
        self.root.configure(bg="lightgray")

        # Меню
        menu_bar = tk.Menu(self.root)
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Открыть")
        file_menu.add_command(label="Сохранить")
        file_menu.add_command(label="Выйти", command=self.root.quit)
        menu_bar.add_cascade(label="Файл", menu=file_menu)

        edit_menu = tk.Menu(menu_bar, tearoff=0)
        edit_menu.add_command(label="Копировать")
        edit_menu.add_command(label="Вставить")
        menu_bar.add_cascade(label="Правка", menu=edit_menu)

        view_menu = tk.Menu(menu_bar, tearoff=0)
        view_menu.add_command(label="Увеличить")
        view_menu.add_command(label="Уменьшить")
        menu_bar.add_cascade(label="Вид", menu=view_menu)

        help_menu = tk.Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="О программе", command=self.show_about)
        menu_bar.add_cascade(label="Помощь", menu=help_menu)

        self.root.config(menu=menu_bar)

        # Верхняя рамка с основной иконкой и текстом
        top_frame = tk.Frame(self.root, bg="lightgray")

        # Основная иконка
        self.main_icon_label = tk.Label(top_frame, bg="lightgray")
        self.main_icon_label.pack(side=tk.LEFT, padx=5)

        self.main_icon = self.load_icon(41)  # Основная иконка (дерево)
        if self.main_icon:
            self.main_icon_label.configure(image=self.main_icon)
            self.main_icon_label.image = self.main_icon

        # Основное содержимое (панель управления)
        content_frame = tk.Frame(self.root, bg="white", relief=tk.SUNKEN, borderwidth=2)
        content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.create_control_panel(content_frame)

    def show_about(self):
        about_window = tk.Toplevel(self.root)
        about_window.title("О программе")
        about_window.geometry("300x200")
        about_window.configure(bg="lightgray")

        icon_label = tk.Label(about_window, bg="lightgray")
        icon_label.pack(pady=10)

        if self.main_icon:
            icon_label.configure(image=self.main_icon)
            icon_label.image = self.main_icon

        tk.Label(about_window, text="Моя Программа\nВерсия 1.0\nКлассический стиль Windows 95.", bg="lightgray").pack(pady=10)
        tk.Button(about_window, text="Закрыть", command=about_window.destroy).pack(pady=10)

    def load_icon(self, icon_index):
        dll_path = r"C:\\Windows\\System32\\shell32.dll"
        hicon = ctypes.windll.shell32.ExtractIconW(0, dll_path, icon_index)

        if hicon:
            hdc = ctypes.windll.user32.GetDC(0)
            hdc_mem = ctypes.windll.gdi32.CreateCompatibleDC(hdc)
            bmp = ctypes.windll.gdi32.CreateCompatibleBitmap(hdc, 32, 32)
            old_bmp = ctypes.windll.gdi32.SelectObject(hdc_mem, bmp)
            ctypes.windll.user32.DrawIconEx(hdc_mem, 0, 0, hicon, 32, 32, 0, 0, 0x0003)
            ctypes.windll.gdi32.SelectObject(hdc_mem, old_bmp)
            ctypes.windll.user32.ReleaseDC(0, hdc)

            # Создаем структуру BITMAPINFOHEADER
            class BITMAPINFOHEADER(ctypes.Structure):
                _fields_ = [
                    ("biSize", ctypes.c_uint32),
                    ("biWidth", ctypes.c_int32),
                    ("biHeight", ctypes.c_int32),
                    ("biPlanes", ctypes.c_uint16),
                    ("biBitCount", ctypes.c_uint16),
                    ("biCompression", ctypes.c_uint32),
                    ("biSizeImage", ctypes.c_uint32),
                    ("biXPelsPerMeter", ctypes.c_int32),
                    ("biYPelsPerMeter", ctypes.c_int32),
                    ("biClrUsed", ctypes.c_uint32),
                    ("biClrImportant", ctypes.c_uint32)
                ]

            bih = BITMAPINFOHEADER()
            bih.biSize = ctypes.sizeof(BITMAPINFOHEADER)
            bih.biWidth = 32
            bih.biHeight = 32
            bih.biPlanes = 1
            bih.biBitCount = 32
            bih.biCompression = 0  # BI_RGB
            bih.biSizeImage = 32 * 32 * 4

            bits = ctypes.create_string_buffer(bih.biSizeImage)
            ctypes.windll.gdi32.GetDIBits(hdc_mem, bmp, 0, 32, bits, bih, 0)

            image = Image.frombuffer('RGBA', (32, 32), bits, 'raw', 'BGRA', 0, 1)
            image = image.transpose(Image.FLIP_TOP_BOTTOM)

            img_path = "icon_temp.bmp"
            image.save(img_path)

            img = Image.open(img_path)
            return ImageTk.PhotoImage(img)

        return None

    def create_control_panel(self, content_frame):
        # Создаем панель управления (несколько иконок и текстов)
        panel_items = [
            ("Параметры", 41),
            ("Администрирование", 41),
            ("Настройки системы", 41),
            ("Обслуживание", 41),
            ("Программы", 41),
            ("Сеть", 41),
            ("Звук и мультимедиа", 41),
            ("Дата и время", 41),
            ("Региональные параметры", 41),
        ]

        self.selected_icon_label = None  # Сохраняем ссылку на выбранную иконку

        row, col = 0, 0
        for text, icon_index in panel_items:
            icon = self.load_icon(icon_index)
            icon_label = tk.Label(content_frame, image=icon, bg="white")
            icon_label.image = icon  # Сохраняем ссылку на изображение

            # Добавляем обработчик нажатий
            icon_label.bind("<Button-1>", lambda event, label=icon_label, text=text: self.on_icon_click(event, label, text))

            icon_label.grid(row=row, column=col, padx=10, pady=10)

            label = tk.Label(content_frame, text=text, bg="white", font=("Arial", 10))
            label.grid(row=row+1, column=col, padx=10)

            col += 1
            if col > 2:  # Убираем на новую строку после 3-х элементов
                col = 0
                row += 2

    def on_icon_click(self, event, label, text):
        # Снимаем выделение с предыдущей иконки, если она была выбрана
        if self.selected_icon_label and self.selected_icon_label != label:
            self.selected_icon_label.configure(bg="white", relief=tk.FLAT)  # Убираем выделение с предыдущей иконки

        # Логика для выделения иконки при первом нажатии и открытия окна при втором
        if label.cget("bg") == "#208c48":
            self.show_about()  # Открыть окно "О программе"
            label.configure(bg="white", relief=tk.FLAT)  # Снимаем выделение
        else:
            label.configure(bg="#208c48", relief=tk.RAISED)  # Выделить иконку зеленым цветом
            if self.selected_icon_label != label:
                self.selected_icon_label = label  # Запоминаем текущую иконку

if __name__ == "__main__":
    root = tk.Tk()
    app = ClassicWin95App(root)
    # Устанавливаем возможность изменения размера окна
    root.resizable(True, True)
    # Запуск основного цикла обработки событий
    root.mainloop()