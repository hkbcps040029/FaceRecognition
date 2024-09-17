import urllib
import numpy as np
import mysql.connector
import cv2
import pyttsx3
import pickle
from datetime import datetime
import sys
import PySimpleGUI as sg
import tkinter as tk
from test_trans_view import *

globalCurrentName = 'Jack'
globalCurrentID = 1003
globalAccountID = None

# 1 Create database connection
# myconn = mysql.connector.connect(host="localhost", user="root", passwd="123456", database="face3278")


date = datetime.utcnow()
date = date.strftime('%Y-%m-%d %H:%M:%S')

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

args = values
gui_confidence = args["confidence"]
win_started = False

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


                update =  "INSERT INTO Login_History VALUES ('%s', %i)" % (date, data[0])
                cursor.execute(update)
                myconn.commit()
                hello = ("Hello ", globalCurrentName, "Welcom to the Bank ABC", "\nYour current login time is: %s" % (date))
                engine.say(hello)

                select_history = "SELECT date_time FROM Login_History WHERE customer_id=%i ORDER BY date_time DESC" % (data[0])
                cursor.execute(select_history)
                history = cursor.fetchall()

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
user_account = []
account_summary = []

layout = [
    [sg.Text(hello_msg_1, size=(50, 1), font=('Any',24), key='_W_MSG_1_', justification='center')],
    [sg.Text(hello_msg_2, size=(50, 1), font=('Any',24), key='_W_MSG_2_', justification='center')],
    [sg.pin(sg.Listbox(values=all_history, key='_HISTORY_' , size=(18,10), font=('Any',24), visible=False))],
    [sg.pin(sg.Listbox(values=user_account, key='_ACCOUNT_' , size=(18,10), font=('Any',24), select_mode='LISTBOX_SELECT_MODE_SINGLE', change_submits=True, enable_events=True, visible=False))],
    [sg.pin(sg.Listbox(values=account_summary, key='_SUMMARY_' , size=(36,4), font=('Any',24), visible=False))],
    [sg.pin(sg.Text("Check your account's transaction history here.", key='_CHECK_TRAN_MSG_', size=(50, 1), font=('Any',16), justification='center', visible=False))],
    [sg.pin(sg.Button('Transaction View', key='_TV_', visible=False))],
    [sg.Text('', size=(50, 1), font=('Any',24), key='buffer', justification='center')],
    [sg.Button('Login History'), sg.Button('Account View'), sg.Exit()]
]

# , sg.Button('Transaction List')

win = sg.Window('Bank System',
        element_justification='c',
        default_element_size=(60, 30),
        text_justification='right',
        auto_size_text=False).Layout(layout)

# every element need a key
# transactio appear only in account view

c = [-1]

while True:
    event, values = win.Read()
    if event is None or event == 'Exit':
        win.close()
        exit(0)
    if event == 'Account View':
        c[0] = 1
        win.Element('_W_MSG_1_').Update(value='%s, this is your account view.' % (globalCurrentName))
        win.Element('_W_MSG_2_').Update(visible=False)
        win.Element('_HISTORY_').Update(visible=False)
        win.Element('_ACCOUNT_').Update(visible=True)
        win.Element('_SUMMARY_').Update(visible=False)
        
        select_account = "SELECT account_id FROM Account WHERE customer_id=%i" % (data[0])
        cursor.execute(select_account)

        user_account_id = cursor.fetchall()

        all_account_id = ['Account ID: '+str(i[0]) for i in user_account_id]
        win.Element('_ACCOUNT_').Update(values=all_account_id)

        choosing_account = True
        while choosing_account:
            event, values = win.Read()

            if event == '_ACCOUNT_':
                win.Element('_CHECK_TRAN_MSG_').Update(visible=True)
                win.Element('_TV_').Update(visible=True)
                win.Element('_SUMMARY_').Update(visible=True)

                acc_id = int(values['_ACCOUNT_'][0].split(' ')[-1])
                globalAccountID = acc_id

                select_account_summary = "SELECT account_type, currency, (CASE WHEN currency='USD' THEN balance*0.13 ELSE balance END) FROM Account WHERE customer_id=%i and account_id=%i" % (data[0], acc_id)
                cursor.execute(select_account_summary)
                account_summary = cursor.fetchall()[0]

                summary = ['Account Summary',
                           'Account type: %s' % (account_summary[0]),
                           'Currency: %s' % (account_summary[1]),
                           'Account type: %f (HKD)' % (account_summary[2])]

                win.Element('_SUMMARY_').Update(visible=True)
                win.Element('_SUMMARY_').Update(values=summary)

                event, values = win.Read()
                if event == '_TV_':
                    transview()

            else:
                choosing_account = False

    if event == 'Login History':
        c[0] = 0
        win.Element('_W_MSG_1_').Update(value='%s, this is your login history.' % (globalCurrentName))
        win.Element('_W_MSG_2_').Update(visible=False)
        win.Element('_HISTORY_').Update(visible=True)
        win.Element('_ACCOUNT_').Update(visible=False)
        win.Element('_SUMMARY_').Update(visible=False)
        win.Element('_CHECK_TRAN_MSG_').Update(visible=False)
        win.Element('_TV_').Update(visible=False)
