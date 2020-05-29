class FileOut:
    def __init__(self, filePath: str):
        if filePath is None:
            self.fp = None
        else:
            self.fp = open(filePath, "w")

    def setPlayers(self, players: list):
        if self.fp is None:
            return

        self.fp.write("Players: ")
        for i in range(0, len(players)):
            if i != 0:
                self.fp.write(', ')
            self.fp.write(players[i])

    def filePrint(self, val='', end='\n'):
        if self.fp is None:
            return

        self.fp.write(val)
        self.fp.write(end)

    def print(self, val='', end='\n'):
        print(val, end=end)
        self.filePrint(val, end)

    def close(self):
        if self.fp is not None:
            self.fp.close()
