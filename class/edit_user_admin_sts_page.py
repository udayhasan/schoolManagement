class edit_user_admin_sts_page(Frame):
	screen = 3
	login_conn = None
	login_cur  = None

	error_msg  = " "

	def __init__(self,master, name):
		super(edit_user_admin_sts_page,self).__init__(master)
		self.login_conn = sqlite3.connect('./db/users.db')
		self.login_cur  = self.login_conn.cursor()
		self.name       = name
		self.pack()
		self.define_widgets()

	def define_widgets(self):
		frame1 = Frame(self)
		frame1.pack()
		edit_name_label=Label(frame1,text="::Edit Admin Status::")
		edit_name_label.config(width=200, font=("Courier", 25))
		edit_name_label.pack(pady=5)

		canvas = Canvas(frame1, height=2, borderwidth=0, highlightthickness=0, bg="black")
		canvas.pack(fill=X, padx=80, pady=10)
		
		#Add admin
		frame2 = Frame(self)
		frame2.pack()
		
		assigned_to_label=Label(frame2,text="Make Admin:", width=20, anchor=W)
		assigned_to_label.pack(side=LEFT, pady=5)

		self.login_cur.execute("SELECT name FROM users")
		name_list = self.login_cur.fetchall()

		self.assigned_to_name=StringVar()
		self.assigned_to_name.set('admin')

		assigned_to_list=OptionMenu(frame2,self.assigned_to_name, *name_list)
		assigned_to_list.config(width=35)
		assigned_to_list.pack(side=LEFT, padx=2, pady=5)

		admin_btn = Button(frame2,text="Make Admin", command=self.make_admin_def, fg = 'white', bg = 'DeepSkyBlue4', width=10)
		admin_btn.pack(side=LEFT, padx=2, pady=2)

		#Remove from admin
		if(self.name == "admin"):
			frame3 = Frame(self)
			frame3.pack()
			
			remove_from_label=Label(frame3,text="Remove Admin:", width=20, anchor=W)
			remove_from_label.pack(side=LEFT, pady=5)

			self.remove_from_name=StringVar()
			self.remove_from_name.set('admin')

			remove_from_list=OptionMenu(frame3,self.remove_from_name, *name_list)
			remove_from_list.config(width=35)
			remove_from_list.pack(side=LEFT, padx=2, pady=5)

			remove_btn = Button(frame3,text="Remove Admin", command=self.remove_admin_def, fg = 'white', bg = 'DeepSkyBlue4', width=10)
			remove_btn.pack(side=LEFT, padx=2, pady=2)

		frameBelow = Frame(self)
		frameBelow.pack()

		back=Button(frameBelow,text="< Prev", command=self.go_prev, width=10)
		back.pack(side=LEFT, padx=2, pady=2)

		exit=Button(frameBelow,text="Exit", bg = "brown3", fg = "white", command=self.leave, width=10)
		exit.pack(side=LEFT, padx=2, pady=2)

	def create_user_table(self):
		self.login_cur.execute("CREATE TABLE IF NOT EXISTS users(name TEXT, email TEXT, password TEXT, admin_status TEXT)")

	def make_admin_def(self):
		if(messagebox.askyesno("Warning", "Are you sure?")):
			self.create_user_table()
			if(self.assigned_to_name.get()==''):
				self.error_msg = "Name field cannot be empty!"
				messagebox.showinfo("Error", self.error_msg)
			else:
				try:
					self.login_cur.execute("UPDATE users SET admin_status = ? WHERE name = ?", ('1', self.assigned_to_name.get()[2:len(self.assigned_to_name.get())-3]))
					self.login_conn.commit()
					time.sleep(0.02)
					print("User %s is made an Admin" %(self.assigned_to_name.get()[2:len(self.assigned_to_name.get())-3]))
					self.screen = 3
					self.quit()
				except Exception:
					self.error_msg = "Invalid search name!"
					messagebox.showinfo("Error", self.error_msg)

	def remove_admin_def(self):
		if(messagebox.askyesno("Warning", "Are you sure?")):
			self.create_user_table()
			if(self.remove_from_name.get()==''):
				self.error_msg = "Name field cannot be empty!"
				messagebox.showinfo("Error", self.error_msg)
			elif(self.remove_from_name.get()=='admin'):
				self.error_msg = "You cannot delete 'admin'"
				messagebox.showinfo("Error", self.error_msg)
			else:
				try:
					self.login_cur.execute("UPDATE users SET admin_status = ? WHERE name = ?", ('0', self.remove_from_name.get()[2:len(self.remove_from_name.get())-3]))
					self.login_conn.commit()
					time.sleep(0.02)
					print("User %s is removed from Admin" %(self.remove_from_name.get()[2:len(self.remove_from_name.get())-3]))
					self.screen = 3
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