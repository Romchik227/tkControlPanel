import tkinter as tk
import ctypes
from PIL import Image, ImageTk

class NetworkMapApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Network Map")

        self.canvas = tk.Canvas(self.root, bg="white", width=800, height=600)
        self.canvas.pack()

        nodes = {
            "Node1": (100, 100),
            "Node2": (300, 100),
            "Node3": (200, 300),
            "Node4": (500, 400)
        }

        connections = [
            ("Node1", "Node2"),
            ("Node2", "Node3"),
            ("Node3", "Node4"),
            ("Node1", "Node3")
        ]

        self.icon_size = 32  # Default icon size
        node_icon_map = {
            "Node1": 2,  # Assign icon index 2 to Node1
            "Node2": 3,  # Assign icon index 3 to Node2
            "Node3": 4,  # Assign icon index 4 to Node3
            "Node4": 8   # Assign icon index 5 to Node4
        }
        self.icons = {node: self.load_icon(icon_index, self.icon_size) for node, icon_index in node_icon_map.items()}

        self.create_menu()
        self.draw_network(nodes, connections)

    def create_menu(self):
        menu_bar = tk.Menu(self.root)
        view_menu = tk.Menu(menu_bar, tearoff=0)
        view_menu.add_command(label="Стандартный", command=lambda: self.set_icon_size(32))
        view_menu.add_command(label="Большой", command=lambda: self.set_icon_size(48))
        view_menu.add_command(label="Маленький", command=lambda: self.set_icon_size(24))
        menu_bar.add_cascade(label="Вид", menu=view_menu)
        self.root.config(menu=menu_bar)

    def set_icon_size(self, size):
        self.icon_size = size
        node_icon_map = {
            "Node1": 2,
            "Node2": 3,
            "Node3": 4,
            "Node4": 8
        }
        self.icons = {node: self.load_icon(icon_index, size) for node, icon_index in node_icon_map.items()}
        self.canvas.delete("all")
        nodes = {
            "Node1": (100, 100),
            "Node2": (300, 100),
            "Node3": (200, 300),
            "Node4": (500, 400)
        }
        connections = [
            ("Node1", "Node2"),
            ("Node2", "Node3"),
            ("Node3", "Node4"),
            ("Node1", "Node3")
        ]
        self.draw_network(nodes, connections)

    def load_icon(self, icon_index, size=32):
        try:
            dll_path = r"C:\\Windows\\System32\\netcenter.dll"
            hicon = ctypes.windll.shell32.ExtractIconW(0, dll_path, icon_index)
            if hicon:
                hdc = ctypes.windll.user32.GetDC(0)
                hdc_mem = ctypes.windll.gdi32.CreateCompatibleDC(hdc)
                bmp = ctypes.windll.gdi32.CreateCompatibleBitmap(hdc, size, size)
                old_bmp = ctypes.windll.gdi32.SelectObject(hdc_mem, bmp)

                ctypes.windll.user32.DrawIconEx(hdc_mem, 0, 0, hicon, size, size, 0, 0, 0x0003)
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
                bih.biWidth = size
                bih.biHeight = size
                bih.biPlanes = 1
                bih.biBitCount = 32
                bih.biCompression = 0  # BI_RGB
                bih.biSizeImage = size * size * 4

                bits = ctypes.create_string_buffer(bih.biSizeImage)
                ctypes.windll.gdi32.GetDIBits(hdc_mem, bmp, 0, size, bits, bih, 0)
                byte_data = bytes(bits)
                image = Image.frombytes('RGBA', (size, size), byte_data, 'raw', 'BGRA', 0, 1)
                image = image.transpose(Image.FLIP_TOP_BOTTOM)
                return ImageTk.PhotoImage(image)
        except Exception as e:
            print(f"Не удалось загрузить иконку: {e}")
        return None

    def draw_network(self, nodes, connections):
        node_radius = 20

        for node, (x, y) in nodes.items():
            icon = self.icons.get(node)
            if icon:
                self.canvas.create_image(x, y, image=icon)
                self.canvas.image = icon  # Keep a reference to the icon to prevent garbage collection
            else:
                self.canvas.create_oval(x - node_radius, y - node_radius, x + node_radius, y + node_radius, fill="lightblue")
            self.canvas.create_text(x, y, text=node, font=("Arial", 12, "bold"))

        for node1, node2 in connections:
            if node1 in nodes and node2 in nodes:
                x1, y1 = nodes[node1]
                x2, y2 = nodes[node2]
                self.canvas.create_line(x1, y1, x2, y2)
            else:
                print(f"One of the nodes {node1} or {node2} does not exist.")

if __name__ == "__main__":
    root = tk.Tk()
    app = NetworkMapApp(root)
    root.mainloop()
