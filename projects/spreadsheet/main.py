import tkinter as tk

class SpreadsheetApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Giovani's Spreadsheet App")
        self.geometry("800x600")  # Set the initial size of the window
        self.create_menu()
        self.create_grid()

    def donothing():
        pass

    def create_grid(self):
        # Creating a grid of Entry widgets
        self.cells = {}
        for i in range(10): # 10 rows
            for j in range(5): # 5 columns
                cell = tk.Entry(self, width=10)
                cell.grid(row=i, column=j)
                self.cells[(i, j)] = cell

    def create_menu(self):
        menu = tk.Menu(self)
        self.config(menu=menu)

        filemenu = tk.Menu(menu,tearoff=0)
        filemenu.add_command(label="New", command=self.donothing)
        filemenu.add_command(label="Open", command=self.donothing)
        filemenu.add_command(label="Save", command=self.donothing)
        filemenu.add_command(label="Save as...", command=self.donothing)
        filemenu.add_command(label="Close", command=self.donothing)

        menu.add_cascade(label="File", menu=filemenu)

    def run(self):
        self.mainloop()

if __name__ == "__main__":
    app = SpreadsheetApp()
    app.run()
