import tkinter as tk
from PIL import Image, ImageFilter
import cv2
import numpy as np
import random

class ArrayFilterApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Array Filter App")

        self.array_size_label = tk.Label(self.root, text="Enter Array Size (k):")
        self.array_size_label.grid(row=0, column=0)

        self.array_size_entry = tk.Entry(self.root)
        self.array_size_entry.grid(row=0, column=1)

        self.file_label = tk.Label(self.root, text="Enter File Name:")
        self.file_label.grid(row=1, column=0)

        self.file_entry = tk.Entry(self.root)
        self.file_entry.grid(row=1, column=1)

        self.create_array_button = tk.Button(self.root, text="Create Array", command=self.create_array)
        self.create_array_button.grid(row=0, column=2)

        self.array_frame = tk.Frame(self.root)
        self.array_frame.grid(row=3, column=0, columnspan=3)

    def create_array(self):
        size = int(self.array_size_entry.get())
        self.root.destroy()  # Close the current window
        new_app = ArrayFilterApp()  # Create a new instance of the app
        new_app.create_array_gui(size)  # Create new array GUI with the specified size

    def create_array_gui(self, size):
        self.array = []
        for i in range(size):
            row = []
            for j in range(size):
                entry = tk.Entry(self.array_frame, width=5, justify="center")  # Align text to the center
                entry.grid(row=i, column=j)
                entry.insert(tk.END, "0")  # Initialize with "0"
                row.append(entry)
            self.array.append(row)

        self.threshold_label = tk.Label(self.root, text="Threshold:")
        self.threshold_label.grid(row=size+3, column=0)

        self.threshold_entry = tk.Entry(self.root)
        self.threshold_entry.grid(row=size+3, column=1)
        self.threshold_entry.config(state=tk.DISABLED)  # Disable by default

        self.threshold_checked = tk.BooleanVar()
        self.threshold_checkbox = tk.Checkbutton(self.root, text="Threshold", variable=self.threshold_checked, command=self.toggle_threshold)
        self.threshold_checkbox.grid(row=size+3, column=2)

        self.min_label = tk.Label(self.root, text="Min:")
        self.min_label.grid(row=size+4, column=1)
        self.min_entry = tk.Entry(self.root)
        self.min_entry.grid(row=size+4, column=2)

        self.max_label = tk.Label(self.root, text="Max:")
        self.max_label.grid(row=size+4, column=3)
        self.max_entry = tk.Entry(self.root)
        self.max_entry.grid(row=size+4, column=4)

        self.random_button = tk.Button(self.root, text="Random", command=self.fill_with_random)
        self.random_button.grid(row=size+4, column=0)

        self.apply_filter_button = tk.Button(self.root, text="Apply Filter", command=self.apply_filter)
        self.apply_filter_button.grid(row=size+6, column=1)

        self.fill_zeros_button = tk.Button(self.root, text="Fill with Zeros", command=self.fill_with_zeros)
        self.fill_zeros_button.grid(row=size+6, column=0)

        self.fill_ones_button = tk.Button(self.root, text="Fill with Ones", command=self.fill_with_ones)
        self.fill_ones_button.grid(row=size+6, column=2)

        self.root.mainloop()

    def toggle_threshold(self):
        if self.threshold_checked.get():
            self.threshold_entry.config(state=tk.NORMAL)
        else:
            self.threshold_entry.config(state=tk.DISABLED)

    def fill_with_zeros(self):
        for row in self.array:
            for entry in row:
                entry.delete(0, tk.END)
                entry.insert(tk.END, "0")

    def fill_with_ones(self):
        for row in self.array:
            for entry in row:
                entry.delete(0, tk.END)
                entry.insert(tk.END, "1")

    def fill_with_random(self):
        try:
            min_val = int(self.min_entry.get())
            max_val = int(self.max_entry.get())
            for row in self.array:
                for entry in row:
                    entry.delete(0, tk.END)
                    random_val = random.randint(min_val, max_val)
                    entry.insert(tk.END, str(random_val))
        except ValueError:
            print("Please enter valid integer values for Min and Max.")

    def get_filter_array(self):
        filter_array = []
        for row in self.array:
            filter_row = []
            for entry in row:
                value = entry.get()
                if value.strip() == "":
                    value = 0
                else:
                    value = int(value)
                filter_row.append(value)
            filter_array.append(filter_row)
        return filter_array

    def apply_filter(self):
        try:
            filter_array = np.array(self.get_filter_array())
            if np.sum(filter_array) > 0:
                kernel = filter_array / np.sum(filter_array)
            else:
                kernel = filter_array
            file_name = self.file_entry.get()
            img = cv2.imread(file_name, cv2.IMREAD_GRAYSCALE)  # Use the provided file name
            filtered_img = cv2.filter2D(img, -1, kernel)
            filtered_img = np.abs(filtered_img)

            # Check if thresholding is enabled
            if self.threshold_checked.get():
                threshold = int(self.threshold_entry.get())
                _, filtered_img = cv2.threshold(filtered_img, threshold, 255, cv2.THRESH_BINARY)

            cv2.imshow('filtered image', filtered_img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        except Exception as e:
            print("Error applying filter:", e)

if __name__ == "__main__":
    app = ArrayFilterApp()
    app.root.mainloop()
