#!/usr/bin/env python

"""
Module docstring.
"""

import sys
import optparse

DEBUG = 0

def process_command_line(argv):
    """
    Return a 2-tuple: (settings object, args list).
    `argv` is a list of arguments, or `None` for ``sys.argv[1:]``.
    """
    if argv is None:
        argv = sys.argv[1:]
    
    """
    # initialize the parser object:
    parser = optparse.OptionParser(
        formatter=optparse.TitledHelpFormatter(width=78),
        add_help_option=None)

    # define options here:
    parser.add_option(      # customized description; put --help last
        '-c', '-h', '--help', action='help',
        help='Show this help message and exit.')

    settings, args = parser.parse_args(argv)

    # check number of arguments, verify values, etc.:
    if args:
        parser.error('program takes no command-line arguments; '
                     '"%s" ignored.' % (args,))

    # further process settings & args if necessary
    # return settings, args
"""
    return argv

def main(argv=None):
    args = process_command_line(argv)
    # application code here, like:
    # run(settings, args)
    #print settings
    output = []
    if DEBUG: print args
    if len(args):
	host = args[0]
    else:
	host = "ya.ru"
    if DEBUG: print host
    output.append(host)
    import subprocess
    pingResult = subprocess.Popen(["/bin/ping", "-c4", "-w10", host], stdout=subprocess.PIPE).stdout.read()	
    #nok = subprocess.Popen(["/bin/ping", "-c1", "-w10", "ya.ya"], stdout=subprocess.PIPE).stdout.read()
    NOK = 10000.0
    import re
    percentPacketLoss = int(re.findall("(\d+)% packet loss",pingResult)[0])
    output.append(percentPacketLoss)
    if percentPacketLoss<>100:
        try:
            ok1 = pingResult[pingResult.find("rtt"):]
            # rtt min/avg/max/mdev = 0.783/0.783/0.783/0.000 ms
            ok2 = [float(i) for i in re.findall("(\d+.\d+)",ok1)]
            # [0.783, 0.783, 0.783, 0.0]
        except:
            if DEBUG: print "some error"
            ok2 = [NOK]*4
    else:
        ok2 = [NOK]*4
    output += ok2
    if DEBUG: print output
    
    import sqlite3
    db = sqlite3.connect('/home/pi/db/plc_ping.db', detect_types=sqlite3.PARSE_DECLTYPES)
    curs=db.cursor()
    add_data=("INSERT INTO rpi_plc"
	"(destination, packet_loss, min, avg, max, mdev)"
	"VALUES(?, ?, ?, ?, ?, ?)")
    curs.execute (add_data, output)
    db.commit()
    db.close()

    
if __name__ == '__main__':
    status = main()
    sys.exit(status)
