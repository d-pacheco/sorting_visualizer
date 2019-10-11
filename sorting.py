import tkinter as tk
from tkinter import ttk
import random

class SortingVisualizer:

    def __init__(self):
        self.root = tk.Tk()
        self.root.wm_title("Sorting Visualizer")
        self.root.wm_minsize(width=600, height=500)
        self.root.wm_resizable(width=False, height=False)

        self.sort_canvas = tk.Canvas(self.root)
        self.num_label = None
        self.num_operations = 0
        self.bars = []
        self.bar_width = 0
        self.bar_gap = 0

        self.top_frame = tk.Frame(self.root)
        self.top_frame.grid(row=0, sticky='w')

        self.gen_button = ttk.Button(self.top_frame, text="Generate New Array", command=self.new_array)
        self.gen_button.grid(row=0, column=0)

        self.s1 = ttk.Scale(self.top_frame, orient='horizontal', from_=4, to=61, command=self.set_array_properties)
        self.s1.set(15)
        self.s1.grid(row=0, column=1)

        self.sort_options = ['Select Algorithm', 'Bubble Sort', 'Quicksort', 'Merge Sort', 'Heap Sort']
        self.option_var = tk.StringVar()
        self.option_drop = ttk.OptionMenu(self.top_frame, self.option_var, *self.sort_options)
        self.option_drop.config(width=15)
        self.option_drop.grid(row=0, column=3, sticky='ew')

        self.sort_button = ttk.Button(self.top_frame, text="Sort", command=self.get_select)
        self.sort_button.grid(row=0, column=4, sticky='w')

        self.num_op_label = tk.Label(self.top_frame, text="Number of Operations: ")
        self.num_op_label.grid(row=1, column=0)

    def set_array_properties(self, val):
        val = round(float(val))
        self.array_size = val
        self.speed = 1000//val
        self.bar_width = (550-(3*(val-1)))//val
        self.new_array()

    def get_select(self):
        selection = self.option_var.get()
        if selection == 'Select Algorithm':
            return
        self.sort_button.config(state='disabled')
        self.gen_button.config(state='disabled')
        self.s1.state(['disabled'])
        if selection == 'Bubble Sort':
            bubble_sort(self.array)
        elif selection == 'Quicksort':
            quickSort(self.array, 0, len(self.array)-1)
        elif selection == 'Merge Sort':
            mergeSort(self.array)
        elif selection == 'Heap Sort':
            heapSort(self.array)

        self.blip_canvas(self.array, True)  # Display the sorted array as completed
        # re-enable buttons after sorting is finished
        self.sort_button.config(state='normal')
        self.gen_button.config(state='normal')
        self.s1.state(['normal'])

    def new_array(self):
        label = str(self.num_operations)
        if self.num_label == None:
            self.num_label = tk.Label(self.top_frame, text=label)
        else:
            self.num_label.destroy()
            self.num_label = tk.Label(self.top_frame, text=label)
        self.num_label.grid(row=1, column=1, sticky='w')
        
        self.generate_array()
        self.blip_canvas(self.array, False)

    def generate_array(self):
        self.array = []
        self.num_operations = 0
        i = 0
        while i < self.array_size:
            height = random.randint(15, 200)
            self.array.append(height)
            i += 1

    def draw_canvas(self, array, sort_done, bar_a=None, bar_b=None, pivot=None):
        self.num_label.destroy()
        label = str(self.num_operations)
        self.num_label = tk.Label(self.top_frame, text=label)
        self.num_label.grid(row=1, column=1, sticky='w')

        self.sort_canvas = tk.Canvas(self.root, width=600, height=450)
        self.sort_canvas.create_line(15,15,585,15)
        self.sort_canvas.grid(row=1)

        bar_gap = self.bar_width + 3
        start_x = 30
        start_y = 15
        self.bars = []
        for i in range(len(array)):
            x1 = start_x + self.bar_width
            y1 = start_y + array[i]
            if not sort_done and i != bar_a and i != bar_b:
                self.bars.append(self.sort_canvas.create_rectangle(start_x, start_y, x1, y1*2, fill='pink'))
            elif not sort_done and i == bar_a or i == bar_b:
                self.bars.append(self.sort_canvas.create_rectangle(start_x, start_y, x1, y1*2, fill='RoyalBlue'))
            else:
                self.bars.append(self.sort_canvas.create_rectangle(start_x, start_y, x1, y1*2, fill='green'))
            if not sort_done and i == pivot:
                self.bars.append(self.sort_canvas.create_rectangle(start_x, start_y, x1, y1*2, fill='yellow'))
            start_x = start_x + bar_gap

    def blip_canvas(self, array, sort_done, i=None, j=None, pivot=None):
        self.sort_canvas.destroy()
        self.draw_canvas(array, sort_done, i, j, pivot)
        self.root.update()
        self.root.after(self.speed)

    def start(self):
        tk.mainloop()



if __name__ == '__main__':
    app = SortingVisualizer()
    app.start()