import tkinter as tk
from itertools import cycle
from pathlib import Path
from PIL import Image, ImageTk
from homepg import Homepage
from loginpage import LoginPage


def launch_homepage():
    root = tk.Tk()
    root.title("Pharmacy managent system")
    root.geometry("1920x1080")
    root.state("zoomed")

    bg_label = tk.Label(root)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    top_bar = tk.Frame(root, bg="navy", height=50)
    top_bar.pack(side="top", fill="x")
    title_label = tk.Label(top_bar, text="Pharmacy managent system", fg="white", bg="navy", font=("Arial", 20, "bold"))
    title_label.pack(pady=5)

    footer = tk.Frame(root, bg="gray", height=40)
    footer.pack(side="bottom", fill="x")
    footer_label = tk.Label(footer, text="© 2026 pharmacy  managent system. All rights reserved.", bg="gray", fg="white")
    footer_label.pack(pady=5)

    container = tk.Frame(root, bg="white", width=500, height=400)
    container.place(relx=0.5, rely=0.5, anchor="center")
    container.pack_propagate(False)
    container.grid_propagate(False)
    container.grid_rowconfigure(0, weight=1)
    container.grid_columnconfigure(0, weight=1)
    frames = {}

    for page in (Homepage, LoginPage):
        page_name = page.__name__
        frame = page(container, controller=root)
        frames[page_name] = frame
        frame.grid(row=0, column=0, sticky="nsew")

    def show_frame(page_name):
        frames[page_name].tkraise()

    root.show_frame = show_frame
    show_frame("Homepage")

    bg_images = ["bg1.jpg", "bg.jpg"]
    base_path = Path(__file__).resolve().parent
    loaded_images = []

    for img_name in bg_images:
        img_path = base_path / img_name
        if img_path.exists():
            loaded_images.append(Image.open(img_path))

    if loaded_images:
        bg_cycle = cycle(loaded_images)
        current_img = loaded_images[0]
        fade_steps = 20
        fade_delay = 50

        def fade_to_next(step=0, next_img=None):
            nonlocal_current = fade_to_next.current_image
            w, h = max(root.winfo_width(), 1), max(root.winfo_height(), 1)
            if next_img is None:
                next_img = next(bg_cycle)
            alpha = step / fade_steps
            blended = Image.blend(
                nonlocal_current.resize((w, h), Image.Resampling.LANCZOS),
                next_img.resize((w, h), Image.Resampling.LANCZOS),
                alpha,
            )
            photo = ImageTk.PhotoImage(blended)
            bg_label.config(image=photo)
            bg_label.image = photo

            if step < fade_steps:
                root.after(fade_delay, fade_to_next, step + 1, next_img)
            else:
                fade_to_next.current_image = next_img
                root.after(2000, fade_to_next)

        fade_to_next.current_image = current_img
        fade_to_next()
    else:
        bg_label.config(bg="#f0f4ff")

    root.mainloop()


if __name__ == "__main__":
    launch_homepage()
