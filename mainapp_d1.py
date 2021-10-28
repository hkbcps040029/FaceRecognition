import urllib
import numpy as np
#import mysql.connector
#import cv2
#import pyttsx3
#import pickle
from datetime import datetime
import sys
import PySimpleGUI as sg


def mainLoop(globalCurrentName, globalCurrentID):
    viewMode = 0 #set viewmode to be something else

    layout = [


    ]

    win = sg.Window('Bank System',
            default_element_size=(90, 30),
            text_justification='right',
            auto_size_text=False).Layout(layout)



    while True:
        if viewMode == 0:
            # call loginview
            a = 2
        elif viewMode == 1:
            # call accountview
            print("hi")
        elif viewMode == 2:
            # call transview
            print("yo")
        else:
            b = 2


def setInvisible(viewMode, win):
    viewElements = [] # Store corresponding view elements
    for i in range(0, 3):
        if i == viewMode:
            # Set visible
            # For each ele list
            b = 2
        else:
            # Set invisible
            b = 1

def disableDates(win, isDisabled):
    win.Element('trans_lowcal').update(disabled=isDisabled)
    win.Element('trans_upcal').update(disabled=isDisabled)

def disableYear(win, isDisabled):
    win.Element('trans_year_low').update(disabled=isDisabled)
    win.Element('trans_year_up').update(disabled=isDisabled)

def disableMonth(win, isDisabled):
    win.Element('trans_month_low').update(disabled=isDisabled)
    win.Element('trans_month_up').update(disabled=isDisabled)

def disableDay(win, isDisabled):
    win.Element('trans_day_low').update(disabled=isDisabled)
    win.Element('trans_day_up').update(disabled=isDisabled)

def disableTime(win, isDisabled):
    win.Element('trans_time_low').update(disabled=isDisabled)

def disableDisableButtons(win, isDisabled):
    win.Element('trans_dates_disable').update(disabled=isDisabled)
    win.Element('trans_year_disable').update(disabled=isDisabled)
    win.Element('trans_month_disable').update(disabled=isDisabled)
    win.Element('trans_day_disable').update(disabled=isDisabled)
    win.Element('trans_time_disable').update(disabled=isDisabled)
    disableDates(win, isDisabled)
    disableYear(win, isDisabled)
    disableMonth(win, isDisabled)
    disableDay(win, isDisabled)
    disableTime(win, isDisabled)


def transview():

    max_width = 120


    choices_time = ['00:00 to 00:59', '01:00 to 01:59', '02:00 to 02:59', '03:00 to 03:59', '04:00 to 04:59', '05:00 to 05:59', '06:00 to 06:59', '07:00 to 07:59', '08:00 to 08:59', '09:00 to 09:59', '10:00 to 10:59', '11:00 to 11:59', '12:00 to 12:59', '13:00 to 13:59', '14:00 to 14:59', '15:00 to 15:59', '16:00 to 16:59', '17:00 to 17:59', '18:00 to 18:59', '19:00 to 19:59', '20:00 to 20:59', '21:00 to 21:59', '22:00 to 22:59', '23:00 to 23:59']
    choices_month = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    #1st: [title, back option]
    #2nd: [limits selection, calendar period]
    #3rd: [disable checkboxes, see all]
    #4th: [search, switch recevie/send view]
    #5th: [scroll panel to display selected data]

    current_date = datetime.now().date()
    current_year = current_date.year
    current_day = current_date.day

    calendar_start_date = '1995-08-15'

    calendar_start_year = (int) (calendar_start_date[0:4])

    #calendar_low_title = calendar_start_date

    #calendar_up_title = current_date

    trans_sent = choices_time
    trans_received = choices_month

    tab_layout_sent =  [[sg.T('Sent to others', size=(max_width, 1), justification='center')], [sg.Listbox(values=trans_sent, key='trans_sent', enable_events=True, size=(max_width, int(max_width/4)))]]
    tab_layout_received =  [[sg.T('Received from others', size=(max_width, 1), justification='center')], [sg.Listbox(values=trans_received, key='trans_received', enable_events=True, size=(max_width, int(max_width/4)))]]


    layout = [
        [sg.Button('Logout', key='logout_button'), sg.Text("<Username>'s Transactions", size=(max_width, 1), justification='center'), sg.Button('Back to Accounts', key='trans_back_acc')], # 1st layer
        [
         sg.In(key='trans_low', enable_events=True, default_text=calendar_start_date, readonly = True),
         sg.CalendarButton('->', target='trans_low', pad=None, font=('MS Sans Serif', 10, 'bold'),
                button_color=('red', 'white'), key='trans_lowcal', format=('%Y-%m-%d')),
         sg.Text('to', key='trans_cal_to', size=(2, 1)),
         sg.In(key='trans_up', enable_events=True, default_text=current_date, readonly = True),
         sg.CalendarButton('->', target='trans_up', pad=None, font=('MS Sans Serif', 10, 'bold'),
                        button_color=('red', 'white'), key='trans_upcal', format=('%Y-%m-%d')),
         sg.Text('Year', key='trans_year_title', size=(4, 1)), sg.Combo([i for i in range(calendar_start_year, current_year+1)], default_value=calendar_start_year, key='trans_year_low', readonly=True, size=(6, 1)), sg.Text(':', key='trans_year_colon', size=(1, 1)), sg.Combo([i for i in range(calendar_start_year, current_year+1)], default_value=current_year, key='trans_year_up', readonly=True, size=(6, 1)),
         sg.Text('Month', key='trans_month_title', size=(5, 1)), sg.Combo(choices_month, key='trans_month_low', default_value=choices_month[0], readonly=True, size=(6, 1)), sg.Text(':', key='trans_month_colon', size=(1, 1)), sg.Combo(choices_month, key='trans_month_up', default_value=choices_month[-1], readonly=True, size=(6, 1))
        ],
        [
         sg.Text('Day Range', key='trans_day_title', size=(9, 1)), sg.Spin([i for i in range(1,32)], initial_value=1, key='trans_day_low', readonly=True, size=(6, 1)), sg.Text(':', key='trans_day_colon', size=(1, 1)), sg.Spin([i for i in range(1,32)], initial_value=31, key='trans_day_up', readonly=True, size=(6, 1)),
         sg.Text('Time', key='trans_time_title', size=(4, 1)), sg.Combo(choices_time, key='trans_time_low', default_value=choices_time[0], readonly=True, size=(12, 1)),
         sg.Text('Amount', key='trans_amount_title', size=(6, 1)), sg.Spin([i for i in range(0, 10**7, 1000)], initial_value=0, key='trans_amount_low', readonly=True, size=(6, 1)), sg.Text('to', key='trans_amount_to', size=(1, 1)), sg.Spin([i for i in range(0, 10**7, 1000)], initial_value=5000, key='trans_amount_up', readonly=True, size=(6, 1)),
         # sg.Combo(choices_time, key='trans_time_up', default_value=choices_time[-1], size=(12, 1)) # in case want upper limit
        ], # 2nd layer
        [sg.Checkbox('Search All', default=False, key='trans_search_all', enable_events=True, size=(15, 1)),
         sg.Checkbox('Disable Dates', default=False, key='trans_dates_disable', enable_events=True, size=(15, 1)),
         sg.Checkbox('Disable Year', default=False, key='trans_year_disable', enable_events=True, size=(15, 1)),
         sg.Checkbox('Disable Month', default=False, key='trans_month_disable', enable_events=True, size=(15, 1)),
         sg.Checkbox('Disable Day', default=False, key='trans_day_disable', enable_events=True, size=(15, 1)),
         sg.Checkbox('Disable Time', default=False, key='trans_time_disable', enable_events=True, size=(15, 1)),
        ], # 3rd layer
        [
         sg.Button('Search', key='trans_search'),
         # sg.Radio('Received', "recsent", default=True, key='trans_received', enable_events=True),
         # sg.Radio('Sent', "recsent", default=False, key='trans_sent', enable_events=True),

        ], # 4th layer
        #[sg.Listbox(values=['Listbox 1', 'Listbox 2', 'Listbox 3'], size=(int(max_width*0.9), 6), key='trans_data')] # 5th layer

        [sg.TabGroup([[sg.Tab('Sent', tab_layout_sent, key='tab_sent'), sg.Tab('Received', tab_layout_received, key='tab_received')]])]


    ]
    # Mod year by current year + 1, check if lower yr < upper yr
    # Mod date by 32
    # what if we assume that the bank started operations since year 2000
    # When enabling and disabling, set values to default again
    # Warning: Listbox update scrolls top auto
    win = sg.Window('Bank System',
            default_element_size=(10, 30),
            #text_justification='right',
            auto_size_text=False).Layout(layout)

    while True:
        event, values = win.Read()
        #calendar_low_title = values['trans_low']
        #calendar_up_title = values['trans_up']
        #win.Element().update
        print(event, values)
        if event is None:
            win.close()
            exit(0)
        if event == 'Search':
            print('abc', values)


        if values['trans_search_all'] == True:
            disableDisableButtons(win, True)
        else:
            disableDisableButtons(win, False)

            if values['trans_dates_disable'] == True:
                disableDates(win, True)
            else:
                disableDates(win, False)

            if values['trans_year_disable'] == True:# how about we have disabling functions to clean the code up a bit?
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

        #if values['trans_sent'] == True:
        #    win.Element('trans_data').update(values=choices_month)
        #else:
        #    win.Element('trans_data').update(values=choices_time)


def testTab():

    values0 = ['Listbox 1', 'Listbox 2', 'Listbox 3']
    values1 = ['abc', 'bcd', 'cde']

    tab1_layout =  [[sg.T('This is inside tab 1')], [sg.Listbox(values=values0, key='v0', enable_events=True)]]

    tab2_layout = [[sg.T('This is inside tab 2')],
                [sg.In(key='in')]]

    layout = [[sg.TabGroup([[sg.Tab('Tab 1', tab1_layout), sg.Tab('Tab 2', tab2_layout)]])],
              [sg.Button('Read')]]


    win = sg.Window('Bank System',
            default_element_size=(90, 1),
            text_justification='right',
            auto_size_text=False).Layout(layout)
    c = 0
    while True:
        event, values = win.read()
        print(event, values)

        values0[0] = 'joj'
        if event is None:
            win.close()
            exit(0)
        if c == 0:
            win.Element('v0').update(values=values0)
            c += 1

#testTab()



transview()
