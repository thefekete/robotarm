class config(object):

    ID = None
    servocontroller = None
    servomap = dict()
    trim = dict()
    beams = None
    valid_servos = ('shoulder', 'elbow', 'base',
                    'wrist', 'grip', 'wrist_rotate')

    def __init__(self, filename=None):
        if filename is not None:
            try:
                self.f = open(filename, 'r')
                self.data = list()
                for lineno, line in enumerate(self.f):
                    # skip blank lines and comments
                    if not line.strip() or line.strip().startswith('#'):
                        continue
                    self.data.append((lineno+1, line.strip().lower()))
            finally:
                self.f.close()

            self.parse()

    def parseError(self, lineno, err, line=None):
        errmsg = "[%s] on line %i: %s" % \
                 (self.f.name, lineno, err)
        if line is not None:
            errmsg += "\n...\t'%s' is not valid" % line
        raise IOError, errmsg

    def parse(self):
        for lineno, line in self.data:
            try:
                key, val = [ sub.strip() for sub in line.split('=') ]
            except ValueError:
                err = "Lines must be formatted 'derective = value'"
                self.parseError(lineno, err, line)

            if key.startswith('id'):
                self.ID = val

            elif key.startswith('type'):
                self.type = val

            elif key.startswith('servocontroller'):
                self.servocontroller = val

            elif key.startswith('servomap'):
                servo = key.split()[1].strip()
                if servo not in self.valid_servos:
                    err = "Invalid servo '%s' must be one of %s" % \
                          (servo, ', '.join(self.valid_servos))
                    self.parseError(lineno, err, line)
                else:
                    self.servomap.update({servo: int(val)})

            elif key.startswith('trim'):
                channel = int(key.split()[1].strip())
                if channel not in self.servomap.values():
                    err = "Channel %i not in servo map %s" % \
                          (channel, self.servomap.values())
                    self.parseError(lineno, err, line)
                else:
                    self.trim.update({channel: float(val)})

            elif key.startswith('beams'):
                try:
                    self.beams = tuple([ [ float(x) for x in
                                           beam.strip('\t [](){}').split(',') ]
                                         for beam in val.split(';')])
                except:
                    err = "Error processing beams directive"
                    self.parseError(lineno, err, line)

            else:
                self.parseError(lineno, "Unknown directive '%s'" % key, line)


if __name__ == '__main__':
    c = config('arm.conf')
    print "ID:", c.ID
    print "Servo Controller:", c.servocontroller
    print "Servo Map:", c.servomap
    print "Trim:", c.trim
    print "Beams:", c.beams
