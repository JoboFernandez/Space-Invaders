class Message:

    def __init__(self):
        self.msg = ""
        self.size = 0
        self.color = (0, 0, 0)
        self.left = 0
        self.top = 0

    def set(self, msg: str, size: int, color: tuple, left: int, top: int):
        self.msg = msg
        self.size = size
        self.color = color
        self.left = left
        self.top = top
