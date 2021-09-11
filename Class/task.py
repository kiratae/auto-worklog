
class Task:
    def __init__(self, date, project, timeSpent, name, desc):
        self.date = date
        self.project = project
        self.timeSpent = int(timeSpent)
        self.name = name
        self.desc = desc

    def printString(self):
        print("[ date: {0}, project: {1}, timeSpent: {2}, name: '{3}' , desc: '{4}' ]".format(self.date, self.project, self.timeSpent, self.name, self.desc))

    def toString(self):
        return "[ date: {0}, project: {1}, timeSpent: {2}, name: '{3}' , desc: '{4}' ]".format(self.date, self.project, self.timeSpent, self.name, self.desc)