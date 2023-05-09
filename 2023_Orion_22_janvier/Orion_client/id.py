import tkinter as tk

class ScienceTree:
    def __init__(self, parent):
        self.parent = parent
        self.canvas = tk.Canvas(parent, width=1000, height=1000)
        self.canvas.pack()
        self.nodes = []

        # Add root node
        root = ScienceNode(self.canvas, "Science", 300, 50, fill="green")
        self.nodes.append(root)

        # Add first level nodes
        physics = ScienceNode(self.canvas, "Physics", 150, 150)
        self.nodes.append(physics)
        chemistry = ScienceNode(self.canvas, "Chemistry", 300, 150)
        self.nodes.append(chemistry)
        biology = ScienceNode(self.canvas, "Biology", 450, 150)
        self.nodes.append(biology)

        # Add second level nodes
        classical_mechanics = ScienceNode(self.canvas, "Classical Mechanics", 50, 250)
        self.nodes.append(classical_mechanics)
        quantum_mechanics = ScienceNode(self.canvas, "Quantum Mechanics", 150, 250)
        self.nodes.append(quantum_mechanics)
        thermodynamics = ScienceNode(self.canvas, "Thermodynamics", 250, 250)
        self.nodes.append(thermodynamics)
        organic_chemistry = ScienceNode(self.canvas, "Organic Chemistry", 350, 250)
        self.nodes.append(organic_chemistry)
        genetics = ScienceNode(self.canvas, "Genetics", 450, 250)
        self.nodes.append(genetics)
        evolution = ScienceNode(self.canvas, "Evolution", 550, 250)
        self.nodes.append(evolution)

        # Connect nodes with edges
        self.connect_nodes(root, [physics, chemistry, biology])
        self.connect_nodes(physics, [classical_mechanics, quantum_mechanics])
        self.connect_nodes(chemistry, [thermodynamics, organic_chemistry])
        self.connect_nodes(biology, [genetics, evolution])

    def connect_nodes(self, parent, children):
        for child in children:
            self.canvas.create_line(
                parent.x, parent.y + parent.height / 2,
                child.x + child.width, child.y + child.height / 2,
                fill="black"
            )

class ScienceNode:
    def __init__(self, canvas, label, x, y, width=100, height=50, fill="white"):
        self.canvas = canvas
        self.label = label
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.fill = fill

        self.draw()
        self.bind_click()

    def draw(self):
        self.rect = self.canvas.create_rectangle(
            self.x, self.y, self.x + self.width, self.y + self.height,
            fill=self.fill
        )

        self.label_text = self.canvas.create_text(
            self.x + self.width / 2, self.y + self.height / 2,
            text=self.label, fill="black"
        )

    def bind_click(self):
        self.canvas.tag_bind(self.rect, '<Button-1>', self.onClick)

    def onClick(self, event):
        print(f"You clicked on {self.label}")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Science Tree")
    science_tree = ScienceTree(root)
    root.mainloop()