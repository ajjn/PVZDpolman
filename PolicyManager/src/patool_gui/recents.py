from patool_gui_settings import RECENTS_MAX_SIZE

class Recents(list):
    def __init__(self):
        self.add_recent("")

    def add_recent(self, item):
        # Discard duplicate adding
        if item in self:
            return
        self.insert(0, item)
        if len(self) > RECENTS_MAX_SIZE:
            del self[-1]

