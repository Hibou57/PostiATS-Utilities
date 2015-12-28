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
#
# In https://groups.google.com/d/msg/ats-lang-users/i_AKS-nggZY/MAkwU4KAnf8J
# Hongwei Xi said:
# You can set it as follows:

# #define JNI_targetloc "$PATSHOMERELOC/contrib/JNI"
# In reply to Brandon Barker asking:
# > How do you set $JNI? Environment variables seems to not be the answer.

# Search paths
# ----------------------------------------------------------------------------

CWD = os.getcwd()
PATSHOME = os.getenv("PATSHOME")

PATHLST = []  # Filled with `-IATS` command line arguments
PREPATHLST = []  # Filled with only `PATSHOME` so far.

if PATSHOME is not None:
    PREPATHLST.append(PATSHOME)
else:
    print(
        "WARNING: the `PATSHOME` environment variable isn't set.",
        file=sys.stderr)

SEARCH_DIRECTORIES = [CWD] + PATHLST + PREPATHLST  # Order by definition.


def handle_iats_args():
    """ Interpret and delete `-IATS` arguments in `sys.argv`.

    Each `-IATS` argument value is added to `PATHLST` in the order there
    appear. `-IIATS` arguments are handled like `-IATS`.

    """
    i = 1
    while i < len(sys.argv):
        if sys.argv[i] in ["-IATS", "-IIATS"]:
            del sys.argv[i]
            if i < len(sys.argv):
                path = sys.argv[i]
                del sys.argv[i]
                PATHLST.append(path)
            else:
                # PATHLST.append("")  Redundant with `CWD`.
                pass
        else:
            i += 1


handle_iats_args()

# Path variables
# ----------------------------------------------------------------------------
VARIABLE_SUFFIX = "_targetloc"

PATSHOMERELOC = os.getenv("PATSHOMERELOC")

PATH_VARIABLES = {}
# Prefilled with `PATSHOME` and `PATSHOMERELOC`.
# Completed with `-(DD|D)ATS XYZ_targetloc=something` command line arguments.

if PATSHOME is not None:
    PATH_VARIABLES["PATSHOME"] = PATSHOME

if PATSHOMERELOC is not None:
    PATH_VARIABLES["PATSHOMERELOC"] = PATSHOMERELOC
else:
    print(
        "WARNING: the `PATSHOMERELOC` environment variable isn't set.",
        file=sys.stderr)


def handle_dats_args():
    """ Interpret and delete `-DATS` arguments in `sys.argv`.

    Only the `-DATS` arguments of the form `-DATS XYZ_targetloc=something` has
    an effect: the key “XYZ” with value “something” is added to
    `PATH_VARIABLES`. Others `-DATS` arguments are read, however dropped.

     `-DDATS` arguments are handled like `-DATS`.

    """
    i = 1
    while i < len(sys.argv):
        if sys.argv[i] in ["-DATS", "-DDATS"]:
            del sys.argv[i]
            if i < len(sys.argv):
                arg = sys.argv[i]
                del sys.argv[i]
                pair = arg.split("=", 1)
                if len(pair) == 2:
                    (name, value) = pair
                    if name.endswith(VARIABLE_SUFFIX):
                        name = name[:-len(VARIABLE_SUFFIX)]
                        PATH_VARIABLES[name] = value

        else:
            i += 1


handle_dats_args()


def end_of_name(text, start):
    """ End of a variable name at `start`. Return `start` if no name.

    Returning `start` just means the name at `start`, is empty.

    """
    # TODO: are underscore allowed?
    result = start
    end = len(text)
    while result < end and text[result].isalnum():
        result += 1
    return result


def find_variable(text, start):
    """ Return `(name, var_start, var_end)` or None.

    The variable may be of two forms: `$XYZ` or `{$XYZ}`. The latter is to
    be used when otherwise the variable name would be followed by a name
    character, which would make it ambiguous.

    """
    result = None
    i = text.find("{$", start)  # Must be tested before "$" alone.
    if i != -1:
        # i is start of variable.
        j = i + len("{$")
        # j is start of name.
        k = end_of_name(text, j)
        if k > j:
            if k < len(text) and text[k] == "}":
                name = text[j:k]
                k += len("}")
                # k is now end of variable.
                result = (name, i, k)
    else:
        i = text.find("$", start)
        if i != -1:
            # i is start of variable.
            j = i + len("$")
            # j is start of name
            k = end_of_name(text, j)
            if k > j:
                name = text[j:k]
                # k is end of name and variable.
                result = (name, i, k)
    return result


def variables_substituted(text):
    """ Substitute path variables to their values.

    The variable may be of two forms: `$XYZ` or `{$XYZ}`. The latter is to
    be used when otherwise the variable name would be followed by a name
    character, which would make it ambiguous.

    """
    # TODO: is substitution recursive?
    # TODO: what if a variable is unknown?
    result = ""
    i = 0  # end of last substituted variable.
    while True:
        variable = find_variable(text, i)
        if variable is None:
            # Remaining of text starts at i.
            break
        (name, var_start, var_end) = variable
        if name in PATH_VARIABLES:
            substitution = PATH_VARIABLES[name]
        else:
            substitution = ""
        result += text[i:var_start]  # Segment after previous, before current.
        result += substitution  # Instead of substring var_start to var_end.
        i = var_end  # Resume after current.

    result += text[i:]
    return result


# Searching for files
# ============================================================================

def is_readable(path):
    """ True if `file_name` can be opened for reading. """
    result = False
    if os.path.exists(path):
        try:
            open(path, "r").close()
            result = True
        except OSError:
            pass
        except IOError:
            pass
    return result


def find_in_directory(directory, file_name):
    """ Search for `file_name` in `directory`, return its path or None.

    Search is not recursive. Postiats search path works like the usual `PATH`
    environment variable. The file must not only exists as a directory entry,
    it also must be readable as a file (so file permissions matters).

    If a path is returned, it is normalized (without any “.” or “..”).

    """
    result = None
    directory = variables_substituted(directory)
    path = os.path.join(directory, file_name)
    path = os.path.normpath(path)
    if is_readable(path):
        result = path
    return result


def get_candidates(file_name, stop_at_first):
    """ For implementation of `which` and `which_candidates`. """
    result = []
    file_name = variables_substituted(file_name)
    first = True
    for directory in SEARCH_DIRECTORIES:
        found = find_in_directory(directory, file_name)
        if found is not None:
            result.append(found)
            if first and stop_at_first:
                break
            if first and os.path.isabs(file_name):
                break
            first = False
    return result


def which(file_name):
    """ Like the UNIX `which` command, for files in Postiats search path. """
    result = None
    candidates = get_candidates(file_name, stop_at_first=True)
    if len(candidates) > 0:
        result = candidates[0]
    return result


def which_candidates(file_name):
    """ Like `which`, except it returns a list of all candidates.

    Candidates are listed by priority. The first one is the one which would
    be returned by `which` and the other are implicitly hidden. If not found,
    an empty list is returned (where `which` would return None).

    """
    result = get_candidates(file_name, stop_at_first=False)
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
