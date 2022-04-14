#!/usr/bin/python

"""
This script creates symlinks in your home directory to your dotfiles in the
Git repository.

By default it will delete any file that stands in the way of its mission to
create a better world.

Usage: python setup.py [--nice] [--home=DIRECTORY]

  --nice               Don't trample existing dot files.
  --home=DIRECTORY     Place links in DIRECTORY instead of $HOME.
  --pretend            Don't change anything, just say what would be done.

"""

import os, sys, getopt, socket
import shutil
import string

class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg

""" Create links to dotfiles """
def makeDots(base, home, nice = False, pretend = False):
    # First make a map of dot files to files in the repository.
    dotfiles = getMap(base + "/base/")
    
    # Get host specific overrides
    hostname = socket.getfqdn().lower().split(".")
    for i in range(len(hostname)):
        name = string.join(hostname[-(i+1):], ".")
        directory = base + "/host-overrides/" + name
        if os.path.isdir(directory):
            mergeDicts(dotfiles, getMap(directory))

    if pretend:
        print "I would make these links:"
    else:
        print "I am making these links:"

    makeLinks(dotfiles, home + "/.", nice, pretend)

def makeLinks(dotfiles, prefix, nice, pretend):
    keys = dotfiles.keys()
    keys.sort()
    for dst in keys:
        src = dotfiles[dst]
        realDest = prefix + dst

        if type(src) is dict:
            try:
                if not pretend:
                    if os.path.islink(realDest):
                        os.unlink(realDest) # Only remove symlinks. Don't try to replace a file with a directory.
                    if not os.path.isdir(realDest): 
                        os.mkdir(realDest)
                if os.path.lexists(realDest):
                    print "%50s  => <NEW DIRECTORY>" % (realDest)
                else:
                    print "%50s *=> <NEW DIRECTORY>" % (realDest)
                makeLinks(src, realDest + "/", nice, pretend)
            except OSError,e:
                print "Could not mkdir %s. Will not link subitems: %s" % (realDest, str(e))

        else:
            try:
                fileExists = os.path.lexists(realDest)
                if not pretend:
                    success = makeLink(src, realDest, nice)

                if fileExists:
                    if os.path.realpath(realDest) == os.path.realpath(src):
                        print "%50s  => %s" % (realDest, src)
                    else:
                        print "%50s !=> %s" % (realDest, src)
                else:
                    print "%50s *=> %s" % (realDest, src)

            except IOError,e:
                print "Not linking %s to %s because IOError: %s" % (realDest, src, str(e))

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
        
        if filename == ".git":
            continue # Skip over submodules.

        fullPath = baseDirectory + directory + filename
        
        if os.path.isdir(fullPath) and os.path.exists(fullPath + "/.nolink"):
            # We will not make a link but will make sure this directory exists.
            dots[directory + filename] = getMap(baseDirectory + directory + filename)
        
        else:
            dots[directory + filename] = fullPath

    return dots

""" Make a link from src to realDest.
    If nice is true, don't overwrite realDest.
    If src is an empty string, just create a directory. """
def makeLink(src, realDest, nice = False):
    if os.path.lexists(realDest):
        if nice:
            return False
        if os.path.isdir(realDest) and not os.path.islink(realDest):
            shutil.rmtree(realDest)
        else:
            os.unlink(realDest)
    
    os.symlink(src, realDest)

    return True

""" Recursively merge the second dictionary into the first. The latter takes precedence."""
def mergeDicts(a, b):
    for key, value in b.items():
        if key in a and type(value) is dict and type(a[key]) is dict:
            mergeDicts(a[key], value)
        else:
            a[key] = value

""" Main Method """
def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        try:
            opts, args = getopt.getopt(argv[1:], 
                    "hnd:p", ["help", "nice", "home=", "pretend"])
        except getopt.error, msg:
             raise Usage(msg)

        # Settings:
        nice = False
        pretend = False
        home = os.environ.get("HOME")

        for o, a in opts:
            if o in ("-h", "--help"):
                print __doc__
                return 0

            if o in ("-n", "--nice"):
                nice = True

            elif o in ("-p", "--pretend"):
                pretend = True

            elif o in ("-d", "--home"):
                home = a

        if not home:
            raise Usage("No home provided")

        makeDots(os.getcwd(), home, nice, pretend)

    except Usage, err:
        print >>sys.stderr, err.msg
        print >>sys.stderr, "for help use --help"
        return 2

if __name__ == "__main__":
    sys.exit(main())
