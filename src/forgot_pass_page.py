class forgot_pass_page(Frame):
	screen = 7
	login_conn = None
	login_cur  = None

	error_msg  = " "

	def __init__(self,master):
		super(forgot_pass_page,self).__init__(master)
		self.login_conn = sqlite3.connect('./db/users.db')
		self.login_cur  = self.login_conn.cursor()
		self.pack()
		self.define_widgets()

	def define_widgets(self):
		frame1 = Frame(self)
		frame1.pack()
		forgot_user_password=Label(frame1,text="Forgot Password?")
		forgot_user_password.config(width=200, font=("Courier", 25))
		forgot_user_password.pack(pady=5)

		canvas = Canvas(frame1, height=2, borderwidth=0, highlightthickness=0, bg="black")
		canvas.pack(fill=X, padx=80, pady=10)

		frame2 = Frame(self)
		frame2.pack()

		forgot_pass_name=Label(frame2,text="User Name:", width=20, anchor=W)
		forgot_pass_name.pack(side=LEFT, padx=2, pady=2)

		self.forgot_pass_name=StringVar()
		forgot_pass_name_entry=Entry(frame2,textvariable=self.forgot_pass_name, width=40)
		forgot_pass_name_entry.pack(side=LEFT, padx=2, pady=2)
		forgot_pass_name_entry.focus_set()

		frame3 = Frame(self)
		frame3.pack()

		forgot_pass_email=Label(frame3,text="Email:", width=20, anchor=W)
		forgot_pass_email.pack(side=LEFT, padx=2, pady=2)

		self.forgot_pass_email=StringVar()
		forgot_pass_email_entry=Entry(frame3,textvariable=self.forgot_pass_email, width=40)
		forgot_pass_email_entry.pack(side=LEFT, padx=2, pady=2)

		frame4 = Frame(self)
		frame4.pack()

		forgot_pass_btn=Button(frame4,text="Send Password", bg="DeepSkyBlue4", fg = "white", command=self.forgot_pass_send, width=10)
		forgot_pass_btn.pack(side=LEFT, padx=2, pady=2)

		back=Button(frame4,text="< Prev", command=self.go_prev, width=10)
		back.pack(side=LEFT, padx=2, pady=2)

		exit=Button(frame4,text="Exit", bg = "brown3", fg = "white", command=self.leave, width=10)
		exit.pack(side=LEFT, padx=2, pady=2)

	def create_user_table(self):
		self.login_cur.execute("CREATE TABLE IF NOT EXISTS users(name TEXT, email TEXT, password TEXT)")

	def forgot_pass_send(self):
		self.create_user_table()
		if(self.forgot_pass_name.get() == '' or self.forgot_pass_email.get() == ''):
			self.error_msg = "Necessary field(s) cannot be empty!"
			messagebox.showinfo("Error", self.error_msg)
		else:
			try:
				self.login_cur.execute("SELECT password FROM users WHERE name = ? and email = ?", (self.forgot_pass_name.get(), self.forgot_pass_email.get()))
				password = self.login_cur.fetchall()
	
				me      = "noreply.nslstatus@gmail.com"
				you     = self.forgot_pass_email.get()
				body    = "Dear "+self.forgot_pass_name.get()+",\nYour lost password is :"+str(password[0][0])+"\nN.B: You don't need to reply this message.\nThanks.\n"+time.asctime(time.localtime(time.time()))

				msg = MIMEMultipart()
				msg['Subject'] = "Forgotten user password"
				msg['From'] = me
				msg['To'] = you
				msg.attach(MIMEText(str(body), 'html'))

				server  = smtplib.SMTP("smtp.gmail.com", 25)
				server.ehlo()
				server.starttls()
				server.login(me, 'a1234567890z')
				server.sendmail(me, you, msg.as_string())
				server.quit()
				self.login_conn.close()
				print("Mail sent successfully!")
				self.screen = 7
				self.quit()
	
			except Exception as e:
				self.error_msg = "Error happened!\nError: "+str(e)
				messagebox.showinfo("Error", self.error_msg)

	def go_prev(self):
		self.screen = 0
		self.quit()

	def leave(self):
		quit()