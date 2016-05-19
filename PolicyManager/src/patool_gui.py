from patool_gui_settings import *
import tkinter as tk
from CreateEDDialog import CreateEDDialog
from DeleteEDDialog import DeleteEDDialog
from Recents import Recents
from tkinter import filedialog
from tkinter import messagebox
from send_mail import send_files_via_email
import pickle
import sys
import os
import re
import logging
from PAtool import run_me

class PAtoolGUI(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.parent = master
        self.parent.title("Portal Admin Tool")
        self.pack( fill=tk.BOTH, expand=True)
        self.initialize_variables()
        self.create_widgets()
        self.define_bindings()

    def updateGUI():
        self.update_directory_listing()
        self.parent.after(1000, updateGUI) # run itself again after 1000 ms

    def update_directory_listing(self):
        self.set_input_entry(self.get_input_dir())
        self.set_output_entry(self.get_output_dir())
        try:
            for file in os.listdir(self.get_input_dir()):
                self.add_input_file(file)
        except:
            logging.error("Could not list dir")
        try:
            for file in os.listdir(self.get_output_dir()):
                self.add_output_file(file)
        except:
            logging.error("Could not list dir")
        
    def define_bindings(self):
        # Define key bindings
        self.input_entry.bind("<Return>", self.add_input_file_from_entry)
        self.output_entry.bind("<Return>", self.add_output_file_from_entry)
        # Bind window closing event
        self.parent.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        print("Quiting")
        # Save settings
        self.save_variables()
        self.parent.destroy()

    def load_variables(self):
        try:
            f = open(os.path.join(os.environ['HOME'], GUI_SAVED_SETTINGS_FILE), 'rb' )
            settings = pickle.load(f)
            f.close()
            self.set_input_dir(settings['input_dir'])
            self.set_output_dir(settings['output_dir'])
            self.set_padding(settings['padding'])
            self.set_recent_entityIDs(settings['recent_entityIDs'])
            self.set_recent_entityID_suffices(settings['recent_entityID_suffices'])
            self.set_geometry(settings['geometry'])
        except:
            self.initialize_saveable_variables()
    
    def save_variables(self):
        settings = {}
        settings['input_dir'] = self.get_input_dir()
        settings['output_dir'] = self.get_output_dir()
        settings['padding'] = self.get_padding()
        settings['recent_entityIDs'] = self.get_recent_entityIDs()
        settings['recent_entityID_suffices'] = self.get_recent_entityID_suffices()
        settings['geometry'] = self.get_geometry()
        try:
            f = open(os.path.join(os.environ['HOME'], GUI_SAVED_SETTINGS_FILE), 'wb' )
            pickle.dump( settings, f )
            f.close()
        except:
            logging.warning("Could not save GUI settings")
            
    def initialize_saveable_variables(self):
        self.set_input_dir(".")
        self.set_output_dir(".")
        # Default size
        sw = self.get_screen_width()
        sh = self.get_screen_height()
        # Put to the middle of the screen by default
        x = int((sw - MAIN_WINDOW_WIDTH) / 2)
        y = int((sh - MAIN_WINDOW_HEIGHT) / 2)
        geometry = "%dx%d+%d+%d" % (MAIN_WINDOW_WIDTH,
                                    MAIN_WINDOW_HEIGHT,
                                    x, y)

        self.parent.geometry(geometry)
        self.set_padding(PADDING)
        self.set_recent_entityIDs(Recents())
        self.set_recent_entityID_suffices(Recents())
        
    def initialize_variables(self):
        self.load_variables()
        self.set_input_file("")
        self.set_output_files([])
        self.set_entityID("")
        self.set_entityID_suffix("")
        self.set_samlrole("")
        
    def get_window_x(self):
        return self.parent.winfo_x()
        
    def get_window_y(self):
        return self.parent.winfo_y()
        
    def get_window_width(self):
        return self.parent.winfo_width()

    def get_window_height(self):
        return self.parent.winfo_height()

    def get_screen_width(self):
        return self.parent.winfo_screenwidth()

    def get_screen_height(self):
        return self.parent.winfo_screenheight()

    def get_geometry(self):
        return self.parent.geometry()

    def set_geometry(self, geometry):
        self.parent.geometry(geometry)

    
    def create_widgets(self):
        # Create three rows as frames
        row1 = tk.Frame(self)
        row1.pack(fill=tk.BOTH, expand=True)
        row2 = tk.Frame(self, height=1, bd=1, relief=tk.RIDGE)
        row2.pack(fill=tk.X, expand=True)
        row3 = tk.Frame(self)
        row3.pack(fill=tk.BOTH, expand=True)
        
        # For row1 create three equal frames
        row1c1 = tk.Frame(row1)
        row1c1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        row1c2 = tk.Frame(row1)
        row1c2.pack(side=tk.LEFT, fill=tk.Y, expand=True)
        row1c3 = tk.Frame(row1)
        row1c3.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # First column on first row has text entry for input file and
        # browse button on top.
        tk.Label(row1c1, text="Input").pack(anchor=tk.NW,
                                                 padx=self.get_padding(),
                                                 pady=self.get_padding())
        input_entry_frame = tk.Frame(row1c1)
        input_entry_frame.pack(fill=tk.X, expand=True)
        self.input_entry = tk.Entry(input_entry_frame)
        self.input_entry.pack(side=tk.LEFT, fill=tk.X,
                              expand=True, padx=self.get_padding(),
                              pady=self.get_padding())

        ## Image for browse object
        self.browse_image = tk.PhotoImage(file="images/browse.gif")
        self.browse_input_file = tk.Button(input_entry_frame,
                                         image=self.browse_image,
                                         command= self.browse_for_input)
        self.browse_input_file.pack(side=tk.RIGHT, padx=self.get_padding(),
                                  pady=self.get_padding())

        input_list_frame = tk.Frame(row1c1)
        input_list_frame.pack(fill=tk.BOTH, expand=True)

        self.input_scrollbar = tk.Scrollbar(input_list_frame)
        self.input_scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=self.get_padding(),
                                 pady=self.get_padding())

        self.input_file_list = tk.Listbox(input_list_frame,
                                          exportselection=0,
                                          yscrollcommand=self.input_scrollbar.set)
        self.input_file_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True,
                                padx=self.get_padding(), pady=self.get_padding())

        self.input_scrollbar.config(command=self.input_file_list.yview)


        # Middle column has tree buttons
        b0f = tk.Frame(row1c2, height=TWO_LINES_BUTTON_HEIGHT,
                       width=BUTTON_WIDTH)
        b0f.pack_propagate(0)
        b0f.pack(anchor=tk.CENTER, expand=True)
        b1f = tk.Frame(row1c2, height=TWO_LINES_BUTTON_HEIGHT,
                       width=BUTTON_WIDTH)
        b1f.pack_propagate(0)
        b1f.pack(anchor=tk.CENTER, expand=True)
        tk.Button(b1f, text="create ED\nfrom cert",
                  command=self.createED_dialog).pack(fill=tk.BOTH,
                                                     expand=True,
                                                     padx=self.get_padding(),
                                                     pady=self.get_padding())

        b2f = tk.Frame(row1c2, height=BUTTON_HEIGHT,
                       width=BUTTON_WIDTH)
        b2f.pack_propagate(0)
        b2f.pack(anchor=tk.CENTER, expand=True)
        tk.Button(b2f, text="sign ED",
                  command=self.signED).pack(fill=tk.BOTH,
                                            expand=True,
                                            padx=self.get_padding(),
                                            pady=self.get_padding())

        b3f = tk.Frame(row1c2, height=TWO_LINES_BUTTON_HEIGHT,
                       width=BUTTON_WIDTH)
        b3f.pack_propagate(0)
        b3f.pack(anchor=tk.CENTER, expand=True)
        tk.Button(b3f, text='create request\n"delete ED"',
                  command=self.deleteED_dialog).pack(fill=tk.BOTH,
                                                     expand=True,
                                                     padx=self.get_padding(),
                                                     pady=self.get_padding())


        # Third column on first row has text entry for output file,
        # list of output files and a send button
        tk.Label(row1c3, text="Output").pack(anchor=tk.NW,
                                                  padx=self.get_padding(),
                                                  pady=self.get_padding())
        output_entry_frame = tk.Frame(row1c3)
        output_entry_frame.pack(fill=tk.X, expand=True)
        self.output_entry = tk.Entry(output_entry_frame)
        self.output_entry.pack(side=tk.LEFT, fill=tk.X, expand=True,
                              padx=self.get_padding(), pady=self.get_padding())

        self.browseoutput_file = tk.Button(output_entry_frame,
                                           image=self.browse_image,
                                           command= self.browse_for_output)
        self.browseoutput_file.pack(side=tk.RIGHT, padx=self.get_padding(),
                                   pady=self.get_padding())

        output_list_frame = tk.Frame(row1c3)
        output_list_frame.pack(fill=tk.BOTH, expand=True)

        self.output_scrollbar = tk.Scrollbar(output_list_frame)
        self.output_scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=self.get_padding(),
                                  pady=self.get_padding())

        self.output_file_list = tk.Listbox(output_list_frame,
                                           selectmode="multiple",
                                           exportselection=0,
                                           yscrollcommand=self.output_scrollbar.set)
        self.output_file_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True,
                                 padx=self.get_padding(), pady=self.get_padding())

        self.output_scrollbar.config(command=self.output_file_list.yview)

        self.send_button = tk.Button(row1c3,
                                     text="Send",
                                     command=self.send)
        self.send_button.pack(padx=self.get_padding(), pady=self.get_padding())

        ## Second row has separators and label of history

        tk.Label(row2, text="History").pack(anchor=tk.NW,
                                                 padx=self.get_padding(),
                                                 pady=self.get_padding())
   
        # Third row is the log window

        self.log_view_scrollbar = tk.Scrollbar(row3)
        self.log_view_scrollbar.pack(side=tk.RIGHT, fill=tk.Y,
                                   padx=self.get_padding(), pady=self.get_padding())
        self.log_view = tk.Text(row3,
                               yscrollcommand= self.log_view_scrollbar.set)
        self.log_view.config(state='disabled')
        self.log_view.pack(side=tk.RIGHT, fill=tk.BOTH,
                          padx=self.get_padding(), pady=self.get_padding(), expand=True)
        self.log_view_scrollbar.config(command=self.log_view.yview)


        # Update directories
        self.update_directory_listing()


    def set_recent_entityIDs(self, recents):
        self.recent_entityIDs = recents

    def get_recent_entityIDs(self):
        return self.recent_entityIDs

    def set_recent_entityID_suffices(self, recents):
        self.recent_entityID_suffices = recents

    def get_recent_entityID_suffices(self):
        return self.recent_entityID_suffices

    def set_padding(self, padding):
        self.padding = padding

    def get_padding(self):
        return self.padding

    def set_entityID(self, entityID):
        self.entityID = entityID

    def get_entityID(self):
        return self.entityID

    def set_entityID_suffix(self, id_suffix):
        self.entityID_suffix = id_suffix

    def get_entityID_suffix(self):
        return self.entityID_suffix

    def get_selected_input(self):
        indices = self.input_file_list.curselection()
        if len(indices) > 0:
            return self.input_file_list.get(indices[0])
        else:
            return False

    def get_selected_output(self):
        indices = self.output_file_list.curselection()
        output = []
        for index in indices:
            output.append(self.output_file_list.get(index))
        return output

    def set_input_file(self, input):
        self.input_file = input
    
    def get_input_file(self):
        return self.input_file

    def set_input_dir(self, input):
        self.input_dir = os.path.abspath(input)

    def get_input_dir(self):
        return self.input_dir

    def set_output_dir(self, output):
        self.output_dir = os.path.abspath(output)

    def get_output_dir(self):
        return self.output_dir

    def set_output_files(self, output):
        self.output_files = output

    def get_output_files(self):
        return self.output_files

    def set_input_entry(self, text):
        self.input_entry.delete(0, 'end')
        self.input_entry.insert(0, text)
        self.set_input_dir(text)

        
    def get_input_entry(self):
        return self.input_entry.get()
            
    def set_output_entry(self, text):
        self.output_entry.delete(0, 'end')
        self.output_entry.insert(0,text)
        self.set_output_dir(text)
    
    def get_output_entry(self):
        return self.output_entry.get()

    def set_samlrole(self, samlrole):
        self.samlrole = samlrole
    
    def get_samlrole(self):
        return self.samlrole

    def log(self, text):
        self.log_view.config(state='normal')
        self.log_view.insert(tk.END, str(text) + '\n')
        self.log_view.see(tk.END)
        self.log_view.config(state='disabled')

    def clear_input_list(self):
        self.input_file_list.delete(0,tk.END)
        
    def clear_output_list(self):
        self.output_file_list.delete(0,tk.END)
        
    def add_input_file(self, filename):
        self.input_file_list.insert(tk.END, filename)

    def add_input_file_from_entry(self, event):
        # Validate directory
        directory = self.get_input_entry()
        if not self.validate_dir(directory):
            messagebox.showinfo("Input directory",
                                "Cannot open input directory\n%s" % directory)
            return
        
        self.set_input_dir(directory)
        self.clear_input_list()
        for file in os.listdir(directory):
            self.add_input_file(file)
        
    def add_output_file(self, filename):
        self.output_file_list.insert(tk.END, filename)

    def add_output_file_from_entry(self, event):
        directory = self.output_entry.get()
        # Validate directory
        if not self.validate_dir(directory):
            messagebox.showinfo("Output directory",
                                "Cannot open output directory\n%s" % directory)
            return

        self.set_output_dir(directory)
        self.clear_output_list()
        for file in os.listdir(directory):
            self.add_output_file(file)

    def browse_for_input(self):
        directory = filedialog.askdirectory()
        if directory:
            try:
                self.clear_input_list()
                for file in os.listdir(directory):
                    self.add_input_file(file)
            except:
                text = "Failed to read directory \n'%s'"%directory
                self.log(text)
                messagebox.showerror(text)
        self.set_input_entry(directory)
        
    def browse_for_output(self):
        directory = filedialog.askdirectory()
        if directory:
            try:
                self.clear_output_list()
                for file in os.listdir(directory):
                    self.add_output_file(file)
            except:
                text = "Failed to read directory \n'%s'"%directory
                self.log(text)
                messagebox.showerror(text)
        self.set_output_entry(directory)

    def validate_dir(self, dir):
        # Validate selected file and directory as a proper file
        if os.path.isdir(dir):
            return True
        else:
            return False
        
    def validate_dir_file(self, dir, file):
        # Validate selected file and directory as a proper file
        if not self.validate_dir(dir):
            return False
        if os.path.isfile(os.path.join(dir, file)):
            return True
        else:
            return False

    def validate_entityID(self, url):
        # Taken from
        # http://stackoverflow.com/questions/827557/how-do-you-validate-a-url-with-a-regular-expression-in-python
        regex = re.compile(
            r'^https?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        return url is not None and regex.search(url)

    def createED_dialog(self):
        # Validate input directory
        if not self.validate_dir(self.get_input_entry()):
            messagebox.showinfo("Input directory",
                                "Cannot open input directory\n%s" % self.get_input_entry())
            return
            
        # Validate selection
        if not self.get_selected_input():
            messagebox.showinfo("Input selection",
                                "Please, select an input file")
            return
        # Validate file
        if not self.validate_dir_file(self.get_input_entry(), self.get_selected_input()):
            messagebox.showinfo(
                "Input file is invalid",
                "Cannot open this file\n%s" % self.get_selected_input())
            return

        # Validate output directory
        if not self.validate_dir(self.get_output_entry()):
            messagebox.showinfo("Output directory",
                                "Cannot open output directory\n%s" % self.get_output_entry())
            return

        # Set user entries
        self.set_input_file(self.get_selected_input())
        self.set_input_dir(self.get_input_entry())
        self.set_output_dir(self.get_output_entry())

        # Calculate the dialog position
        x = self.get_window_width() + self.get_window_x()
        y = int(self.get_window_height()/3) + self.get_window_y()
        self.createED_window_geometry = "%dx%d+%d+%d" % (CREATE_ED_WINDOW_WIDTH,
                                                         CREATE_ED_WINDOW_HEIGHT,
                                                         x,y)
        CreateEDDialog(self)

    def deleteED_dialog(self):
        # Validate input directory
        if not self.validate_dir(self.get_input_entry()):
            messagebox.showinfo("Input directory",
                                "Cannot open directory\n%s" % self.get_input_entry())
            return
            
        # Validate selection
        if not self.get_selected_input():
            messagebox.showinfo("Input selection",
                                "Please, select an input file")
            return
        # Validate file
        if not self.validate_dir_file(self.get_input_entry(), self.get_selected_input()):
            messagebox.showinfo(
                "Input file is invalid",
                "Cannot open this file\n%s" % self.get_selected_input())
            return

        # Set user entries
        self.set_input_file(self.get_selected_input())
        self.set_input_dir(self.get_input_entry())

        # Calculate the dialog position
        x = self.get_window_width() + self.get_window_x()
        y = int(self.get_window_height()/3) + self.get_window_y()
        self.deleteED_window_geometry = "%dx%d+%d+%d" % (DELETE_ED_WINDOW_WIDTH,
                                                         DELETE_ED_WINDOW_HEIGHT,
                                                         x,y)
        DeleteEDDialog(self)

    def createED(self):
        cli = "PAtool.py createED"
        cli += " -e " + str(self.get_entityID())
        cli += " -o " + str(self.get_output_dir())
        cli += " -r " + str(self.get_samlrole())
        if self.get_entityID_suffix() != "":
            cli += " -S " + str(self.get_entityID_suffix())
        cli += " " + str(os.path.join(self.get_input_dir(),
                                      self.get_input_file()))
        self.log(cli)
        self.rewrite_sys_argv(cli)
        self.invoke_PAtool()
        
    def create_and_signED(self):
        cli = "PAtool.py createED"
        cli += " -e " + str(self.get_entityID())
        cli += " -o " + str(self.get_output_dir())
        cli += " -r " + str(self.get_samlrole())
        cli += " -S " + str(self.get_entityID_suffix())
        cli += " -s " 
        cli += str(os.path.join(self.get_input_dir(),
                                self.get_input_file()))
        self.log(cli)
        self.rewrite_sys_argv(cli)
        self.invoke_PAtool()
        
    def signED(self):
        self.set_input_file(self.get_selected_input())
        self.set_input_dir(self.get_input_entry())
        self.set_output_dir(self.get_output_entry())

        cli = "PAtool.py signED"
        cli += " -o " + str(self.get_output_dir())
        cli += " " + str(os.path.join(self.get_input_dir(),
                                      self.get_input_file()))
        self.log(cli)
        self.rewrite_sys_argv(cli)
        self.invoke_PAtool()

        
    def deleteED(self):
        cli = "PAtool.py deleteED"
        cli += " -e " + str(self.get_entityID())
        cli += " -o " + str(self.get_output_dir())
        self.log(cli)
        self.rewrite_sys_argv(cli)
        self.invoke_PAtool()

    def send(self):
        self.set_output_files(self.get_selected_output())
        print (self.get_output_files())
        self.log("Invoking send")
        result = send_files_via_email(self.get_output_dir(), self.get_output_files())
        if result:
            self.log("Files sent!")
        else:
            self.log("Could not send files!")
        
    def rewrite_sys_argv(self, command_line_string):
        sys.argv = command_line_string.split()

    def invoke_PAtool(self):
        self.log("Invoking PAtool.py")
        run_me()
    
root = tk.Tk()
app = PAtoolGUI(master=root)
app.mainloop()



