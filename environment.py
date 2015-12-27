#!/usr/bin/env python3
# -*- coding:utf-8; mode:python3; indent-tabs-mode:nil; tab-width:4; -*-

""" Postiats environment definition and utilities. """

import os
import sys

# Environment definitions
# ============================================================================

# In https://groups.google.com/d/msg/ats-lang-users/fS9R7QhgZVY/ovXDtooiSlQJ]
# Hongwei Xi said:
# > the search path ranges over the following in the listed order:
# >
# > the current directory of the filename being processed
# >
# > the ones in PATHLST (added by the flag -IATS)
# >
# > the ones in PREPATHLST (${PATSHOME} is the only one as of now)
#
# `PATSHOMERELOC` is only used for substitution of the define variable of the
# same name.

CWD = os.getcwd()
PATSHOME = os.getenv("PATSHOME")
PATSHOMERELOC = os.getenv("PATSHOMERELOC")

PATHLST = []
PREPATHLST = []

if PATSHOME is not None:
    PREPATHLST.append(PATSHOME)

if PATSHOME is None:
    print(
        "WARNING: the `PATSHOME` environment variable isn't set.",
        file=sys.stderr)

if PATSHOMERELOC is None:
    print(
        "WARNING: the `PATSHOMERELOC` environment variable isn't set.",
        file=sys.stderr)

SEARCH_DIRECTORIES = [CWD] + PATHLST + PREPATHLST


def handle_sys_argv():
    """ Interpret and delete -IATS arguments in `sys.argv`. """
    i = 1
    while i < len(sys.argv):
        if sys.argv[i] == "-IATS":
            del sys.argv[i]
            if i < len(sys.argv):
                path = sys.argv[i]
                PATHLST.append(path)
                del sys.argv[i]
            else:
                # PATHLST.append("")  Redundant with `CWD`.
                pass
        else:
            i += 1


handle_sys_argv()


# Searching for files
# ============================================================================

def find_in_directory(directory, file_name):
    """Search for `file_name` in `directory`, return its path or None.

    Search is not recursive. Postiats search path works like the usual `PATH`
    environment variable. The file must not only exists as a directory entry,
    it also must be readable as a file (so file permissions matters).

    If a path is returned, it is normalized (without any “.” or “..”).

    """
    result = None
    path = os.path.join(directory, file_name)
    if os.path.exists(path):
        try:
            open(path, "r").close()
            result = os.path.normpath(path)
        except OSError:
            pass
        except IOError:
            pass
    return result


def which(file_name):
    """ Like the UNIX `which` command, for files in Postiats search path. """
    result = None
    for directory in SEARCH_DIRECTORIES:
        result = find_in_directory(directory, file_name)
        if result is not None:
            break
    return result


def which_candidates(file_name):
    """ Like `which`, except it returns a list of all candidates.

    Candidates are listed by priority. The first one is the one which would
    be returned by `which` and the other are implicitly hidden. If not found,
    an empty list is returned (where `which` would return None).

    """
    result = []
    for directory in SEARCH_DIRECTORIES:
        found = find_in_directory(directory, file_name)
        if found is not None:
            result.append(found)
    return result


# Main
# ============================================================================

def main():
    """ Main. """
    if len(sys.argv) == 2:
        file_name = sys.argv[1]
        candidates = which_candidates(file_name)
        if len(candidates) == 0:
            print("Not found.", file=sys.stderr)
            exit(1)
        first = True
        for candidate in candidates:
            if first:
                print(candidate)
            else:
                print("%s (hidden)" % candidate, file=sys.stderr)
            first = False
    else:
        print("Usage: environment file-name.", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
