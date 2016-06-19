__author__ = 'r2h2'

import json
import sys
import os
import re
import logging
import constants
try:
    loglevel_str = os.environ['PATOOLGUI_LOGLEVEL']
    loglevel_int = constants.LOGLEVELS[loglevel_str]
    logging.basicConfig(filename=os.path.join(os.environ['HOME'], 'patoolgui.log'),
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=loglevel_int)
except Exception as e:
    pass
import tkinter as tk
from create_ed_dialog import CreateEDDialog
from delete_ed_dialog import DeleteEDDialog
from recents import Recents
from tkinter import filedialog
from tkinter import messagebox
from tkinter import font
from send_mail import send_files_via_email
sys.path.append('..')  # TODO: make this directory a package
from PAtool import run_me
from config_reader import ConfigReader

class PAtoolGUI(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.parent = master
        self.parent.title("Portal Admin Tool")
        self.pack(fill=tk.BOTH, expand=True)
        self.conf = ConfigReader()
        self.custom_font = font.Font(family=self.conf.FONT_FAMILY, size=self.conf.FONT_SIZE)
        self.initialize_variables()
        self.create_widgets()
        self.define_bindings()
        self.updateGUI()

    def updateGUI(self):
        # refresh display every second to updatedirectory listings
        self.conditional_update_directory_listing()
        self.parent.after(1000, self.updateGUI)
        return True
    
    def conditional_update_directory_listing(self):
        #self.set_input_entry(self.get_input_dir())
        #self.set_output_entry(self.get_output_dir())
        if not self.any_input_file_selected():
            try:
                self.clear_input_list()
                for file in os.listdir(self.get_input_dir()):
                    self.add_input_file(file)
            except:
                logging.error("Could not list dir " + self.get_input_dir())
        if not self.any_output_file_selected():
            try:
                self.clear_output_list()
                for file in os.listdir(self.get_output_dir()):
                    self.add_output_file(file)
            except:
                logging.error("Could not list dir " + self.get_output_dir())
        
    def update_directory_listing(self):
        self.set_input_entry(self.get_input_dir())
        self.set_output_entry(self.get_output_dir())
        try:
            self.clear_input_list()
            for file in os.listdir(self.get_input_dir()):
                self.add_input_file(file)
        except:
            logging.error("Could not list dir " + self.get_input_dir())
        try:
            self.clear_output_list()
            for file in os.listdir(self.get_output_dir()):
                self.add_output_file(file)
        except:
            logging.error("Could not list dir " + self.get_output_dir())
        
    def define_bindings(self):
        # Define key bindings
        self.input_entry.bind("<Return>", self.add_input_file_from_entry)
        self.output_entry.bind("<Return>", self.add_output_file_from_entry)
        # Bind window closing event
        self.parent.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        print("Exiting")
        # Save settings
        self.save_variables()
        self.parent.destroy()

    def load_variables(self):
        try:
            with open(os.path.join(os.environ['HOME'], self.conf.GUI_SAVED_SETTINGS_FILE), 'rb') as fd:
                s = fd.read().decode('UTF-8')
                settings = json.loads(s)
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
            fpath = os.path.join(os.environ['HOME'], self.conf.GUI_SAVED_SETTINGS_FILE)
            with open(fpath, 'wb') as fd:
                j = json.dumps(settings, indent=2)
                fd.write(j.encode('UTF-8'))
                logging.debug("saved profile in " + fpath)
        except Exception as e:
            logging.warning("Could not save GUI settings: " + str(e))
            
    def initialize_saveable_variables(self):
        self.set_input_dir(".")
        self.set_output_dir(".")
        # Default size
        sw = self.get_screen_width()
        sh = self.get_screen_height()
        # Put to the middle of the screen by default
        x = int((sw - self.conf.MAIN_WINDOW_WIDTH) / 2)
        y = int((sh - self.conf.MAIN_WINDOW_HEIGHT) / 2)
        geometry = "%dx%d+%d+%d" % (self.conf.MAIN_WINDOW_WIDTH, self.conf.MAIN_WINDOW_HEIGHT, x, y)
        self.parent.geometry(geometry)
        self.set_padding(self.conf.PADDING)
        recents = Recents(self.conf.RECENTS_MAX_SIZE)
        self.set_recent_entityIDs(recents)
        self.set_recent_entityID_suffices(Recents(self.conf.RECENTS_MAX_SIZE))
        
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
        row1e = tk.Frame(self)
        row1e.pack(fill=tk.BOTH, expand=True)
        row2 = tk.Frame(self, height=1, bd=1, relief=tk.RIDGE)
        row2.pack(fill=tk.X, expand=True)
        row3 = tk.Frame(self)
        row3.pack(fill=tk.BOTH, expand=True)
        
        # For row1 create three equal frames
        row1c1 = tk.Frame(row1)
        row1c1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        row1c2 = tk.Frame(row1)
        row1c2.pack(side=tk.LEFT, fill=tk.Y, expand=False)
        row1c3 = tk.Frame(row1)
        row1c3.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # First column on first row has text entry for input file and
        # browse button on top.
        tk.Label(row1c1, text="Input", font=self.custom_font).pack(anchor=tk.NW,
                                                 padx=self.get_padding(),
                                                 pady=self.get_padding())
        input_entry_frame = tk.Frame(row1c1)
        input_entry_frame.pack(fill=tk.X, expand=True)
        self.input_entry = tk.Entry(input_entry_frame, font=self.custom_font)
        self.input_entry.pack(side=tk.LEFT, fill=tk.X,
                              expand=True, padx=self.get_padding(),
                              pady=self.get_padding())

        ## Image for browse object
        scriptdir = os.path.dirname(os.path.realpath(__file__))
        self.browse_image = tk.PhotoImage(file=os.path.join(scriptdir, "images/browse.gif"))
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
                                          font=self.custom_font,
                                          exportselection=0,
                                          yscrollcommand=self.input_scrollbar.set)
        self.input_file_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True,
                                padx=self.get_padding(), pady=self.get_padding())

        self.input_scrollbar.config(command=self.input_file_list.yview)


        # Middle column has tree buttons
        b0f = tk.Frame(row1c2, height=self.conf.TWO_LINES_BUTTON_HEIGHT,
                       width=self.conf.BUTTON_WIDTH)
        b0f.pack_propagate(0)
        b0f.pack(anchor=tk.CENTER, expand=True)
        b1f = tk.Frame(row1c2, height=self.conf.TWO_LINES_BUTTON_HEIGHT,
                       width=self.conf.BUTTON_WIDTH)
        b1f.pack_propagate(0)
        b1f.pack(anchor=tk.CENTER, expand=True)
        tk.Button(b1f, font=self.custom_font, text="create ED\nfrom cert",
                  command=self.createED_dialog).pack(fill=tk.BOTH,
                                                     expand=True,
                                                     padx=self.get_padding(),
                                                     pady=self.get_padding())

        b2f = tk.Frame(row1c2, height=self.conf.BUTTON_HEIGHT,
                       width=self.conf.BUTTON_WIDTH)
        b2f.pack_propagate(0)
        b2f.pack(anchor=tk.CENTER, expand=True)
        tk.Button(b2f, font=self.custom_font, text="sign ED",
                  command=self.signED).pack(fill=tk.BOTH,
                                            expand=True,
                                            padx=self.get_padding(),
                                            pady=self.get_padding())

        b3f = tk.Frame(row1c2, height=self.conf.TWO_LINES_BUTTON_HEIGHT,
                       width=self.conf.BUTTON_WIDTH)
        b3f.pack_propagate(0)
        b3f.pack(anchor=tk.CENTER, expand=True)
        tk.Button(b3f, font=self.custom_font, text='create request\n"delete ED"',
                  command=self.deleteED_dialog).pack(fill=tk.BOTH,
                                                     expand=True,
                                                     padx=self.get_padding(),
                                                     pady=self.get_padding())


        # Third column on first row has font=self.custom_font, text entry for output file,
        # list of output files and a send button
        tk.Label(row1c3, font=self.custom_font, text="Output").pack(anchor=tk.NW,
                                                  padx=self.get_padding(),
                                                  pady=self.get_padding())
        output_entry_frame = tk.Frame(row1c3)
        output_entry_frame.pack(fill=tk.X, expand=True)
        self.output_entry = tk.Entry(output_entry_frame, font=self.custom_font)
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
                                           font=self.custom_font,
                                           selectmode="multiple",
                                           exportselection=0,
                                           yscrollcommand=self.output_scrollbar.set)
        self.output_file_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True,
                                 padx=self.get_padding(), pady=self.get_padding())

        self.output_scrollbar.config(command=self.output_file_list.yview)


        # Second row has separators and label of history

        b4f = tk.Frame(row1e, height=self.conf.BUTTON_HEIGHT,
                       width=self.conf.BUTTON_WIDTH)
        b4f.pack_propagate(0)
        b4f.pack(anchor=tk.E, expand=True,padx=60)
        tk.Button(b4f, font=self.custom_font, text="Send",
                  command=self.send).pack(fill=tk.BOTH,
                                          expand=True,
                                          padx=self.get_padding(),
                                          pady=self.get_padding())


        tk.Label(row2, font=self.custom_font, text="History").pack(anchor=tk.NW,
                                                 padx=self.get_padding(),
                                                 pady=self.get_padding())
   
        # Third row is the log window

        self.log_view_scrollbar = tk.Scrollbar(row3)
        self.log_view_scrollbar.pack(side=tk.RIGHT, fill=tk.Y,
                                   padx=self.get_padding(), pady=self.get_padding())
        self.log_view = tk.Text(row3, font=self.custom_font,
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

    def any_input_file_selected(self):
        indices = self.input_file_list.curselection()
        if len(indices) > 0:
            return True
        else:
            return False

    def any_output_file_selected(self):
        indices = self.output_file_list.curselection()
        if len(indices) > 0:
            return True
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
        #validate directory
        if self.validate_dir(directory):
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
        if self.validate_dir(directory):
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
        if not dir:
            return False
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
        # Validate URL format
        regex = re.compile(
            r'^https://'  # https://  only
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        return url is not None and regex.search(url)

    def is_valid_certfile(self, file) -> bool:
        """ take a file and check if it is a RFC 7468 conformant base64-encoded certificate
        """
        begin = False
        end = False
        with open(file) as fd:
            for l in fd.readlines():
                if l == '-----BEGIN CERTIFICATE-----\n':
                    begin = True
                    continue
                if begin:
                    if l.startswith('-----END CERTIFICATE-----'):
                        end = True
                        break
        return (begin and end)

    def createED_dialog(self):
        # Validate input directory
        if not self.validate_dir(self.get_input_entry()):
            messagebox.showinfo("Input directory",
                                "Cannot open input directory:\n%s" % self.get_input_entry())
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
                "Cannot open this file:\n%s" % self.get_selected_input())
            return
        if not self.is_valid_certfile(os.path.join(self.get_input_entry(), self.get_selected_input())):
            messagebox.showinfo(
                "Invalid selection",
                "Certificate must contain '-----BEGIN/END CERTIFICATE-----' delimiters conforming to RFC 7468. Cannot open this file\n%s" % self.get_selected_input())
            return

        # Validate output directory
        if not self.validate_dir(self.get_output_entry()):
            messagebox.showinfo("Output directory",
                                "Cannot open output directory:\n%s" % self.get_output_entry())
            return

        # Set user entries
        self.set_input_file(self.get_selected_input())
        self.set_input_dir(self.get_input_entry())
        self.set_output_dir(self.get_output_entry())

        # Calculate the dialog position
        x = self.get_window_width() + self.get_window_x()
        y = int(self.get_window_height()/3) + self.get_window_y()
        self.createED_window_geometry = "%dx%d+%d+%d" % (self.conf.CREATE_ED_WINDOW_WIDTH,
                                                         self.conf.CREATE_ED_WINDOW_HEIGHT,
                                                         x,y)
        CreateEDDialog(self)

    def deleteED_dialog(self):
        # Validate input directory
        if not self.validate_dir(self.get_input_entry()):
            messagebox.showinfo("Input directory",
                                "Cannot open directory\n%s" % self.get_input_entry())
            return
            
        # Set user entries
        self.set_input_file(self.get_selected_input())
        self.set_input_dir(self.get_input_entry())

        # Calculate the dialog position
        x = self.get_window_width() + self.get_window_x()
        y = int(self.get_window_height()/3) + self.get_window_y()
        self.deleteED_window_geometry = "%dx%d+%d+%d" % (DELETE_ED_WINDOW_WIDTH,
                                                         DELETE_ED_WINDOW_HEIGHT,
                                                         x, y)
        DeleteEDDialog(self)

    def createED(self):
        cli = "PAtool.py createED"
        cli += " -e " + str(self.get_entityID())
        cli += " -o " + str(self.get_output_dir())
        cli += " -r " + str(self.get_samlrole())
        if self.get_entityID_suffix() != "":
            cli += " -S " + str(self.get_entityID_suffix())
        if self.sign_after_create:
            cli += " -s "
        cli += " " + str(os.path.join(self.get_input_dir(),
                                      self.get_input_file()))
        self.log(cli)
        self.rewrite_sys_argv(cli)
        self.invoke_PAtool()
        self.update_directory_listing()

    def create_and_signED(self):
        cli = "PAtool.py createED"
        cli += " -e " + str(self.get_entityID())
        cli += " -o " + str(self.get_output_dir())
        cli += " -r " + str(self.get_samlrole())
        if self.get_entityID_suffix() != "":
            cli += " -S " + str(self.get_entityID_suffix())
        cli += " -s " 
        cli += str(os.path.join(self.get_input_dir(),
                                self.get_input_file()))
        self.log(cli)
        self.rewrite_sys_argv(cli)
        self.invoke_PAtool()
        self.update_directory_listing()
        
    def signED(self):
        # Validate input directory
        if not self.validate_dir(self.get_input_entry()):
            messagebox.showinfo("Invalid directory",
                                "Cannot open input directory\n%s" % self.get_input_entry())
            return
            
        # Validate selection
        if not self.get_selected_input():
            messagebox.showinfo("Input selection",
                                "Select an input file")
            return
        # Validate file
        if not self.validate_dir_file(self.get_input_entry(), self.get_selected_input()):
            messagebox.showinfo(
                "Invalid input file",
                "Cannot open this file\n%s" % self.get_selected_input())
            return
        if not self.get_selected_input()[-4:] == '.xml':
            messagebox.showinfo(
                "Invalid input file",
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

        cli = "PAtool.py signED"
        cli += " -o " + str(self.get_output_dir())
        cli += " " + str(os.path.join(self.get_input_dir(),
                                      self.get_input_file()))
        self.log(cli)
        self.rewrite_sys_argv(cli)
        self.invoke_PAtool()
        self.update_directory_listing()

        
    def deleteED(self):
        cli = "PAtool.py deleteED"
        cli += " -e " + str(self.get_entityID())
        cli += " -o " + str(self.get_output_dir())
        self.log(cli)
        self.rewrite_sys_argv(cli)
        self.invoke_PAtool()
        self.update_directory_listing()

    def send(self):
        self.set_output_files(self.get_selected_output())
        self.log("Invoking send")
        result = send_files_via_email(self.conf, self.get_output_dir(), self.get_output_files())
        if result == 'OK':
            self.log("Files mailed:" + ', '.join(self.get_output_files()))
            logging.info("Files mailed:" + ', '.join(self.get_output_files()))
        else:
            self.log("Failed to send. " + result)
        
    def rewrite_sys_argv(self, command_line_string):
        sys.argv = command_line_string.split()

    def invoke_PAtool(self):
        self.log("Invoking PAtool.py")
        run_me()
    
root = tk.Tk()
app = PAtoolGUI(master=root)
app.mainloop()



