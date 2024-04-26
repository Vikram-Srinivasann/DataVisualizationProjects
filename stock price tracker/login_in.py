from tkinter import *
from PIL import ImageTk, Image
import stock_price_tracker as spt
import mysql.connector
import tkinter.messagebox as messagebox

#functions
def on_enter1():
    urn = username.get()
    return urn
    
def on_enter2():
    pwd = password.get()
    return pwd

def check_login():
    urn = on_enter1()
    pwd = on_enter2()
    c.execute("SELECT * FROM login_details;")
    result = c.fetchall()
    for row in result:
        if row[0] == urn:
            if row[1] == pwd:
                root.destroy()
                spt.main()
            else:
                password.delete(0, END)
                messagebox.showerror("Login Failed", "Invalid Username or Password!")
        
#gui
root = Tk()
root.geometry("1000x500")
root.resizable(0,0)
root.title("Stock Management System")
user_name = StringVar()
pass_word = StringVar()


conn = mysql.connector.connect(user='username',
                                host='hostname',
                                password="password",
                                database="stock_management_system")
c = conn.cursor()

image = Image.open("stock_graph.jpg")
background_image = ImageTk.PhotoImage(image)

Label1 = Label(root ,image=background_image)
Label1.place(x=-100, y=-800)

signin = Label(root,text="SIGN-IN",font=('Arial',20,'bold'), highlightbackground="SystemButtonFace",  bg="SystemButtonFace")
signin.place(x=450,y=100)

signin = Label(text="Username:",font=('Time New Roman',15))
signin.place(x=400,y=150)

username = Entry(width=15, font=(10))
username.place(x=400,y=200)
signin = Label(text="Password:",font=('Time New Roman',15))
signin.place(x=400,y=250)

password = Entry(root,width=15, show="*", font=(10))
password.place(x=400,y=300)

login_button = Button(root ,text="LOGIN",font=('Arial',10,'bold'),cursor='hand2',width=10, command=lambda:(check_login()), fg="white", bg="black")
login_button.place(x=450,y=350)
root.mainloop()
