import os
from tkinter import Tk, Label, Button, filedialog, StringVar, messagebox, Canvas, Frame, Scrollbar
from tkinter.ttk import Progressbar
from PIL import Image, ImageDraw, ImageFont


class ImageToGifApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image and GIF Processor")
        self.root.geometry("800x450")  # Increased height to display destination path
        self.images = []
        self.folders = []
        self.save_location = None

        # Set up GUI elements
        Label(root, text="Images and Folders to Process:").pack(pady=5)

        # Scrollable Frame for Items
        self.canvas = Canvas(root)
        self.scrollbar = Scrollbar(root, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")),
        )
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True, padx=10, pady=5)
        self.scrollbar.pack(side="right", fill="y")

        # Buttons for Adding Images, Folders, and Save Destination
        Button(root, text="Add Images", command=self.add_images).pack(pady=5)
        Button(root, text="Add Folders", command=self.add_folders).pack(pady=5)
        Button(root, text="Set Destination", command=self.set_save_location).pack(pady=5)

        # Destination Path Display
        self.destination_label = Label(root, text="Destination: Not Set", anchor="w", fg="blue")
        self.destination_label.pack(fill="x", padx=10, pady=5)

        Button(root, text="Start Processing", command=self.start_processing).pack(pady=10)

        self.progress_label = Label(root, text="")
        self.progress_label.pack(pady=10)

        self.progress_bar = Progressbar(root, orient="horizontal", length=400, mode="indeterminate")
        self.progress_bar.pack(pady=5)

    def add_images(self):
        file_paths = filedialog.askopenfilenames(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        for path in file_paths:
            if path not in self.images:
                self.images.append(path)
                self.add_to_listbox(path, "image")

    def add_folders(self):
        folder_path = filedialog.askdirectory()
        if folder_path and folder_path not in self.folders:
            self.folders.append(folder_path)
            self.add_to_listbox(folder_path, "folder")

    def set_save_location(self):
        location = filedialog.askdirectory()
        if location:
            self.save_location = location
            self.destination_label.config(text=f"Destination: {location}")

    def add_to_listbox(self, path, item_type):
        frame = Frame(self.scrollable_frame)
        frame.pack(fill="x", pady=2)

        Label(frame, text=path, anchor="w").pack(side="left", fill="x", expand=True)
        Button(frame, text="Remove", command=lambda: self.remove_item(frame, path, item_type)).pack(side="right")

    def remove_item(self, frame, path, item_type):
        frame.destroy()
        if item_type == "image":
            self.images.remove(path)
        elif item_type == "folder":
            self.folders.remove(path)

    def start_processing(self):
        if not self.images and not self.folders:
            messagebox.showerror("Error", "Please add at least one image or folder.")
            return

        if not self.save_location:
            messagebox.showerror("Error", "Please set a destination folder.")
            return

        self.progress_label.config(text="Processing...")
        self.progress_bar.start()

        # Process images
        for image_path in self.images:
            self.process_image(image_path)

        # Process images in folders
        for folder_path in self.folders:
            for file_name in os.listdir(folder_path):
                if file_name.lower().endswith((".png", ".jpg", ".jpeg")):
                    self.process_image(os.path.join(folder_path, file_name))

        self.progress_bar.stop()
        self.progress_label.config(text="Processing complete!")
        messagebox.showinfo("Success", "All images processed successfully!")

    def process_image(self, input_path):
        try:
            # Open the image
            img = Image.open(input_path)
            draw = ImageDraw.Draw(img)

            # Define text content
            text = "I FEEL SO SIGMA!!!"

            # Define Impact font path
            font_path = "C:/Windows/Fonts/impact.ttf"
            font_size = 50
            font = ImageFont.truetype(font_path, font_size)

            # Calculate dynamic font size to ensure a 10% buffer on both sides
            img_width = img.width
            buffer = img_width * 0.1
            while draw.textbbox((0, 0), text, font=font)[2] < img_width - (2 * buffer):
                font_size += 1
                font = ImageFont.truetype(font_path, font_size)

            font_size -= 1
            font = ImageFont.truetype(font_path, font_size)

            # Calculate text position (centered and near the top)
            text_bbox = draw.textbbox((0, 0), text, font=font)
            text_width, text_height = text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1]
            position = ((img_width - text_width) // 2, text_height // 2)

            # Add shadow, outline, and main text
            shadow_offset = 2
            outline_width = 5
            shadow_color = "black"
            outline_color = "black"
            text_color = "white"

            for x_offset in range(-outline_width, outline_width + 1):
                for y_offset in range(-outline_width, outline_width + 1):
                    if x_offset != 0 or y_offset != 0:
                        draw.text(
                            (position[0] + x_offset, position[1] + y_offset),
                            text,
                            font=font,
                            fill=outline_color,
                        )

            draw.text(
                (position[0] + shadow_offset, position[1] + shadow_offset),
                text,
                font=font,
                fill=shadow_color,
            )

            draw.text(position, text, font=font, fill=text_color)

            # Save the edited image
            base_name = os.path.basename(input_path)
            name, ext = os.path.splitext(base_name)
            edited_path = os.path.join(self.save_location, f"{name}_edited.png")
            img.save(edited_path)

            # Convert to GIF
            gif_path = os.path.join(self.save_location, f"{name}.gif")
            img.save(gif_path, format="GIF")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to process {input_path}: {str(e)}")


# Run the application
if __name__ == "__main__":
    root = Tk()
    app = ImageToGifApp(root)
    root.mainloop()
