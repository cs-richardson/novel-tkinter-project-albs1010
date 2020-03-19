#Albert
from tkinter import *
import tkinter as tk
from tkinter import messagebox
from datetime import datetime, date


import sqlite3 as sq


con = sq.connect("novel.db")
c = con.cursor()

#Function gets author's data from the table
def get_author():
    res = c.execute("SELECT AuthorID, AuthorDOB, AuthorName from Author")
    data = c.fetchall() 
    return data

#Function gets novel's data from the table
def get_novel():
    res = c.execute("SELECT * from Novel")
    data = c.fetchall()
    return data

#Creates a data with only novel, author and publication date
def get_novel_report():
    res = c.execute("SELECT Title, AuthorName, NovelPD from author, novel where author.AuthorID = novel.AuthorID")
    data = c.fetchall()
    return data
#This function adds a new novel into the tables
def add_novel(dt, authorID, bookID, novel_name):
    ins_str = 'INSERT INTO Novel (BookID, Title, NovelPD, AuthorID) Values (' + str(bookID) + ', "' + str(novel_name) + '", "' + str(dt) + '", ' + str(authorID) + ');'
    res = c.execute(ins_str)
    con.commit()		




# This function gives the user 3 button options, novel report, add novel, or exit
#main menu
def render_menu():
 
    window = Tk()
    window.title("Novel Main Menu")
    window.geometry("200x100")

    rpt = Button(window, text="All Novels & Authors", command = novel_report)
    rpt.pack()

    
    res = Button(window, text="Enter New Novel", command = enter_novel)
    res.pack()

    ext = Button(window, text="Exit", command = lambda:end_program(window))
    ext.pack()
    window.mainloop()

def end_program(w):
    con.close()
    w.destroy()

#This function gives the novel report in a messagebox
def novel_report():
   
    report = get_novel_report()
    tbl = "Novel Name, Author, Publication Date"
    tbl += "\n" + "-" * 40 
    count = 0
    for row in report:
        count = count + 1
        tbl += "\n" + str(count) + ". "
        for field in row:
            tbl += str(field)
            tbl += ", "
        tbl += "\n"
    tbl += "-" * 40
    messagebox.showinfo("Report results", tbl)
    
'''
This function gives the user a selection of authors where they can choose from on the right.
On the left, it lets the user type in the novel name and publication date
'''

def enter_novel():

    res_req_win = Tk()
    res_req_win.title("Enter New Novel")
    res_req_win.geometry("520x300")

    date_frame = Frame(res_req_win)
    date_frame.pack(side = LEFT)

    nn = tk.StringVar(res_req_win)
    dd = tk.StringVar(res_req_win)
    mm = tk.StringVar(res_req_win)
    yyyy = tk.StringVar(res_req_win)
  
   
    lbl = Label(date_frame, text = "1. Choose an author\n 2. Type the novel name\n 3. Enter publication day, month, and year").pack()

    lblnn = Label(date_frame, text = "Novel Name").pack()
    novelname = Entry(date_frame, text="NN", textvariable = nn).pack()
    
    lbldd = Label(date_frame, text = "Publication Day").pack()
    day = Entry(date_frame, text="DD", textvariable = dd).pack()

    lblmm = Label(date_frame, text = "Publication Month").pack()
    month = Entry(date_frame, text="MM", textvariable = mm).pack()

    lblyyyy = Label(date_frame, text = "Publication Year").pack()
    year = Entry(date_frame, text="YYYY", textvariable = yyyy).pack()

    option_frame = Frame(res_req_win)
    option_frame.pack(side = RIGHT)

    author = get_author()
    authorlb = author_lb(res_req_win, option_frame, author)

    c.execute("select count(BookID) from novel")
    bookid = c.fetchone()[0] + 1

    rpt = Button(date_frame, text="Enter Novel",
                 command = lambda: check_and_enter_selection(dd.get(), mm.get(), yyyy.get(),
                            author[authorlb.curselection()[0]][0], bookid, nn.get())).pack()
                           

    res_req_win.mainloop()
    
#This shows the author options 
def author_lb(w, f, author):

    lblauthor = Label(f,text = "AuthorID, Date of Birth, Author").pack(side = TOP)

    Lb = Listbox(f, height = 8, width = 26,font=("arial", 12), exportselection = False) 
    Lb.pack(side = TOP, fill = Y)
                
    scroll = Scrollbar(w, orient = VERTICAL) 
    scroll.config(command = Lb.yview)
    scroll.pack(side = RIGHT, fill = Y)
    Lb.config(yscrollcommand = scroll.set)
    

    i = 0
    for author in author:
        Lb.insert(i, author)
        i += 1
    Lb.selection_set(first = 0)

    return Lb


# This function checks for errors in the system and spits out an error message if there are.
def check_and_enter_selection(d, m, y, a, b, n):

    try: 
        dt = date(int(y), int(m) , int(d))
        add_novel(dt, a, b, n)
        messagebox.showinfo("Success", "Your Novel has been added")

    except:
        messagebox.showinfo("Error- Try again", "Possible errors:  \nthere is already a novel for that combination, you chose an invalid author\nthe date is in an invalid format, \nsomeone else is entering a novel at the same time")
        return


#Actual Code
render_menu()


