import tkinter as tk 
from tkinter import *
from tkinter import ttk 
from tkinter.ttk import *

root = Tk()
# width and height
w = 450
h = 525
# background color
bgcolor = "#bdc3c7"

# ----------- CENTER FORM ------------- #
root.overrideredirect(1) # remove border
ws = root.winfo_screenwidth()
hs = root.winfo_screenheight()
x = (ws-w)/2
y = (hs-h)/2
root.geometry("%dx%d+%d+%d" % (w, h, x, y))

# ----------- HEADER ------------- #

headerframe = tk.Frame(root, highlightbackgroun='yellow', highlightcolor='yellow', highlightthickness=2, bg='#95a5a6', width=w, height=70)
titleframe = tk.Frame(headerframe, bg='yellow', padx=1, pady=1)
title_label = tk.Label(titleframe, text='Register', padx=20, pady=5, bg='green', fg='#fff', font=('Tahoma',24), width=8)
close_button = tk.Button(headerframe, text='x', borderwidth=1, relief='solid', font=('Verdana',12))

headerframe.pack()
titleframe.pack()
title_label.pack()
close_button.pack()

titleframe.place(y=26, relx=0.5, anchor=CENTER)
close_button.place(x=410, y=10)

# close window
def close_win():
    root.destroy()

close_button['command'] = close_win

# ----------- END HEADER ------------- #

mainframe = tk.Frame(root, width=w, height=h)

# ----------- Login Page ------------- #
loginframe = tk.Frame(mainframe, width=w, height=h)
login_contentframe = tk.Frame(loginframe, padx=30, pady=100, highlightbackgroun='yellow', highlightcolor='yellow', highlightthickness=2, bg=bgcolor)

username_label = tk.Label(login_contentframe, text='Username:', font=('Verdana',16), bg=bgcolor)
password_label = tk.Label(login_contentframe, text='Password:', font=('Verdana',16), bg=bgcolor)

username_entry = tk.Entry(login_contentframe, font=('Verdana',16))
password_entry = tk.Entry(login_contentframe, font=('Verdana',16), show='*')

login_button = tk.Button(login_contentframe,text="Login", font=('Verdana',16), bg='#2980b9',fg='#fff', padx=25, pady=10, width=25)
go_register_label = tk.Label(login_contentframe, text=">>Don't have an account? Create one" , font=('Verdana',10), bg=bgcolor, fg='red')

mainframe.pack(fill='both', expand=1)
loginframe.pack(fill='both', expand=1)
login_contentframe.pack(fill='both', expand=1)

username_label.grid(row=0, column=0, pady=10)
username_entry.grid(row=0, column=1)

password_label.grid(row=1, column=0, pady=10)
password_entry.grid(row=1, column=1)

login_button.grid(row=2, column=0, columnspan=2, pady=40)
go_register_label.grid(row=3, column=0, columnspan=2, pady=20)

# create a function to display the register frame
def go_to_register():
    loginframe.forget()
    registerframe.pack(fill="both", expand=1)
    title_label['text'] = 'Register'
    title_label['bg'] = '#27ae60'

go_register_label.bind("<Button-1>", lambda page: go_to_register())

# ----------- Register Page ------------- #

registerframe = tk.Frame(mainframe, width=w, height=h)
register_contentframe = tk.Frame(registerframe, padx=15, pady=75, highlightbackgroun='yellow', highlightcolor='yellow', highlightthickness=2, bg=bgcolor)

fullname_label_rg = tk.Label(register_contentframe, text='Fullname:', font=('Verdana',14), bg=bgcolor)
username_label_rg = tk.Label(register_contentframe, text='Username:', font=('Verdana',14), bg=bgcolor)
password_label_rg = tk.Label(register_contentframe, text='Password:', font=('Verdana',14), bg=bgcolor)
confirmpass_label_rg = tk.Label(register_contentframe, text='Re-Password:', font=('Verdana',14), bg=bgcolor)

fullname_entry_rg = tk.Entry(register_contentframe, font=('Verdana',14), width=22)
username_entry_rg = tk.Entry(register_contentframe, font=('Verdana',14), width=22)
password_entry_rg = tk.Entry(register_contentframe, font=('Verdana',14), width=22, show='*')
confirmpass_entry_rg = tk.Entry(register_contentframe, font=('Verdana',14), width=22, show='*')

register_button = tk.Button(register_contentframe,text="Register", font=('Verdana',16), bg='#2980b9',fg='#fff', padx=25, pady=10, width=25)
go_login_label = tk.Label(register_contentframe, text=">>Already have an account? Sign in" , font=('Verdana',10), bg=bgcolor, fg='red')

register_contentframe.pack(fill='both', expand=1)

fullname_label_rg.grid(row=0, column=0, pady=5)
fullname_entry_rg.grid(row=0, column=1)

username_label_rg.grid(row=1, column=0, pady=5)
username_entry_rg.grid(row=1, column=1)

password_label_rg.grid(row=2, column=0, pady=5)
password_entry_rg.grid(row=2, column=1)

confirmpass_label_rg.grid(row=3, column=0, pady=5)
confirmpass_entry_rg.grid(row=3, column=1)

register_button.grid(row=5, column=0, columnspan=2, pady=20)
go_login_label.grid(row=6, column=0, columnspan=2, pady=10)

# --------------------------------------- #

# create a function to display the login frame
def go_to_login():
    registerframe.forget()
    loginframe.pack(fill="both", expand=1)
    title_label['text'] = 'Login'
    title_label['bg'] = '#2980b9'

go_login_label.bind("<Button-1>", lambda page: go_to_login())
# --------------------------------------- #

root.mainloop()