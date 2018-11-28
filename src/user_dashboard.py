from tkinter import *
import sqlite3
import datetime
class user_dashboard(Frame):

	screen = 1

	name   = None
	admin  = None

	me     		= "noreply.nslstatus@gmail.com"
	you    		= "noreply.nslstatus@gmail.com"
	password 	= 'a1234567890z'
	to_email    = []

	task_id 	= None

	def __init__(self,master, name, admin):
		super(user_dashboard,self).__init__(master)
		self.pack()
		self.name = name
		self.admin = admin

		self.login_conn = sqlite3.connect('./db/users.db')
		self.login_cur  = self.login_conn.cursor()

		self.task_conn = sqlite3.connect("./db/tasks.db")
		self.task_cur  = self.task_conn.cursor()

		self.food_conn = sqlite3.connect("./db/foods.db")
		self.food_cur  = self.food_conn.cursor()

		self.define_widgets()

	def create_user_table(self):
		self.login_cur.execute("CREATE TABLE IF NOT EXISTS users(name TEXT, email TEXT, password TEXT, admin_status TEXT)")

	def create_food_table(self):
		self.food_cur.execute("CREATE TABLE IF NOT EXISTS foods(name TEXT, value TEXT, dates TEXT, weeks TEXT, months TEXT, years TEXT)")

	def backup_def(self):
		try:
			self.create_user_table()
			self.login_cur.execute("SELECT email FROM users WHERE admin_status = 1")
			data = self.login_cur.fetchall()

			for mail in data:
				self.to_email.append(mail[0])

			print(self.to_email)

			msg = MIMEMultipart()
			msg['Subject'] = 'Backup-'+datetime.datetime.now().strftime("%d-%b-%Y")+"-"+datetime.datetime.now().strftime("%H:%M:%S")
			msg['From'] = self.me
			msg['To'] = ", ".join(self.to_email)
			msg.attach(MIMEText("This is backup on "+datetime.datetime.now().strftime("%d-%b-%Y")+" at time: "+datetime.datetime.now().strftime("%H:%M:%S"), 'html'))

			attachment = ['./db/users.db', './db/status.db', './db/tasks.db', './db/attns.db', './db/foods.db']

			for f in attachment:
				with open(f, 'rb') as a_file:
					basename = os.path.basename(f)
					part = MIMEApplication(a_file.read(), Name=basename)
				part['Content-Disposition'] = 'attachment; filename="%s"' % basename
				msg.attach(part)

			server  = smtplib.SMTP("smtp.gmail.com", 25)
			server.ehlo()
			server.starttls()
			server.login(self.me, self.password)
			server.sendmail(self.me, self.to_email, msg.as_string())
			server.quit()
		except Exception as e:
			print(e)

	def define_widgets(self):
		#for line1:
		frame1 = Frame(self)
		frame1.pack()
		dash_board_label=Label(frame1,text="::Dashboard - "+self.name+"::")
		dash_board_label.config(width=200, font=("Courier", 25))
		dash_board_label.pack(pady=5)

		canvas = Canvas(frame1, height=2, borderwidth=0, highlightthickness=0, bg="black")
		canvas.pack(fill=X, padx=80, pady=10)

		if(self.admin==1):
			dash_btn_width = 16
		else:
			dash_btn_width = 32

		frameHolder = Frame(self)
		frameHolder.pack()

		#for user buttons:
		frame2 = Frame(frameHolder)
		frame2.pack(side=LEFT)

		manage_status_btn=Button(frame2,text="Manage\nStatus",command=lambda: self.set_value(9), width = dash_btn_width, height=3, bd=4, bg="OliveDrab2")
		manage_status_btn.pack(padx=2, pady=2)

		self.create_task_table()
		self.task_cur.execute("SELECT ids, a_by, task_list, description, deadline, priority, status FROM tasks WHERE a_to = ?", (self.name,))
		data2 = self.task_cur.fetchall()
		data3 = []

		for i in range(len(data2)):
			if(data2[i][6] != 'complete'):
				data3.append(data2[i])

		manage_task_btn=Button(frame2,text="Manage Tasks\nUnfinished ("+str(len(data3))+")",command=lambda: self.set_value(23), width = dash_btn_width, height=3, bd=4, bg="chartreuse2")
		manage_task_btn.pack(padx=2, pady=2)

		manage_profile_btn=Button(frame2,text="Manage\nProfile",command=lambda: self.set_value(4), width = dash_btn_width, height=3, bd=4, bg="green2")
		manage_profile_btn.pack(padx=2, pady=2)

		self.create_food_table()
		dates 	= datetime.datetime.now().strftime("%d-%b-%Y")
		self.food_cur.execute("SELECT value, name FROM foods WHERE name = ? and dates = ?", (self.name, dates))
		foodData = self.food_cur.fetchall()

		if(len(foodData) > 0 and int(foodData[0][0]) == 1):

			self.food_btn=Button(frame2,text="Attendance\n& Food", bg="green3", fg = "white", command = lambda : self.set_value(24), width = dash_btn_width, height=3, bd=4)
			self.food_btn.pack(padx=2, pady=2)
			
		elif(len(foodData) > 0 and int(foodData[0][0]) == 0):

			self.food_btn=Button(frame2, text="Attendance\n& Food", bg="tomato", fg = "white", command = lambda : self.set_value(24), width = dash_btn_width, height=3, bd=4)
			self.food_btn.pack(padx=2, pady=2)

		elif(len(foodData) == 0):

			self.food_btn=Button(frame2, text="Attendance\n& Food", bg="tomato", fg = "white", command = lambda : self.set_value(24), width = dash_btn_width, height=3, bd=4)
			self.food_btn.pack(padx=2, pady=2)

		else:
			self.error_msg = "Error Happend!"
			messagebox.showinfo("Error", self.error_msg)

		#for admin buttons:
		frame3 = Frame(frameHolder)
		frame3.pack(side=LEFT)

		if(self.admin == 1):
			manage_users_btn=Button(frame3,text="Manage\nUsers",command=lambda: self.set_value(25), width = dash_btn_width, height=3, bd=4, bg="peach puff")
			manage_users_btn.pack(padx=2, pady=2)

			all_task_btn=Button(frame3,text="All Tasks",command=lambda: self.set_value(17), width = dash_btn_width, height=3, bd=4, bg="salmon")
			all_task_btn.pack(padx=2, pady=2)

			export_report_btn=Button(frame3,text="Export\nReport",command=lambda: self.set_value(22), width = dash_btn_width, height=3, bd=4, bg="firebrick2")
			export_report_btn.pack(padx=2, pady=2)

			backup_btn=Button(frame3,text="Backup",command=self.backup_def, width = dash_btn_width, height=3, bd=4, bg="red3")
			backup_btn.pack(padx=2, pady=2)

		#for logout:
		log_out=Button(frame2,text="Log Out",command=self.set_logout, bg="green4", fg = "white", width = dash_btn_width, height=3, bd=4)
		log_out.pack(padx=2, pady=2)

		if(self.admin==1):
			exit=Button(frame3,text="Exit", bg = "red4", fg = "white", command=self.leave, width = dash_btn_width, height=3, bd=4)
			exit.pack(padx=2, pady=2)
		else:
			exit=Button(frame2,text="Exit", bg = "red4", fg = "white", command=self.leave, width = dash_btn_width, height=3, bd=4)
			exit.pack(padx=2, pady=2)

	def create_task_table(self):
		self.task_cur.execute("CREATE TABLE IF NOT EXISTS tasks(ids TEXT, dates TEXT, up_time TEXT, a_by TEXT, a_to TEXT, task_list TEXT, description TEXT, est_date TEXT, deadline TEXT, comments TEXT, priority TEXT, remarks TEXT, status TEXT)")

	def set_logout(self):
		self.screen = 0
		self.quit()

	def set_value(self, value):
		self.screen = value
		print(self.screen)
		self.quit()

	def leave(self):
		quit()
