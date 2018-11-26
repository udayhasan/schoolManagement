class add_user_page(Frame):
	screen = 2
	login_conn = None
	login_cur  = None

	error_msg  = " "

	def __init__(self,master):
		super(add_user_page,self).__init__(master)
		self.login_conn = sqlite3.connect('./db/users.db')
		self.login_cur  = self.login_conn.cursor()
		self.pack()
		self.define_widgets()

	def define_widgets(self):
		frame1 = Frame(self)
		frame1.pack(pady=5)
		add_page_label=Label(frame1,text="::Add User::")
		add_page_label.config(width=200, font=("Courier", 25))
		add_page_label.pack()

		canvas = Canvas(frame1, height=2, borderwidth=0, highlightthickness=0, bg="black")
		canvas.pack(fill=X, padx=80, pady=10)

		frame2 = Frame(self)
		frame2.pack()

		add_name_label=Label(frame2,text="User Name:", width=13, anchor=W)
		add_name_label.pack(side=LEFT, padx=2, pady=2)

		self.add_name=StringVar()
		add_name_entry=Entry(frame2,textvariable=self.add_name, width=40)
		add_name_entry.pack(side=LEFT, padx=2, pady=2)
		add_name_entry.focus_set()

		frame3 = Frame(self)
		frame3.pack()

		add_email_label=Label(frame3,text="User Email:", width=13, anchor=W)
		add_email_label.pack(side=LEFT, padx=2, pady=2)

		self.add_email=StringVar()
		add_email_entry=Entry(frame3,textvariable=self.add_email, width=40)
		add_email_entry.pack(side=LEFT, padx=2, pady=2)

		frame4 = Frame(self)
		frame4.pack()

		add_pass_label=Label(frame4,text="Password:", width=13, anchor=W)
		add_pass_label.pack(side=LEFT, padx=2, pady=2)

		self.add_pass=StringVar()
		add_pass_entry=Entry(frame4,textvariable=self.add_pass, width=40)
		add_pass_entry.pack(side=LEFT, padx=2, pady=2)

		frame6 = Frame(self)
		frame6.pack()

		self.admin_status=IntVar()
		add_admin_check=Checkbutton(frame6,text="Add as admin?", variable=self.admin_status, width=30)
		add_admin_check.pack(side=RIGHT, padx=2, pady=2)

		frame5 = Frame(self)
		frame5.pack()

		add_btn=Button(frame5,text="Add User", bg="DeepSkyBlue4", fg = "white", command=self.add_user)
		add_btn.pack(side=LEFT, padx=2, pady=2)

		back=Button(frame5,text="< Prev", command=self.go_prev)
		back.pack(side=LEFT, padx=2, pady=2)

		exit=Button(frame5,text="Exit", bg = "brown3", fg = "white", command=self.leave)
		exit.pack(side=LEFT, padx=2, pady=2)

	def create_user_table(self):
		self.login_cur.execute("CREATE TABLE IF NOT EXISTS users(name TEXT, email TEXT, password TEXT, admin_status TEXT)")

	def add_user(self):
		if(messagebox.askyesno("Warning", "Are you sure?")):
			self.create_user_table()
			if(self.add_name.get() == '' or self.add_email.get() == '' or self.add_pass.get() == ''):
				self.error_msg = "Necessary field(s) cannot be empty!"
				messagebox.showinfo("Error", self.error_msg)
			else:
				try:
					self.login_cur.execute("SELECT name, email FROM users")
					user_details = self.login_cur.fetchall()
					user_names  = [user_details[i][0] for i in range(len(user_details))]
					user_emails = [user_details[i][1] for i in range(len(user_details))]

					print(user_names, user_emails)

					if((self.add_name.get() not in user_names) and (self.add_email.get() not in user_emails)):
						self.login_cur.execute("INSERT INTO users(name, email, password, admin_status) VALUES (?, ?, ?, ?)", (self.add_name.get(), self.add_email.get(), self.add_pass.get(), str(self.admin_status.get())))
						self.login_conn.commit()
						time.sleep(0.02)
						print("New User named %s is added to the database" %(self.add_name.get()))
						self.screen = 2
						self.quit()
					else:
						self.error_msg = "You cannot add this User Name/Email, already exists!"
						messagebox.showinfo("Error", self.error_msg)
						self.screen = 2
						self.quit()
				except Exception as e:
					self.error_msg = "Error happened!\nError: "+str(e)
					messagebox.showinfo("Error", self.error_msg)

	def go_prev(self):
		self.login_conn.close()
		self.screen = 25
		self.quit()

	def leave(self):
		self.login_conn.close()
		quit()
