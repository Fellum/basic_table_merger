from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from table_merger import merge_tables


def set_dir_path(*args):
    value = filedialog.askdirectory(initialdir="./", title="Select dir")
    if value:
        dir_path.set(value)


def set_base_path(*args):
    value = filedialog.askopenfilename(initialdir="./", title="Select file")
    if value:
        base_path.set(value)


def set_res_path(*args):
    value = filedialog.asksaveasfilename(initialdir="./", title="Select file")
    if value:
        res_path.set(value)


def merge_tables_event(*args):
    if dir_path.get() != "set dir path" and res_path.get() != "set res path" and base_path.get() != "set base path":
        merge_tables(base_path.get(), dir_path.get(), res_path.get())
    else:
        messagebox.showerror("Error", "Some fields unset!!!")


root = Tk()
root.title("Table merger")
mainframe = ttk.Frame(root, padding="12 12 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

res_path = StringVar()
dir_path = StringVar()
base_path = StringVar()

res_path.set("set res path")
dir_path.set("set dir path")
base_path.set("set base path")

ttk.Label(mainframe, textvariable=dir_path).grid(column=1, row=1, sticky=(W, E))
ttk.Label(mainframe, textvariable=base_path).grid(column=1, row=2, sticky=(W, E))
ttk.Label(mainframe, textvariable=res_path).grid(column=1, row=3, sticky=(W, E))

ttk.Button(mainframe, text="Browse", command=set_dir_path).grid(column=3, row=1, sticky=E)
ttk.Button(mainframe, text="Browse", command=set_base_path).grid(column=3, row=2, sticky=E)
ttk.Button(mainframe, text="Browse", command=set_res_path).grid(column=3, row=3, sticky=E)

ttk.Button(mainframe, text="Run!", command=merge_tables_event).grid(column=2, row=4, sticky=(E, W))

for child in mainframe.winfo_children():
    child.grid_configure(padx=5, pady=5)

root.mainloop()
