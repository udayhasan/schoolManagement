class forgot_id_page(Frame):
	screen = 12
	login_conn = None
	login_cur  = None
	forgot_id_name_label = None

	error_msg  = " "

	def __init__(self,master):
		super(forgot_id_page,self).__init__(master)
		self.login_conn = sqlite3.connect('./db/users.db')
		self.login_cur  = self.login_conn.cursor()
		self.pack()
		self.define_widgets()

	def define_widgets(self):
		frame1 = Frame(self)
		frame1.pack()
		forgot_user_password=Label(frame1,text="::Forgot User Name?::")
		forgot_user_password.config(width=200, font=("Courier", 25))
		forgot_user_password.pack(pady=5)

		canvas = Canvas(frame1, height=2, borderwidth=0, highlightthickness=0, bg="black")
		canvas.pack(fill=X, padx=80, pady=10)

		frame2 = Frame(self)
		frame2.pack()

		forgot_id_email=Label(frame2,text="Email:", width=10, anchor=W)
		forgot_id_email.pack(side=LEFT, padx=2, pady=2)

		self.forgot_id_email=StringVar()
		forgot_id_email_entry=Entry(frame2,textvariable=self.forgot_id_email, width=40)
		forgot_id_email_entry.pack(side=LEFT, padx=2, pady=2)
		forgot_id_email_entry.focus_set()

		frame3 = Frame(self)
		frame3.pack()

		forgot_id_btn=Button(frame3,text="Find", bg="DeepSkyBlue4", fg = "white", command=self.pre_forgot_id_find, width=10)
		forgot_id_btn.pack(side=LEFT, padx=2, pady=2)

		back=Button(frame3,text="< Prev", command=self.go_prev, width=10)
		back.pack(side=LEFT, padx=2, pady=2)

		exit=Button(frame3,text="Exit", bg = "brown3", fg = "white", command=self.leave, width=10)
		exit.pack(side=LEFT, padx=2, pady=2)

		self.frame4 = Frame(self)
		self.frame4.pack()

	def create_user_table(self):
		self.login_cur.execute("CREATE TABLE IF NOT EXISTS users(name TEXT, email TEXT, password TEXT)")

	def pre_forgot_id_find(self):
		self.frame4.pack_forget()
		self.frame4 = Frame(self)
		self.frame4.pack()
		self.forgot_id_name_label=Label(self.frame4, relief=RIDGE, text="<User ID>", state=DISABLED)
		self.forgot_id_name_label.pack(side=LEFT, padx=2, pady=2)
		self.forgot_id_find()

	def forgot_id_find(self):
		self.create_user_table()
		if(self.forgot_id_email.get() == ''):
			self.error_msg = "Necessary field(s) cannot be empty!"
			messagebox.showinfo("Error", self.error_msg)
			self.screen = 12
			self.quit()
		else:
			try:
				self.login_cur.execute("SELECT name FROM users WHERE email = ?", (self.forgot_id_email.get(),))
				id_name = self.login_cur.fetchall()
				self.forgot_id_name_label.configure(text=":: "+str(id_name[0][0])+" ::", state=ACTIVE, fg="blue", font=("Courier", 25))
			except Exception as e:
				self.error_msg = "Error Happened!\nError: "+str(e)
				messagebox.showinfo("Error", self.error_msg)

	def go_prev(self):
		self.login_conn.close()
		self.screen = 0
		self.quit()

	def leave(self):
		self.login_conn.close()
		quit()