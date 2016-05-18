from patool_gui_settings import *
import tkinter as tk
from tkinter import filedialog
import sys
import os
import os.path
from PAtool import run_me

class DeleteEDDialog(tk.Toplevel):
    def __init__(self, master=None):
        tk.Toplevel.__init__(self, master)
        self.parent = master
        self.title("Create deletion request for an eEtity")
        self.create_widgets()

    def create_widgets(self):
        # Create four rows as frames
        row1 = tk.Frame(self)
        row1.pack(fill=tk.BOTH, expand=True)
        row2 = tk.Frame(self)
        row2.pack(fill=tk.X, expand=True)

        # Row 1 has entityID Entry and 
        # recent entityIDs dropdownlist
        tk.Label(row1, text="entityID: ").pack(side=tk.LEFT,
                                                    padx=self.parent.get_padding(),
                                                    pady=self.parent.get_padding())

        self.entityID_entry = tk.Entry(row1)
        self.entityID_entry.pack(side=tk.LEFT, fill=tk.X,
                              expand=True, padx=self.parent.get_padding(),
                              pady=self.parent.get_padding())

        self.recent_entityID = tk.StringVar()
        self.recent_entityID.set("") # default value

        tk.OptionMenu(row1, self.recent_entityID, "one", "two",
                      "three").pack(side=tk.LEFT,
                                 padx=self.parent.get_padding(),
                                 pady=self.parent.get_padding(),
                                 fill=tk.X, expand=True)

        # Row 2 has two buttons
        tk.Button(row2,
                  text="Create and sign",
                  command=self.create_and_sign_deletion_request).pack(side=tk.LEFT,
                                                       padx=self.parent.get_padding(),
                                                       pady=self.parent.get_padding(),
                                                       expand=True)
        tk.Button(row2,
                  text="Cancel",
                  command=self.cancel).pack(side=tk.LEFT,
                                            padx=self.parent.get_padding(),
                                            pady=self.parent.get_padding(),
                                            expand=True)

    def get_entityID_entry(self):
        return(self.entityID_entry.get())
    
    def create_and_sign_deletion_request(self):
        self.parent.set_entityID(self.get_entityID_entry())
        self.parent.deleteED()
        self.destroy()
        
    def cancel(self):
        self.destroy()

    
class CreateEDDialog(tk.Toplevel):
    def __init__(self, master=None):
        tk.Toplevel.__init__(self, master)
        self.parent = master
        self.title("Create ED from cert")
        self.create_widgets()

    def create_widgets(self):
        # Create four rows as frames
        row1 = tk.Frame(self)
        row1.pack(fill=tk.BOTH, expand=True)
        row2 = tk.Frame(self)
        row2.pack(fill=tk.X, expand=True)
        row3 = tk.Frame(self)
        row3.pack(fill=tk.BOTH, expand=True)
        row4 = tk.Frame(self)
        row4.pack(fill=tk.BOTH, expand=True)

        # Row 1 has SAML role radiobuttons
        tk.Label(row1, text="SAML role: ").pack(side=tk.LEFT,
                                                 padx=self.parent.get_padding(),
                                                 pady=self.parent.get_padding())

        self.saml = tk.IntVar()
        tk.Radiobutton(row1, text="IDP", variable=self.saml,
                       value=1).pack(side=tk.LEFT,
                                     padx=self.parent.get_padding(),
                                     pady=self.parent.get_padding())
        tk.Radiobutton(row1, text="SP", variable=self.saml,
                       value=2).pack(side=tk.LEFT,
                                     padx=self.parent.get_padding(),
                                     pady=self.parent.get_padding())


        # Row 2 has entityID entry and dropdownlist

        tk.Label(row2, text="entityID: ").pack(side=tk.LEFT,
                                                    padx=self.parent.get_padding(),
                                                    pady=self.parent.get_padding())

        self.entityID_entry = tk.Entry(row2)
        self.entityID_entry.pack(side=tk.LEFT, fill=tk.X,
                              expand=True, padx=self.parent.get_padding(),
                              pady=self.parent.get_padding())

        self.recent_entityID = tk.StringVar()
        self.recent_entityID.set("") # default value

        tk.OptionMenu(row2, self.recent_entityID, "one", "two",
                      "three").pack(side=tk.LEFT,
                                 padx=self.parent.get_padding(),
                                 pady=self.parent.get_padding(),
                                 fill=tk.X, expand=True)

        # Row 3 has entityID suffix entry and dropdownlist
        tk.Label(row3, text="entityID Suffix: ").pack(side=tk.LEFT,
                                                           padx=self.parent.get_padding(),
                                                           pady=self.parent.get_padding())

        self.entityID_suffix_entry = tk.Entry(row3)
        self.entityID_suffix_entry.pack(side=tk.LEFT, fill=tk.X,
                              expand=True, padx=self.parent.get_padding(),
                              pady=self.parent.get_padding())

        self.entityID_suffix = tk.StringVar()
        self.entityID_suffix.set("") # default value

        tk.OptionMenu(row3, self.entityID_suffix, "one", "two",
                      "three").pack(side=tk.LEFT,
                                 padx=self.parent.get_padding(),
                                 pady=self.parent.get_padding(),
                                 fill=tk.X, expand=True)

        # Row 4 has three buttons
        tk.Button(row4,
                  text="Create",
                  command=self.createED).pack(side=tk.LEFT,
                                              padx=self.parent.get_padding(),
                                              pady=self.parent.get_padding(),
                                              expand=True)
        tk.Button(row4,
                  text="Create and sign",
                  command=self.create_and_signED).pack(side=tk.LEFT,
                                                       padx=self.parent.get_padding(),
                                                       pady=self.parent.get_padding(),
                                                       expand=True)
        tk.Button(row4,
                  text="Cancel",
                  command=self.cancel).pack(side=tk.LEFT,
                                            padx=self.parent.get_padding(),
                                            pady=self.parent.get_padding(),
                                            expand=True)


    def get_entityID_entry(self):
        return(self.entityID_entry.get())

    def get_entityID_suffix_entry(self):
        return(self.entityID_suffix_entry.get())

    def get_samlrole(self):
        if self.saml.get() == 1:
            return("IDP")
        elif self.saml.get() == 2:
            return("SP")
        else:
            return ("")
        
    def createED(self):
        # Invoke the creation and destroy the dialog
        self.parent.set_entityID(self.get_entityID_entry())
        self.parent.set_entityID_suffix(self.get_entityID_suffix_entry())
        self.parent.set_samlrole(self.get_samlrole())
        self.parent.createED()
        self.destroy()

    def create_and_signED(self):
        self.parent.create_and_signED()
        self.destroy()

    def cancel(self):
        self.destroy()

        
class PAtoolGUI(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.parent = master
        self.parent.title("Portal Admin Tool")
        self.pack( fill=tk.BOTH, expand=True)
        self.initialize_variables()
        self.create_widgets()

        
    def initialize_variables(self):
        self.set_padding(5)
        self.set_input_file("")
        self.set_input_dir("")
        self.set_output_dir("")
        self.set_output_files([])
        self.set_entityID("")
        self.set_entityID_suffix("")
        self.set_samlrole("")
        
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
        row1c2.pack(side=tk.LEFT, fill=tk.BOTH)
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
        tk.Button(row1c2, text="create ED\nfrom cert",
                  command=self.createED_dialog).pack(padx=self.get_padding(),
                                                     pady=self.get_padding())

        tk.Button(row1c2, text="sign ED",
                  command=self.signED).pack(padx=self.get_padding(),
                                            pady=self.get_padding())

        tk.Button(row1c2, text='create request\n"delete ED"',
                  command=self.deleteED_dialog).pack(padx=self.get_padding(),
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

        # Define key bindings
        self.input_entry.bind("<Return>", self.add_input_file_from_entry)
        self.output_entry.bind("<Return>", self.add_output_file_from_entry)

    def set_padding(self, padding):
        self.padding = padding

    def get_padding(self):
        return(self.padding)

    def set_entityID(self, entityID):
        self.entityID = entityID

    def get_entityID(self):
        return(self.entityID)

    def set_entityID_suffix(self, id_suffix):
        self.entityID_suffix = id_suffix

    def get_entityID_suffix(self):
        return(self.entityID_suffix)

    def get_selected_input(self):
        indices = self.input_file_list.curselection()
        self.log(self.input_file_list.get(indices[0]))
        return(self.input_file_list.get(indices[0]))

    def get_selected_output(self):
        indices = self.output_file_list.curselection()
        self.log(self.output_file_list.get(indices[0]))
        output = []
        for index in indices:
            output.append(self.output_file_list.get(index))
        return(output)

    def set_input_file(self, input):
        self.input_file = input
    
    def get_input_file(self):
        return(self.input_file)

    def set_input_dir(self, input):
        self.input_dir = input

    def get_input_dir(self):
        return(self.input_dir)

    def set_output_dir(self, output):
        self.output_dir = output

    def get_output_dir(self):
        return(self.output_dir)

    def set_output_files(self, output):
        self.output_files = output

    def get_output_files(self):
        return(self.output_files)

    def set_input_entry(self, text):
        self.input_entry.delete(0, 'end')
        self.input_entry.insert(0,text)
    
    def get_input_entry(self):
        return(self.input_entry.get())
            
    def set_output_entry(self, text):
        self.output_entry.delete(0, 'end')
        self.output_entry.insert(0,text)
    
    def get_output_entry(self):
        return(self.output_entry.get())

    def set_samlrole(self, samlrole):
        self.samlrole = samlrole
    
    def get_samlrole(self):
        return(self.samlrole)

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
        self.clear_input_list()
        directory = self.input_entry.get()
        for file in os.listdir(directory):
            self.add_input_file(file)
        
    def add_output_file(self, filename):
        self.output_file_list.insert(tk.END, filename)

    def add_output_file_from_entry(self, event):
        self.clear_output_list()
        directory = self.output_entry.get()
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

    def createED_dialog(self):
        self.set_input_file(self.get_selected_input())
        self.set_input_dir(self.get_input_entry())
        self.set_output_dir(self.get_output_entry())
        CreateEDDialog(self)

    def deleteED_dialog(self):
        self.set_input_file(self.get_selected_input())
        self.set_input_dir(self.get_input_entry())
        DeleteEDDialog(self)

    def createED(self):
        cli = "PAtool.py createED"
        cli += " -e " + str(self.get_entityID())
        cli += " -o " + str(self.get_output_dir())
        cli += " -r " + str(self.get_samlrole())
        cli += " -S " + str(self.get_entityID_suffix())
        cli += " " + str(os.path.join(self.get_input_dir(), self.get_input_file()))
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
        cli += str(os.path.join(self.get_input_dir(), self.get_input_file()))
        self.log(cli)
        self.rewrite_sys_argv(cli)
        self.invoke_PAtool()
        
    def signED(self):
        self.set_input_file(self.get_selected_input())
        self.set_input_dir(self.get_input_entry())
        self.set_output_dir(self.get_output_entry())

        cli = "PAtool.py signED"
        cli += " -o " + str(self.get_output_dir())
        cli += " " + str(os.path.join(self.get_input_dir(), self.get_input_file()))
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
        self.log("Invoking send")

    def rewrite_sys_argv(self, command_line_string):
        sys.argv = command_line_string.split()

    def invoke_PAtool(self):
        self.log("Invoking PAtool.py")
        run_me()
    
root = tk.Tk()
app = PAtoolGUI(master=root)
app.mainloop()



