class Recents(list):
    def __init__(self, maxsize=8, items=[]):
        self.RECENTS_MAX_SIZE = maxsize
        self.add_recent("")
        # When dumping as json the object type is lost. This function restores it after loading.
        for item in items:
            self.add_recent(item)

    def add_recent(self, item):
        # Discard duplicate adding
        if item in self:
            return
        self.insert(0, item)
        if len(self) > self.RECENTS_MAX_SIZE:
            del self[-1]
