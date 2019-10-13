import tkinter as tk
from tkinter import ttk
import random

class SortingVisualizer:

    def __init__(self):
        # Set window propeties
        self.root = tk.Tk()
        self.root.wm_title("Sorting Visualizer")
        self.root.wm_minsize(width=600, height=500)
        self.root.wm_resizable(width=False, height=False)

        self.sort_canvas = tk.Canvas(self.root)
        self.num_label = None       # Initialize Label of number of operation to be None
        self.num_operations = 0     # Number of operations done during a single sort
        self.bars = []              # List of bar objects being displayed

        self.top_frame = tk.Frame(self.root)
        self.top_frame.grid(row=0, sticky='w')

        self.gen_button = ttk.Button(self.top_frame, text="Generate New Array", command=self.new_array)
        self.gen_button.grid(row=0, column=0)

        self.array_label = tk.Label(self.top_frame, text="Array Size & Sorting Speed")
        self.array_label.grid(row=0, column=1)

        self.s1 = ttk.Scale(self.top_frame, orient='horizontal', from_=4, to=61, command=self.set_array_properties)
        self.s1.set(15)
        self.s1.grid(row=0, column=2)

        # Set properties for the Select Algorithm drop down menu
        self.sort_options = ['Select Algorithm', 'Bubble Sort', 'Quicksort', 'Heap Sort', 'Insertion Sort']
        self.option_var = tk.StringVar()
        self.option_drop = ttk.OptionMenu(self.top_frame, self.option_var, *self.sort_options)
        self.option_drop.config(width=15)
        self.option_drop.grid(row=0, column=3, sticky='ew')

        self.sort_button = ttk.Button(self.top_frame, text="Sort", command=self.sort)
        self.sort_button.grid(row=0, column=4, sticky='w')

        self.num_op_label = tk.Label(self.top_frame, text="Number of Operations: ")
        self.num_op_label.grid(row=1, column=0)

    def set_array_properties(self, val):
        # Set the properties of the array to be sorted and generate a new array with those properties
            # self: The SortingVisualizer object
            # val: The current value the slider is set at
        val = round(float(val))
        self.array_size = val
        self.speed = 2000//val
        self.bar_width = (550-(3*(val-1)))//val
        self.new_array()

    def sort(self):
        # Get selected sorting algorithm from OptionMenu and calls that selected sorting algorithm
            # self: The SortingVisualizer object

        selection = self.option_var.get()
        if selection == 'Select Algorithm':
            return
        # Temporarly disable buttons and array slider during sorting
        self.sort_button.config(state='disabled')
        self.gen_button.config(state='disabled')
        self.s1.state(['disabled'])

        if selection == 'Bubble Sort':
            bubble_sort(self.array)
        elif selection == 'Quicksort':
            quickSort(self.array, 0, len(self.array)-1)
        elif selection == 'Heap Sort':
            heapSort(self.array)
        elif selection == 'Insertion Sort':
            insertionSort(self.array)

        self.draw_canvas(self.array, True)  # Display the sorted array as completed
        # re-enable buttons after sorting is finished
        self.sort_button.config(state='normal')
        self.gen_button.config(state='normal')
        self.s1.state(['!disabled'])

    def new_array(self):
        # Sets up the window for newly generated array
            # self: The SortingVisualizer object

        label = str(self.num_operations)
        if self.num_label == None:
            self.num_label = tk.Label(self.top_frame, text=label)
        else:
            self.num_label.destroy()
            self.num_label = tk.Label(self.top_frame, text=label)
        self.num_label.grid(row=1, column=1, sticky='w')
        
        self.generate_array()
        self.draw_canvas(self.array, False)

    def generate_array(self):
        # Generates a new random array of length denoted by the scale
            # self: The SortingVisualizer object
        self.array = []
        self.num_operations = 0
        i = 0
        while i < self.array_size:
            height = random.randint(15, 200)
            self.array.append(height)
            i += 1

    def draw_canvas(self, array, sort_done, bar_a=None, bar_b=None, pivot=None):
        # Draws the Bars that are being sorted on the canvas
            # self: The sortingVisualizer object
            # array: The array to be displayed
            # sort_done: If the array sorting has been completed
            # bar_a: The index of a current bar being compared
            # bar_b: The index of a current bar being compared
            # pivot: The index of the bar acting as the piviot value

        self.sort_canvas.destroy()
        self.num_label.destroy()
        label = str(self.num_operations)
        self.num_label = tk.Label(self.top_frame, text=label)
        self.num_label.grid(row=1, column=1, sticky='w')
        bar_gap = self.bar_width + 3
        start_x = 30
        start_y = 425

        self.sort_canvas = tk.Canvas(self.root, width=600, height=450)
        self.sort_canvas.create_line(15,start_y,585,start_y)
        self.sort_canvas.grid(row=1)

        self.bars = []
        for i in range(len(array)):
            x1 = start_x + self.bar_width
            y1 = start_y - array[i]*2
            if not sort_done and i != bar_a and i != bar_b:
                self.bars.append(self.sort_canvas.create_rectangle(start_x, start_y, x1, y1, fill='pink'))
            elif not sort_done and i == bar_a or i == bar_b:
                self.bars.append(self.sort_canvas.create_rectangle(start_x, start_y, x1, y1, fill='RoyalBlue'))
            else:
                self.bars.append(self.sort_canvas.create_rectangle(start_x, start_y, x1, y1, fill='green'))
            if not sort_done and i == pivot:
                self.bars.append(self.sort_canvas.create_rectangle(start_x, start_y, x1, y1, fill='yellow'))
            start_x = start_x + bar_gap

        self.root.update()
        self.root.after(self.speed)

    def start(self):
        tk.mainloop()

def bubble_sort(array):
    n = len(array)
    for i in range(n):
        for j in range(n-i-1):
            app.draw_canvas(array, False, j, j+1)  # Update the array displayed on screen
            if array[j] > array[j+1]:
                array[j], array[j+1] = array[j+1], array[j]
                app.num_operations += 1

def quickSort(array, low, high):
    if low < high:
        pivot = partition(array, low, high)
        quickSort(array, low, pivot-1)
        quickSort(array, pivot+1, high)

def partition(array, low, high):
    i = low-1
    pivot = array[high]

    for j in range(low, high):
        if array[j] <= pivot:
            i+= 1
            array[j], array[i], = array[i], array[j]
            app.draw_canvas(array, False, j, i, high)  # Update the array displayed on screen
            app.num_operations += 1
    array[high], array[i+1] = array[i+1], array[high]
    app.draw_canvas(array, False, high, i+1)  # Update the array displayed on screen
    app.num_operations += 1
    return(i+1)

def heapSort(array):
    n = len(array)

    # Build Maxheap
    for i in range(n, -1, -1):
        heapify(array, n, i)
    for i in range(n-1, 0, -1):
        array[i], array[0] = array[0], array[i]
        app.num_operations += 1
        heapify(array, i, 0)

def heapify(array, n, i):
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2

    if left < n and array[i] < array[left]:
        largest = left
    if right < n and array[largest] < array[right]:
        largest = right

    if largest != i:
        array[largest], array[i] = array[i], array[largest]
        app.num_operations += 1
        app.draw_canvas(array, False, largest, i)  # Update the array displayed on screen
        heapify(array, n, largest)

def insertionSort(array):
    for i in range(1, len(array)):
        key = array[i]

        j = i-1
        while j >= 0 and key < array[j]:
            array[j+1] = array[j]
            app.draw_canvas(array, False, j+1, j, i)
            app.num_operations += 1

            j -= 1
        array[j+1] = key

if __name__ == '__main__':
    app = SortingVisualizer()
    app.start()