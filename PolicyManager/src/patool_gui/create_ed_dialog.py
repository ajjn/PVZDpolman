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
               fill=tk.X, expand=False)
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

    def get_entityID_entry(self):
        return self.entityID_entry.get()

    def update_entityID_entry(self, *args):
        self.set_entityID_entry(self.recent_entityID.get())
        
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
                                "EntityID must be a valid URI, such as https://hostname/idp.xml")
            return
        # Let us add the entityID to the recents
        self.parent.get_recent_entityIDs().add_recent(self.get_entityID_entry())

        # Invoke the creation and destroy the dialog
        self.parent.set_entityID(self.get_entityID_entry())
        self.parent.set_samlrole(self.get_samlrole())
        self.parent.createED()
        self.destroy()

    def create_and_signED(self):
        self.createED(sign_after_create=True)

    def cancel(self):
        self.destroy()

        
