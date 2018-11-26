class manage_users_page(Frame):

	screen = 25

	error_msg  = " "

	def __init__(self,master):
		super(manage_users_page,self).__init__(master)
		self.pack()
		self.define_widgets()

	def define_widgets(self):
		#for line1:
		frame1 = Frame(self)
		frame1.pack()
		dash_board_label=Label(frame1,text="::Export Reports::")
		dash_board_label.config(width=200, font=("Courier", 25))
		dash_board_label.pack(pady=5)

		canvas = Canvas(frame1, height=2, borderwidth=0, highlightthickness=0, bg="black")
		canvas.pack(fill=X, padx=80, pady=10)

		frameButton = Frame(self)
		frameButton.pack()

		add_user_btn=Button(frameButton,text="Add User", bg="DeepSkyBlue4", fg = "white", command = lambda : self.set_value(2), width=16, height=3, bd = 4)
		add_user_btn.pack(side=LEFT, padx=2, pady=5)

		delete_user_btn=Button(frameButton,text="Delete user", bg="DeepSkyBlue4", fg = "white", command = lambda : self.set_value(6), width=16, height=3, bd = 4)
		delete_user_btn.pack(side=LEFT, padx=2, pady=5)

		admin_privilege_btn=Button(frameButton,text="Admin Privilege", bg="DeepSkyBlue4", fg = "white", command = lambda : self.set_value(3), width=16, height=3, bd = 4)
		admin_privilege_btn.pack(side=LEFT, padx=2, pady=5)

		frameLast = Frame(self)
		frameLast.pack()

		back=Button(frameLast,text="< Prev", command=self.go_prev, width=10)
		back.pack(side=LEFT, padx=2, pady=5)

		exit=Button(frameLast,text="Exit", bg = "brown3", fg = "white", command=self.leave, width=10)
		exit.pack(side=LEFT, padx=2, pady=5)

		self.frameTable = Frame(self)
		self.frameTable.pack()

	def set_value(self, value):
		self.screen = value
		self.quit()

	def go_prev(self):
		self.screen = 1
		self.quit()

	def leave(self):
		quit()