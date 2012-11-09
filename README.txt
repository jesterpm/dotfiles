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
                                  on bismuth.jesterpm.net in

setup.py                          A script to setup links to the dot files.


setup.py
-------------------------------------------------------------------------------
The setup scripts makes the following links:
 
 * For every file X in base/, ~/.X is linked to base/X

If a file already exists, it is deleted unless the --nice flag is given.
 
