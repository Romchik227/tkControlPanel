import tkinter as tk

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

        self.draw_network(nodes, connections)

    def draw_network(self, nodes, connections):
        node_radius = 20

        for node, (x, y) in nodes.items():
            self.canvas.create_oval(x - node_radius, y - node_radius, x + node_radius, y + node_radius, fill="lightblue")
            self.canvas.create_text(x, y, text=node, font=("Arial", 12, "bold"))

        for node1, node2 in connections:
            if node1 in nodes and node2 in nodes:
                x1, y1 = nodes[node1]
                x2, y2 = nodes[node2]
                self.canvas.create_line(x1, y1, x2, y2)
            else:
                print(f"One of the nodes {node1} or {node2} does not exist.")
                # Or add logging:
                # logging.error(f"One of the nodes {node1} or {node2} does not exist.")

if __name__ == "__main__":
    root = tk.Tk()
    app = NetworkMapApp(root)
    root.mainloop()
