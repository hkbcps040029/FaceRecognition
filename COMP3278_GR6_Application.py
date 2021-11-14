import urllib
import numpy as np
import mysql.connector
import cv2
import pyttsx3
import pickle
from datetime import datetime
import sys
from pandas import DataFrame
import PySimpleGUI as sg
import tkinter as tk

sg.theme('lightblue3')

globalCurrentName = 'Jack'
globalCurrentID = 1003
globalAccountID = None
prev_currency = 'HKD'

# 1 Create database connection
myconn = mysql.connector.connect(host="localhost", user="root", passwd="123456", database="comp3278gr6")


date = datetime.now()

date = date.strftime('%Y-%m-%d %H:%M:%S')

now = datetime.now()
current_time = now.strftime("%H:%M:%S")
cursor = myconn.cursor()

#Function for logout view
def logout_button(win):
    win.Element('_W_MSG_1_').Update(value='%s, you have logged out, please close this application.' % (globalCurrentName))
    win.Element('_EXIT_').update(visible=True)
    win.Element('_W_MSG_2_').Update(visible=False)
    win.Element('Logout').update(visible=False)
    win.Element('_HISTORY_').Update(visible=False)
    win.Element('_ACCOUNT_').Update(visible=False)
    win.Element('_TV_').Update(visible=False)
    win.Element('trans_frame').update(visible=False)
    win.Element('log_view').update(visible=False)
    win.Element('acc_view').update(visible=False)
    win.Element('trans_back_acc').update(visible=False)
    #exit once Exit button is pressed
    event, values = win.Read()
    exit(0)


#disable/enable search by date for transactions
def disableDates(win, isDisabled):
    win.Element('trans_lowcal').update(disabled=isDisabled)
    win.Element('trans_upcal').update(disabled=isDisabled)

#disable/enable search by year for transactions
def disableYear(win, isDisabled):
    win.Element('trans_year_low').update(disabled=isDisabled)
    win.Element('trans_year_up').update(disabled=isDisabled)

#disable/enable search by month for transactions
def disableMonth(win, isDisabled):
    win.Element('trans_month_low').update(disabled=isDisabled)
    win.Element('trans_month_up').update(disabled=isDisabled)

#disable/enable search by day for transactions
def disableDay(win, isDisabled):
    win.Element('trans_day_low').update(disabled=isDisabled)
    win.Element('trans_day_up').update(disabled=isDisabled)

#disable/enable search by hour for transactions
def disableTime(win, isDisabled):
    win.Element('trans_time_low').update(disabled=isDisabled)

#disable/enable search limits for transactions, to enable search all transactions
def disableDisableButtons(win, isDisabled):
    win.Element('trans_dates_disable').update(disabled=isDisabled)
    win.Element('trans_year_disable').update(disabled=isDisabled)
    win.Element('trans_month_disable').update(disabled=isDisabled)
    win.Element('trans_day_disable').update(disabled=isDisabled)
    win.Element('trans_time_disable').update(disabled=isDisabled)
    win.Element('trans_amount_disable').update(disabled=isDisabled)
    disableDates(win, isDisabled)
    disableYear(win, isDisabled)
    disableMonth(win, isDisabled)
    disableDay(win, isDisabled)
    disableTime(win, isDisabled)
    disableAmount(win, isDisabled)

#disable/enable search by amount for transactions
def disableAmount(win, isDisabled):
    win.Element('trans_amount_low').update(disabled=isDisabled)
    win.Element('trans_amount_up').update(disabled=isDisabled)

#updates sent and received tabs after getting table entries from queries
def updateTabs(send_tab_query, receive_tab_query, win, currency):
    conversion_ratio = {'USD': 1/7, 'HKD': 1, 'INR': 10}
    ratio = conversion_ratio[currency]
    cursor.execute(send_tab_query)
    result = cursor.fetchall()
    df = DataFrame(result)
    dataShown = df.values.tolist()
    for i in range(0,len(dataShown)):
        dataShown[i][3] = f'{ratio * dataShown[i][3] : .2f}'

    win.Element('trans_sent').update(values=dataShown)

    cursor.execute(receive_tab_query)
    result = cursor.fetchall()
    df = DataFrame(result)
    dataShown = df.values.tolist()
    for i in range(0,len(dataShown)):
        dataShown[i][3] = f'{ratio * dataShown[i][3] : .2f}'

    win.Element('trans_received').update(values=dataShown)

#called when search button in transactions is clicked
def searchFunction(win, search_limits, account_number, currency, sortType, orderType):
    conversion_ratio = {'USD': 1/7, 'HKD': 1, 'INR': 10}

    order_stringlist = [f"date_n_time {'DESC' if (orderType=='Descending') else 'ASC'}", f"amount {'DESC' if (orderType=='Descending') else 'ASC'}"]

    send_tab_query = f'''SELECT *
    FROM (
    SELECT IT.transaction_id AS transaction_id, T.transaction_description AS transaction_description, T.date_n_time AS date_n_time, T.amount AS amount, IT.target_acc AS target_acc, BankName.c AS bankname
    FROM Internal_Trans AS IT,(
    SELECT "ABC Bank" COLLATE utf8mb4_general_ci
    ) as BankName(c),
    Transactions AS T
    WHERE IT.account_id = {account_number} AND
    T.transaction_id = IT.transaction_id AND
    DATE(T.date_n_time) >="{search_limits['date'][0]}" AND
    DATE(T.date_n_time) <="{search_limits['date'][1]}" AND
    HOUR(T.date_n_time) >={search_limits['hour'][0]} AND
    HOUR(T.date_n_time) <={search_limits['hour'][1]} AND
    YEAR(T.date_n_time) >={search_limits['year'][0]} AND
    YEAR(T.date_n_time) <={search_limits['year'][1]} AND
    MONTH(T.date_n_time) >={search_limits['month'][0]} AND
    MONTH(T.date_n_time) <={search_limits['month'][1]} AND
    DAY(T.date_n_time) >={search_limits['day'][0]} AND
    DAY(T.date_n_time) <={search_limits['day'][1]} AND
    T.amount >= {int(search_limits['amount'][0]) / conversion_ratio[currency]} AND
    T.amount <= {int(search_limits['amount'][1]) / conversion_ratio[currency]}

    UNION

    SELECT ES.transaction_id AS transaction_id, T.transaction_description AS transaction_description, T.date_n_time AS date_n_time, T.amount AS amount, ES.receiver_account_id AS target_acc, ES.receiver_bank_name AS bankname
    FROM ExternalSend AS ES, Transactions AS T
    WHERE ES.sender_account_id = {account_number} AND
    T.transaction_id = ES.transaction_id AND
    DATE(T.date_n_time) >="{search_limits['date'][0]}" AND
    DATE(T.date_n_time) <="{search_limits['date'][1]}" AND
    HOUR(T.date_n_time) >={search_limits['hour'][0]} AND
    HOUR(T.date_n_time) <={search_limits['hour'][1]} AND
    YEAR(T.date_n_time) >={search_limits['year'][0]} AND
    YEAR(T.date_n_time) <={search_limits['year'][1]} AND
    MONTH(T.date_n_time) >={search_limits['month'][0]} AND
    MONTH(T.date_n_time) <={search_limits['month'][1]} AND
    DAY(T.date_n_time) >={search_limits['day'][0]} AND
    DAY(T.date_n_time) <={search_limits['day'][1]} AND
    T.amount >= {int(search_limits['amount'][0]) / conversion_ratio[currency]} AND
    T.amount <= {int(search_limits['amount'][1]) / conversion_ratio[currency]}
    ) as A
    ORDER BY {order_stringlist[0]+','+order_stringlist[1]+';' if(sortType == 'Time') else order_stringlist[1]+','+order_stringlist[0]+';'}
    '''

    receive_tab_query = f'''SELECT *
    FROM (
    SELECT IT.transaction_id AS transaction_id, T.transaction_description AS transaction_description, T.date_n_time AS date_n_time, T.amount AS amount, IT.account_id AS sender, BankName.c AS bankname
    FROM Internal_Trans AS IT,(
    SELECT "ABC Bank" COLLATE utf8mb4_general_ci
    ) as BankName(c),
    Transactions AS T
    WHERE IT.target_acc = {account_number} AND
    T.transaction_id = IT.transaction_id AND
    DATE(T.date_n_time) >="{search_limits['date'][0]}" AND
    DATE(T.date_n_time) <="{search_limits['date'][1]}" AND
    HOUR(T.date_n_time) >={search_limits['hour'][0]} AND
    HOUR(T.date_n_time) <={search_limits['hour'][1]} AND
    YEAR(T.date_n_time) >={search_limits['year'][0]} AND
    YEAR(T.date_n_time) <={search_limits['year'][1]} AND
    MONTH(T.date_n_time) >={search_limits['month'][0]} AND
    MONTH(T.date_n_time) <={search_limits['month'][1]} AND
    DAY(T.date_n_time) >={search_limits['day'][0]} AND
    DAY(T.date_n_time) <={search_limits['day'][1]} AND
    T.amount >= {int(search_limits['amount'][0]) / conversion_ratio[currency]} AND
    T.amount <= {int(search_limits['amount'][1]) / conversion_ratio[currency]}

    UNION

    SELECT ER.transaction_id AS transaction_id, T.transaction_description AS transaction_description, T.date_n_time AS date_n_time, T.amount AS amount, ER.sender_account_id AS sender, ER.sender_bank_name AS bankname
    FROM ExternalReceive AS ER, Transactions AS T
    WHERE target_account_id = {account_number} AND
    ER.transaction_id = T.transaction_id AND
    DATE(T.date_n_time) >="{search_limits['date'][0]}" AND
    DATE(T.date_n_time) <="{search_limits['date'][1]}" AND
    HOUR(T.date_n_time) >={search_limits['hour'][0]} AND
    HOUR(T.date_n_time) <={search_limits['hour'][1]} AND
    YEAR(T.date_n_time) >={search_limits['year'][0]} AND
    YEAR(T.date_n_time) <={search_limits['year'][1]} AND
    MONTH(T.date_n_time) >={search_limits['month'][0]} AND
    MONTH(T.date_n_time) <={search_limits['month'][1]} AND
    DAY(T.date_n_time) >={search_limits['day'][0]} AND
    DAY(T.date_n_time) <={search_limits['day'][1]} AND
    T.amount >= {int(search_limits['amount'][0]) / conversion_ratio[currency]} AND
    T.amount <= {int(search_limits['amount'][1]) / conversion_ratio[currency]}
    ) as A
    ORDER BY {order_stringlist[0]+','+order_stringlist[1]+';' if(sortType == 'Time') else order_stringlist[1]+','+order_stringlist[0]+';'}
    '''

    #function to update list boxes in tabs in gui
    updateTabs(send_tab_query, receive_tab_query, win, currency)


#handles transaction view
def transview(account_number, win):
    curr_date = datetime.now().date()
    current_date = str(curr_date)
    current_year = curr_date.year
    current_day = curr_date.day

    global prev_currency

    calendar_start_date = '1995-08-15'
    calendar_start_year = (int) (calendar_start_date[0:4])

    conversion_ratio = {'USD': 1/7, 'HKD': 1, 'INR': 10}

    max_width = 120


    search_limits = {'date': [calendar_start_date, current_date], 'hour': [0, 23], 'year': [1995, current_year], 'month': [1, 12], 'day': [1, 31], 'amount': [0, 10**7]}
    search_limits_default = {'date': [calendar_start_date, current_date], 'hour': [0, 23], 'year': [1995, current_year], 'month': [1, 12], 'day': [1, 31], 'amount': [0, 10**7]}

    currencies = ['USD', 'HKD', 'INR']


    choices_time = ['00:00 to 00:59', '01:00 to 01:59', '02:00 to 02:59', '03:00 to 03:59', '04:00 to 04:59', '05:00 to 05:59', '06:00 to 06:59', '07:00 to 07:59', '08:00 to 08:59', '09:00 to 09:59', '10:00 to 10:59', '11:00 to 11:59', '12:00 to 12:59', '13:00 to 13:59', '14:00 to 14:59', '15:00 to 15:59', '16:00 to 16:59', '17:00 to 17:59', '18:00 to 18:59', '19:00 to 19:59', '20:00 to 20:59', '21:00 to 21:59', '22:00 to 22:59', '23:00 to 23:59']
    choices_month = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    list_box_width = 160

    trans_sent = choices_time
    trans_received = choices_month


    while True:
        event, values = win.Read()

        win.Element('trans_amount_low').update(value =( int((float(values['trans_amount_low']) * (conversion_ratio[values['trans_currencies']] / conversion_ratio[prev_currency])) /1000) * 1000))
        win.Element('trans_amount_up').update(value =( int((float(values['trans_amount_up']) * (conversion_ratio[values['trans_currencies']] / conversion_ratio[prev_currency])) /1000) * 1000))
        prev_currency = values['trans_currencies']
        if event is None:
            win.close()
            exit(0)
        if event == 'trans_back_acc':
            return
        if event == 'Logout':
            logout_button(win)
        if event == 'Search':
            # Update search_limits dictionary
            search_limits['hour'][0] = search_limits_default['hour'][0] if (values['trans_search_all'] or values['trans_time_disable']) else values['trans_time_low'][0:2]
            search_limits['hour'][1] = search_limits_default['hour'][1] if (values['trans_search_all'] or values['trans_time_disable']) else values['trans_time_low'][0:2]
            search_limits['year'][0] = search_limits_default['year'][0] if (values['trans_search_all'] or values['trans_year_disable']) else values['trans_year_low']
            search_limits['year'][1] = search_limits_default['year'][1] if (values['trans_search_all'] or values['trans_year_disable']) else values['trans_year_up']
            for i in range(0, 12):
                if choices_month[i] == values['trans_month_low']:
                    search_limits['month'][0] = 0 if (values['trans_search_all'] or values['trans_month_disable']) else i+1
                if choices_month[i] == values['trans_month_up']:
                    search_limits['month'][1] = 12 if (values['trans_search_all'] or values['trans_month_disable']) else i+1
            search_limits['day'][0] = search_limits_default['day'][0] if (values['trans_search_all'] or values['trans_day_disable']) else values['trans_day_low']
            search_limits['day'][1] = search_limits_default['day'][1] if (values['trans_search_all'] or values['trans_day_disable']) else values['trans_day_up']
            search_limits['date'][0] = search_limits_default['date'][0] if (values['trans_search_all'] or values['trans_dates_disable']) else values['trans_low']
            search_limits['date'][1] = search_limits_default['date'][1] if (values['trans_search_all'] or values['trans_dates_disable']) else values['trans_up']
            search_limits['amount'][0] = search_limits_default['amount'][0] if (values['trans_search_all'] or values['trans_amount_disable']) else values['trans_amount_low']
            search_limits['amount'][1] = search_limits_default['amount'][1] if (values['trans_search_all'] or values['trans_amount_disable']) else values['trans_amount_up']
            searchFunction(win, search_limits, account_number, values['trans_currencies'], values['trans_sort'], values['trans_order'])



        if values['trans_search_all'] == True:
            disableDisableButtons(win, True)


        else:
            disableDisableButtons(win, False)

            if values['trans_dates_disable'] == True:
                disableDates(win, True)
            else:
                disableDates(win, False)

            if values['trans_year_disable'] == True:
                disableYear(win, True)
            else:
                disableYear(win, False)

            if values['trans_month_disable'] == True:
                disableMonth(win, True)
            else:
                disableMonth(win, False)

            if values['trans_day_disable'] == True:
                disableDay(win, True)
            else:
                disableDay(win, False)

            if values['trans_time_disable'] == True:
                disableTime(win, True)
            else:
                disableTime(win, False)

            if values['trans_amount_disable'] == True:
                disableAmount(win, True)
            else:
                disableAmount(win, False)









#2 Load recognize and read label from model
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("train.yml")

labels = {"person_name": 1}
with open("labels.pickle", "rb") as f:
    labels = pickle.load(f)
    labels = {v: k for k, v in labels.items()}

# create text to speech
engine = pyttsx3.init()
rate = engine.getProperty("rate")
engine.setProperty("rate", 175)

# Define camera and detect face
face_cascade = cv2.CascadeClassifier('haarcascade/haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)


layout =  [
    [sg.Text('Welcome to ABC Bank! Do you want to start facial recognition?', size=(50,1), font=('Any',18), text_color='black', justification='center')],
    [sg.Text('Confidence', key='cfd', visible=False), sg.Slider(range=(0,100),orientation='h', resolution=1, default_value=100, size=(15,15), key='confidence', visible=False)],
    [sg.Button('Yes'), sg.Button('Login with password'), sg.Button('Exit', key='login_exit')]
      ]
win = sg.Window('ABC Bank Login',
        element_justification='c',
        default_element_size=(200,100),
        text_justification='center',
        auto_size_text=True).Layout(layout)

event, values = win.Read()

recognize_face = False

if event == 'Yes':
    recognize_face = True
    win.Close()
    args = values
    gui_confidence = args["confidence"]
    win_started = False

elif event == 'login_exit' or event == 'Exit' or event == None:
    exit(0)
else:
    win.Close()

    #login by password window
    layout = [
        [sg.T('Please enter your customer ID and password', size=(145, 1), justification='center')],
        [sg.T('Username/Password incorrect', size=(145, 1), justification='center', visible=False, key='loginfail')],
        [sg.T('Enter Customer ID:', size=(20, 1)), sg.Input(key='_pwd_cid_',size=(60,1))],
        [sg.T('Enter Password:', size=(20, 1)), sg.Input(key='_pwd_pwd_', password_char='*',size=(60,1))],
        [sg.Button('Login'),sg.Button('Exit')]
    ]
    win = sg.Window('ABC Bank Login',
            element_justification='c',
            default_element_size=(200,100),
            text_justification='center',
            auto_size_text=True).Layout(layout)
    while True:
        event, values = win.Read()
        if event == 'Login':
            result = ['error']
            if values['_pwd_cid_'] == '' or values['_pwd_pwd_'] == '':
                win.Element('loginfail').update(visible=True)
            else:
                try:
                    select = "SELECT customer_id, customer_name, face_id FROM Customer WHERE customer_id=%s AND password=%s" % (values['_pwd_cid_'],values['_pwd_pwd_'])
                    name = cursor.execute(select)
                    result = cursor.fetchall()
                except:
                    result = ['error']
            data = "error"

            for x in result:
                data = x


            # If the customer's information is not found in the database
            if data == "error":
                # the customer's data is not in the database
                win.Element('loginfail').update(visible=True)
                win.Element('_pwd_cid_').update(value='')
                win.Element('_pwd_pwd_').update(value='')

            # If the customer's information is found in the database
            else:
                """
                Implement useful functions here.


                """
                globalCurrentID = data[0]
                globalCurrentName = data[1]

                date = datetime.now()
                date = date.strftime('%Y-%m-%d %H:%M:%S')

                update =  "INSERT INTO Login_History VALUES ('%s', %i)" % (date, data[0])
                cursor.execute(update)
                myconn.commit()
                hello = ("Hello ", globalCurrentName, "Welcome to the ABC Bank", "\nYour current login time is: %s" % (date))
                break
            if event == 'Exit' or event == None:
                exit(0)





# 4 Open the camera and start face recognition
while recognize_face:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=3)

    for (x, y, w, h) in faces:
        print(x, w, y, h)
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = frame[y:y + h, x:x + w]
        # predict the id and confidence for faces
        id_, conf = recognizer.predict(roi_gray)

        # 4.1 If the face is recognized
        if conf >= gui_confidence:
            font = cv2.QT_FONT_NORMAL
            id = 0
            id += 1
            name = labels[id_]
            current_name = name
            globalCurrentName = current_name
            globalCurrentID = id_ + 1

            color = (255, 0, 0)
            stroke = 2
            cv2.putText(frame, name, (x, y), font, 1, color, stroke, cv2.LINE_AA)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), (2))

            # Find the customer information in the database.
            select = "SELECT customer_id, customer_name, face_id FROM Customer WHERE face_id=%i" % (globalCurrentID)
            name = cursor.execute(select)
            result = cursor.fetchall()
            data = "error"

            for x in result:
                data = x


            # If the customer's information is not found in the database
            if data == "error":
                # the customer's data is not in the database
                print("The customer", current_name, "is NOT FOUND in the database.")

            # If the customer's information is found in the database
            else:
                """
                Implement useful functions here.


                """
                globalCurrentID = data[0]
                globalCurrentName = data[1]
                date = datetime.now()
                date = date.strftime('%Y-%m-%d %H:%M:%S')
                update =  "INSERT INTO Login_History VALUES ('%s', %i)" % (date, data[0])
                cursor.execute(update)
                myconn.commit()
                hello = ("Hello ", globalCurrentName, "Welcome to the ABC Bank", "\nYour current login time is: %s" % (date))
                engine.say(hello)

                recognize_face = False

        # 4.2 If the face is unrecognized
        else:
            color = (255, 0, 0)
            stroke = 2
            font = cv2.QT_FONT_NORMAL
            cv2.putText(frame, "UNKNOWN", (x, y), font, 1, color, stroke, cv2.LINE_AA)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), (2))
            hello = ("Your face is not recognized")
            engine.say(hello)


    # GUI
    imgbytes = cv2.imencode('.png', frame)[1].tobytes()
    if not win_started:
        win_started = True
        layout = [
            [sg.Text('iKYC System Interface', size=(30,1))],
            [sg.Image(data=imgbytes, key='_IMAGE_')],
            [sg.Text('Confidence'),
                sg.Slider(range=(0, 100), orientation='h', resolution=1, default_value=100, size=(15, 15), key='confidence')],
            [sg.Exit()]
        ]
        win = sg.Window('iKYC System',
                default_element_size=(14, 1),
                text_justification='right',
                auto_size_text=False).Layout(layout).Finalize()
        image_elem = win.FindElement('_IMAGE_')

    else:
        image_elem.Update(data=imgbytes)


    event, values = win.Read(timeout=20)


    if event is None or event == 'Exit':
        exit(0)
        break
    gui_confidence = values['confidence']




win.Close()
cap.release()

#GUI once user logs in successfully

#getting user login history
select_history = "SELECT date_time FROM Login_History WHERE customer_id=%i ORDER BY date_time DESC" % (data[0])
cursor.execute(select_history)
history = cursor.fetchall()



hello_msg_1 = 'Hello %s! Welcome to ABC Bank!' % (globalCurrentName)
hello_msg_2 = 'Your current login time is: %s' % (date)


all_history = []
for i in history:
    all_history.append( [ str(i[0])[0:10], str(i[0])[11: len(str(i))] ] )

user_account = []
account_summary = []




curr_date = datetime.now().date()
current_date = str(curr_date)
current_year = curr_date.year
current_day = curr_date.day

prev_currency='HKD'

calendar_start_date = '1995-08-15'
calendar_start_year = (int) (calendar_start_date[0:4])

conversion_ratio = {'USD': 1/7, 'HKD': 1, 'INR': 10}

max_width = 120


search_limits = {'date': [calendar_start_date, current_date], 'hour': [0, 23], 'year': [1995, current_year], 'month': [1, 12], 'day': [1, 31], 'amount': [0, 10**7]}
search_limits_default = {'date': [calendar_start_date, current_date], 'hour': [0, 23], 'year': [1995, current_year], 'month': [1, 12], 'day': [1, 31], 'amount': [0, 10**7]}

currencies = ['USD', 'HKD', 'INR']



choices_time = ['00:00 to 00:59', '01:00 to 01:59', '02:00 to 02:59', '03:00 to 03:59', '04:00 to 04:59', '05:00 to 05:59', '06:00 to 06:59', '07:00 to 07:59', '08:00 to 08:59', '09:00 to 09:59', '10:00 to 10:59', '11:00 to 11:59', '12:00 to 12:59', '13:00 to 13:59', '14:00 to 14:59', '15:00 to 15:59', '16:00 to 16:59', '17:00 to 17:59', '18:00 to 18:59', '19:00 to 19:59', '20:00 to 20:59', '21:00 to 21:59', '22:00 to 22:59', '23:00 to 23:59']
choices_month = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

#1st: [title, back option]
#2nd: [limits selection, calendar period]
#3rd: [disable checkboxes, see all]
#4th: [search, switch recevie/send view]
#5th: [scroll panel to display selected data]


list_box_width = 160 #int(max_width/4)

trans_sent = choices_time
trans_received = choices_month



#layout for search in sent tab in transaction view
tab_layout_sent =  [[sg.T('Sent to others', size=(145, 1), justification='center')],
                    [sg.Table(values = [], headings=['Transaction ID', 'Description', 'Date and Time','Amount', "Receiver's Account", "Receiver's Bank"], col_widths=[12, 52, 20, 10, 15, 20],
            alternating_row_color = 'lightgrey',
            background_color='white',
            text_color='black',
            justification="right",
            auto_size_columns=False,
            enable_events=True,
            key='trans_sent',)
                    ]
                   ]

#layout for search in received tab in transaction view
tab_layout_received =  [[sg.T('Received from others', size=(145, 1), justification='center')],
                            [sg.Table(values = [], headings=['Transaction ID', 'Description', 'Date and Time','Amount', "Sender's Account", "Sender's Bank"], col_widths=[12, 52, 20, 10, 15, 20],
                    alternating_row_color = 'lightgrey',
                    background_color='white',
                    text_color='black',
                    justification="right",
                    auto_size_columns=False,
                    enable_events=True,
                    key='trans_received',)
                            ]
                        ]



#layout for the GUI
layout = [
    [sg.Text(hello_msg_1, size=(145, 1), key='_W_MSG_1_', justification='center')],
    [sg.Text(hello_msg_2, size=(50, 1), key='_W_MSG_2_', justification='center')],
    [ sg.Button('Logout'), sg.Button('Login History',key='log_view', visible=False),  sg.Button('Back to Accounts', key='trans_back_acc', visible=False), sg.Button('Account View',key='acc_view'), sg.Button('Exit', key='_EXIT_',visible=False)],
    [
    sg.Frame('',[[
                sg.Table(values = all_history, headings=['Date', 'Time'], col_widths=[15, 15],size=(30,20),hide_vertical_scroll=True,
        alternating_row_color = 'lightgrey',
        background_color='white',
        text_color='black',
        justification="center",
        auto_size_columns=False,
        )
    ]], key = '_HISTORY_'), sg.Frame('',[[
                sg.Table(values = [], headings=['Account ID', 'Account Type', 'Balance', 'Currency'], col_widths=[15, 15, 15,15],size=(30,20),hide_vertical_scroll=True,
        alternating_row_color = 'lightgrey',
        background_color='white',
        text_color='black',
        justification="center",
        auto_size_columns=False,
        enable_events=True,
        key='_ACCOUNT_TABLE_'
        )
    ]], key = '_ACCOUNT_',visible=False), sg.Frame('',[
        [
         sg.In(key='trans_low', enable_events=True, default_text=calendar_start_date, readonly = True, size=(12,1)),
         sg.CalendarButton('->', target='trans_low', pad=None, font=('MS Sans Serif', 10, 'bold'),
                button_color=('red', 'white'), key='trans_lowcal', format=('%Y-%m-%d')),
         sg.Text('to', key='trans_cal_to', size=(2, 1)),
         sg.In(key='trans_up', enable_events=True, default_text=current_date, readonly = True, size=(12,1)),
         sg.CalendarButton('->', target='trans_up', pad=None, font=('MS Sans Serif', 10, 'bold'),
                        button_color=('red', 'white'), key='trans_upcal', format=('%Y-%m-%d')),
         sg.Text('Year', key='trans_year_title', size=(4, 1)), sg.Combo([i for i in range(calendar_start_year, current_year+1)], default_value=calendar_start_year, key='trans_year_low', readonly=True, size=(6, 1)), sg.Text(':', key='trans_year_colon', size=(1, 1)), sg.Combo([i for i in range(calendar_start_year, current_year+1)], default_value=current_year, key='trans_year_up', readonly=True, size=(6, 1)),
         sg.Text('Month', key='trans_month_title', size=(5, 1)), sg.Combo(choices_month, key='trans_month_low', default_value=choices_month[0], readonly=True, size=(6, 1)), sg.Text(':', key='trans_month_colon', size=(1, 1)), sg.Combo(choices_month, key='trans_month_up', default_value=choices_month[-1], readonly=True, size=(6, 1))
        ],
        [
         sg.Text('Day Range', key='trans_day_title', size=(9, 1)), sg.Spin([i for i in range(1,32)], initial_value=1, key='trans_day_low', readonly=True, size=(6, 1)), sg.Text(':', key='trans_day_colon', size=(1, 1)), sg.Spin([i for i in range(1,32)], initial_value=31, key='trans_day_up', readonly=True, size=(6, 1)),
         sg.Text('Time', key='trans_time_title', size=(4, 1)), sg.Combo(choices_time, key='trans_time_low', default_value=choices_time[0], readonly=True, size=(12, 1), disabled=True),
         sg.Text('Amount', key='trans_amount_title', size=(6, 1)), sg.Spin([i for i in range(0, 10**7, 1000)], initial_value=0, key='trans_amount_low', readonly=True, size=(8, 1)), sg.Text('to', key='trans_amount_to', size=(1, 1)), sg.Spin([i for i in range(0, 10**7, 1000)], initial_value=100000, key='trans_amount_up', readonly=True, size=(8, 1)),
         sg.Text('Currency', key='trans_currency_title', size=(8, 1)), sg.Combo(currencies, key='trans_currencies', enable_events=True, default_value=currencies[1], readonly=True, size=(4, 1)),
         sg.Text('Sort By', key='trans_sort_time_title', size=(6, 1)), sg.Combo(['Time','Amount'], key='trans_sort', default_value='Time', readonly=True, size=(7, 1)),
         sg.Text('Order', key='trans_sort_amount_title', size=(6, 1)), sg.Combo(['Ascending','Descending'], key='trans_order', default_value='Descending', readonly=True, size=(10, 1)),
        ],
        [sg.Checkbox('Search All', default=False, key='trans_search_all', enable_events=True, size=(15, 1)),
         sg.Checkbox('Disable Dates', default=False, key='trans_dates_disable', enable_events=True, size=(15, 1)),
         sg.Checkbox('Disable Year', default=False, key='trans_year_disable', enable_events=True, size=(15, 1)),
         sg.Checkbox('Disable Month', default=False, key='trans_month_disable', enable_events=True, size=(15, 1)),
         sg.Checkbox('Disable Day', default=False, key='trans_day_disable', enable_events=True, size=(15, 1)),
         sg.Checkbox('Disable Time', default=True, key='trans_time_disable', enable_events=True, size=(15, 1)),
         sg.Checkbox('Disable Amount', default=False, key='trans_amount_disable', enable_events=True, size=(15, 1))
        ],
        [
         sg.Button('Search'),

        ],

        [sg.TabGroup([[sg.Tab('Sent', tab_layout_sent, key='tab_sent'), sg.Tab('Received', tab_layout_received, key='tab_received')]])]
        ], key='trans_frame', visible=False)
    ],
    [sg.pin(sg.Button('Transaction View', key='_TV_', visible=False))],
]

win = sg.Window('Bank System',
        element_justification='c',
        default_element_size=(60, 30),
        text_justification='right',
        auto_size_text=False, resizable=True).Layout(layout)



select_account = "SELECT account_id, account_type, balance, currency FROM Account WHERE customer_id=%i" % (data[0])
cursor.execute(select_account)

user_account_id = cursor.fetchall()

conversion_ratio = {'USD': 1/7, 'HKD': 1, 'INR': 10}

df = DataFrame(user_account_id)
all_account_id = df.values.tolist()
for i in range(0,len(all_account_id)):
    all_account_id[i][2] = f'{conversion_ratio[all_account_id[i][3]] * all_account_id[i][2] : .2f}'



while True:
    event, values = win.Read()
    if event is None or event == 'Exit':
        win.close()
        exit(0)

    #if user moves to account view
    if event == 'Account View' or event=='acc_view':
        win.Element('_W_MSG_1_').Update(value='%s, this is your account view.' % (globalCurrentName))
        win.Element('_W_MSG_2_').Update('Please select an account to enable view transaction button.')
        win.Element('_W_MSG_2_').Update(visible=True)
        win.Element('_HISTORY_').Update(visible=False)
        win.Element('_ACCOUNT_').Update(visible=True)
        win.Element('trans_frame').update(visible=False)
        win.Element('acc_view').update(visible=False)
        win.Element('log_view').update(visible=True)
        win.Element('_ACCOUNT_TABLE_').Update(values=all_account_id)

    #if user selects an account from accounts table
    if event == '_ACCOUNT_TABLE_':
        win.Element('_TV_').Update(visible=True)

    #if user moves to login history view
    if event == 'Login History' or event == 'log_view':
        win.Element('_W_MSG_1_').Update(value='%s, this is your login history.' % (globalCurrentName))
        win.Element('_W_MSG_2_').Update(visible=False)
        win.Element('_HISTORY_').Update(visible=True)
        win.Element('_ACCOUNT_').Update(visible=False)
        win.Element('_TV_').Update(visible=False)
        win.Element('trans_frame').update(visible=False)
        win.Element('log_view').update(visible=False)
        win.Element('acc_view').update(visible=True)

    #if user presses the logout button
    if event == 'Logout':
        logout_button(win)

    #if user moves to transaction view
    if event == '_TV_':
        trans_account_id = int(all_account_id[values['_ACCOUNT_TABLE_'][0]][0])
        win.Element('_W_MSG_1_').Update(value='%s, this is your transaction history for Account ID = %d.' % (globalCurrentName, trans_account_id))
        win.Element('_W_MSG_2_').Update(visible=False)
        win.Element('_HISTORY_').Update(visible=False)
        win.Element('trans_back_acc').Update(visible=True)
        win.Element('_ACCOUNT_').Update(visible=False)
        win.Element('_TV_').Update(visible=False)
        win.Element('trans_frame').update(visible=True)
        win.Element('log_view').update(visible=False)
        win.Element('acc_view').update(visible=False)
        win.Element('_ACCOUNT_TABLE_').Update(values=all_account_id)
        transview(trans_account_id, win)

        win.Element('_W_MSG_1_').Update(value='%s, this is your account view.' % (globalCurrentName))
        win.Element('_W_MSG_2_').Update('Please select an account to enable view transaction button.')
        win.Element('_W_MSG_2_').Update(visible=True)
        win.Element('_HISTORY_').Update(visible=False)
        win.Element('_ACCOUNT_').Update(visible=True)
        win.Element('trans_frame').update(visible=False)
        win.Element('acc_view').update(visible=False)
        win.Element('log_view').update(visible=True)
        win.Element('trans_back_acc').Update(visible=False)
        win.Element('trans_sent').update(values=[])
        win.Element('trans_received').update(values=[])
