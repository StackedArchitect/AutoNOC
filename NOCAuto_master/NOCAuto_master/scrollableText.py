import customtkinter as ctk
import tkinter as tk

class ScrollableText(ctk.CTkFrame):
    def __init__(self, parent, width=400, height=300, **kwargs):
        super().__init__(parent, **kwargs)

        # Extract proper color codes from the theme (use only hex codes)
        bg_color = ctk.ThemeManager.theme["CTkFrame"]["fg_color"][1]  # Extracting hex only
        fg_color = ctk.ThemeManager.theme["CTkLabel"]["text_color"][1]  # Extracting hex only

        # Create a CTk-style scrollbar
        self.scrollbar = ctk.CTkScrollbar(self, command=self.on_scroll)

        # Create a Text widget with proper color settings (bg, fg)
        self.text_widget = tk.Text(self, wrap='word', font=("Arial", 16),
                                   bg=bg_color,  # Background color in hex format
                                   fg=fg_color,  # Foreground (text) color in hex format
                                   bd=0, insertbackground="white")

        # Configure scrollbar to work with the Text widget
        self.text_widget.configure(yscrollcommand=self.scrollbar.set)

        # Set the size of the text box
        self.text_widget.config(width=width, height=height)

        # Place text widget and scrollbar in the frame
        self.text_widget.grid(row=0, column=0, sticky='nsew')
        self.scrollbar.grid(row=0, column=1, sticky='ns')

        # Configure the grid to make sure the text box resizes with the frame
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def on_scroll(self, *args):
        """Link scrolling to both scrollbar and text widget."""
        self.text_widget.yview(*args)

    def add_text(self, text):
        """Method to insert text into the Text widget."""
        self.text_widget.insert(tk.END, text)
        self.text_widget.see(tk.END)


    def clear_text(self):
        """Method to clear all text in the Text widget."""
        self.text_widget.delete(1.0, tk.END)


# Example Usage
if __name__ == "__main__":
    app = ctk.CTk()
    app.geometry("500x400")

    # Create an instance of ScrollableText
    scrollable_text = ScrollableText(app, width=60, height=20)
    scrollable_text.pack(padx=10, pady=10, fill="both", expand=True)

    # Add some text
    for  i in range(100):
        scrollable_text.add_text("This is a scrollable text box with CustomTkinter style!\n")

    app.mainloop()
