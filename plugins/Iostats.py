# Copyright (c) 2010 ShootQ Inc. <development [at] shootq [dot] com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.


"""An IOSTAT plugin for ServerDensity that displays nice data for 
every device

     The output of this iostat plugin ncludes  the  following
     information (most of the information found in the iostat
     man page):

     device    name of the disk

     r/s       reads per second

     w/s       writes per second

     kr/s      kilobytes read per second

     kw/s      kilobytes written per second

     wait      average number of transactions waiting for service
               (queue length)

     actv      average number of transactions actively being ser-
               viced  (removed  from  the  queue but not yet com-
               pleted)

     svc_t     average  response  time  of  transactions, in mil-
               liseconds

     %w        percent of time there are transactions waiting for
               service (queue non-empty)

     %b        percent of time the disk is busy (transactions  in
               progress)

"""

from subprocess         import Popen, PIPE


class Iostats(object):

    def __init__(self, agentConfig=None, checksLogger=None, rawConfig=None):
	    self.agentConfig = agentConfig
	    self.checksLogger = checksLogger
	    self.rawConfig = rawConfig
		
    def iostat(self):
        """Run the iostat command with the parameters we need
        and return them in a nice dictionary."""
        command = Popen("iostat -x 1 2", shell=True, stdout=PIPE, close_fds=True).communicate()[0]
        stats = {}
        rs = []
        ws = []
        krs = []
        kws = []
        wait = []
        actv = []
        svc_t = []
        w = []
        b = []

        count = 0
        for i in command.split('\n'):
            if i.startswith('device') or 'extend' in i: 
                count +=1
                continue
            if count >= 4:
                foo = i.split()
                if len(foo) < 1: continue
                rs.append(int(float(foo[1])))
                ws.append(int(float(foo[2])))
                krs.append(int(float(foo[3])))
                kws.append(int(float(foo[4])))
                wait.append(int(float(foo[5])))
                actv.append(int(float(foo[6])))
                svc_t.append(int(float(foo[7])))
                w.append(int(float(foo[8])))
                b.append(int(float(foo[9])))


        stats = {
            "Reads/s"   : self.average(rs),
            "Writes/s"   : self.average(ws),
            "KB reads/s"  : self.average(krs),
            "Waits" : self.average(wait, just_add=True),
            "Active" : self.average(actv, just_add=True),
            "Response Times": self.average(svc_t),
            "Trns Wait percent"    : self.average(w),
            "Busy Disk percent"    : self.average(b)
            }

        return stats

    def average(self, items, just_add=False):
        """Add up all elements in a list and divide them by the length thus
        giving you an average"""
        # make sure we are full of ints:
        total = 0
        items_n = len(items)
        for i in items:
            total += i
        if total == 0:
            return 0
        if just_add:
            return int(total)
        return int(total/items_n)


    def run(self):
        """Get called by the SD Agent"""
        return self.iostat()

foo = Iostats()
print foo.iostat()
