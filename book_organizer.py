import tkinter as tk
import json
import csv
import sys
from tkinter import messagebox
from tkinter import filedialog


def create_app():
    app = tk.Tk()
    app.title("Book Organizer")
    load_data()
    app.protocol("WM_DELETE_WINDOW", on_close)

    # Keyboard shortcuts added
    app.bind("<Control-a>", lambda event: get_entry_values())
    app.bind("<Control-r>", lambda event: remove_book())

    return app

def export_to_csv():
    # Ask the user to choose a file name for the CSV File
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])

    # If the user cancels the file dialog, return
    if not file_path:
        return
    
    # Write the book list to the CSV file
    try:
        with open(file_path, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            for book in book_titles:
                writer.writerow([book])
        
        messagebox.showinfo("Export Success", "Book list exported to CSV File.")
    except Exception as e:
        messagebox.showerror("Export Error", f"An error occurred while exporting to CSV: {e}")

def on_close():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        save_data()
        app.destroy()
        sys.exit()

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

def show_saved_data():
    try:
        with open("book_titles.json", "r") as file:
            data = json.load(file)
            print(data)  # You can display or process the data as needed
    except FileNotFoundError:
        print("JSON file not found.")

def setup_gui(app):
    global entry_title, entry_author, entry_publisher, search_entry  # Declare them as global variables

    input_frame = tk.Frame(app, padx=10, pady=5, relief=tk.RAISED, borderwidth=1)
    input_frame.pack()

    title_label = tk.Label(input_frame, text="Title:")
    title_label.grid(row=0, column=0, padx=5, pady=5)
    entry_title = tk.Entry(input_frame)
    entry_title.grid(row=0, column=1, padx=5, pady=5)

    author_label = tk.Label(input_frame, text="Author:")
    author_label.grid(row=1, column=0, padx=5, pady=5)
    entry_author = tk.Entry(input_frame)
    entry_author.grid(row=1, column=1, padx=5, pady=5)

    publisher_label = tk.Label(input_frame, text="Publisher:")
    publisher_label.grid(row=2, column=0, padx=5, pady=5)
    entry_publisher = tk.Entry(input_frame)
    entry_publisher.grid(row=2, column=1, padx=5, pady=5)

    # Create a separate frame for the buttons
    button_frame = tk.Frame(input_frame)
    button_frame.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

    add_button = tk.Button(button_frame, text="Add Book", command=get_entry_values)
    add_button.grid(row=0, column=0, padx=2, pady=5)

    remove_button = tk.Button(button_frame, text="Remove Book", command=remove_book)
    remove_button.grid(row=0, column=1, padx=3, pady=5)

    sort_search_frame = tk.Frame(input_frame)
    sort_search_frame.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

    sort_button = tk.Button(sort_search_frame, text="Sort Titles", command=sort_titles)
    sort_button.grid(row=0, column=0, padx=2, pady=5)

    search_button = tk.Button(sort_search_frame, text="Search Titles", command=search_titles)
    search_button.grid(row=0, column=1, padx=3, pady=5)

    search_label = tk.Label(input_frame, text="Search:")
    search_label.grid(row=5, column=0, padx=5, pady=5)

    export_button = tk.Button(button_frame, text="Export CSV", command=export_to_csv)
    export_button.grid(row=0, column=2, padx=3, pady=5)

    search_entry = tk.Entry(input_frame)
    search_entry.grid(row=5, column=1, padx=5, pady=5)

    list_frame = tk.Frame(app, padx=10, pady=5, relief=tk.RAISED, borderwidth=1)
    list_frame.pack()

    listbox = tk.Listbox(list_frame)
    listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    details_label = tk.Label(list_frame, text="", wraplength=300)
    details_label.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    listbox.bind("<<ListboxSelect>>", on_select)

    return listbox, list_frame, details_label, search_entry




if __name__ == "__main__":
    book_titles = []
    app = create_app()
    listbox, list_frame, details_label, search_entry = setup_gui(app)
    load_data()
    app.mainloop()