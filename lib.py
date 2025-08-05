from db import Db
import time
import pandas as pd
import pyttsx3

class LMS:
    def __init__(self, a):
        self.db = a
    def creating_account(self):
        id = int(input("ENTER YOUR STUDENT ID :"))
        q1 = f"SELECT STUDENT_ID FROM STUDENTS WHERE STUDENT_ID = {id}"
        cursor = self.db.cursor()
        cursor.execute(q1)
        result = cursor.fetchone()
        if result:
            print("IT SEEMS LIKE YOU HAVE ALREADY CREATED A ACCOUNT")
            s.say("IT SEEMS LIKE YOU HAVE ALREADY CREATED A ACCOUNT")
            s.runAndWait()
            time.sleep(3)
        else:
            name = input("ENTER YOUR NAME :")
            city = input("ENTER YOUR CITY :")
            phone = input("ENTER YOUR PHONE NUMBER :")
            q2 = f"INSERT INTO STUDENTS VALUES({id},'{name}','{city}','{phone}',0)"
            cursor.execute(q2)
            self.db.commit()
            print("IT'S A GOOD NEWS, YOUR ACCOUNT HAS BEEN CREATED SUCCESSFULLY")
            s.say("IT'S A GOOD NEWS, YOUR ACCOUNT HAS BEEN CREATED SUCCESSFULLY")
            s.runAndWait()
    def book_issue(self):
     id = int(input("ENTER YOUR STUDENT ID :"))
     q1 = f"SELECT STUDENT_ID, PENALTY, STUDENT_NAME FROM STUDENTS WHERE STUDENT_ID = {id}"
     cursor = self.db.cursor()
     cursor.execute(q1)
     result = cursor.fetchone()
     if result is None:
        print("Sorry! It seems like you have not created an account in our library.")
        s.say("Sorry! It seems like you have not created an account in our library.")
        s.runAndWait()
     else:
        if result[1] > 0:
            print(f"Oops! It looks like you have a pending penalty of ₹{result[1]}. Kindly clear it before proceeding further.")
            s.say(f"Oops! It looks like you have a pending penalty of ₹{result[1]}. Kindly clear it before proceeding further.")
            s.runAndWait()
        else:
            id2 = int(input("ENTER THE BOOK ID :"))
            q2 = f"SELECT QUANTITY FROM BOOKS_DETAILS WHERE BOOK_ID = {id2}"
            cursor.execute(q2)
            result2 = cursor.fetchone()
            if result2 == None:
                print(f"SORRY! Book with ID {id2} is not available.")
                s.say(f"SORRY! Book with ID {id2} is not available.")
                s.runAndWait()
            else:
                date = input("ENTER THE DATE OF ISSUE (YYYY-MM-DD) :")
                q3 = f"INSERT INTO BOOKS_ISSUED (STUDENT_ID, BOOK_ID, ISSUE_DATE) VALUES ({id}, {id2}, '{date}')"
                cursor.execute(q3)
                q4 = f"UPDATE BOOKS_DETAILS SET QUANTITY = QUANTITY - 1 WHERE BOOK_ID = {id2}"
                cursor.execute(q4)
                self.db.commit()
                print(f"HAPPY TO SHARE THAT THE BOOK HAS BEEN SUCCESSFULLY ISSUED TO {result[2]}")
                s.say(f"HAPPY TO SHARE THAT THE BOOK HAS BEEN SUCCESSFULLY ISSUED TO {result[2]}")
                s.runAndWait()
   
       
    
    def book_return(self):
      id = int(input("ENTER YOUR STUDENT ID :"))
      book_id = int(input("ENTER THE BOOK ID :"))
      return_date = input("ENTER THE DATE OF RETURN (YYYY-MM-DD) : ")
      cursor = self.db.cursor()

      q1 = f"SELECT BOOK_ID FROM BOOKS_ISSUED WHERE BOOK_ID = {book_id}"
      cursor.execute(q1)
      result = cursor.fetchone()

      if result is None:
         print("SORRY! No such book issue record found.")
         s.say("SORRY! No such book issue record found.")
         s.runAndWait()
      else:
        book_id = result[0]

        
        q4 = f"SELECT ISSUE_DATE FROM BOOKS_ISSUED WHERE BOOK_ID = {book_id}"
        cursor.execute(q4)
        result_issue = cursor.fetchone()

        if result_issue:
            issue_date_str = result_issue[0]
            issue_date = pd.to_datetime(issue_date_str)
            return_date = pd.to_datetime(return_date)

            days_diff = (return_date - issue_date).days
            penalty = 0

            if days_diff > 10:
                penalty = (days_diff - 10) * 5

            try:
                q2 = f"INSERT INTO BOOKS_RETURNED (ISSUE_ID, RETURN_DATE) VALUES ({issue_id}, '{return_date.strftime('%Y-%m-%d')}')"
                cursor.execute(q2)

                q3 = f"UPDATE BOOKS_DETAILS SET QUANTITY = QUANTITY + 1 WHERE BOOK_ID = {book_id}"
                cursor.execute(q3)

                q5 = f"UPDATE STUDENTS SET PENALTY = PENALTY + {penalty} WHERE STUDENT_ID = {id}"
                cursor.execute(q5)

                self.db.commit()

                print("BOOK RETURNED SUCCESSFULLY!")
                s.say("BOOK RETURNED SUCCESSFULLY!")
                s.runAndWait()

                if penalty > 0:
                    print(f"You returned the book {days_diff} days after issue. A penalty of ₹{penalty} has been added to your account.")
                    s.say(f"You returned the book {days_diff} days after issue. A penalty of ₹{penalty} has been added to your account.")
                    s.runAndWait()
                else:
                    print("Thank you for returning the book on time!")
                    s.say("Thank you for returning the book on time!")
                    s.runAndWait()

            except Exception as e:
                self.db.rollback()
                print("An error occurred while returning the book: ,e")
                s.say("An error occurred while returning the book")
                s.runAndWait()
        else:
            print("No issue date found for the given issue ID.")
            s.say("No issue date found for the given issue ID.")
            s.runAndWait()

    def check_penalty(self):
        id =  int(input("ENTER STUDENT ID: "))
        q1 = f"SELECT PENALTY FROM STUDENTS WHERE STUDENT_ID = {id}"
        cursor = self.db.cursor()
        cursor.execute(q1)
        result = cursor.fetchone()
        if result:
            print(f"Your penalty is {result[0]}")
            s.say(f"Your penalty is {result[0]}")
            s.runAndWait()
        else:
            print("No penalty found for the given student ID.") 
            s.say("No penalty found for the given student ID.")
            s.runAndWait()
            
    def pay_penalty(self):
        id =  int(input("ENTER STUDENT ID: "))
        q1 = f"SELECT PENALTY FROM STUDENTS WHERE STUDENT_ID = {id}"
        cursor = self.db.cursor()
        cursor.execute(q1)
        result = cursor.fetchone()
        if result is None:
            print("HAPPY TO SAY THAT THERE IS NO PENALTY TO {name} .")
            s.say("HAPPY TO SAY THAT THERE IS NO PENALTY TO {name}.")
            s.runAndWait()
        else:
            print(f"your current penalty is {result[0]}")
            s.say(f"your current penalty is {result[0]}")
            s.runAndWait()
            penalty = int(input("Enter the amount to pay: "))
            if penalty > result[0]:
                print("You have entered more than your penalty.")
                s.say("You have entered more than your penalty.")
                s.runAndWait()
            else:
                q2 = f"UPDATE STUDENTS SET PENALTY = PENALTY - {penalty} WHERE STUDENT_ID = {id}"
                cursor.execute(q2)
                self.db.commit()
                print(f"Your penalty has been paid successfully. Your remaining penalty is {result[0]-penalty}")
                s.say(f"Your penalty has been paid successfully. Your remaining penalty is {result[0]-penalty}")
                s.runAndWait()
    def display(self):
        q1 = "SELECT * FROM BOOKS_DETAILS"
        cursor = self.db.cursor()
        cursor.execute(q1)
        result = cursor.fetchall()
        df = pd.DataFrame({"Book_id":[],"Book_name":[],"Author":[], "Quantity":[]})
        for i in range(len(result)):
            df.loc[i] = result[i]
        print(df)



obj = Db()
db_connect = obj.creating_connection()

if db_connect is None:
    print("Failed to connect to the database. Please check your credentials or server status.")
    exit()

obj2 = LMS(db_connect)
s = pyttsx3.init()
voices = s.getProperty('voices')
s.setProperty('voice',voices[1].id)

print("Welcome! In this library, every page opens a new possibility.")
while True:
    time.sleep(3)
    print("1.Creating account\n2.Book issusing\n3.Book returning\n4.Checking penalty\n5.Paying penalty\n6.Available books\n7.Exit")
    n = int(input("Choose one of the above: "))
    if n == 7:
        time.sleep(2)
        print("Like every good book, we hope your visit was a memorable page in your day.")
        s.say("Like every good book, we hope your visit was a memorable page in your day.")
        s.runAndWait()
        break
    elif n == 6:
        obj2.display()
    elif n == 1:
        obj2.creating_account()
    elif n == 2:
        obj2.book_issue()
    elif n == 3:
        obj2.book_return()
    elif n == 4:
        obj2.check_penalty()
    elif n == 5:
        obj2.pay_penalty()
    
    else:
        print("That’s a lovely choice, but it’s not a valid option. Let’s find the right one together!")
        s.say("That’s a lovely choice, but it’s not a valid option. Let’s find the right one together!")
        s.runAndWait()
