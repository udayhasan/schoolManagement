from tkinter import *
import sqlite3

class login_page(Frame):

	screen     = 0

	login_conn = None
	login_cur  = None

	error_msg  = " "
	admin      = None

	def __init__(self,master):
		super(login_page,self).__init__(master)
		self.login_conn = sqlite3.connect('./db/users.db')
		self.login_cur  = self.login_conn.cursor()
		self.pack()
		self.define_widgets()

	def create_user_table(self):
		self.login_cur.execute("CREATE TABLE IF NOT EXISTS users(name TEXT, email TEXT, password TEXT, admin_status TEXT)")

	def login(self, name, password):
		#print(name, password)
		if(name == ''):
			self.error_msg = "Name field cannot be empty!"
			messagebox.showinfo("Error", self.error_msg)
		elif(password == ''):
			self.error_msg = "Password field cannot be empty!"
			messagebox.showinfo("Error", self.error_msg)
		else:
			try:
				success = 0
				admin   = 0
				self.login_cur.execute("SELECT password, admin_status FROM users WHERE name = ?", (name,))
				check = self.login_cur.fetchall()
				if(password == check[0][0]):
					success = 1
					self.screen = 1
					if(check[0][1] == '1'):
						admin = 1
					else:
						admin = 0
				else:
					self.screen = 0
					self.error_msg = "Incorrect Password!"
					messagebox.showinfo("Error", self.error_msg)
				return success, admin
			except Exception as e:
				self.error_msg = "Error happened!\nError: "+str(e)
				messagebox.showinfo("Error", self.error_msg)
				return success, admin

	def define_widgets(self):
		#for line1:
		frame1=Frame(self)
		frame1.pack()

		login_page_label=Label(frame1,text="::Login Page::")
		login_page_label.config(width=200, font=("Courier", 25))
		login_page_label.pack(pady=10)

		#for line2:
		frame2=Frame(self)
		frame2.pack()

		login_name_label=Label(frame2,text="User ID:", anchor=W)
		login_name_label.config(width=10, height=1)
		login_name_label.pack(side=LEFT, pady=5)

		self.login_name=StringVar()
		login_name_entry=Entry(frame2,textvariable=self.login_name)
		login_name_entry.config(width=25)
		login_name_entry.bind('<Return>', self.login_action_enter)
		login_name_entry.pack(side=LEFT, pady=5)
		login_name_entry.focus_set()

		#for line3:
		frame3=Frame(self)
		frame3.pack()
		login_pass_label=Label(frame3,text="Password:", anchor=W)
		login_pass_label.config(width=10, height=1)
		login_pass_label.pack(side=LEFT, pady=5)

		self.login_pass=StringVar()
		login_pass_entry=Entry(frame3,textvariable=self.login_pass,show="*")
		login_pass_entry.config(width=25)
		login_pass_entry.bind('<Return>', self.login_action_enter)
		login_pass_entry.pack(side=LEFT, pady=5)

		#forline5:
		frame5=Frame(self)
		frame5.pack()
		login_btn=Button(frame5,text="Login", bg="DeepSkyBlue4", fg = "white", command=self.login_action)
		login_btn.bind('<Return>', self.login_action_enter)
		login_btn.pack(side=LEFT, pady=5)

		exit=Button(frame5,text="Exit", bg = "brown3", fg = "white", command=self.leave)
		exit.pack(side=LEFT, pady=5)

		#for line4:
		frame4=Frame(self)
		frame4.pack()

		forgot_id_label=Label(frame4,text="Forgot User ID?", fg = "blue", underline=True)
		forgot_id_label.bind('<Button-1>',self.forgot_id)
		forgot_id_label.pack(side=LEFT)

		forgot_pass_label=Label(frame4,text="Forgot Password?", fg = "blue", underline=True)
		forgot_pass_label.bind('<Button-1>',self.forgot_password)
		forgot_pass_label.pack(side=LEFT)

	def login_action(self):
		self.create_user_table()
		success, self.admin = self.login(self.login_name.get(), self.login_pass.get())
		
		if(success ==1): self.screen = 1
		else: self.screen = 0

		print(self.screen)

		self.quit()

	def login_action_enter(self, *entry):
		self.create_user_table()
		success, self.admin = self.login(self.login_name.get(), self.login_pass.get())
		
		if(success ==1): self.screen = 1
		else: self.screen = 0

		print(self.screen)

		self.quit()

	def forgot_id(self,event):
		self.screen = 12
		self.quit()

	def forgot_password(self,event):
		self.screen = 7
		self.quit()

	def leave(self):
		quit()
