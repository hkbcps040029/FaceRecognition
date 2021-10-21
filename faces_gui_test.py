import urllib
import numpy as np
import mysql.connector
import cv2
import pyttsx3
import pickle
from datetime import datetime
import sys
import PySimpleGUI as sg
# from prettytable import PrettyTable
# remember to "pip install PTable"

globalCurrentName = 'Jack'
globalCurrentID = 1003

# 1 Create database connection
myconn = mysql.connector.connect(host="localhost", user="root", passwd="123456", database="face3278")

date = datetime.utcnow()
date = date.strftime('%Y-%m-%d %H:%M:%S')

print(date)

now = datetime.now()
current_time = now.strftime("%H:%M:%S")
cursor = myconn.cursor()


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


# 3 Define pysimplegui setting
# Small gui window
layout =  [
    [sg.Text('Welcome to ABC Bank! Do you want to start recognition?', size=(50,1), font=('Any',18), text_color='#ffffff', justification='center')],
    [sg.Text('Confidence', key='cfd', visible=False), sg.Slider(range=(0,100),orientation='h', resolution=1, default_value=60, size=(15,15), key='confidence', visible=False)],
    [sg.Button('Yes'), sg.Button('No')]
      ]
win = sg.Window('ABC Bank Login',
        element_justification='c',
        default_element_size=(200,100),
        text_justification='center',
        auto_size_text=True).Layout(layout)

event, values = win.Read()

if event == 'Yes':
    win.Close()

elif event == 'No':
    exit()

# if event is None or event =='Cancel':
#     exit()


args = values
gui_confidence = args["confidence"]
win_started = False

# win.close() # Closes small window after pressing "Ok"

print("I'm there")

breakCount = 0

recognize_face = True

# 4 Open the camera and start face recognition
# while True:
while recognize_face:
    # breakCount = -1
    # break # self added
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
            # print(id_)
            # print(labels[id_])
            font = cv2.QT_FONT_NORMAL
            id = 0
            id += 1
            name = labels[id_]
            current_name = name
            globalCurrentName = current_name
            globalCurrentID = id_

            color = (255, 0, 0)
            stroke = 2
            cv2.putText(frame, name, (x, y), font, 1, color, stroke, cv2.LINE_AA)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), (2))

            # Find the customer information in the database.
            select = "SELECT customer_id, customer_name, face_id FROM Customer WHERE face_id=%i" % (globalCurrentID)
            # print(globalCurrentID)
            name = cursor.execute(select)
            result = cursor.fetchall()
            # print(result)
            data = "error"
            # print(result)

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


                update =  "INSERT INTO Login_History VALUES ('%s', %i)" % (date, data[0])
                cursor.execute(update)
                myconn.commit()
                hello = ("Hello ", globalCurrentName, "Welcom to the Bank ABC", "\nYour current login time is: %s" % (date))
                engine.say(hello)



                select_history = "SELECT date_time FROM Login_History WHERE customer_id=%i ORDER BY date_time DESC" % (data[0])
                cursor.execute(select_history)
                history = cursor.fetchall()

            
                recognize_face = False

                # table way
                # history_table = PrettyTable()
                # history_table.col = ["Login Date", "Login Time"]
                # for i in history:
                #     h_date = i.split(' ')[0]
                #     h_time = i.split(' ')[1]
                #     history_table.add_row([h_date, h_time])

                # print(history_table)
                # engine.say(history_table)

                #sg way







        # 4.2 If the face is unrecognized
        else:
            color = (255, 0, 0)
            stroke = 2
            font = cv2.QT_FONT_NORMAL
            cv2.putText(frame, "UNKNOWN", (x, y), font, 1, color, stroke, cv2.LINE_AA)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), (2))
            hello = ("Your face is not recognized")
            engine.say(hello)
            # engine.runAndWait()

    # if breakCount == -1:
    #     break


    # GUI
    imgbytes = cv2.imencode('.png', frame)[1].tobytes()
    if not win_started:
        win_started = True
        layout = [
            [sg.Text('iKYC System Interface', size=(30,1))],
            [sg.Image(data=imgbytes, key='_IMAGE_')],
            [sg.Text('Confidence'),
                sg.Slider(range=(0, 100), orientation='h', resolution=1, default_value=60, size=(15, 15), key='confidence')],
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
        break
    gui_confidence = values['confidence']



win.Close()
cap.release()

# if breakCount != -1:
#     print("Premature closing")
#     exit(0)

# Start Experimenting

hello_msg_1 = 'Hello %s! Welcome to Bank ABC!' % (globalCurrentName)
hello_msg_2 = 'Your current login time is: %s' % (date)

all_history = [i[0] for i in history]

layout = [
    [sg.Text(hello_msg_1, size=(50, 1), font=('Any',24), key='msg1', justification='center')],
    [sg.Text(hello_msg_2, size=(50, 1), font=('Any',24), key='msg2', justification='center')],
    [sg.Listbox(values=all_history, key='_HISTORY_' , size=(18,10), font=('Any',24), select_mode='extended', visible=False)],
    [sg.Text('', size=(50, 1), font=('Any',24), key='buffer', justification='center')],
    [sg.Button('Login History'), sg.Button('Account View'), sg.Button('Transaction List'), sg.Exit()]    
]
win = sg.Window('Bank System',
        element_justification='c',
        default_element_size=(60, 30),
        text_justification='right',
        auto_size_text=False).Layout(layout)


while True:
    event, values = win.Read()
    if event is None or event == 'Exit':
        win.close()
        exit(0)
    if event == 'Account View':
        # Call function here
        win.Element('msg1').Update(value='%s, this is your account view.' % (globalCurrentName))
        win.Element('_HISTORY_').Update(visible=False)

        cursor.execute("SELECT * FROM Account")
        print(cursor.fetchall())

    if event == 'Login History':
        win.Element('msg1').Update(value='%s, this is your login history.' % (globalCurrentName))
        win.Element('msg2').Update(visible=False)
        win.Element('_HISTORY_').Update(visible=True)


    if event == 'Transaction List':
        win.Element('msg1').Update(value='%s, this is your transaction list.' % (globalCurrentName))
        win.Element('_HISTORY_').Update(visible=False)


# ======== Page Navigation Functions =========




# ======== SQL Functions =========

def testSQL(myconn):
    myconn.database = "face3278"
    query =  "SELECT * FROM Customer"
    mycursor = myconn.cursor()
    mycursor.execute(query)
    return


# ======== Login =========
def login(myconn):
    # hello = ("Hello ", current_name, "Welcom to the iKYC System")
    hello = ("Hello ", globalCurrentName, "Welcom to the Bank ABC", "\nYour current login time is: %s" (date))
    # hello = ("Hello ", globalCurrentName, "Welcom to the Bank ABC", "\nYour current login time is: %s" %(date))
    print(hello)
    engine.say(hello)


    select_history = "SELECT * FROM Login_history WHERE customer_id=%i ORDER BY date_time ASC"
    val = (globalCurrentID)
    cursor.execute(select_history, val)
    myconn.commit()
    history = cursor.fetchall()

    sg.update()

    # table way
    history_table = PrettyTable()
    history_table.col = ["Login Date", "Login Time"]
    for i in history:
        h_date = i.split(' ')[0]
        h_time = i.split(' ')[1]
        history_table.add_row([h_date, h_time])

    # print(history_table)
    # engine.say(history_table)

    #sg way


