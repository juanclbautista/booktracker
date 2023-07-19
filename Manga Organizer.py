import tkinter as tk
from tkinter import messagebox
from tkinter import PhotoImage
from PIL import Image, ImageTk
import json

def create_app():
    app = tk.Tk()
    app.title("Book Organizer")
    load_data()
    app.protocol("WM_DELETE_WINDOW", on_close)
    return app

def on_close():
    save_data()
    app.destroy()

def get_entry_values():
    book_title = entry_title.get()
    author = entry_author.get()
    publisher = entry_publisher.get()
    add_book(book_title, author, publisher)

def add_book(book_title, author, publisher):
    if not book_title or not author or not publisher:
        # Display an error message if any of the fields are empty
        messagebox.showerror("Error", "Please provide all the required information (Title, Author, Publisher).")
        return

    # Disconnect the event binding temporarily to avoid duplicates
    listbox.unbind("<<ListboxSelect>>")
    book_titles.append(f"{book_title} (Author: {author}, Publisher: {publisher})")
    update_listbox()
    entry_title.delete(0, tk.END)
    entry_author.delete(0, tk.END)
    entry_publisher.delete(0, tk.END)
    # Reconnect the event binding after updating the listbox
    listbox.bind("<<ListboxSelect>>", on_select)




def remove_book():
    selected_index = listbox.curselection()
    if selected_index:
        confirmation = messagebox.askyesno("Confirmation", "Are you sure you want to remove this book title?")
        if confirmation:
            book_titles.pop(selected_index[0])
            update_listbox()

def save_data():
    with open("book_titles.json", "w") as file:
        json.dump(book_titles, file)

def load_data():
    try:
        with open("book_titles.json", "r") as file:
            loaded_titles = json.load(file)
            decoded_titles = [title.encode().decode("unicode_escape") for title in loaded_titles]
            book_titles.clear()
            book_titles.extend(decoded_titles)
    except FileNotFoundError:
        pass

def update_listbox():
    listbox.delete(0, tk.END)
    for title in book_titles:
        listbox.insert(tk.END, title)
    details_label.config(text="")

def resize_image(image_path, width, height):
    image = Image.open(image_path)
    resized_image = image.resize((width, height), Image.LANCZOS)
    return ImageTk.PhotoImage(resized_image)

def on_select(event):
    selected_index = listbox.curselection()
    if selected_index:
        selected_title = book_titles[selected_index[0]]
        details_label.config(text=selected_title)

def sort_titles():
    book_titles.sort()
    update_listbox()

def search_titles():
    search_term = search_entry.get().strip()
    if search_term:
        matching_titles = [title for title in book_titles if search_term.lower() in title.lower()]
        update_listbox_with_search_results(matching_titles)
    else:
        update_listbox()

def update_listbox_with_search_results(results):
    listbox.delete(0, tk.END)
    for title in results:
        listbox.insert(tk.END, title)
    details_label.config(text="")

def setup_gui(app):
    global entry_title, entry_author, entry_publisher  # Declare them as global variables

    input_frame = tk.Frame(app, padx=10, pady=5, relief=tk.RAISED, borderwidth=1)
    input_frame.pack()

    title_label = tk.Label(input_frame, text="Title:")
    title_label.grid(row=0, column=0, padx=5, pady=5)
    entry_title = tk.Entry(input_frame)
    entry_title.grid(row=0, column=1, padx=5, pady=5)

    entry_author = tk.Entry(input_frame)
    entry_author.grid(row=1, column=1, padx=5, pady=5)

    entry_publisher = tk.Entry(input_frame)
    entry_publisher.grid(row=2, column=1, padx=5, pady=5)

    add_button = tk.Button(input_frame, text="Add Book", command=get_entry_values)

    add_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

    sort_button = tk.Button(input_frame, text="Sort Titles", command=sort_titles)
    sort_button.grid(row=3, column=2, padx=5, pady=5)

    search_label = tk.Label(input_frame, text="Search:")
    search_label.grid(row=4, column=0, padx=5, pady=5)
    search_entry = tk.Entry(input_frame)
    search_entry.grid(row=4, column=1, padx=5, pady=5)

    search_button = tk.Button(input_frame, text="Search Titles", command=search_titles)
    search_button.grid(row=4, column=2, padx=5, pady=5)

    list_frame = tk.Frame(app, padx=10, pady=5, relief=tk.RAISED, borderwidth=1)
    list_frame.pack()

    listbox = tk.Listbox(list_frame)
    listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    details_label = tk.Label(list_frame, text="", wraplength=300)
    details_label.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    listbox.bind("<<ListboxSelect>>", on_select)

    return listbox, list_frame, details_label



if __name__ == "__main__":
    book_titles = []
    app = create_app()
    listbox, list_frame, details_label = setup_gui(app)
    load_data()
    app.mainloop()
