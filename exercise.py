from tkinter import *
from tkinter import messagebox
from tkinter.messagebox import *


def verify():
    age = int(age_var.get())
    if age >= 18:
        messagebox.showinfo("Age", "You are Adult")
    else:
        messagebox.showwarning("Age", "You are Child")



top = Tk()
top.title("information")
top.geometry("200x100")

l1= Label(top, text="Enter Age")
l1.grid(row=0, column=0)

age_var = StringVar()
e1 = Entry(top, textvariable = age_var)
e1.grid(row=0, column=1)

b1 = Button(top, text="verify", command=verify)
b1.grid(row=1, column=0)

top.mainloop()