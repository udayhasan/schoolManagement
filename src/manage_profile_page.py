class manage_profile_page(Frame):
	screen = 4
	name = None
	login_conn = None
	login_cur  = None

	error_msg  = " "

	def __init__(self,master, name):
		super(manage_profile_page,self).__init__(master)
		self.name = name
		self.login_conn = sqlite3.connect('./db/users.db')
		self.login_cur  = self.login_conn.cursor()
		self.pack()
		self.define_widgets()

	def define_widgets(self):

		frame1 = Frame(self)
		frame1.pack()
		edit_email_label=Label(frame1,text="::Manage Profile::")
		edit_email_label.config(width=200, font=("Courier", 25))
		edit_email_label.pack(pady=5)

		canvas = Canvas(frame1, height=2, borderwidth=0, highlightthickness=0, bg="black")
		canvas.pack(fill=X, padx=80, pady=10)

		self.create_user_table()
		self.login_cur.execute("SELECT email FROM users WHERE name = ?", (self.name,))
		data = self.login_cur.fetchall()

		frameDetails = Frame(self)
		frameDetails.pack()

		user_name_label=Label(frameDetails,text="User Name:", width=20, anchor=W)
		user_name_label.pack(side=LEFT, padx=2, pady=2)

		user_name_entry=Label(frameDetails,text=self.name, width=40, anchor=W)
		user_name_entry.pack(side=LEFT, padx=2, pady=2)

		frameEmail = Frame(self)
		frameEmail.pack()

		user_email_label=Label(frameEmail,text="User Email:", width=20, anchor=W)
		user_email_label.pack(side=LEFT, padx=2, pady=2)

		self.edit_email_cur=StringVar()
		self.edit_email_cur.set(data[0][0])
		user_email_entry=Label(frameEmail,textvariable=self.edit_email_cur, width=40, anchor=W)
		user_email_entry.pack(side=LEFT, padx=2, pady=2)

		frameLine = Frame(self)
		frameLine.pack()

		canvas = Canvas(frameLine, height=2, width=650, borderwidth=0, highlightthickness=0, bg="black")
		canvas.pack(pady=10)

		frame2 = Frame(self)
		frame2.pack()

		frame3 = Frame(self)
		frame3.pack()

		edit_email_new_label=Label(frame3,text="New Email:", width=20, anchor=W)
		edit_email_new_label.pack(side=LEFT, padx=2, pady=2)

		self.edit_email_new=StringVar()
		edit_email_new_entry=Entry(frame3,textvariable=self.edit_email_new, width=40)
		edit_email_new_entry.pack(side=LEFT, padx=2, pady=2)

		frame4 = Frame(self)
		frame4.pack()

		edit_email_btn=Button(frame4,text="Change Email", bg="DeepSkyBlue4", fg = "white", command=self.edit_user_email, width=16)
		edit_email_btn.pack(side=LEFT, padx=2, pady=2)

		frame10 = Frame(self)
		frame10.pack()

		canvas = Canvas(frame10, height=2, width=650, borderwidth=0, highlightthickness=0, bg="black")
		canvas.pack(pady=10)

		frame5 = Frame(self)
		frame5.pack()

		edit_pass_cur_label=Label(frame5,text="Current Password:", width=20, anchor=W)
		edit_pass_cur_label.pack(side=LEFT, padx=2, pady=2)

		self.edit_pass_cur=StringVar()
		edit_pass_cur_entry=Entry(frame5,textvariable=self.edit_pass_cur, width=40, show="*")
		edit_pass_cur_entry.pack(side=LEFT, padx=2, pady=2)

		frame6 = Frame(self)
		frame6.pack()

		edit_pass_new_label=Label(frame6,text="New Password:", width=20, anchor=W)
		edit_pass_new_label.pack(side=LEFT, padx=2, pady=2)

		self.edit_pass_new=StringVar()
		edit_pass_new_entry=Entry(frame6,textvariable=self.edit_pass_new, width=40, show="*")
		edit_pass_new_entry.pack(side=LEFT, padx=2, pady=2)

		frame7 = Frame(self)
		frame7.pack()

		edit_pass_confirm_label=Label(frame7,text="Confirm Password:", width=20, anchor=W)
		edit_pass_confirm_label.pack(side=LEFT, padx=2, pady=2)

		self.edit_pass_confirm=StringVar()
		edit_pass_confirm_entry=Entry(frame7,textvariable=self.edit_pass_confirm, width=40, show="*")
		edit_pass_confirm_entry.pack(side=LEFT, padx=2, pady=2)

		frame8 = Frame(self)
		frame8.pack()

		edit_pass_btn=Button(frame8,text="Change Password", bg="DeepSkyBlue4", fg = "white", command=self.edit_user_password, width=16)
		edit_pass_btn.pack(side=LEFT, padx=2, pady=2)

		frame9=Frame(self)
		frame9.pack(pady=15)

		back=Button(frame9,text="< Prev", command=self.go_prev, width=6)
		back.pack(side=LEFT, padx=2, pady=2)

		exit=Button(frame9,text="Exit", bg = "brown3", fg = "white", command=self.leave, width=6)
		exit.pack(side=LEFT, padx=2, pady=2)

	def create_user_table(self):
		self.login_cur.execute("CREATE TABLE IF NOT EXISTS users(name TEXT, email TEXT, password TEXT)")

	def edit_user_email(self):
		self.create_user_table()
		if(self.edit_email_cur.get() == '' or self.edit_email_new.get() == ''):
			self.error_msg = "Necessary field(s) cannot be empty!"
			messagebox.showinfo("Error", self.error_msg)
		else:
			try:
				self.create_user_table()
				self.login_cur.execute("SELECT * FROM users WHERE name = ? and email = ?", (self.name,self.edit_email_cur.get()))
				data = self.login_cur.fetchall()

				if(len(data)==0):
					self.error_msg = "Incorrect inputs!"
					messagebox.showinfo("Error", self.error_msg)

				else:
					if(messagebox.askyesno("Warning", "Are you sure?")):
						self.login_cur.execute("UPDATE users SET email = ? WHERE name = ? and email = ?", (self.edit_email_new.get(), self.name, self.edit_email_cur.get()))
						self.login_conn.commit()
						time.sleep(0.02)
						self.login_conn.close()
						print("User email of %s is replaced by %s" %(self.edit_email_cur.get(), self.edit_email_new.get()))
						messagebox.showinfo("Success Message", "User email changed\nfrom: "+self.edit_email_cur.get()+"\nto: "+self.edit_email_new.get())
					else:
						print("Email is not changed!")
				self.screen = 4
				self.quit()
			except Exception as e:
				self.error_msg = "Error happened!\nError: "+str(e)
				messagebox.showinfo("Error", self.error_msg)

	def edit_user_password(self):
		self.create_user_table()
		if(self.edit_pass_confirm.get() == '' or self.edit_pass_cur.get() == '' or self.edit_pass_new.get() == ''):
			self.error_msg = "Necessary field(s) cannot be empty!"
			messagebox.showinfo("Error", self.error_msg)
		elif(self.edit_pass_confirm.get() == self.edit_pass_new.get()):
			try:
				self.create_user_table()
				self.login_cur.execute("SELECT * FROM users WHERE name = ? and password = ?", (self.name, self.edit_pass_cur.get()))
				data = self.login_cur.fetchall()

				if(len(data)==0):
					self.error_msg = "Incorrect inputs!"
					messagebox.showinfo("Error", self.error_msg)

				else:
					if(messagebox.askyesno("Warning", "Are you sure?")):
						self.login_cur.execute("UPDATE users SET password = ? WHERE name = ? and password = ?", (self.edit_pass_new.get(), self.name, self.edit_pass_cur.get()))
						self.login_conn.commit()
						time.sleep(0.02)
						self.login_conn.close()
						print("Password for %s is changed successfully!" %(name))
						messagebox.showinfo("Success Message", "User password changed successfully!")
					else:
						print("Password is not changed!")
				self.screen = 4
				self.quit()
			except Exception as e:
				self.error_msg = "Error happened!\nError: "+str(e)
				messagebox.showinfo("Error", self.error_msg)
		else:
			self.error_msg = "Your password is not confirmed correctly!"
			messagebox.showinfo("Error", self.error_msg)

	def go_prev(self):
		self.screen = 1
		self.quit()

	def leave(self):
		quit()