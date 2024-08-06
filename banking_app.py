import streamlit as st
import sqlite3
import datetime as dt
from PIL import Image

# Display the logo and bank name


def display_logo():
    st.markdown(
        """
        <style>
        .container {
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .logo {
            margin-right: 20px;
        }
        .bank-name {
            font-size: 48px;
            font-weight: bold;
            color: #FFA500;
        }
        </style>
        """, unsafe_allow_html=True
    )
    col1, col2 = st.columns([1, 3])  # Adjust column ratios as needed

    with col1:
        logo = Image.open('./logo.png')  # Ensure the image is in the 'images' folder
        st.image(logo, width=100)  # Adjust width as needed

    with col2:
        st.markdown('<div class="bank-name">RICH BANK OF INDIA (RBI)</div>', unsafe_allow_html=True)

# Apply pastel theme
def set_theme():
    st.markdown(
        """
        <style>
        body {
            background-color: #3E2723; /* Dark brown background */
            color: #FFFFFF; /* White text color */
        }

        .stTextInput, .stNumberInput, .stTextArea, .stSelectbox, .stDateInput {
            background-color: transparent; /* Transparent background */
            border: none; /* Remove border */
            color: #FFFFFF; /* Text color inside input fields */
        }

        .stButton>button {
            background-color: #FEC89A; /* Pastel orange */
            color: #000000;
        }
        .stButton>button:hover {
            background-color: #FCA5A5; /* Lighter pastel orange on hover */
        }

        .css-1d391kg {
            background-color: #FEC89A; /* Pastel orange for sidebar */
        }
        .css-1d391kg .css-14xtw13 {
            color: #000000; /* Black text color in sidebar */
        }
        </style>
        """, unsafe_allow_html=True
    )

# Create a New Account (Sign Up)
def create_account():
    mycon = sqlite3.connect('banking_system.db')
    mycur = mycon.cursor()

    st.header("Create a New Account (Sign Up)")
    name = st.text_input("Enter Your Name")
    username = st.text_input("Enter Your UserName")
    password = st.text_input("Enter Your Password", type="password")
    today = dt.date.today()
    dob = st.date_input(
        "Enter Your Date of Birth",
        value=today - dt.timedelta(days=18*365),  # Default to 18 years ago
        min_value=dt.date(1900, 1, 1),
        max_value=today
    )
    address = st.text_area("Enter Your Address")
    mobile = st.text_input("Enter Your Mobile Number")
    aadhar = st.text_input("Enter Your Aadhar Number")
    account_type = st.selectbox("Enter Account Type", ['Savings', 'Current'])
    balance = st.number_input("Enter Initial Deposit", min_value=0.0, step=0.01)

    if st.button("Create Account"):
        if not (name and username and password and dob and address and mobile and aadhar and account_type and balance):
            st.error("Please fill out all fields.")
        else:
            dob = dob.strftime('%Y-%m-%d')
            mycur.execute('''
                INSERT INTO bank (UserName, Name, Password, DOB, Address, Mobile_Number, Aadhar_no, Balance, AccountType)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (username, name, password, dob, address, mobile, aadhar, balance, account_type))

            mycon.commit()
            mycon.close()
            st.success("Account Created Successfully!")


# Sign In (Existing Users)
def sign_in():
    mycon = sqlite3.connect('banking_system.db')
    mycur = mycon.cursor()

    st.header("Sign In (Existing Users)")
    username = st.text_input("Enter Your UserName")
    password = st.text_input("Enter Your Password", type="password")

    if st.button("Sign In"):
        if not (username and password):
            st.error("Please enter both username and password.")
        else:
            mycur.execute("SELECT * FROM bank WHERE UserName = ? AND Password = ?", (username, password))
            user = mycur.fetchone()

            if user:
                st.session_state['username'] = username
                st.success(f"Welcome back, {user[1]}!")
            else:
                st.error("Invalid credentials. Please try again.")

    mycon.close()


# View Balance Status
def view_balance(username):
    mycon = sqlite3.connect('banking_system.db')
    mycur = mycon.cursor()

    mycur.execute("SELECT Balance FROM bank WHERE UserName = ?", (username,))
    balance = mycur.fetchone()[0]

    st.write(f"<h2 style='text-align: center; color: #4A5568;'>Your current balance is: {balance} ₹</h2>", unsafe_allow_html=True)

    mycon.close()

# View Account Details
def view_account_details(username):
    mycon = sqlite3.connect('banking_system.db')
    mycur = mycon.cursor()

    mycur.execute("SELECT * FROM bank WHERE UserName = ?", (username,))
    user = mycur.fetchone()

    if user:
        st.write("<h2 style='text-align: center; color: #C05621;'>--- Account Details ---</h2>", unsafe_allow_html=True)
        st.write(f"<h3 style='text-align: center;'>Name: {user[1]}</h3>", unsafe_allow_html=True)
        st.write(f"<h3 style='text-align: center;'>Date of Birth: {user[3]}</h3>", unsafe_allow_html=True)
        st.write(f"<h3 style='text-align: center;'>Address: {user[4]}</h3>", unsafe_allow_html=True)
        st.write(f"<h3 style='text-align: center;'>Mobile Number: {user[5]}</h3>", unsafe_allow_html=True)
        st.write(f"<h3 style='text-align: center;'>Aadhar Number: {user[6]}</h3>", unsafe_allow_html=True)
        st.write(f"<h3 style='text-align: center;'>Balance: {user[7]} ₹</h3>", unsafe_allow_html=True)
        st.write(f"<h3 style='text-align: center;'>Account Type: {user[8]}</h3>", unsafe_allow_html=True)
    else:
        st.error("User not found.")

    mycon.close()

# Update Account Details
def update_account_details(username):
    mycon = sqlite3.connect('banking_system.db')
    mycur = mycon.cursor()

    st.header("Update Account Details")
    new_address = st.text_area("Enter New Address")
    new_mobile = st.text_input("Enter New Mobile Number")

    if st.button("Update Details"):
        mycur.execute('''
            UPDATE bank 
            SET Address = ?, Mobile_Number = ? 
            WHERE UserName = ?
        ''', (new_address, new_mobile, username))

        mycon.commit()
        mycon.close()

        st.success("Account details updated successfully!")

# Withdraw Money
def withdraw_money(username):
    mycon = sqlite3.connect('banking_system.db')
    mycur = mycon.cursor()

    st.header("Withdraw Money")
    amount = st.number_input("Enter the amount to withdraw", min_value=0.0, step=0.01)

    if st.button("Withdraw"):
        mycur.execute("SELECT Balance FROM bank WHERE UserName = ?", (username,))
        balance = mycur.fetchone()[0]

        if amount > balance:
            st.error("Insufficient balance.")
        else:
            new_balance = balance - amount
            mycur.execute("UPDATE bank SET Balance = ? WHERE UserName = ?", (new_balance, username))
            mycur.execute("INSERT INTO transactions (UserName, Date, Type, Amount, Balance_After) VALUES (?, ?, ?, ?, ?)", 
                          (username, dt.datetime.now(), 'Withdrawal', amount, new_balance))
            mycon.commit()
            st.success(f"Withdrawal successful. New balance is: {new_balance} ₹")

    mycon.close()


# Deposit Money
def deposit_money(username):
    mycon = sqlite3.connect('banking_system.db')
    mycur = mycon.cursor()

    st.header("Deposit Money")
    amount = st.number_input("Enter the amount to deposit", min_value=0.0, step=0.01)

    if st.button("Deposit"):
        mycur.execute("SELECT Balance FROM bank WHERE UserName = ?", (username,))
        balance = mycur.fetchone()[0]
        
        new_balance = balance + amount
        mycur.execute("UPDATE bank SET Balance = ? WHERE UserName = ?", (new_balance, username))
        mycur.execute("INSERT INTO transactions (UserName, Date, Type, Amount, Balance_After) VALUES (?, ?, ?, ?, ?)", 
                      (username, dt.datetime.now(), 'Deposit', amount, new_balance))
        mycon.commit()
        st.success(f"Deposit successful. New balance is: {new_balance} ₹")

    mycon.close()


# Calculate Interest
def calculate_interest(username):
    mycon = sqlite3.connect('banking_system.db')
    mycur = mycon.cursor()

    mycur.execute("SELECT Balance, AccountType FROM bank WHERE UserName = ?", (username,))
    balance, account_type = mycur.fetchone()

    if account_type == 'Savings':
        interest_rate = 0.04
    else:
        interest_rate = 0.02

    interest = balance * interest_rate / 12
    new_balance = balance + interest
    mycur.execute("UPDATE bank SET Balance = ? WHERE UserName = ?", (new_balance, username))
    mycur.execute("INSERT INTO transactions (UserName, Date, Type, Amount, Balance_After) VALUES (?, ?, ?, ?, ?)", 
                  (username, dt.datetime.now(), 'Interest', interest, new_balance))
    mycon.commit()
    st.success(f"Interest added. New balance is: {new_balance} ₹")

    mycon.close()


# Transaction Report
def transaction_report(username):
    mycon = sqlite3.connect('banking_system.db')
    mycur = mycon.cursor()

    st.header("Transaction History")
    mycur.execute("SELECT Date, Type, Amount, Balance_After FROM transactions WHERE UserName = ? ORDER BY Date DESC", (username,))
    transactions = mycur.fetchall()

    if transactions:
        st.write("<h2 style='text-align: center; color: #C05621;'>--- Transaction History ---</h2>", unsafe_allow_html=True)
        for transaction in transactions:
            st.write(f"<h3 style='text-align: center;'>Date: {transaction[0]}, Type: {transaction[1]}, Amount: {transaction[2]} ₹, Balance After: {transaction[3]} ₹</h3>", unsafe_allow_html=True)
    else:
        st.write("<h3 style='text-align: center;'>No transactions found.</h3>", unsafe_allow_html=True)

    mycon.close()




# Send Money
def send_money(username):
    mycon = sqlite3.connect('banking_system.db')
    mycur = mycon.cursor()

    st.header("Send Money")
    recipient_username = st.text_input("Enter the recipient's username")
    amount = st.number_input("Enter the amount to send", min_value=0.0, step=0.01)

    if st.button("Send Money"):
        mycur.execute("SELECT UserName FROM bank WHERE UserName = ?", (recipient_username,))
        recipient = mycur.fetchone()

        if not recipient:
            st.error("Recipient not found.")
        else:
            mycur.execute("SELECT Balance FROM bank WHERE UserName = ?", (username,))
            sender_balance = mycur.fetchone()[0]

            if amount > sender_balance:
                st.error("Insufficient balance.")
            else:
                new_sender_balance = sender_balance - amount
                mycur.execute("UPDATE bank SET Balance = ? WHERE UserName = ?", (new_sender_balance, username))
                mycur.execute("INSERT INTO transactions (UserName, Date, Type, Amount, Balance_After) VALUES (?, ?, ?, ?, ?)", 
                              (username, dt.datetime.now(), 'Transfer Out', amount, new_sender_balance))
                
                mycur.execute("SELECT Balance FROM bank WHERE UserName = ?", (recipient_username,))
                recipient_balance = mycur.fetchone()[0]
                new_recipient_balance = recipient_balance + amount
                mycur.execute("UPDATE bank SET Balance = ? WHERE UserName = ?", (new_recipient_balance, recipient_username))
                mycur.execute("INSERT INTO transactions (UserName, Date, Type, Amount, Balance_After) VALUES (?, ?, ?, ?, ?)", 
                              (recipient_username, dt.datetime.now(), 'Transfer In', amount, new_recipient_balance))

                mycon.commit()
                st.success(f"Money sent successfully! Your new balance is: {new_sender_balance} ₹")

    mycon.close()

# Main Menu
def main():
    st.set_page_config(page_title="RICH BANK OF INDIA", page_icon=":bank:", layout="wide", initial_sidebar_state="expanded")
    set_theme()
    display_logo()

    menu = ["Sign Up", "Sign In"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Sign Up":
        create_account()
    elif choice == "Sign In":
        sign_in()
        if 'username' in st.session_state:
            username = st.session_state['username']
            st.sidebar.write(f"Logged in as: {username}")
            st.sidebar.button("Logout", on_click=lambda: st.session_state.pop('username', None))

            sub_menu = ["View Balance", "View Account Details", "Update Account Details", "Withdraw Money", "Deposit Money", "Calculate Interest", "Transaction Report", "Send Money"]
            sub_choice = st.sidebar.selectbox("Actions", sub_menu)

            if sub_choice == "View Balance":
                view_balance(username)
            elif sub_choice == "View Account Details":
                view_account_details(username)
            elif sub_choice == "Update Account Details":
                update_account_details(username)
            elif sub_choice == "Withdraw Money":
                withdraw_money(username)
            elif sub_choice == "Deposit Money":
                deposit_money(username)
            elif sub_choice == "Calculate Interest":
                calculate_interest(username)
            elif sub_choice == "Transaction Report":
                transaction_report(username)
            elif sub_choice == "Send Money":
                send_money(username)

if __name__ == '__main__':
    main()
