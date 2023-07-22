import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import customtkinter as ctk
import os
import subprocess
import tempfile
import ffmpy
import shlex
from pathlib import Path
import ffmpy
import tempfile
import os
from pathlib import Path

class VideoProcessor:
    """
    A utility class for video processing operations.
    Methods:
        combine_videos(file_paths, output_file_path): Combines multiple video files into a single video.
    """

    @staticmethod
    def combine_videos(file_paths, output_file_path):
        """
        Combines multiple video files into a single video.
        Args:
            file_paths (list): A list of input file paths.
            output_file_path (str): The output file path for the combined video.
        Returns:
            str: The output file path of the combined video if successful, None otherwise.
        """
        try:
            temp_file_path = VideoProcessor._create_temp_file(file_paths)
            inputs = {temp_file_path: ["-f", "concat", "-safe", "0"]}
            outputs = {output_file_path: ["-c", "copy"]}
            ff = ffmpy.FFmpeg(inputs=inputs, outputs=outputs)
            ff.run()
            os.unlink(temp_file_path)
            return output_file_path
        except Exception as e:
            print(f"Error occurred during video combining: {str(e)}")
            return None

    @staticmethod
    def _create_temp_file(file_paths):
        """
        Creates a temporary file listing the input file paths.
        Args:
            file_paths (list): A list of input file paths.
        Returns:
            str: The path of the temporary file.
        """
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
            for path in file_paths:
                f.write(f"file '{path}'\n")
            return Path(f.name).as_posix()
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class VideoCombiner(ctk.CTk):
    """
    A GUI application for combining multiple video files into a single video.
    Attributes:
        file_listbox (tk.Listbox): The listbox widget to display the selected video files.
        add_file_button (ctk.CTkButton): The button to add video files.
        remove_file_button (ctk.CTkButton): The button to remove selected video files.
        move_up_button (ctk.CTkButton): The button to move the selected video file up in the list.
        move_down_button (ctk.CTkButton): The button to move the selected video file down in the list.
        combine_button (ctk.CTkButton): The button to initiate the video combining process.
    """

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """
        Initializes the user interface of the application.
        """
        self.title("Agglomerator")
      
        self.geometry("700x600")
      
        self.configure(padx=10, pady=10)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.file_listbox = tk.Listbox(self, selectmode=tk.SINGLE, exportselection=False, font=("Roboto Condensed", 20))
        self.file_listbox.grid(row=0, column=0, columnspan=5, sticky="nsew")
        self.add_file_button = ctk.CTkButton(self, text="Add Video File", command=self.add_file)
        self.add_file_button.grid(row=1, column=0, sticky="nsew")
        self.remove_file_button = ctk.CTkButton(self, text="Remove Video File", command=self.remove_file)
        self.remove_file_button.grid(row=1, column=1, sticky="nsew")
        self.move_up_button = ctk.CTkButton(self, text="Move Up", command=lambda: self.move_file(-1))
        self.move_up_button.grid(row=1, column=2, sticky="nsew")
        self.move_down_button = ctk.CTkButton(self, text="Move Down", command=lambda: self.move_file(1))
        self.move_down_button.grid(row=1, column=3, sticky="nsew")
        self.combine_button = ctk.CTkButton(self, text="Combine Videos", command=self.combine_videos)
        self.combine_button.grid(row=1, column=4, sticky="nsew")
        for i in range(5):
            self.columnconfigure(i, weight=1)
        self.rowconfigure(1, weight=0)

    def add_file(self):
        """
        Opens a file dialog to select video files and adds them to the file listbox.
        """
        file_paths = filedialog.askopenfilenames(multiple=True)
        if file_paths:
            for file_path in file_paths:
                self.file_listbox.insert(tk.END, file_path)

    def remove_file(self):
        """
        Removes the selected video file from the file listbox.
        """
        selected_index = self.file_listbox.curselection()
        if selected_index:
            self.file_listbox.delete(selected_index)
          
    def move_file(self, direction):
        """
        Moves the selected video file up or down in the file listbox.

        Args:
            direction (int): The direction to move the file (-1 to move up, 1 to move down).
        """
        selected_index = self.file_listbox.curselection()
        if selected_index and 0 <= selected_index[0] + direction < self.file_listbox.size():
            selected_item = self.file_listbox.get(selected_index)
            self.file_listbox.delete(selected_index)
            new_index = selected_index[0] + direction
            self.file_listbox.insert(new_index, selected_item)
            self.file_listbox.select_set(new_index)

    def combine_videos(self):
        """
        Combines the selected video files into a single video.
        Displays a save file dialog to select the output file path.
        Shows a success message box upon successful combination.
        """
        file_paths = self.file_listbox.get(0, tk.END)
        output_file_path = filedialog.asksaveasfilename(defaultextension=".mp4", filetypes=[("Video Files", "*.mp4")])
        if not output_file_path:
            return
          
        result = VideoProcessor.combine_videos(file_paths, output_file_path)
        if result:
            messagebox.showinfo("Success", "Video files combined successfully.")
        else:
            messagebox.showerror("Error", "Failed to combine video files.")


if __name__ == "__main__":
    app = VideoCombiner()
    app.mainloop()


