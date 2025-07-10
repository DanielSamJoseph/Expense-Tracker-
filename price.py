from shlex import join
import sqlite3
from datetime import datetime
today = datetime.now().strftime("%Y-%m-%d")

conn = sqlite3.connect('expense_tracker\\price.sqlite')
cur = conn.cursor()

cur.execute('''
CREATE TABLE IF NOT EXISTS Price (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    amount REAL NOT NULL,
    category TEXT NOT NULL,
    note TEXT,
    date TEXT NOT NULL
)
''')

while True:
    user=int(input("what would you like to do \n" 
    "1. add_expense()\n"
    "2. view_expenses()\n"
    "3. delete_expense()\n"
    "4. get_daily_summary()\n"
    "5. filter_by_category()\n"
    "6. exit_app() \n"
    "Enter your response:"))



    def add_expense():
        x=input('What is the category where ur saving:')
        y=float(input('Enter amount:'))
        z=input('Anything you want to say:')
        d=(input('Do you want to enter a custom date? (y/n):')).lower()
        if d=="y":
            d=(input('date:'))
        else:
            d=today
        cur.execute('''
    INSERT INTO Price (amount, category, note, date)
    VALUES (?, ?, ?, ?)
    ''', (y, x, z, d))
        conn.commit()
        print("Expense saved.")



    def view_expense():
        info = cur.execute('''select * from price''')
        for line in info:
            x = ' || '.join(str(item) for item in line)
            print(x)
            print("-----------------------------")



    def delete_expense():
        view_expense()
        id=int(input("Enter the id of the expense you want to delete: "))
        cur.execute('''DELETE FROM PRICE WHERE id=?''', (id,))
        conn.commit()
        print("Expense deleted.")



    def get_daily_summary():
        choice = int(input("Do you want to see today's summary or from a specific ID (select 1 or 2):\n"))

        if choice == 1:
            cur.execute('''SELECT * FROM Price WHERE date=?''', (today,))
            info = cur.fetchall()

            if info:
                print("Today's Expenses for", today)
                print("-----------------------------")
                total = sum(item[1] for item in info)
                print("Total Expenses:", total)
                print("\nBreakdown of Expenses:")

                for item in info:
                    print(f" Category: {item[2]}")
                    print(f" Amount  : {item[1]}")
                    print(f" Note    : {item[3]}")
                    print(f" Date    : {item[4]}")
                    print("-----------------------------")
            else:
                print("No expenses found for today.")

        elif choice == 2:
            id = int(input("Enter the ID: "))
            cur.execute('''SELECT * FROM Price WHERE id=?''', (id,))
            info = cur.fetchall()

            if info:
                print("Expenses for ID", id)
                print("-----------------------------")
                for item in info:
                    print(f" Category: {item[2]}")
                    print(f" Amount  : {item[1]}")
                    print(f" Note    : {item[3]}")
                    print(f" Date    : {item[4]}")
                    print("-----------------------------")
            else:
                print("No expenses found for ID:", id)



    def filter_by_category():
        category = input("Enter the category to filter by: ")
        cur.execute('''SELECT * FROM Price WHERE LOWER(category) = LOWER(?)''', (category,))
        info = cur.fetchall()
        
        if info:
            print(f"\nExpense under category: {category}")
            print("-" * 60)
            print("ID\tAmount\tCategory\t\tNote\t\t\tDate")
            for row in info:
                print(f"{row[0]}\t{row[1]}\t{row[2]}\t\t{row[3]}\t\t{row[4]}")
            print("-" * 60)
        else:
            print(f"\nNo expenses found for category: {category}")

        


    if user==1:
        add_expense()
    elif user==2:
        view_expense()
    elif user==3:
        delete_expense()
    elif user==4:
        get_daily_summary()
    elif user==5:
        filter_by_category()
    elif user==6:
        print("Exiting the app.")
        break
    else:
        print("something is wrong")