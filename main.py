from tkinter import *
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageDraw, ImageFont

class App(Tk):
    def __init__(self):
        super().__init__()
        self.title("WaterMarker")
        self.config(padx=20, pady=20)
        self.max_image_size = {"width": 1024, "height": 768}
        self.filetypes = [("Image Files", "*.tif *.jpg *.png *.JPG ")]
        # Canvas
        self.canvas = Canvas(width=self.max_image_size["width"], height=self.max_image_size["height"])
        self.upload_icon = ImageTk.PhotoImage(Image.open("placeholder.jfif"))
        self.image_container = self.canvas.create_image(self.max_image_size["width"] / 2, self.max_image_size["height"]
                                                        / 2, image=self.upload_icon)
        self.canvas.grid(column=0, row=8, columnspan=2)
        # Button
        self.upload_button = Button(text="Upload your image", command=self.watermark)
        self.upload_button.grid(column=0, row=4, columnspan=2)
        # Watermark Labels and Entries
        self.watermark_label = Label(text="Configure Your Watermark:", font=24)
        self.watermark_label.grid(column=0, row=0, columnspan=2)

        self.watermark_entry_label = Label(text="Watermark Text:")
        self.watermark_entry_label.grid(column=0, row=1, sticky="e")

        self.watermark_entry = Entry(width=30)
        self.watermark_entry.grid(column=1, row=1, sticky="w")

        self.watermark_loc = Label(text="Location in X, Y:")
        self.watermark_loc.grid(column=0, row=2, sticky="e")

        self.watermark_loc_entry = Entry(width=10)
        self.watermark_loc_entry.grid(column=1, row=2, sticky="w")

        self.watermark_size_label = Label(text="Font Size:")
        self.watermark_size_label.grid(column=0, row=3, sticky="e")

        self.watermark_size_entry = Entry(width=10)
        self.watermark_size_entry.grid(column=1, row=3, sticky="w")

    def open_file(self):
        filename = filedialog.askopenfilename(initialdir="/", title="Select A File", filetypes=self.filetypes)
        return filename

    def watermark(self):
        # File select and resize file to fit the canvas
        file = self.open_file()
        image = Image.open(file)
        aspect_ratio = image.width / image.height
        new_height = self.max_image_size["height"]
        new_width = int(self.max_image_size["height"] * aspect_ratio)
        resized_image = image.resize((new_width, new_height), Image.ANTIALIAS)
        upload_image = ImageTk.PhotoImage(resized_image)
        self.canvas.itemconfig(self.image_container, image=upload_image)
        self.canvas.image = upload_image
        # Apply watermark
        if upload_image:
            edit_image = resized_image
            drawing = ImageDraw.Draw(edit_image)
            text = self.watermark_entry.get()
            position = eval(self.watermark_loc_entry.get())
            font = ImageFont.truetype("C:\WINDOWS\FONTS\CALIBRI.TTF", size=int(self.watermark_size_entry.get()))
            drawing.text(xy=position, text=text, font=font)
            watermarked_image = ImageTk.PhotoImage(edit_image)
            self.canvas.itemconfig(self.image_container, image=watermarked_image)
            self.canvas.image = watermarked_image
        # Save file
            if watermarked_image:
                save_file = messagebox.askyesno(title="Save?", message="Would you like to save your new image?")
                if save_file:
                    save_filename = filedialog.asksaveasfilename(title="Save Your Image", filetypes=self.filetypes)
                    if save_filename:
                        edit_image.save(save_filename)
                        run_again = messagebox.askyesno(title="Run Again?", message="File saved! Would you like to "
                                                                                    "watermark another image?")
                        if not run_again:
                            App.quit(self)
                        else:
                            self.watermark_entry.delete(0, END)
                            self.watermark_loc_entry.delete(0, END)
                            self.watermark_size_entry.delete(0, END)
                            self.watermark_entry.focus()
                            self.canvas.itemconfig(self.image_container, image=self.upload_icon)

app = App()

app.mainloop()
