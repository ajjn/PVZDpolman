class Recents(list):
    def __init__(self, initial_list = []):
        if len(initial_list) > 0:
            for item in initial_list:
                self.add_recent(item)
        else:
            self.add_recent("")

    def add_recent(self, item):
        # Discard duplicate adding
        if item in self:
            return
        self.insert(0, item)
        if len(self) > self.RECENTS_MAX_SIZE:
            del self[-1]

