import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import ctypes
from PIL import Image, ImageTk

class ClassicWinNTApp:
    def __init__(self, root):
        """
        Инициализирует приложение, устанавливает параметры окна и создает элементы интерфейса.

        :param root: Основное окно tkinter.
        """
        self.root = root
        self.root.title("Программа")
        self.root.geometry("500x250")

        # Добавляем уголок для изменения размера
        resize_grip = ttk.Sizegrip(root)
        resize_grip.pack(side="right", anchor="se")

        # Установка классической темы
        self.root.configure(bg="lightgray")

        # Меню
        self.create_menu()

        # Верхняя рамка с основной иконкой и текстом
        self.create_top_frame()

        # Основное содержимое (панель управления)
        self.create_content_frame()

    def create_menu(self):
        """
        Создает меню приложения.
        """
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
        menu_bar.add_cascade(label="Справка", menu=help_menu)

        self.root.config(menu=menu_bar)

    def create_top_frame(self):
        """
        Создает верхнюю рамку с основной иконкой и текстом.
        """
        top_frame = tk.Frame(self.root, bg="lightgray")
        top_frame.pack(side=tk.TOP, fill=tk.X)

        # Основная иконка
        self.main_icon_label = tk.Label(top_frame, bg="lightgray")
        self.main_icon_label.pack(side=tk.LEFT, padx=5)

        # Загружаем иконку для главной панели
        self.main_icon = self.load_icon(8)  # Основная иконка
        if self.main_icon:
            self.main_icon_label.configure(image=self.main_icon)
            self.main_icon_label.image = self.main_icon

    def create_content_frame(self):
        """
        Создает основное содержимое (панель управления).
        """
        content_frame = tk.Frame(self.root, bg="white", relief=tk.SUNKEN, borderwidth=2)
        content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.create_control_panel(content_frame)

    def show_about(self):
        """
        Показывает окно "О программе".
        """
        about_window = tk.Toplevel(self.root)
        about_window.title("О программе")
        about_window.geometry("300x200")
        about_window.configure(bg="lightgray")

        icon_label = tk.Label(about_window, bg="lightgray")
        icon_label.pack(pady=10)

        if self.main_icon:
            icon_label.configure(image=self.main_icon)
            icon_label.image = self.main_icon

        tk.Label(about_window, text="Программа\nВерсия 1.4-tc\nКлассический стиль Windows NT.", bg="lightgray").pack(pady=10)
        tk.Button(about_window, text="Закрыть", command=about_window.destroy).pack(pady=10)

    def load_icon(self, icon_index):
        """
        Загружает иконку из библиотеки .dll по индексу и возвращает ее в формате Tkinter.

        :param icon_index: Индекс иконки в библиотеке .dll.
        :return: Изображение в формате Tkinter или None, если загрузка не удалась.
        """
        try:
            dll_path = r"C:\\Windows\\System32\\netcenter.dll"
            hicon = ctypes.windll.shell32.ExtractIconW(0, dll_path, icon_index)
            if hicon:
                hdc = ctypes.windll.user32.GetDC(0)
                hdc_mem = ctypes.windll.gdi32.CreateCompatibleDC(hdc)
                bmp = ctypes.windll.gdi32.CreateCompatibleBitmap(hdc, 32, 32)
                old_bmp = ctypes.windll.gdi32.SelectObject(hdc_mem, bmp)

                ctypes.windll.user32.DrawIconEx(hdc_mem, 0, 0, hicon, 32, 32, 0, 0, 0x0003)
                ctypes.windll.gdi32.SelectObject(hdc_mem, old_bmp)
                ctypes.windll.user32.ReleaseDC(0, hdc)

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
                byte_data = bytes(bits)
                image = Image.frombytes('RGBA', (32, 32), byte_data, 'raw', 'BGRA', 0, 1)
                image = image.transpose(Image.FLIP_TOP_BOTTOM)
                return ImageTk.PhotoImage(image)
        except Exception as e:
            messagebox.showerror("Ошибка загрузки иконки", f"Не удалось загрузить иконку: {e}")
        return None

    def create_control_panel(self, content_frame):
        """
        Создает панель управления с иконками и текстом.

        :param content_frame: Родительский фрейм для панели управления.
        """
        panel_items = [
            ("Параметры", 1),
            ("Администрирование", 2),
            ("Настройки системы", 3),
            ("Обслуживание", 4),
            ("Программы", 5),
            ("Сеть", 6),
            ("Звук и мультимедиа", 7),
            ("Дата и время", 8),
            ("Региональные параметры", 9),
        ]

        self.selected_icon_label = None

        row, col = 0, 0
        for text, icon_index in panel_items:
            icon = self.load_icon(icon_index)
            if icon:
                icon_label = tk.Label(content_frame, image=icon, bg="white")
                icon_label.image = icon
                icon_label.bind("<Button-1>", lambda event, label=icon_label, text=text: self.on_icon_click(event, label, text))
                icon_label.grid(row=row, column=col, padx=10, pady=10)

                label = tk.Label(content_frame, text=text, bg="white", font=("Arial", 10))
                label.grid(row=row+1, column=col, padx=10)

                col += 1
                if col > 2:
                    col = 0
                    row += 2

    def on_icon_click(self, event, label, text):
        """
        Обработчик нажатий на иконки в панели управления.

        :param event: Событие нажатия.
        :param label: Нажатая иконка.
        :param text: Текст, связанный с иконкой.
        """
        if self.selected_icon_label and self.selected_icon_label != label:
            self.selected_icon_label.configure(bg="white", relief=tk.FLAT)

        if label.cget("bg") == "#208c48":
            self.show_about()
            label.configure(bg="white", relief=tk.FLAT)
        else:
            label.configure(bg="#208c48", relief=tk.RAISED)
            if self.selected_icon_label != label:
                self.selected_icon_label = label

if __name__ == "__main__":
    root = tk.Tk()
    app = ClassicWinNTApp(root)
    root.resizable(True, True)
    root.mainloop()
