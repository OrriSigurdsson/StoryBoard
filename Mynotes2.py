
import tkinter as tk
from tkinter import ttk, colorchooser
import json

GRID_SIZE = 20



DEFAULT_TAG_COLORS = {
    "Scene": "#fff59d",
    "Character": "#90caf9",
    "Twist": "#f48fb1",
    "World": "#a5d6a7"
}

class Note:
    def __init__(self, app, x, y, data=None):
        self.app = app
        self.canvas = app.canvas

        self.width = 220
        self.height = 160

        if data:
            self.title = data["title"]
            self.bullets = data["bullets"]
            self.tag = data["tag"]
            self.color = data["color"]
        else:
            self.title = "New Note"
            self.bullets = []
            self.tag = "Scene"
            self.color = DEFAULT_TAG_COLORS[self.tag]

        self.rect = self.canvas.create_rectangle(
            x, y, x+self.width, y+self.height,
            fill=self.color,
            outline="black"
        )

        self.text = self.canvas.create_text(
            x+10, y+10,
            anchor="nw",
            width=self.width-20,
            text=self.format_text(),
            font=("Arial", 10)
        )

        self.bind_events()

    def format_text(self):
        content = self.title + "\n\n"
        for bullet in self.bullets:
            content += "• " + bullet + "\n"

        content += f"\n[{self.tag}]"
        content += f"\nWords: {self.word_count()}"

        return content

    def word_count(self):
        text = self.title + " " + " ".join(self.bullets)
        return len(text.split())

    def bind_events(self):
        for item in (self.rect, self.text):
            self.canvas.tag_bind(item, "<Button-1>", self.start_drag)
            self.canvas.tag_bind(item, "<B1-Motion>", self.drag)
            self.canvas.tag_bind(item, "<ButtonRelease-1>", self.snap)
            self.canvas.tag_bind(item, "<Button-3>", self.edit_note)

        self.drag_data = {"x": 0, "y": 0}

    def start_drag(self, event):
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y

    def drag(self, event):
        dx = event.x - self.drag_data["x"]
        dy = event.y - self.drag_data["y"]

        self.canvas.move(self.rect, dx, dy)
        self.canvas.move(self.text, dx, dy)

        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y

    def snap(self, event):
        x1, y1, x2, y2 = self.canvas.coords(self.rect)
        x = round(x1 / GRID_SIZE) * GRID_SIZE
        y = round(y1 / GRID_SIZE) * GRID_SIZE

        dx = x - x1
        dy = y - y1

        self.canvas.move(self.rect, dx, dy)
        self.canvas.move(self.text, dx, dy)

    def edit_note(self, event=None):
        EditDialog(self)

    def update_visual(self):
        self.canvas.itemconfig(self.rect, fill=self.color)
        self.canvas.itemconfig(self.text, text=self.format_text())

    def get_data(self):
        x1, y1, x2, y2 = self.canvas.coords(self.rect)
        return {
            "x": x1,
            "y": y1,
            "title": self.title,
            "bullets": self.bullets,
            "tag": self.tag,
            "color": self.color
        }


class EditDialog:
    def __init__(self, note):
        self.note = note
        self.top = tk.Toplevel()
        self.top.title("Edit Note")

        self.custom_color = False  # Track manual color selection

        tk.Label(self.top, text="Title").pack()
        self.title_entry = tk.Entry(self.top, width=40)
        self.title_entry.pack()
        self.title_entry.insert(0, note.title)

        tk.Label(self.top, text="Bullets (max 10)").pack()

        self.bullet_entries = []
        for i in range(10):
            entry = tk.Entry(self.top, width=40)
            entry.pack(pady=1)
            if i < len(note.bullets):
                entry.insert(0, note.bullets[i])
            self.bullet_entries.append(entry)

        tk.Label(self.top, text="Tag").pack()
        self.tag_var = tk.StringVar(value=note.tag)

        tag_menu = ttk.Combobox(
            self.top,
            textvariable=self.tag_var,
            values=list(DEFAULT_TAG_COLORS.keys()),
            state="readonly"
        )
        tag_menu.pack()

        tk.Button(self.top, text="Pick Color", command=self.pick_color).pack(pady=5)

        tk.Button(self.top, text="Save", command=self.save).pack(pady=10)

    def pick_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.note.color = color
            self.custom_color = True
            self.note.update_visual()  # live preview

    def save(self):
        self.note.title = self.title_entry.get()
        self.note.bullets = [
            e.get() for e in self.bullet_entries if e.get().strip()
        ]

        new_tag = self.tag_var.get()
        self.note.tag = new_tag

        # Only apply tag default color if user didn't manually pick one
        if not self.custom_color:
            self.note.color = DEFAULT_TAG_COLORS[new_tag]

        self.note.update_visual()
        self.top.destroy()



class WhiteboardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Story Whiteboard")

        self.zoom_scale = 1.0
        
        self.notes = []

        self.canvas = tk.Canvas(root, bg="white")
        self.canvas.pack(fill="both", expand=True)

        self.canvas.bind("<Control-MouseWheel>", self.mouse_zoom)
        self.canvas.bind("<Control-Button-4>", self.mouse_zoom)
        self.canvas.bind("<Control-Button-5>", self.mouse_zoom)


        self.canvas.configure(scrollregion=(0, 0, 5000, 5000))

        self.hbar = tk.Scrollbar(root, orient="horizontal", command=self.canvas.xview)
        self.hbar.pack(fill="x", side="bottom")

        self.vbar = tk.Scrollbar(root, orient="vertical", command=self.canvas.yview)
        self.vbar.pack(fill="y", side="right")

        self.canvas.configure(xscrollcommand=self.hbar.set,
                              yscrollcommand=self.vbar.set)

        self.canvas.bind("<Double-1>", self.create_note)

        toolbar = tk.Frame(root)
        toolbar.pack(fill="x")

        tk.Button(toolbar, text="Save", command=self.save).pack(side="left")
        tk.Button(toolbar, text="Load", command=self.load).pack(side="left")
        tk.Label(toolbar, text="Zoom").pack(side="left", padx=10)

        self.zoom_slider = tk.Scale(
            toolbar,
            from_=50,
            to=200,
            orient="horizontal",
            command=self.slider_zoom
        )
        self.zoom_slider.set(100)
        self.zoom_slider.pack(side="left")


    def slider_zoom(self, value):
        value = float(value) / 100
        factor = value / self.zoom_scale
        self.zoom(factor)

    def zoom(self, factor, center=None):
        self.zoom_scale *= factor

        if center:
            x, y = center
        else:
            x, y = 0, 0

        self.canvas.scale("all", x, y, factor, factor)
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))


    def mouse_zoom(self, event):
        # Windows / Mac
        if event.delta:
            if event.delta > 0:
                factor = 1.1
            else:
                factor = 0.9
        else:
            # Linux support
            if event.num == 4:
                factor = 1.1
            elif event.num == 5:
                factor = 0.9
            else:
                return

        self.zoom(factor, (event.x, event.y))

        self.zoom(factor)

        # Update slider
        self.zoom_slider.set(int(self.zoom_scale * 100))



    def create_note(self, event):
        note = Note(self, event.x, event.y)
        self.notes.append(note)

    def save(self):
        data = [note.get_data() for note in self.notes]
        with open("board.json", "w") as f:
            json.dump(data, f)

    def load(self):
        with open("board.json", "r") as f:
            data = json.load(f)

        for note in self.notes:
            self.canvas.delete(note.rect)
            self.canvas.delete(note.text)

        self.notes.clear()

        for note_data in data:
            note = Note(self, note_data["x"], note_data["y"], note_data)
            self.notes.append(note)


root = tk.Tk()
root.geometry("1200x800")
app = WhiteboardApp(root)
root.mainloop()

