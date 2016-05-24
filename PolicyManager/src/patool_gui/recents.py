class Recents(list):
    def __init__(maxsize, conf):
        self.add_recent("")
        self.RECENTS_MAX_SIZE = conf.maxsize

    def add_recent(self, item):
        # Discard duplicate adding
        if item in self:
            return
        self.insert(0, item)
        if len(self) > self.RECENTS_MAX_SIZE:
            del self[-1]

