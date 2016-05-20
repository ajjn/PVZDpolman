import tkinter as tk
from tkinter import messagebox

class CreateEDDialog(tk.Toplevel):
    def __init__(self, master=None):
        tk.Toplevel.__init__(self, master)
        self.parent = master
        self.title("Create ED from cert")
        self.geometry(self.parent.createED_window_geometry)
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
        tk.Label(row1, font=self.parent.custom_font, text="SAML role: ").pack(side=tk.LEFT,
                                                 padx=self.parent.get_padding(),
                                                 pady=self.parent.get_padding())

        self.saml = tk.IntVar()
        self.saml.set(1)
        tk.Radiobutton(row1, font=self.parent.custom_font, text="IDP", variable=self.saml,
                       value=1).pack(side=tk.LEFT,
                                     padx=self.parent.get_padding(),
                                     pady=self.parent.get_padding())
        tk.Radiobutton(row1, font=self.parent.custom_font, text="SP", variable=self.saml,
                       value=2).pack(side=tk.LEFT,
                                     padx=self.parent.get_padding(),
                                     pady=self.parent.get_padding())


        # Row 2 has entityID entry and dropdownlist

        tk.Label(row2, font=self.parent.custom_font, text="entityID: ").pack(side=tk.LEFT,
                                                    padx=self.parent.get_padding(),
                                                    pady=self.parent.get_padding())

        self.entityID_entry = tk.Entry(row2, font=self.parent.custom_font)
        self.entityID_entry.pack(side=tk.LEFT, fill=tk.X,
                              expand=True, padx=self.parent.get_padding(),
                              pady=self.parent.get_padding())

        self.recent_entityID = tk.StringVar()
        self.recent_entityID.set("") # default value

        # Track the value change to update the entity field
        self.recent_entityID.trace("w", self.update_entityID_entry)
        w = tk.OptionMenu(row2, self.recent_entityID,
                      *self.parent.get_recent_entityIDs())
        w.pack(side=tk.LEFT,
               padx=self.parent.get_padding(),
               pady=self.parent.get_padding(),
               fill=tk.X, expand=True)
        menu = w.nametowidget(w.menuname) 
        menu.configure(font=self.parent.custom_font)
        # Row 3 has entityID suffix entry and dropdownlist
        tk.Label(row3, font=self.parent.custom_font, text="entityID Suffix: ").pack(side=tk.LEFT,
                                                           padx=self.parent.get_padding(),
                                                           pady=self.parent.get_padding())

        self.entityID_suffix_entry = tk.Entry(row3, font=self.parent.custom_font)
        self.entityID_suffix_entry.pack(side=tk.LEFT, fill=tk.X,
                              expand=True, padx=self.parent.get_padding(),
                              pady=self.parent.get_padding())

        self.entityID_suffix = tk.StringVar()
        self.entityID_suffix.set("") # default value
        # Track the value change to update the entity field
        self.entityID_suffix.trace("w", self.update_entityID_suffix_entry)
        w = tk.OptionMenu(row3, self.entityID_suffix,
                      *self.parent.get_recent_entityID_suffices())
        w.pack(side=tk.LEFT,
               padx=self.parent.get_padding(),
               pady=self.parent.get_padding(),
               fill=tk.X, expand=True)
        menu = w.nametowidget(w.menuname) 
        menu.configure(font=self.parent.custom_font)

        # Row 4 has three buttons
        tk.Button(row4,
                  font=self.parent.custom_font, text="Create",
                  command=self.createED).pack(side=tk.LEFT,
                                              padx=self.parent.get_padding(),
                                              pady=self.parent.get_padding(),
                                              expand=True)
        tk.Button(row4,
                  font=self.parent.custom_font, text="Create and sign",
                  command=self.create_and_signED).pack(side=tk.LEFT,
                                                       padx=self.parent.get_padding(),
                                                       pady=self.parent.get_padding(),
                                                       expand=True)
        tk.Button(row4,
                  font=self.parent.custom_font, text="Cancel",
                  command=self.cancel).pack(side=tk.LEFT,
                                            padx=self.parent.get_padding(),
                                            pady=self.parent.get_padding(),
                                            expand=True)


    def set_entityID_entry(self, text):
        self.entityID_entry.delete(0, "end")
        self.entityID_entry.insert(0, text)

    def set_entityID_suffix_entry(self, text):
        self.entityID_suffix_entry.delete(0, "end")
        self.entityID_suffix_entry.insert(0, text)

    def get_entityID_entry(self):
        return self.entityID_entry.get()

    def get_entityID_suffix_entry(self):
        return self.entityID_suffix_entry.get()

    def update_entityID_entry(self, *args):
        self.set_entityID_entry(self.recent_entityID.get())
        
    def update_entityID_suffix_entry(self, *args):
        self.set_entityID_suffix_entry(self.entityID_suffix.get())
        
    def get_samlrole(self):
        if self.saml.get() == 1:
            return "IDP"
        elif self.saml.get() == 2:
            return "SP"
        else:
            return ""
        
    def createED(self, sign_after_create=False):
        self.parent.sign_after_create = sign_after_create
        # Validate entityID i.e. url
        if not self.parent.validate_entityID(self.get_entityID_entry()):
            messagebox.showinfo("Invalid EntityID",
                                "EntityID is not valid\n%s" % self.get_entityID_entry())
            return
        # Let us add the entityID to the recents
        self.parent.get_recent_entityIDs().add_recent(self.get_entityID_entry())
        self.parent.get_recent_entityID_suffices().add_recent(self.get_entityID_suffix_entry())

        # Invoke the creation and destroy the dialog
        self.parent.set_entityID(self.get_entityID_entry())
        self.parent.set_entityID_suffix(self.get_entityID_suffix_entry())
        self.parent.set_samlrole(self.get_samlrole())
        self.parent.createED()
        self.destroy()

    def create_and_signED(self):
        self.createED(sign_after_create=True)

    def cancel(self):
        self.destroy()

        
