import os

porta = 5001
for i in range (10):
    cmd = ('iperf -u -f m -s -p %d &' % (porta))
    porta += 1
    os.system(cmd)
    #print (cmd)