class Color:
    def __init__(self):
        self.HEADER = '\33[42m'
        self.OKBLUE = '\033[94m'
        self.OKGREEN = '\033[92m'
        self.WARNING = '\033[93m'
        self.FAIL = '\033[91m'
        self.ENDC = '\033[0m'
        self.BOLD = '\033[1m'
        self.UNDERLINE = '\033[4m'

    def header(self, msg):
        print("{0}{1}{2}".format(self.HEADER, str(msg), self.ENDC))

    def ok_green(self, msg):
        print("{0}{1}{2}".format(self.OKGREEN, str(msg), self.ENDC))

    def ok_blue(self, msg):
        print("{0}{1}{2}".format(self.OKBLUE, str(msg), self.ENDC))

    def warning(self, msg):
        print("{0}{1}{2}".format(self.WARNING, str(msg), self.ENDC))

    def fail(self, msg):
        print("{0}{1}{2}".format(self.FAIL, str(msg), self.ENDC))

    def bold(self, msg):
        print("{0}{1}{2}".format(self.BOLD, str(msg), self.ENDC))

    def underline(self, msg):
        print("{0}{1}{2}".format(self.UNDERLINE, str(msg), self.ENDC))
