class export_status_report_page(Frame):

	screen = 18

	status_conn = None
	status_cur  = None
	name        = None
	db_name     = "./db/status.db"

	error_msg  = " "

	def __init__(self,master):
		super(export_status_report_page,self).__init__(master)
		self.pack()

		self.login_conn= sqlite3.connect('./db/users.db')
		self.login_cur = self.login_conn.cursor()

		self.status_conn = sqlite3.connect(self.db_name)
		self.status_cur  = self.status_conn.cursor()

		self.pack()
		self.define_widgets()

	def create_user_table(self):
		self.login_cur.execute("CREATE TABLE IF NOT EXISTS users(name TEXT, email TEXT, password TEXT, admin_status TEXT)")

	def create_status_table(self):
		self.status_cur.execute("CREATE TABLE IF NOT EXISTS status(ids TEXT, dates TEXT, up_time TEXT, weeks TEXT, months TEXT, years TEXT, name TEXT, team TEXT,task_list TEXT, progress_status TEXT, meeting_status TEXT, project_status TEXT, remarks TEXT)")

	def define_widgets(self):
		#for line1:
		frame1 = Frame(self)
		frame1.pack()
		dash_board_label=Label(frame1,text="::Status Report::")
		dash_board_label.config(width=200, font=("Courier", 25))
		dash_board_label.pack(pady=5)

		canvas = Canvas(frame1, height=2, borderwidth=0, highlightthickness=0, bg="black")
		canvas.pack(fill=X, padx=80, pady=10)

		self.create_user_table()
		self.create_status_table()

		#Status of
		frameUser = Frame(self)
		frameUser.pack()
		
		status_of_label=Label(frameUser,text="User:", anchor=W)
		status_of_label.pack(side=LEFT, pady=5)

		self.status_cur.execute("SELECT name FROM status")
		user_list = list(set(self.status_cur.fetchall()))
		user_list.append('All')

		self.status_of_name=StringVar()
		self.status_of_name.set('All')

		status_of_box=OptionMenu(frameUser,self.status_of_name, *user_list)
		status_of_box.pack(side=LEFT, padx=2, pady=5)

		#Of Team
		team_label=Label(frameUser,text="Team:", anchor=W)
		team_label.pack(side=LEFT, pady=5)

		self.status_cur.execute("SELECT team FROM status")
		team_list = list(set(self.status_cur.fetchall()))
		team_list.append('All')

		self.team_name=StringVar()
		self.team_name.set('All')

		team_list_box=OptionMenu(frameUser,self.team_name, *team_list)
		team_list_box.pack(side=LEFT, padx=2, pady=5)

		#Of Date	
		date_label=Label(frameUser,text="Date:",anchor=W)
		date_label.pack(side=LEFT, pady=5)

		self.status_cur.execute("SELECT dates FROM status")
		date_list = list(set(self.status_cur.fetchall()))
		date_list.append('All')

		self.date_name=StringVar()
		self.date_name.set('All')

		date_list_box=OptionMenu(frameUser,self.date_name, *date_list)
		date_list_box.pack(side=LEFT, padx=2, pady=5)

		#Of Week
		week_label=Label(frameUser,text="Week:", anchor=W)
		week_label.pack(side=LEFT, pady=5)

		self.status_cur.execute("SELECT weeks FROM status")
		week_list = list(set(self.status_cur.fetchall()))
		week_list.append('All')

		self.week_name=StringVar()
		self.week_name.set('All')

		week_list_box=OptionMenu(frameUser,self.week_name, *week_list)
		week_list_box.pack(side=LEFT, padx=2, pady=5)

		#Of Month
		month_label=Label(frameUser,text="Month:", anchor=W)
		month_label.pack(side=LEFT, pady=5)

		self.status_cur.execute("SELECT months FROM status")
		month_list = list(set(self.status_cur.fetchall()))
		month_list.append('All')

		self.month_name=StringVar()
		self.month_name.set('All')

		month_list_box=OptionMenu(frameUser,self.month_name, *month_list)
		month_list_box.pack(side=LEFT, padx=2, pady=5)

		#Of Year
		year_label=Label(frameUser,text="Year:", anchor=W)
		year_label.pack(side=LEFT, pady=5)

		self.status_cur.execute("SELECT years FROM status")
		year_list = list(set(self.status_cur.fetchall()))
		year_list.append('All')

		self.year_name=StringVar()
		self.year_name.set('All')

		year_list_box=OptionMenu(frameUser,self.year_name, *year_list)
		year_list_box.pack(side=LEFT, padx=2, pady=5)

		frameLast = Frame(self)
		frameLast.pack()

		search_btn=Button(frameLast,text="Refresh", bg="DeepSkyBlue4", fg = "white", command = lambda : self.make_report(), width=10)
		search_btn.pack(side=LEFT, padx=2, pady=5)

		back=Button(frameLast,text="< Prev", command=self.go_prev, width=10)
		back.pack(side=LEFT, padx=2, pady=5)

		exit=Button(frameLast,text="Exit", bg = "brown3", fg = "white", command=self.leave, width=10)
		exit.pack(side=LEFT, padx=2, pady=5)

		self.frameTable = Frame(self)
		self.frameTable.pack()

	def make_report(self):
		file_name = "./status/"

		self.frameTable.pack_forget()
		self.frameTable = Frame(self)
		self.frameTable.pack()

		#Status Of
		if(self.status_of_name.get()=='All'):
			name = '*'
			file_name += 'all_'
		else:
			name = str(self.status_of_name.get()[2:len(self.status_of_name.get())-3])
			file_name += name+"_"

		#Team
		if(self.team_name.get()=='All'):
			team = '*'
			file_name += 'all_'
		else:
			team = str(self.team_name.get()[2:len(self.team_name.get())-3])
			file_name += team+"_"

		#Date
		if(self.date_name.get()=='All'):
			date = '*'
			file_name += 'all_'
		else:
			date = str(self.date_name.get()[2:len(self.date_name.get())-3])
			file_name += date+"_"

		#Week
		if(self.week_name.get()=='All'):
			week = '*'
			file_name += 'all_'
		else:
			week = str(self.week_name.get()[2:len(self.week_name.get())-3])
			file_name += week+"_"

		#Month
		if(self.month_name.get()=='All'):
			month = '*'
			file_name += 'all_'
		else:
			month = str(self.month_name.get())
			file_name += month+"_"

		#Year
		if(self.year_name.get()=='All'):
			year = '*'
			file_name += 'all'
		else:
			year = str(self.year_name.get())
			file_name += year

		file_name += ".csv"

		self.create_status_table()
		self.status_cur.execute("SELECT dates, name, team, task_list, progress_status, meeting_status, project_status, remarks FROM status WHERE name GLOB ? and team GLOB ? and dates GLOB ? and weeks GLOB ? and months GLOB ? and years GLOB ?", (name, team, date, week, month, year))
		self.data = self.status_cur.fetchall()

		#Table Head

		frame4 = Frame(self.frameTable)
		frame4.pack()

		temp = Label(frame4,relief=RIDGE, bg="light blue", text="Date", width=10)
		temp.pack(side=LEFT)

		temp = Label(frame4,relief=RIDGE, bg="light blue", text="User", width=10)
		temp.pack(side=LEFT)

		temp = Label(frame4,relief=RIDGE, bg="light blue", text="Team", width=10)
		temp.pack(side=LEFT)

		temp = Label(frame4,relief=RIDGE, bg="light blue", text="Task List", width=20)
		temp.pack(side=LEFT)

		temp = Label(frame4,relief=RIDGE, bg="light blue", text="Progress Status", width=20)
		temp.pack(side=LEFT)

		temp = Label(frame4,relief=RIDGE, bg="light blue", text="Meeting Status", width=20)
		temp.pack(side=LEFT)

		temp = Label(frame4,relief=RIDGE, bg="light blue", text="Project Status", width=20)
		temp.pack(side=LEFT)

		temp = Label(frame4,relief=RIDGE, bg="light blue", text="Remarks", width=15)
		temp.pack(side=LEFT)

		frame5 = Frame(self.frameTable)
		frame5.pack()

		status_scroll = Scrollbar(frame5)
		status_canvas = Canvas(frame5, height=150, width=1016)
		status_scroll.pack(side=RIGHT, fill=Y)
		status_canvas.pack(side=LEFT)
		status_scroll.config(command=status_canvas.yview)
		status_canvas.config(yscrollcommand=status_scroll.set)

		lists = Frame(status_canvas)
		lists.pack()

		status_canvas.create_window((0,0), window=lists, anchor="nw")

		for i in range(len(self.data)):
			frame_temp = Frame(lists)
			frame_temp.pack(fill=BOTH)
	
			temp = Label(frame_temp,relief=RIDGE, bg="white", width=10, height=1)
			temp.configure(text=self.data[i][0], anchor="nw")
			temp.pack(side=LEFT)
	
			temp = Label(frame_temp,relief=RIDGE, bg="white", width=10, height=1)
			temp.configure(text=self.data[i][1], anchor="nw")
			temp.pack(side=LEFT)
	
			temp = Label(frame_temp,relief=RIDGE, bg="white", width=10, height=1)
			temp.configure(text=self.data[i][2], anchor="nw")
			temp.pack(side=LEFT)
	
			temp = Label(frame_temp,relief=RIDGE, bg="white", width=20, height=1)
			temp.configure(text=self.data[i][3], anchor="nw")
			temp.pack(side=LEFT)
	
			temp = Label(frame_temp,relief=RIDGE, bg="white", width=20, height=1)
			temp.configure(text=self.data[i][4], anchor="nw")
			temp.pack(side=LEFT)
	
			temp = Label(frame_temp,relief=RIDGE, bg="white", width=20, height=1)
			temp.configure(text=self.data[i][5], anchor="nw")
			temp.pack(side=LEFT)
	
			temp = Label(frame_temp,relief=RIDGE, bg="white", width=20, height=1)
			temp.configure(text=self.data[i][6], anchor="nw")
			temp.pack(side=LEFT)
	
			temp = Label(frame_temp,relief=RIDGE, bg="white", width=15, height=1)
			temp.configure(text=self.data[i][7], anchor="nw")
			temp.pack(side=LEFT)

		frameSpace = Frame(self.frameTable)
		frameSpace.pack(pady=10)

		frameTo = Frame(self.frameTable)
		frameTo.pack()

		mail_addr_label = Label(frameTo, text= "To: ", width=10, height=1, anchor='w')
		mail_addr_label.pack(side=LEFT)

		self.mail_to = StringVar()
		mail_addr_entry = Entry(frameTo, textvariable= self.mail_to, width=70)
		mail_addr_entry.pack(side=LEFT)

		frameSub = Frame(self.frameTable)
		frameSub.pack()

		mail_sub_label = Label(frameSub, text= "Subject: ", width=10, height=1, anchor='w')
		mail_sub_label.pack(side=LEFT)

		self.mail_sub = StringVar()
		mail_sub_entry = Entry(frameSub, textvariable= self.mail_sub, width=70)
		mail_sub_entry.pack(side=LEFT)

		frameBody=Frame(self.frameTable)
		frameBody.pack()

		mail_body_label = Label(frameBody, text= "Message: ", width=10, height=1, anchor='w')
		mail_body_label.pack(side=LEFT)

		mail_body_scroll = Scrollbar(frameBody)
		self.mail_body_text = Text(frameBody, height=4, width=68)
		mail_body_scroll.pack(side=RIGHT, fill=Y)
		self.mail_body_text.pack(side=LEFT, fill=Y)
		mail_body_scroll.config(command=self.mail_body_text.yview)
		self.mail_body_text.config(yscrollcommand=mail_body_scroll.set)

		frameGen = Frame(self.frameTable)
		frameGen.pack()

		mail_btn = Button(frameGen,text="Send", bg="DeepSkyBlue4", fg = "white", command = lambda : self.send_report(file_name, str(len(self.data)), self.mail_sub.get(), self.mail_to.get(), self.mail_body_text.get('1.0', 'end-1c')), width=10)
		mail_btn.pack(side=LEFT, pady=5)

		export_btn = Button(frameGen,text="Export", bg="DeepSkyBlue4", fg = "white", command = lambda : self.save_report(file_name, str(len(self.data))), width=10)
		export_btn.pack(side=LEFT, pady=5)

	def save_report(self, file_name):
		if(messagebox.askyesno("Warning", "Are you sure?")):
			try:
				with open(file_name, "w") as csv_file:
					writer = csv.writer(csv_file, delimiter=',')
					writer.writerow(['Date', 'User', 'Team', 'Task List', 'Progress Status', 'Meeting Status', 'Project Status', 'Remarks'])
					for line in self.data:
						writer.writerow(list(line))
					print("Write to ",file_name," is successful!")
					self.screen = 18
					self.quit()
			except Exception as e:
				print(e)

	def send_report(self, file_name, total, sub, you, body):
		if(you == ''):
			messagebox.showinfo("Error", "Mail address cannot be empty while sending an email!")
		elif(messagebox.askyesno("Warning", "Are you sure?")):
			try:
				me = 'noreply.nslstatus@gmail.com'
				password = 'a1234567890z'
				with open(file_name, "w") as csv_file:
					writer = csv.writer(csv_file, delimiter=',')
					writer.writerow(['Date', 'User', 'Team', 'Task List', 'Progress Status', 'Meeting Status', 'Project Status', 'Remarks'])
					for line in self.data:
						writer.writerow(list(line))
					print("Write to ",file_name," is successful!")

				#Sending mail
				msg = MIMEMultipart()
				msg['Subject'] = sub
				msg['From'] = me
				msg['To'] = you
				msg.attach(MIMEText(body, 'html'))

				attachment = [file_name,]

				for f in attachment:
					with open(f, 'rb') as a_file:
						basename = os.path.basename(f)
						part = MIMEApplication(a_file.read(), Name=basename)
					part['Content-Disposition'] = 'attachment; filename="%s"' % basename
					msg.attach(part)

				server  = smtplib.SMTP("smtp.gmail.com", 25)
				server.ehlo()
				server.starttls()
				server.login(me, password)
				server.sendmail(me, you, msg.as_string())
				server.quit()
				if(messagebox.askyesno("Warning", "Do you want to save this file?")):
					messagebox.showinfo("Success", "Mail sent and file saved successfully!")
				else:
					os.system('rm '+file_name)
					messagebox.showinfo("Success", "Mail sent successfully!")
				self.screen = 20
				self.quit()
			except Exception as e:
				print(e)

	def go_prev(self):
		self.screen = 22
		self.quit()

	def leave(self):
		quit()
