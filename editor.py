import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

class MenuBar:
	def __init__(self,parent):
		font_specs = ("windows",12)
		menubar= tk.Menu(parent.master,font =font_specs) #menubar widget
		parent.master.config(menu=menubar)
		file_dropdown = tk.Menu(menubar, font =font_specs,tearoff=0)
		file_dropdown.add_command(label= "New File",accelerator="Ctrl+N", command=parent.new_file)
		file_dropdown.add_command(label ="Open File",accelerator="Ctrl+O", command =parent.open_file)
		file_dropdown.add_command(label ="Save",accelerator="Ctrl+S",command =parent.save)
		file_dropdown.add_command(label="Save As",accelerator="Ctrl+Shift+S",command = parent.save_as)
		file_dropdown.add_separator()				#draws a line between exit and other fields
		file_dropdown.add_command(label="Exit",accelerator="Ctrl+N",command=parent.master.destroy)


		about_dropdown= tk.Menu(menubar, font =font_specs,tearoff=0)

		about_dropdown.add_command(label="Release Notes", command=self.release_notes)
		about_dropdown.add_separator()
		about_dropdown.add_command(label="About",command=self.about_message)

		menubar.add_cascade(label="File", menu = file_dropdown)
		menubar.add_cascade(label="About", menu = about_dropdown)

	def about_message(self):
		box_title="About DevText"
		box_message="DevText is a modern day text editor .This version is 0.1"
		messagebox.showinfo(box_title,box_message)

	def release_notes(self):
		box_title="Release notes"
		box_message="0.1 DebuEditor"
		messagebox.showinfo(box_title,box_message)	


class Statusbar:
	def __init__(self,parent):

		font_specs = ("windows",12)

		self.status= tk.StringVar()
		self.status.set("DevText - 0.1 DebuEditor")

		label = tk.Label(parent.textarea,textvariable = self.status, fg="black", bg ="lightgrey",anchor= 'sw'
						,font=font_specs)
		label.pack(side=tk.BOTTOM, fill=tk.BOTH)

	def update_status(self,*args):
		if isinstance(args[0],bool):
			self.status.set("Your File is Saved")
		else:
			self.status.set("Your File is Saved ")		


class PyText:
	def __init__(self, master):
		master.title("DevText")
		master.geometry("1200x700")		#initial size of the window 

		font_specs = ("windows",16)
		self.master = master
		self.filename= None

		self.textarea = tk.Text(master, font = font_specs)
		self.scroll = tk.Scrollbar(master, command = self.textarea.yview)
		self.textarea.config(yscrollcommand = self.scroll.set)		
		self.textarea.pack(side=tk.LEFT , fill =tk.BOTH ,expand=True) 
		self.scroll.pack(side =tk.RIGHT, fill =tk.Y)

		self.menubar = MenuBar(self)
		self.statusbar = Statusbar(self)
		self.bind_shortcuts()

	def self_window_title(self,name=None):
		if name:
			self.master.title(name + "-DevText")
		else:
			self.master.title("Untitled DevText")
			
		

	def new_file(self,*args):	
		self.textarea.delete(1.0,tk.END)
		self.filename=None
		self.set_window_title()

	def open_file(self,*args):
		self.filename = filedialog.askopenfilename(defaultextension=".txt",filetypes=[("All Types", "*.*")
																			,("Text Files" ,"*.txt")
																			,("Python Scripts","*.py")
																			,("JavaScipt Files","*.js")
																			,("HTML Files","*.html")
																			,("CSS Files","*.css")
																			,("Markdown Documents","*.md")])
		if self.filename:
			self.textarea.delete(1.0,tk.END)
			with open(self.filename, "r") as f:
				self.textarea.insert(1.0,f.read())
			self.set_window_title(self.filename)

	def save(self,*args):
		if self.filename:
			try:
				textarea_content = self.textarea.get(1.0,tk.END)
				with open(self.filename, "w") as f:
					f.write(textarea_content)
				self.statusbar.update_status(True)	
			except Exception as e:
				print(e)
		else:
			self.save_as()				

		

	def save_as(self,*args):
		try:
			new_file = filedialog.asksaveasfilename(initialfile="Untitled.txt",
													defaultextension=".txt",
													filetypes=[("All Types", "*.*")
																			,("Text Files" ,"*.txt")
																			,("Python Scripts","*.py")
																			,("JavaScipt Files","*.js")
																			,("HTML Files","*.html")
																			,("CSS Files","*.css")
																			,("Markdown Documents","*.md")])
			textarea_content= self.textarea.get(1.0,tk.END)
			with open(new_file,"w")as f:
				f.write(textarea_content)
				self.filename=new_file
				self.set_window_title(self.filename)
				self.statusbar.update_status(True)	


		except Execption as e:
			print(e)
			


	def exit(self):
		pass					

	def bind_shortcuts(self):
		self.textarea.bind('<Control-n>',self.new_file)
		self.textarea.bind('<Control-o>',self.open_file)
		self.textarea.bind('<Control-s>',self.save)
		self.textarea.bind('<Control-S>',self.save_as)
		self.textarea.bind('<Key>',self.statusbar.update_status)



if __name__ == "__main__":
	master = tk.Tk()	#initializing the tkinter 's root window
	pt = PyText(master)

	master.mainloop()	# infinite loop to process events until window is closed
