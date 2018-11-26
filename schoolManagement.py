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

root=Tk()
root.title("NSL - Employee daily status update software")
root.geometry("1200x750")

header_img = PhotoImage(file='./img/nslHeader.png')
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
	if screen==1:
		task_id = window.task_id

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