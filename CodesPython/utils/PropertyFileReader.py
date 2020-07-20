import os.path

PROPS_OK = 1
PROPS_NO_EXIST = 0
PROPS_ERROR = -1


class PropertyFileReader:
    def __init__(self, filename_in, create):
        self.PropertyFileRead(filename_in, create)

    def PropertyFileRead(self, filename_in, create):
        if not filename_in:
            print("ERROR: No filename given for the property file\n")
            return

        self.filename = filename_in

        # Open the file for actualization

        if os.path.isfile(filename_in):
            self.file = open(filename_in, "r+")
        else:
            if os.path.isdir(os.path.dirname(filename_in)):
                if create:
                    self.file = open(filename_in, "r+")
            else:
                print("ERROR the file '%s' cannot be opened\n" % filename_in)

    def getProperty(self, name):
        self.file.seek(0)
        line = self.file.readline()
        found = False
        finished = False
        while not (found > 0) and (not finished):
            # skip comments
            if line[0:2] == '//':
                pass
            # skip blank lines
            if line[0:2] == '\r\n':
                pass
            found = line.find(name)
            if found >= 0:
                end = line.find('\r\n')
                value = str(line[found + len(name) + 1:end])
                return PROPS_OK, value
            if line == '':
                finished = True
                # If the property value hasn't been encountered, puts the value to 0
                return PROPS_NO_EXIST, 0
            line = self.file.readline()

    def setProperty(self, name, value):
        self.file.seek(0)
        last_pos = 0
        line = self.file.readline()
        found = False
        finished = False
        while not (found > 0) and (not finished):
            # skip comments
            if line[0:2] == '//':
                pass
            # skip blank lines
            if line[0:2] == '\r\n':
                pass
            found = line.find(name)
            if found >= 0:
                line = line[:found + len(name) + 1] + str(value) + '\r\n'
                self.file.seek(last_pos)
                self.file.write(line)
                return PROPS_OK
            if line == '':
                finished = True
                # If the property value hasn't been encountered, puts the value to 0
                return PROPS_NO_EXIST
            last_pos = self.file.tell()
            line = self.file.readline()
