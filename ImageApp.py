import tkinter as tk
from tkinterdnd2 import TkinterDnD, DND_FILES
from tkinter import filedialog, Scrollbar
from PIL import Image, ImageTk, ImageOps

class ImageApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Viewer")
        self.root.geometry("800x600")  # Збільшили розміри вікна

        # Конфігурація сітки
        self.root.grid_rowconfigure(1, weight=1)  # Дозволяємо canvas розтягуватись
        self.root.grid_columnconfigure(0, weight=1)

        # Створюємо велике поле для перетягування або вибору файлу
        self.drop_area = tk.Label(root, text="Перетягніть файл сюди або натисніть", 
                                  width=40, height=10, bg="lightgray", relief="groove")
        self.drop_area.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        # Додаємо події на клік і перетягування
        self.drop_area.bind("<Button-1>", self.open_file_dialog)

        # Вмикаємо підтримку перетягування файлів
        root.drop_target_register(DND_FILES)
        root.dnd_bind('<<Drop>>', self.drop_file)

        # Додаємо підтримку скролінгу
        self.canvas_frame = tk.Frame(root)
        self.canvas_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        self.scrollbar_y = Scrollbar(self.canvas_frame, orient=tk.VERTICAL)
        self.scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)

        self.scrollbar_x = Scrollbar(self.canvas_frame, orient=tk.HORIZONTAL)
        self.scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)

        self.canvas = tk.Canvas(self.canvas_frame, yscrollcommand=self.scrollbar_y.set, xscrollcommand=self.scrollbar_x.set)
        self.canvas.pack(expand=True, fill=tk.BOTH)

        self.scrollbar_y.config(command=self.canvas.yview)
        self.scrollbar_x.config(command=self.canvas.xview)

        self.image = None
        self.tk_image = None

    def open_file_dialog(self, event=None):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif")]
        )
        if file_path:
            self.load_image(file_path)

    def drop_file(self, event):
        file_path = event.data.strip('{}')  # видаляємо дужки в імені файлу
        self.load_image(file_path)

    def load_image(self, file_path):
        try:
            self.image = Image.open(file_path)
            self.image = self.resize_image_to_fit(self.image)  # Зменшуємо зображення для відображення
            self.display_image()
            self.drop_area.config(text="Перетягніть файл сюди або натисніть", bg="lightgray")
        except Exception as e:
            print(f"Не вдалося завантажити зображення: {e}")

    def display_image(self):
        # Масштабуємо canvas під розміри зображення і центруємо його
        self.canvas.delete("all")
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        # Центруємо зображення на canvas
        x_offset = (canvas_width - self.image.width) // 2
        y_offset = (canvas_height - self.image.height) // 2

        self.tk_image = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(x_offset, y_offset, anchor=tk.NW, image=self.tk_image)

        # Додаємо подію для кліку на зображення
        self.canvas.bind("<Button-1>", self.invert_colors)
        self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))

    def resize_image_to_fit(self, image):
        max_width, max_height = 800, 600  # Максимальні розміри для зображення
        width, height = image.size  # Поточний розмір зображення

        # Обчислюємо масштабування
        scale = min(max_width / width, max_height / height)

        # Перевірка, що розміри більше за нуль
        if scale <= 0:
            scale = 1  # Не дозволяємо масштабуванню бути меншим або рівним 0

        # Новий розмір
        new_size = (int(width * scale), int(height * scale))

        # Переконайтеся, що новий розмір більше за нуль
        if new_size[0] > 0 and new_size[1] > 0:
            return image.resize(new_size, Image.Resampling.LANCZOS)
        else:
            raise ValueError("Invalid size computed for image resizing.")


    def invert_colors(self, event):
        if self.image:
            self.image = ImageOps.invert(self.image.convert("RGB"))
            self.display_image()

if __name__ == "__main__":
    root = TkinterDnD.Tk()  # Використовуємо TkinterDnD для підтримки перетягування файлів
    app = ImageApp(root)
    root.mainloop()
