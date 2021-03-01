import tkinter as tk


class Settings():
    def __init__(self):

        self.root = tk.Tk()
        self.root.geometry("300x120+600+200")
        self.root.title('Settings')

        self.width = 200
        self.height = 150

        self.margin = 10
        self.cell_width = 50
        self.num_cols = int(self.width / self.cell_width)
        self.num_rows = int(self.height / self.cell_width)
        self.size = (self.width + 2 * self.margin,
                     self.height + 2 * self.margin)

        self.robots = tk.IntVar()
        self.sources = tk.IntVar()
        self.size_source = tk.IntVar()

        tk.Label(self.root, text='Enter number of robots : ').grid(
            row=1, column=0)
        tk.Label(self.root, text='Enter number of sources : ').grid(
            row=2, column=0)
        tk.Label(self.root, text='Enter size of source : ').grid(
            row=3, column=0)

        tk.Entry(
            self.root, textvariable=self.robots).grid(row=1, column=1)
        tk.Entry(
            self.root, textvariable=self.sources).grid(row=2, column=1)
        tk.Entry(
            self.root, textvariable=self.size_source).grid(row=3, column=1)

        tk.Button(self.root, text='Submit',
                  command=self.done).grid(row=4, column=0, columnspan=2)

        self.root.protocol("WM_DELETE_WINDOW", self.default)
        self.root.mainloop()

    def done(self):
        self.robots = self.robots.get()
        self.sources = self.sources.get()
        self.size_source = self.size_source.get()
        self.valid = True
        self.root.destroy()

    def default(self):
        self.valid = False
        self.root.destroy()
