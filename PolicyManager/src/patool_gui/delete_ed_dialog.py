import tkinter as tk
from tkinter import messagebox

class DeleteEDDialog(tk.Toplevel):
    def __init__(self, master=None):
        tk.Toplevel.__init__(self, master)
        self.parent = master
        self.geometry(self.parent.deleteED_window_geometry)
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
        tk.Label(row1, font=self.parent.custom_font, text="entityID: ").pack(side=tk.LEFT,
                                                    padx=self.parent.get_padding(),
                                                    pady=self.parent.get_padding())

        self.entityID_entry = tk.Entry(row1, font=self.parent.custom_font)
        self.entityID_entry.pack(side=tk.LEFT, fill=tk.X,
                              expand=True, padx=self.parent.get_padding(),
                              pady=self.parent.get_padding())

        self.recent_entityID = tk.StringVar()
        self.recent_entityID.set("") # default value
        # Track the value change to update the entity field
        self.recent_entityID.trace("w", self.update_entityID_entry)

        w = tk.OptionMenu(row1, self.recent_entityID, 
                      *self.parent.get_recent_entityIDs())
        w.pack(side=tk.LEFT,
               padx=self.parent.get_padding(),
               pady=self.parent.get_padding(),
               fill=tk.X, expand=True)
        menu = w.nametowidget(w.menuname) 
        menu.configure(font=self.parent.custom_font)

        # Row 2 has two buttons
        tk.Button(row2,
                  font=self.parent.custom_font, text="Create and sign",
                  command=self.create_and_sign_deletion_request).pack(side=tk.LEFT,
                                                       padx=self.parent.get_padding(),
                                                       pady=self.parent.get_padding(),
                                                       expand=True)
        tk.Button(row2,
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
        
    def create_and_sign_deletion_request(self):
        # Validate entityID i.e. url
        if not self.parent.validate_entityID(self.get_entityID_entry()):
            messagebox.showinfo("Invalid EntityID",
                                "EntityID is not valid\n%s" % self.get_entityID_entry())
            return

        # Let us add the entityID to the recents
        self.parent.get_recent_entityIDs().add_recent(self.get_entityID_entry())
        self.parent.set_entityID(self.get_entityID_entry())
        self.parent.deleteED()
        self.destroy()
        
    def cancel(self):
        self.destroy()

    
