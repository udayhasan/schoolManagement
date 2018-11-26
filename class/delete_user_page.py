class delete_user_page(Frame):
	screen = 6
	login_conn = None
	login_cur  = None
	name       = None

	error_msg  = " "

	def __init__(self,master, name):
		super(delete_user_page,self).__init__(master)
		self.login_conn = sqlite3.connect('./db/users.db')
		self.login_cur  = self.login_conn.cursor()
		self.name       = name
		self.pack()
		self.define_widgets()

	def define_widgets(self):
		delete_user_label=Label(self,text="Delete User")
		delete_user_label.pack(fill=X, padx=10, pady=10)

		#frame for line1:
		frame1 = Frame(self)
		frame1.pack()
		delete_user_name_label=Label(frame1,text="User Name:")
		delete_user_name_label.pack(side=LEFT)

		self.delete_user_name=StringVar()
		self.delete_user_name_entry=Entry(frame1,textvariable=self.delete_user_name)
		self.delete_user_name_entry.pack(side=LEFT)

		delete_user_btn=Button(frame1,text="Delete User", bg="DeepSkyBlue4", fg = "white", command=self.delete_user)
		delete_user_btn.pack(side=LEFT)

		#frame for line3:
		frame3 = Frame(self)
		frame3.pack()

		temp = Label(frame3,relief=RIDGE, text="Current Users", bg="light blue")
		temp.config(width=23, height=1)
		temp.pack(side=LEFT)

		temp = Label(frame3,relief=RIDGE, text="Email", bg="light blue")
		temp.config(width=70, height=1)
		temp.pack(side=LEFT, pady=5)

		temp = Label(frame3,relief=RIDGE, text="Admin Status", bg="light blue")
		temp.config(width=30, height=1)
		temp.pack(side=LEFT, pady=5)

		#scrolling part start
		scroll_frame = Frame(self)
		scroll_frame.pack()

		#scroll canvas
		list_scrollbar = Scrollbar(scroll_frame)
		scroll_canvas = Canvas(scroll_frame, height=200, width=980)
		scroll_canvas.pack(side=LEFT, expand=True, fill=Y)
		list_scrollbar.pack(side=RIGHT, fill=Y)
		
		list_scrollbar.config(command=scroll_canvas.yview)
		scroll_canvas.config(yscrollcommand=list_scrollbar.set)
		#scroll_canvas.config(scrollregion=scroll_canvas.bbox("all"))

		lists = Frame(scroll_canvas)
		lists.pack(fill=X)

		scroll_canvas.create_window((0,0), window=lists, anchor="nw")

		self.create_user_table()
		self.login_cur.execute("SELECT name, email, admin_status FROM users")
		data = self.login_cur.fetchall()

		self.temp_user_name_btn = []

		for i in range(len(data)):
			self.temp_user_name_btn.append(None)

		for i in range(len(data)):
			frame_temp = Frame(lists)
			frame_temp.pack(fill=BOTH)
			self.temp_user_name_btn[i] = Button(frame_temp, bg="white", fg="black", text=str(data[i][0]), command=lambda i=i : self.copy_name_to_field(i))
			self.temp_user_name_btn[i].config(width = 20, height = 1, anchor="nw")
			self.temp_user_name_btn[i].pack(side=LEFT)

			temp = Label(frame_temp,relief=RIDGE, text=data[i][1], bg="white")
			temp.config(width = 70, height = 1, anchor="nw")
			temp.pack(side=LEFT, fill=X)

			temp = Label(frame_temp,relief=RIDGE, text=data[i][2], bg="white")
			temp.config(width = 30, height = 1, anchor="nw")
			temp.pack(side=LEFT, fill=X)

		#frame for line2:
		frame2 = Frame(self)
		frame2.pack(pady=10)

		refresh_user_btn=Button(frame2,text="Refresh",command=self.refresh_user, bg='DeepSkyBlue4', fg='white')
		refresh_user_btn.pack(side=LEFT)

		back=Button(frame2,text="< Prev", command=self.go_prev)
		back.pack(side=LEFT)

		exit=Button(frame2,text="Exit", bg = "brown3", fg = "white", command=self.leave)
		exit.pack(side=LEFT)

	def copy_name_to_field(self, id):
		print(self.temp_user_name_btn[id]['text'])
		self.delete_user_name.set(self.temp_user_name_btn[id]['text'])

	def create_user_table(self):
		self.login_cur.execute("CREATE TABLE IF NOT EXISTS users(name TEXT, email TEXT, password TEXT, admin_status TEXT)")

	def delete_user(self):
		if(messagebox.askyesno("Warning", "Are you sure to delete this user?")):
			if(self.delete_user_name.get() == ''):
				self.error_msg = "Necessary field(s) cannot be empty!"
				messagebox.showinfo("Error", self.error_msg)
			elif(self.delete_user_name.get() == 'admin'):
				self.error_msg = "You cannot delete admin"
				messagebox.showinfo("Error", self.error_msg)
			else:
				try:
					self.create_user_table()
					self.login_cur.execute("SELECT admin_status FROM users WHERE name = ?", (self.delete_user_name.get(),))
					data = self.login_cur.fetchall()
					print(data[0][0])

					if(self.name == 'admin'):
						try:
							self.login_cur.execute("DELETE FROM users WHERE name = ?", (self.delete_user_name.get(),))
							self.login_conn.commit()
							time.sleep(0.02)
							print("User named %s has been deleted successfully!" %(self.delete_user_name.get()))
							self.screen = 6
							self.quit()
						except Exception:
							self.error_msg = "Invalid search name!"
							messagebox.showinfo("Error", self.error_msg)
					elif(self.name != 'admin' and data[0][0] == '0'):
						try:
							self.login_cur.execute("DELETE FROM users WHERE name = ?", (self.delete_user_name.get(),))
							self.login_conn.commit()
							time.sleep(0.02)
							print("User named %s has been deleted successfully!" %(self.delete_user_name.get()))
							self.screen = 6
							self.quit()
						except Exception:
							self.error_msg = "Invalid search name!"
							messagebox.showinfo("Error", self.error_msg)
					else:
						self.error_msg = "You cannot delete another admin"
						messagebox.showinfo("Error", self.error_msg)
				except Exception as e:
					print(e)

	def refresh_user(self):
		self.screen = 6
		self.quit()

	def go_prev(self):
		self.screen = 25
		self.quit()

	def leave(self):
		quit()