class Reader:
    def __init__(self, board):
        self.board = board

    def read_content(self):
        content = [x.split() for x in self.board]
        temp = [0] * len(content)
        for i in range(0, len(content)):
            for j in range(0, len(content[i])):
                if content[i][j] == "Q":
                    temp[j] = i
        return temp
