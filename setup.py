#!/usr/bin/python

"""
This script creates symlinks in your home directory to your dotfiles in the
Git repository.

By default it will delete any file that stands in the way of its mission to
create a better world.

Usage: python setup.py [--nice] [--home=DIRECTORY]

  --nice               Don't trample existing dot files
  --home=DIRECTORY     Place links in DIRECTORY instead of $HOME

"""

import os, sys, getopt, socket
import string

class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg

""" Create links to dotfiles """
def makeDots(home, nice):
    # First make a map of dot files to files in the repository.
    dotfiles = getMap("base/")
    
    # Get host specific overrides
    hostname = socket.getfqdn().split(".")
    for i in range(len(hostname)):
        name = string.join(hostname[-(i+1):], ".")
        dotfiles = getMap("host-overrides/" + name, dotfiles)



""" Main Method """
def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        try:
            opts, args = getopt.getopt(argv[1:], 
                "hnd", ["help", "nice", "home"])
        except getopt.error, msg:
             raise Usage(msg)

        # Settings:
        nice = False
        home = os.environ["HOME"]

        for o, a in opts:
            if o in ("-h", "--help"):
                print __doc__
                return 0

            if o in ("-n", "--nice"):
                nice = True

            else if o in ("-d", "--home"):
                home = a

        makeDots(home, nice)

    except Usage, err:
        print >>sys.stderr, err.msg
        print >>sys.stderr, "for help use --help"
        return 2

if __name__ == "__main__":
    sys.exit(main())
