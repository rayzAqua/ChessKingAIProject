from tkinter import *
from PIL import ImageTk, Image
import tkinter.messagebox as messagebox
import pymssql as MSSQLCnn
import FormMainMenu
from config import IP, MSSQL_LOGIN, MSSQL_PASSWORD, DB_NAME, LEVEL
import FormGamePlay


def ClickToLogin():
    if usernameEntry.get().strip() == "" or passwordEntry.get().strip() == "":
        messagebox.showerror("Error", "All Fields Are Required")
    else:
        #MSSQL Server ConnectingString
        try:
            MSSQLdb = MSSQLCnn.connect(IP, MSSQL_LOGIN, MSSQL_PASSWORD, DB_NAME)
            mySQLCursor = MSSQLdb.cursor()
        except:
            messagebox.showerror('Error', 'Database Connectivity Issue, Please Try Again')
            return
        mySQLCursor.execute("Select * from player where username = '" + usernameEntry.get().strip() + "' and password = '" + passwordEntry.get().strip() + "';")
        mySQLResult = mySQLCursor.fetchone()
        if mySQLResult == None:
            messagebox.showerror("Error", "Invalid Username or Password")
        else:
            messagebox.showinfo("Success", "Successfully Login")
            # print(showInformation())
            # root.destroy()
            level = showLevel()
            res = ""
            for i in level:
                res += str(i)
            level = int(res)
            FormMainMenu.onePlayer(level)

        MSSQLdb.close()
        mySQLCursor.close()

def SignupPage(event):
    root.destroy()
    import FormSignUp

def showInformation():
    MSSQLdb = MSSQLCnn.connect(IP, MSSQL_LOGIN, MSSQL_PASSWORD, DB_NAME)
    mySQLCursor = MSSQLdb.cursor()
    mySQLCursor.execute("Select username, id_level from player where username = '" + usernameEntry.get().strip() + "' and password = '" + passwordEntry.get().strip() + "';")
    # mySQLCursor.execute("Select username, id_level from player where username = '" + '123' + "' and password = '" + '123' + "';")
    mySQLResult = mySQLCursor.fetchone()
    MSSQLdb.close()
    mySQLCursor.close()
    return mySQLResult

def updateLevel():
    username, temp = showInformation()
    MSSQLdb = MSSQLCnn.connect(IP, MSSQL_LOGIN, MSSQL_PASSWORD, DB_NAME)
    level = FormGamePlay.Level()
    mySQLCursor = MSSQLdb.cursor()
    mySQLCursor.execute("UPDATE player SET id_level = " + str(level) + " where username = '" + username + "';")
    MSSQLdb.commit()
    mySQLCursor.close()
    MSSQLdb.close()

def showLevel():
    MSSQLdb = MSSQLCnn.connect(IP, MSSQL_LOGIN, MSSQL_PASSWORD, DB_NAME)
    mySQLCursor = MSSQLdb.cursor()
    # mySQLCursor.execute("SELECT id_level FROM dbo.player WHERE username = '" + usernameEntry.get().strip() + "' and password = '" + passwordEntry.get().strip() + "';")
    mySQLCursor.execute("SELECT level_name FROM dbo.player as p, dbo.level as l WHERE username = '" + usernameEntry.get().strip() + "' and password = '" + passwordEntry.get().strip() + "' and p.id_level = l.id_level;")
    mySQLResult1 = mySQLCursor.fetchone()
    print(mySQLResult1)
    MSSQLdb.close()
    mySQLCursor.close()
    # print(usernameEntry.get())
    return mySQLResult1
    
root = Tk()
root.title("SIGNIN")

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

width = 800
height = 800
x = (screen_width / 2) - (width / 2)
y = (screen_height / 2) - (height / 2)

root.geometry(f'{width}x{height}+{int(x)}+{int(y)}')
root.resizable(False, False)

bgImage = ImageTk.PhotoImage(file="guiPNG/bgpxl.png")
bgLabel = Label(root, image=bgImage)
bgLabel.grid()

heading = Label(root, text='USER LOGIN', font=('Verdana', 30, 'bold'), bg= '#D9E6F9', fg='firebrick1').place(x=250, y=100)

usernameLabel = Label(root, text='Username', font=('Verdana', 20), bg= '#D9E6F9', fg='firebrick1').place(x=100, y=250)
usernameEntry = Entry(root, width=22, font=('Verdana', 20), bg='white', fg='firebrick1')
usernameEntry.place(x=300, y=250)

passwordLabel = Label(root, text='Password', font=('Verdana', 20), bg= '#D9E6F9', fg='firebrick1').place(x=100, y=330)
passwordEntry = Entry(root, width=22, font=('Verdana', 20), bg='white', fg='firebrick1', show='*')
passwordEntry.place(x=300, y=330)

signinButton = Button(root, text='SIGNIN', font=('Verdana', 30, 'bold'), bd=0, fg='white', bg='firebrick1', cursor='hand2', command=ClickToLogin)
signinButton.place(x=300, y=480)

noaccountLabel = Label(root, text='Don\'t have an account?', font=('Verdana', 15), bg= '#D7F0FF', fg='firebrick1')
noaccountLabel.place(x=150, y=620)


signupLabel = Label(root, text='Create new one', font=('Verdana', 15, 'bold underline'), bg= '#D7F0FF', fg='firebrick1', cursor='hand2')
signupLabel.place(x=450, y=620)
signupLabel.bind("<Button-1>", SignupPage)

def exit():
    root.quit()

def formSignin():
    root.mainloop()