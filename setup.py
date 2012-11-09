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
import shutil
import string

class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg

""" Create links to dotfiles """
def makeDots(home, nice = False, pretend = False):
    # First make a map of dot files to files in the repository.
    dotfiles = getMap("base/")
    
    # Get host specific overrides
    hostname = socket.getfqdn().split(".")
    for i in range(len(hostname)):
        name = string.join(hostname[-(i+1):], ".")
        dotfiles = dotfiles + getMap("host-overrides/" + name)

    if pretend:
        print "I would make these links:"
    else:
        print "I am making these links:"

    for dst, src in dotfiles:
        realDest = home + "/." + dst
        success = True
        if not pretend:
            success = makeLink(src, realDest, nice)

        if success:
            print "%s => %s" % (realDest, dst, src)
        else:
            print "Not linking %s to %s because file exists" % (realDest, src)

""" Return a map of dest => source dotfiles """
def getMap(baseDirectory, directory=""):
    if baseDirectory[-1] != "/":
        baseDirectory = baseDirectory + "/"

    if directory != "" and directory[-1] != "/":
        directory = directory + "/"

    dots = dict()
    for filename in os.listdir(baseDirectory + directory):
        if filename == ".nolink":
            continue

        fullPath = baseDirectory + directory + filename
        
        if os.path.isdir(fullPath) and os.path.exists(fullPath + "/.nolink"):
            # We will not make a link but will make sure this directory exists.
            dots[directory + filename] = ""
            dots += getMap(baseDirectory, directory + filename)
        
        else:
            dots[directory + filename] = fullPath

""" Make a link from src to realDest.
    If nice is true, don't overwrite realDest.
    If src is an empty string, just create a directory. """
def makeLink(src, realDest, nice = False):
    if os.path.exists(realDest):
        if nice:
            return False
        else:
            shutil.rmtree(realDest)
    
    if src == "":
        os.mkdir(realDest)

    os.symlink(src, realDest)

    return True


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
