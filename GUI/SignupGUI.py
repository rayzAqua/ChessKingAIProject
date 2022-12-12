from tkinter import *
import tkinter.messagebox as messagebox
from PIL import ImageTk
import pymssql as MSSQLCnn


def SigninPage(event):
    root.destroy()
    import SigninGUI
    
def ClickToSignup():
    if fullnameEntry.get() == "" or usernameEntry.get().strip() == "" or passwordEntry.get().strip() == "" or confirmEntry.get().strip() == "":
        messagebox.showerror("Error", "All Fields Are Required")
    elif passwordEntry.get() != confirmEntry.get():
        messagebox.showerror("Error", "Password Mismatch")
    else:
        try:
            MSSQLdb = MSSQLCnn.connect("192.168.1.9", "sa", "123", "ChessAIProject")
            mySQLCursor = MSSQLdb.cursor()
            # mySQLCursor1 = MSSQLdb.cursor()
        except:
            messagebox.showerror('Error', 'Database Connectivity Issue, Please Try Again')
            return
        mySQLCursor.execute("Select * from player where username = '" + usernameEntry.get().strip() + "';")
        user = mySQLCursor.fetchone()
        if user is not None:
            messagebox.showerror("Error", "Username already exists")
            return
        mySQLCursor.execute("insert into player (fullname, username, password) values ('" + fullnameEntry.get().strip() +"', '" + usernameEntry.get().strip() + "', '" + passwordEntry.get().strip() + "');")
        MSSQLdb.commit()
        messagebox.showinfo("Success", "Successfully Register")

        MSSQLdb.close()
        mySQLCursor.close()
            


root = Tk()
root.title("Register")

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

width = 800
height = 800
x = (screen_width / 2) - (width / 2)
y = (screen_height / 2) - (height / 2)

root.geometry(f'{width}x{height}+{int(x)}+{int(y)}')
root.resizable(False, False)

bgImage = ImageTk.PhotoImage(file="bgpxl.png")
bgLabel = Label(root, image=bgImage)
bgLabel.grid()

heading = Label(root, text='CREATE AN ACCOUNT', font=('Verdana', 30, 'bold'), bg= '#D9E6F9', fg='firebrick1').place(x=150, y=50)

fullnameLabel = Label(root, text='Fullname', font=('Verdana', 20), bg= '#D9E6F9', fg='firebrick1').place(x=45, y=150)
fullnameEntry = Entry(root, width=22, font=('Verdana', 20), bg='white', fg='firebrick1')
fullnameEntry.place(x=330, y=150)

usernameLabel = Label(root, text='Username', font=('Verdana', 20), bg= '#D9E6F9', fg='firebrick1').place(x=45, y=230)
usernameEntry = Entry(root, width=22, font=('Verdana', 20), bg='white', fg='firebrick1')
usernameEntry.place(x=330, y=230)

passwordLabel = Label(root, text='Password', font=('Verdana', 20), bg= '#D9E6F9', fg='firebrick1').place(x=45, y=310)
passwordEntry = Entry(root, width=22, font=('Verdana', 20), bg='white', fg='firebrick1', show='*')
passwordEntry.place(x=330, y=310)

confirmLabel = Label(root, text='Confirm Password', font=('Verdana', 20), bg= '#D9E6F9', fg='firebrick1').place(x=45, y=390)
confirmEntry = Entry(root, width=22, font=('Verdana', 20), bg='white', fg='firebrick1', show='*')
confirmEntry.place(x=330, y=390)

signupButton = Button(root, text='SIGNUP', font=('Verdana', 30, 'bold'), bd=0, fg='white', bg='firebrick1', cursor='hand2', command=ClickToSignup)
signupButton.place(x=300, y=480)

alreadyaccountLabel = Label(root, text='Already have an account?', font=('Verdana', 15), bg= '#D7F0FF', fg='firebrick1').place(x=250, y=620)

loginLabel = Label(root, text='Login', font=('Verdana', 15, 'bold underline'), bg= '#D7F0FF', fg='firebrick1', cursor='hand2')
loginLabel.place(x=550, y=620)
loginLabel.bind("<Button-1>", SigninPage)


root.mainloop()