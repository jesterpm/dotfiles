dotfiles
================================================================================

This is my collection of dotfiles. They are organized like this:

base/                             Files I want on every host.
host-overrides/
    jesterpm.net/                 These files override those in base/ on hosts
                                  with domains ending in jesterpm.net

        host-specific/            Files in this directory are typically
                                  sourced from files in base to provide
                                  host (or domain) specific extensions.
                                  
    bismuth.jesterpm.net/         These files override those in jesterpm.net/ 
                                  on bismuth.jesterpm.net.

setup.py                          A script to setup links to the dot files.


setup.py
-------------------------------------------------------------------------------

Usage: ./setup.py [--nice] [--pretend] [--home=DIRECTORY]

    --nice         No destructive action. setup will not delete anything.
    --pretend      List the symlinks to make, but don't make them.
    --home         Place the links in DIRECTORY instead of $HOME.

The setup script makes links from your home directory to the appropriate files
in the dotfiles repository. Unless --nice is specified, it will delete any
file that stands in its way. If it fails to make a link, it will report the
error and continue.

Suppose your hostname was bismuth.jesterpm.net. The setup script will check
these directories for files in this order:

    * base/
    * host-overrides/net
    * host-overrides/jesterpm.net
    * host-overrides/bismuth.jesterpm.net

Files found later supersede files found in previous directories, allowing you
to have specific files for specific hosts or domains. If the script finds a
directory and that directory contains a file called .nolink, then that
directory will be created in $HOME instead of linked, and the appropriate
links will be created inside that directory. This process continues
recursively.
 
