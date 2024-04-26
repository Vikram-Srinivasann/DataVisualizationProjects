import requests as rq
import mysql.connector
from tkinter import *
import tkinter.messagebox as messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from datetime import datetime

class Main:
    def __init__(self, root):
        self.root = root
        self.keyword = StringVar()
        self.main_window()

    #GUI
    def update_time(self):
        current_time = datetime.now().strftime('%H:%M:%S %p')
        self.time_label.config(text=current_time, padx=0)
        current_date = datetime.now().strftime('%d-%m-%Y')
        self.date_label.config(text=current_date, padx=0)
        self.root.after(1000, self.update_time)

    def main_window(self):
        self.lbltitle=Label(self.root,bd=50,text="STOCK MANAGEMENT SYSTEM",fg="white",bg="deepskyblue",font=("Arial",40,"bold"))
        self.lbltitle.pack(side=TOP,fill=X)
        self.time_label = Label(self.lbltitle, font=('Helvetica', 14),bg="deepskyblue")
        self.time_label.pack(side=RIGHT)
        self.date_label = Label(self.lbltitle, font=('Helvetica', 14),bg="deepskyblue")
        self.date_label.pack(side=LEFT)
        self.Dataframe1=Frame(self.root, bg="black")
        self.Dataframe1.place(x=0,y=105,width=1535,height=455)
        self.DataframeLeft=LabelFrame(self.Dataframe1, bd=10,padx=10,font=("times new roman",12,"bold"),text="Select The Stock:")
        self.DataframeLeft.place(x=15,y=25, width=775,height=400)
        self.lb = Listbox(self.DataframeLeft)
        self.lb.pack(side=LEFT, fill=BOTH)
        self.update_time()
        self.list_box()
        self.DataframeRight = LabelFrame(self.Dataframe1, bd=10 ,padx=10,font=("times new roman",12,"bold"),text="Graph:")  
        self.DataframeRight.place(x=785,y=25,width=725,height=400)
        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.DataframeRight)
        self.ax = self.fig.add_subplot(111)
        btn1 = Button(self.DataframeLeft, text='SHOW', fg='Black',bg="white" ,width=20, command=lambda:(self.ax.clear(), self.select_item())).pack()
        btn2 = Button(self.DataframeLeft, text='ADD', fg='Black',bg="white" , width=20, command=self.openNewWindow).pack()
        btn3 = Button(self.DataframeLeft, text='DELETE', fg='Black',bg="white" , width=20, command=self.delete_item).pack()
        self.Dataframe2=Frame(self.root,bd=20, bg="black")
        self.Dataframe2.place(x=0,y=530,width=1535,height=255)
        self.DataframeBottom=LabelFrame(self.Dataframe2, bd=10,padx=10,font=("times new roman",12,"bold"),text="Details:", background="white")  
        self.DataframeBottom.place(x=5,y=5,width=1490,height=210)
        self.pr = Label(self.DataframeBottom,font=("times new roman",11, "bold"),text="", background="white")
        self.pr.pack(fill=X)
        self.ne = Label(self.DataframeBottom,font=("times new roman",10),text="", background="white")
        self.ne.pack(fill=X)

    def select_item(self):
        for i in self.lb.curselection():
            self.selected_item(self.lb.get(i))

    def list_box(self):
        scrollbar = Scrollbar(self.DataframeLeft)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.lb.config(yscrollcommand = scrollbar.set, width=100)
        scrollbar.config(command=self.lb.yview)
        mycursor.execute("SELECT * FROM stock_details ORDER BY company_name ASC;")
        myresult = mycursor.fetchall()
        self.lb.delete(0, END)

        for row in myresult:
            self.lb.insert(END, row[1])
        scrollbar.quit()
        
    def openNewWindow(self):
        newWindow = Toplevel(master=self.DataframeLeft, bg="black")
        newWindow.title("Add new Stocks:")
        newWindow.geometry("250x100")
        newWindow.resizable(0, 0)
        label = Label(newWindow, text ="Enter the new keyword", bg="black", fg="white")
        label.place(x=50, y=10)
        entry = Entry(newWindow, textvariable=self.keyword, width=25)
        entry.place(x=50, y=40)
        bt1 = Button(newWindow, text="Ok", background = "white", command = lambda:(self.search_data(), newWindow.destroy()), width=10)
        bt1.place(x=25, y=70)
        bt2 = Button(newWindow, text="cancel",  background = "white", command = lambda:(newWindow.destroy()), width=10)
        bt2.place(x=150, y=70)
        newWindow.mainloop()

    def plot_graph(self):
        mycursor.execute('SELECT * FROM stock_price;')
        data = mycursor.fetchall()
        x = [row[0] for row in data]
        y = [row[1] for row in data]
        self.ax.plot(x, y)
        self.ax.set_xlabel("Date")
        self.ax.set_ylabel("Price")
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=True)

    #Functions
    def add_data(self, stock_symbol, company_name):
        try:
            try:
                    sql = "INSERT INTO stock_details(symbol, company_name) VALUE (%s, %s);"
                    val = (stock_symbol, company_name)
                    mycursor.execute(sql, val)
                    mydb.commit()
                    messagebox.showinfo("Added", "Added Successfully")
            except:
                messagebox.showinfo("info", "Data Already Exsist")
        except:
            mycursor.execute("CREATE TABLE stock_details(symbol VARCHAR(100), company_name VARCHAR(100), CONSTRAINT stock_det UNIQUE(symbol, company_name))")
            mydb.commit()
            self.add_data(stock_symbol, company_name)                
        self.list_box()
        
    def stock_response_name(self, keywords, stock_api_key):
        stock_data_url = f"https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={keywords}&apikey={stock_api_key}"
        stock_response = rq.get(stock_data_url)
        return stock_response

        
    def stock_response_data(self, stock_response):
        stock_api_key = 'API_key'
        COMPANY_NAME = stock_response.json()["bestMatches"][0]['2. name']
        STOCK_SYMBOL = stock_response.json()["bestMatches"][0]['1. symbol']   
        stock_price_url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={STOCK_SYMBOL}&apikey={stock_api_key}'
        stock_resp = rq.get(stock_price_url) 
        return COMPANY_NAME, STOCK_SYMBOL, stock_resp

    def news_api(self, company_name):
        NEWS_API_KEY = 'API_key'
        NEWS_API = "https://newsapi.org/v2/everything"
        news_params = {
        'apiKey' : NEWS_API_KEY,
            'q' : company_name
        }
        news_response = rq.get(url=NEWS_API, params=news_params)
        title = news_response.json()['articles'][0]['title']
        content = news_response.json()['articles'][0]['content']
        return (f"\nHeading:\n{title}\n\nContent:\n{content}")

    def create_table(self, date_price_dict):
        try:
            for key, value in date_price_dict.items():
                date_string = key
                date_format = '%Y-%m-%d'
                date_object = datetime.strptime(date_string, date_format)
                date_only = date_object.date()
                mycursor.execute(("INSERT INTO stock_price (close_date, price) VALUE (%s, %s);"),(date_only, value))
                mydb.commit()
        except:
            try:
                sql= "CREATE TABLE stock_price (close_date DATE, price FLOAT(2), CONSTRAINT date_price UNIQUE(close_date));"
                mycursor.execute(sql)
                mydb.commit()
                self.create_table(date_price_dict)
            except:
                mycursor.execute("DROP TABLE stock_price;")
                mydb.commit()

    def selected_item(self, item):
        keywords = item
        stock_api_key = 'API_key'
        stock_response = self.stock_response_name(keywords, stock_api_key)
        stock_data = self.stock_response_data(stock_response)
        company_name = stock_data[0]
        stock_symbol = stock_data[1]
        resp = stock_data[2]
        data = resp.json()['Time Series (Daily)']
        date_list = [item for item in data]
        yesterday_data = data[date_list[0]]
        yesterday_closing_price = yesterday_data['4. close']
        day_before_yesterday_data = data[date_list[1]]
        day_before_yesterday_closing_price = day_before_yesterday_data['4. close']
        difference = float(yesterday_closing_price) - float(day_before_yesterday_closing_price)
        diff_per = round(difference / float(yesterday_closing_price) * 100, 2)

        if difference >= 0:
            up_down = '🔺'
        elif difference < 0:
            up_down = '🔻'

        price_list = []
        for date in date_list:
            price = resp.json()["Time Series (Daily)"][date]["4. close"]
            price_list.append(price)
        price_list=list(map(float, price_list))
        pairs = zip(date_list, price_list)
        date_price_dict = dict(pairs)
        price = f"{company_name} ({stock_symbol})\n\n${yesterday_closing_price} ({up_down}{abs(diff_per)})%"
        news = self.news_api(company_name)
        self.pr.config(text=f"{price}")
        self.ne.config(text=f"{news}")
        mycursor.execute('TRUNCATE TABLE stock_price;')
        mydb.commit()
        self.create_table(date_price_dict)
        self.plot_graph()

    def delete_item(self):
        for i in self.lb.curselection():
            delete = self.lb.get(i)
        mycursor.execute("SELECT * FROM stock_details;")
        result = mycursor.fetchall()
        for row in result:
            if row[1] == delete:
                mycursor.execute(("DELETE FROM stock_details WHERE company_name = %s AND symbol = %s;"),(row[1], row[0]))
                messagebox.showinfo("Deleted", "Deleted Successfully")
        mydb.commit()
        self.list_box()

    def search_data(self):
        keywords = self.keyword.get()
        stock_api_key = 'API_key'
        stock_response = self.stock_response_name(keywords, stock_api_key)
        stock_data = self.stock_response_data(stock_response)
        company_name = stock_data[0]
        stock_symbol = stock_data[1]
        self.add_data(stock_symbol, company_name)

    def main(self):
        root=Tk()
        root.title("Stock Management System")
        root.geometry("1540x800")
        obj = Main(root)
        root.mainloop()

mydb = mysql.connector.connect(user="username",
                               password="password",
                               host="hostname",
                               database="stock_price_tracker"
)
mycursor = mydb.cursor()
