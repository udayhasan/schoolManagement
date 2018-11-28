#!/usr/bin/python3
import sqlite3
import time
from tkinter import *
from tkinter import messagebox
import os.path
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import datetime
import csv

from src.login_page import *
from src.user_dashboard import *

#from src.add_user_page import *
#from src.delete_user_page import *
#from src.edit_user_admin_sts_page import *

#from src.forgot_id_page import *
#from src.forgot_pass_page import *

#from src.manage_profile_page import *
#from src.manage_users_page import *

#from src.export_attendance_report_page import *
#from src.export_report_page import *
#from src.export_status_report_page import *

root=Tk()
root.title("Management Software")
w, h = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry("%dx%d+0+0" % (w, h))
root.resizable(0,0)

header_img = PhotoImage(file='./img/logo.png')
header = Button(root, relief=FLAT, image = header_img, height = 140, bg="white")
header.pack(fill=X)

bottom_text = Label(root, text = "Developed by: AKM Uday Hasan Bhuiyan. © 2018")
bottom_text.pack(pady=4, side=BOTTOM)

bottom_line = Canvas(root, height=2, borderwidth=0, highlightthickness=0, bg="black")
bottom_line.pack(fill=X, padx=80, side=BOTTOM)

window=login_page(root)
screen=window.screen

name=None
admin=None
task_id=0
prev_screen = None

while True:
	root.mainloop()

	if screen==0:
		name=window.login_name.get()
		admin=window.admin
	# if screen==1:
	# 	task_id = window.task_id

	screen=window.screen
	#print(screen)

	if screen<0:
		print("write data")
		break
		
	#
	# this has to be in a try: as when you click X (window close) rather
	# than exit i get a double destruction problem 
	try:
		window.destroy()
	except TclError:
		quit()

	if screen==0:
		window=login_page(root)
	elif screen==1:
		window=user_dashboard(root, name, admin)