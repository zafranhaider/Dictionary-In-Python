import tkinter as tk
from tkinter import messagebox
import speech_recognition as sr
from PyDictionary import PyDictionary

class DictionaryApp:
    def __init__(self, master):
        self.master = master
        self.master.title("English AI Dictionary")

        # Set window size and center the window
        window_width = 1360
        window_height = 780
        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()
        x_coordinate = (screen_width - window_width) // 2
        y_coordinate = (screen_height - window_height) // 2
        self.master.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

        # Load background image
        self.background_image = tk.PhotoImage(file="back.png")  # Provide the path to your image
        self.background_label = tk.Label(master, image=self.background_image)
        self.background_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.dictionary = PyDictionary()

        # Initialize custom dictionary
        self.custom_dictionary = {}

        # Widgets for searching
        self.search_label = tk.Label(master, text="Enter a word:", bg="white")
        self.search_label.pack(pady=(100, 10))

        self.search_entry = tk.Entry(master)
        self.search_entry.pack(pady=10)

        self.search_button = tk.Button(master, text="Search", command=self.search_word, bg="white")
        self.search_button.pack(pady=10)

        # Widgets for displaying definition
        self.definition_label = tk.Label(master, text="Definition:", bg="red")
        self.definition_label.pack(pady=10)

        self.definition_text = tk.Text(master, height=10, width=90, wrap="word")
        self.definition_text.pack(pady=10)
        scrollbar = tk.Scrollbar(master, command=self.definition_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.definition_text.config(yscrollcommand=scrollbar.set)

        # Widgets for voice input
        self.voice_button = tk.Button(master, text="Voice Input", command=self.voice_input, bg="white")
        self.voice_button.pack(pady=10)

        # Widgets for adding words
        self.add_button = tk.Button(master, text="Add Word", command=self.create_add_word_window, bg="white")
        self.add_button.pack(pady=10)

        # Widget for deleting words
        self.delete_button = tk.Button(master, text="Delete Word", command=self.create_delete_word_window, bg="white")
        self.delete_button.pack(pady=10)

        # Widget for updating words
        self.update_button = tk.Button(master, text="Update Meaning", command=self.create_update_word_window, bg="white")
        self.update_button.pack(pady=10)

    def search_word(self):
        word = self.search_entry.get()
        definition = self.dictionary.meaning(word)

        if definition:
            self.definition_text.delete(1.0, tk.END)
            for pos, mean in definition.items():
                self.definition_text.insert(tk.END, f"{pos.capitalize()}: {', '.join(mean)}\n")
        elif word in self.custom_dictionary:
            self.definition_text.delete(1.0, tk.END)
            self.definition_text.insert(tk.END, f"Custom Definition:\n{', '.join(self.custom_dictionary[word])}")
        else:
            messagebox.showerror("Error", f"'{word}' not found in the dictionary.")

    def voice_input(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Speak:")
            try:
                audio = r.listen(source, timeout=5)
                word = r.recognize_google(audio)
                self.search_entry.delete(0, tk.END)
                self.search_entry.insert(0, word)
            except sr.WaitTimeoutError:
                messagebox.showerror("Error", "Timeout waiting for speech")
            except sr.UnknownValueError:
                messagebox.showerror("Error", "Could not understand audio")
            except sr.RequestError as e:
                messagebox.showerror("Error", f"Could not request results from Google Speech Recognition service; {e}")


    def add_word(self, word, meanings):
        # Add word and meanings to the custom dictionary
        self.custom_dictionary[word] = meanings
        messagebox.showinfo("Success", f"'{word}' added successfully.")

    def delete_word(self, word):
        # Delete word from the custom dictionary
        if word in self.custom_dictionary:
            del self.custom_dictionary[word]
            messagebox.showinfo("Success", f"'{word}' deleted successfully.")
        else:
            messagebox.showerror("Error", f"'{word}' not found in the custom dictionary.")

    def update_word(self, word, new_meanings):
        # Update meanings of a word in the custom dictionary
        if word in self.custom_dictionary:
            self.custom_dictionary[word] = new_meanings
            messagebox.showinfo("Success", f"Meanings of '{word}' updated successfully.")
        else:
            messagebox.showerror("Error", f"'{word}' not found in the custom dictionary.")

    def create_add_word_window(self):
        def add_word_to_dict():
            word = word_entry.get()
            meanings = meanings_entry.get("1.0", tk.END).strip().split('\n')
            self.add_word(word, meanings)
            add_word_window.destroy()

        add_word_window = tk.Toplevel(self.master)
        add_word_window.title("Add Word")
        add_word_window.geometry("400x300")

        word_label = tk.Label(add_word_window, text="Enter a word:")
        word_label.pack(pady=5)

        word_entry = tk.Entry(add_word_window)
        word_entry.pack(pady=5)

        meanings_label = tk.Label(add_word_window, text="Enter meanings (separated by new lines):")
        meanings_label.pack(pady=5)

        meanings_entry = tk.Text(add_word_window, height=10, width=30)
        meanings_entry.pack(pady=5)

        add_button = tk.Button(add_word_window, text="Add", command=add_word_to_dict)
        add_button.pack(pady=10)

    def create_delete_word_window(self):
        def delete_word_from_dict():
            word = word_entry.get()
            self.delete_word(word)
            delete_word_window.destroy()

        delete_word_window = tk.Toplevel(self.master)
        delete_word_window.title("Delete Word")
        delete_word_window.geometry("300x150")

        word_label = tk.Label(delete_word_window, text="Enter a word to delete:")
        word_label.pack(pady=5)

        word_entry = tk.Entry(delete_word_window)
        word_entry.pack(pady=5)

        delete_button = tk.Button(delete_word_window, text="Delete", command=delete_word_from_dict)
        delete_button.pack(pady=10)

    def create_update_word_window(self):
        def update_word_in_dict():
            word = word_entry.get()
            new_meanings = new_meanings_entry.get("1.0", tk.END).strip().split('\n')
            self.update_word(word, new_meanings)
            update_word_window.destroy()

        update_word_window = tk.Toplevel(self.master)
        update_word_window.title("Update Meaning")
        update_word_window.geometry("400x300")

        word_label = tk.Label(update_word_window, text="Enter a word to update:")
        word_label.pack(pady=5)

        word_entry = tk.Entry(update_word_window)
        word_entry.pack(pady=5)

        new_meanings_label = tk.Label(update_word_window, text="Enter new meanings (separated by new lines):")
        new_meanings_label.pack(pady=5)

        new_meanings_entry = tk.Text(update_word_window, height=10, width=30)
        new_meanings_entry.pack(pady=5)

        update_button = tk.Button(update_word_window, text="Update", command=update_word_in_dict)
        update_button.pack(pady=10)

def main():
    root = tk.Tk()
    app = DictionaryApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
