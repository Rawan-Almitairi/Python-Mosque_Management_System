from tkinter import *
import sqlite3
from tkinter import messagebox

#create mosque class:
class Mosque:
    def __init__(self, ID, name, type_mosq, address, coordinate, imam_name):
        self.ID = ID
        self.name = name
        self.type_mosq = type_mosq
        self.address = address
        self.coordinate = coordinate
        self.imam_name = imam_name

#database:
class Database:
    def __init__(self):
        self.conn = sqlite3.connect('mosque.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS mosques (
        ID INTEGER PRIMARY KEY,
        Name TEXT,
        Type TEXT,
        Address TEXT,
        Coordinate TEXT,
        Imam_name TEXT )
        ''')
        self.conn.commit()

    #display function
    def display(self):
        self.cursor.execute(
            "SELECT * FROM mosques"
        )
        return self.cursor.fetchall()
    #search function
    def search(self, name):
        self.cursor.execute(
        "SELECT * FROM mosques WHERE Name = ?",
        (name,)
    )
        return self.cursor.fetchone()
    #update function
    def update(self, imam_name, ID):
        self.cursor.execute('''
        UPDATE mosques
        SET
        Imam_name = ?
        WHERE ID = ?
        ''',(
            imam_name,
            ID
    ))
        self.conn.commit()
    #insert function
    def insert(self, ID, name, type_mosq, address, coordinate, imam_name):
        self.cursor.execute('''
        INSERT INTO mosques
        VALUES (?, ?, ?, ?, ?, ?)
        ''',
        (ID, name, type_mosq, address, coordinate, imam_name)
        )
        self.conn.commit()
    #delete
    def delete(self, ID):
        self.cursor.execute(
        "DELETE FROM mosques WHERE ID = ?",
        (ID,)
    )
        self.conn.commit()
        return self.cursor.rowcount
    #destroy object
    def __del__(self):
        self.conn.close()

db = Database()
searched_mosq_id = None
#build the window
top = Tk()
top.title('Mosques Management System')
top.geometry('680x220')

# add the widget
#part 1:
#row 1
l1= Label(top, text='ID')
l1.grid(row=0, column=0)
id_text = StringVar()
e1= Entry(top, textvariable=id_text)
e1.grid(row=0, column=1)

l2= Label(top, text='Name')
l2.grid(row=0, column=2)
name_text = StringVar()
e2= Entry(top, textvariable=name_text)
e2.grid(row=0, column=3)

#row 2:
l3= Label(top, text='Type')
l3.grid(row=1, column=0)
type_text = StringVar()
e3= OptionMenu(top, type_text, 'Jamea', 'Masjid')
e3.grid(row=1, column=1)

l4= Label(top, text='Address')
l4.grid(row=1, column=2)
address_text = StringVar()
e4= Entry(top, textvariable=address_text)
e4.grid(row=1, column=3)

#row 3:
l5= Label(top, text='coordinate')
l5.grid(row=2, column=0)
coord_text = StringVar()
e5= Entry(top, textvariable=coord_text)
e5.grid(row=2, column=1)

l6= Label(top, text='Imam_name')
l6.grid(row=2, column=2)
imam_name_text = StringVar()
e6= Entry(top, textvariable=imam_name_text)
e6.grid(row=2, column=3)

#part 2:
listbox = Listbox(top, width=40, height=12)
listbox.grid(row=0, column=4, columnspan=3, rowspan=5)

#part 3:
#btn methods:
def clear_entries():
    id_text.set("")
    name_text.set("")
    type_text.set("")
    address_text.set("")
    coord_text.set("")
    imam_name_text.set("")

def display():
    listbox.delete(0, END)
    rows = db.display()
    for row in rows:
        listbox.insert(END, row)

def search():
    global searched_mosq_id
    listbox.delete(0, END)
    row = db.search(name_text.get())
    # for row in rows:
    #     listbox.insert(END, row)
    if row:
        listbox.insert(END, row)
        id_text.set(row[0])
        name_text.set(row[1])
        type_text.set(row[2])
        address_text.set(row[3])
        coord_text.set(row[4])
        imam_name_text.set(row[5])

        searched_mosq_id = row[0]
    else:
        messagebox.showwarning("Not Found",
                            "No Mosques found with this name")
        searched_mosq_id = None
    clear_entries()

def update():
    if searched_mosq_id is None:
        messagebox.showwarning("Warning", "Please search for a mosque by name")
        return
    db.update(
        imam_name_text.get(),
        searched_mosq_id
    )
    messagebox.showinfo(
        "Mosques Updated",
        "Mosques Updated Successfully")

    display()
    clear_entries()

def add_entry():
    try:
        if id_text.get() == "" or name_text.get() == "":
            messagebox.showwarning("Warning", "ID and Name cannot be empty")
            return
        mosq = Mosque(
            int(id_text.get()),
            name_text.get(),
            type_text.get(),
            address_text.get(),
            coord_text.get(),
            imam_name_text.get()
        )
        db.insert(
            mosq.ID,
            mosq.name,
            mosq.type_mosq,
            mosq.address,
            mosq.coordinate,
            mosq.imam_name
        )
        messagebox.showinfo('Mosques Added', 'Mosques Added Successfully')
        display()
        clear_entries()
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid mosque")

def delete():
    if id_text.get() == "":
        messagebox.showwarning("Warning", "Please search for a mosque by ID")
        return
    try:
        delete_rows = db.delete(int(id_text.get()))
        if delete_rows > 0:
            messagebox.showinfo(
                'Mosques Deleted',
                'Mosques Deleted Successfully')
            display()
            clear_entries()
        else:
            messagebox.showwarning("Not Found","This mosque ID not exist")
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid mosque")

#row 4:
b1 = Button(top, text='Display_All', command=display)
b1.grid(row=3, column=1)

b2 = Button(top, text='Search By Name', command=search)
b2.grid(row=3, column=2)

b3 = Button(top, text='Update Entry', command=update)
b3.grid(row=3, column=3)
#row 5:
b4 = Button(top, text='Add Entry', command=add_entry)
b4.grid(row=4, column=1)

b5 = Button(top, text='Delete entry', command=delete)
b5.grid(row=4, column=2)
#part 4:
b6 = Button(top, text='Display on Map')
b6.grid(row=4, column=3)

top.mainloop()


