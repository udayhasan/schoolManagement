class export_report_page(Frame):

	screen = 22

	error_msg  = " "

	def __init__(self,master):
		super(export_report_page,self).__init__(master)
		self.pack()

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

		export_status_btn=Button(frameButton,text="Status\nReport", bg="DeepSkyBlue4", fg = "white", command = lambda : self.set_value(18), width=16, height=3, bd = 4)
		export_status_btn.pack(side=LEFT, padx=2, pady=5)

		export_attns_btn=Button(frameButton,text="Attendance\nReport", bg="DeepSkyBlue4", fg = "white", command = lambda : self.set_value(20), width=16, height=3, bd = 4)
		export_attns_btn.pack(side=LEFT, padx=2, pady=5)

		export_food_btn=Button(frameButton,text="Food\nReport", bg="DeepSkyBlue4", fg = "white", command = lambda : self.set_value(21), width=16, height=3, bd = 4)
		export_food_btn.pack(side=LEFT, padx=2, pady=5)

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