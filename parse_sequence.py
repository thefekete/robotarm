class seq(object):

    park = dict()
    seq = list()
    last_item = -1
    loops = 0
    steps = 0

    def __init__(self, filename):
        try:
            self.f = open(filename, 'r')
            data = [ (lineno+1, line.strip().lower())
                     for lineno, line in enumerate(self.f)
                     if line.strip() and not line.strip().startswith('#') ]
            setup = list()
            loop = list()
        finally:
            self.f.close()

        self.setup_data = list()
        self.loop_data = list()
        into_setup = True
        for lineno, line in data:
            if line == 'start_loop':
                into_setup = False
                continue
            else:
                if into_setup:
                    self.setup_data.append( (lineno, line) )
                else:
                    self.loop_data.append( (lineno, line) )

        self.parseSetup()
        self.parseLoop()

    def getstate(self, s, lineno=None, line=None):
        s = [ [ x.strip() for x in sub.strip().split('=') ]
                  for sub in s.split(';') ]
        state = dict()
        for k,v in s:
            if k.startswith('pos'):
                pos = map(float, v.strip(' []()').split(','))
                state[k] = pos

            elif k.startswith('gripper_angle'):
                state[k] = float(v)

            elif k.startswith('grip'):
                state[k] = float(v)

            elif k.startswith('wrist_rotate'):
                state[k] = float(v)

            else:
                raise IOError, \
                      "Bad state definition on line %s: %s\n...\t%s" % \
                      (lineno, k, line)
            
        return state

    def parseSetup(self):
        for lineno, line in self.setup_data:
            try:
                key, val = [ sub.strip() for sub in line.split(':', 1) ]
            except ValueError:
                err = "Lines must be formatted 'derective: value'"
                err += "\n...\t%s" % line
                raise IOError, err

            if key.startswith('park'):
                self.park = self.getstate(val, lineno, line)

            elif key.startswith('avg_speed'):
                self.avg_speed = float(val)

            else:
                raise IOError, "Bad Directive: %s" % line

    def parseLoop(self):
        for lineno, line in self.loop_data:
            mode, data = line.replace('\t', ' ').split(' ', 1)
            mode = mode.strip()
            data = data.strip()

            if mode == 'move':
                self.seq.append( ['move', self.getstate(data, lineno, line)] )

            elif mode == 'wait':
                if data.endswith('s'):
                    seconds = float(data.replace('s', ''))
                    cond = ('seconds', seconds)
                elif data.startswith('digital'):
                    ch, val = data.replace('digital', '').split()
                    ch = int(ch)
                    if val == 'true' or val == '1':
                        val = True
                    else:
                        val = False
                    cond = ('digital', (ch, val))

                self.seq.append( [mode, cond] )

            else:
                raise IOError, "[%s: %i] Unsuported mode: %s\n    %s" % \
                      (self.f.name, lineno, mode, line)

    def __iter__(self):
        return self

    def next(self):
        """Watch out, this goes forever"""
        self.last_item += 1
        if self.last_item == len(self.seq):
            self.last_item = 0
            self.loops += 1
        item = self.seq[self.last_item]
        self.steps +=1
        return item
        

if __name__ == '__main__':
    q = seq('test.seq')

    print "Setup:"
    for i in q.setup_data: print "\t", i
    print
    print "\tParked State:", q.park
    print "\tAvg Speed:", q.avg_speed
    print


    print "Loop:"
    for i in q.loop_data: print "\t", i
    print
    for i in q.seq: print "\t", i

    for i in q:
        if q.loops > 2: break
        print "Loop: %i\tStep: %i\t%s" % (q.loops, q.last_item, i)
    
