import urllib
import numpy as np
import mysql.connector
import cv2
import pyttsx3
import pickle
from datetime import datetime
import sys
import PySimpleGUI as sg
from prettytable import PrettyTable
# remember to "pip3 install PTable"

globalCurrentName = 'Jack'
globalCurrentID = 1003

# 1 Create database connection
# myconn = mysql.connector.connect(host="localhost", user="root", passwd="123456", database="face3278")
myconn = mysql.connector.connect(host="localhost", user="root", passwd="hkbcps040076", database="facerecognition")

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
    [sg.Text('Setting', size=(18,1), font=('Any',18),text_color='#1c86ee' ,justification='left')],
    [sg.Text('Confidence', key='cfd'), sg.Slider(range=(0,100),orientation='h', resolution=1, default_value=60, size=(15,15), key='confidence')],
    [sg.OK(), sg.Cancel(), sg.Button('Test')]
      ]
win = sg.Window('iKYC System',
        default_element_size=(21,1),
        text_justification='right',
        auto_size_text=False).Layout(layout)
print("I'm here1")
event, values = win.Read()
if event is None or event =='Cancel':
    print("I'm here")
    exit()
if event == 'Test':
    win.Element('cfd').update('Deviance')
    win.Element('confidence').update(visible=False)
    print("Reached")


event, values = win.Read()
if event is None or event =='Cancel':
    exit()

args = values
gui_confidence = args["confidence"]
win_started = False

# win.close() # Closes small window after pressing "Ok"

print("I'm there")

breakCount = 0

# 4 Open the camera and start face recognition
while True:
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
                #cap.release()
                #cv2.destroyAllWindows()
                # breakCount = -1
                # break

                update =  "UPDATE Login_History SET date_time='%s' WHERE customer_id=%i" % (date, data[0])
                # val = (date, data[0])
                cursor.execute(update)
                # update = "UPDATE Customer SET login_time=%s WHERE name=%s"
                # val = (current_time, current_name)
                # cursor.execute(update, val)
                # myconn.commit()

                # hello = ("Hello ", current_name, "Welcom to the iKYC System")
                hello = ("Hello ", globalCurrentName, "Welcom to the Bank ABC", "\nYour current login time is: %s" % (date))
                # hello = ("Hello ", globalCurrentName, "Welcom to the Bank ABC", "\nYour current login time is: %s" %(date))
                # print(hello)
                engine.say(hello)

                select_history = "SELECT * FROM Login_History WHERE customer_id=%i ORDER BY date_time ASC" % (data[0])
                # val = (data[0])
                # cursor.execute(select_history, val)
                # print(select_history)
                cursor.execute(select_history)
                # myconn.commit()
                history = cursor.fetchall()
                break

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
            # cap.release()
            # cv2.destroyAllWindows()
            print(hello)
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

if breakCount != -1:
    print("Premature closing")
    exit(0)

# Start Experimenting
print("Yay I broke free")


layout = [
    [sg.Text('iKYC System Interface', size=(90, 30), key='Title', justification='center')],
    [sg.Button('Account View'), sg.Button('Transaction List'), sg.Button('Back'), sg.Exit()],
    [sg.Text('Confidence', key='conTitle'),
        sg.Slider(range=(0, 100), orientation='h', resolution=1, default_value=60, size=(15, 15), key='confidence')],
    [sg.Button('Show Login History', key='__HISTORY__')]
]
win = sg.Window('Bank System',
        default_element_size=(90, 30),
        text_justification='right',
        auto_size_text=False).Layout(layout)
print("I'm here2")
while True:
    event, values = win.Read()
    if event is None or event == 'Exit':
        win.close()
        exit(0)
    if event == 'Account View':
        # Call function here
        win.Element('Title').Update(visible=False)
        win.Element('conTitle').Update(visible=False)
        win.Element('confidence').Update(visible=False)

        cursor.execute("SELECT * FROM Account")
        print(cursor.fetchall())


    if event == 'Transaction List':
        win.Element('Title').Update(visible=False)
        win.Element('confidence').Update(visible=False)
    if event == 'Back':
        win.Element('Title').Update(visible=True)
        win.Element('conTitle').Update(visible=True)
        win.Element('confidence').Update(visible=True)







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


