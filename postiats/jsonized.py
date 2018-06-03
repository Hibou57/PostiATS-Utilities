#!/usr/bin/env python3
# -*- coding:utf-8; mode:python3; indent-tabs-mode:nil; tab-width:4; -*-

""" Cached JSONized ATS files retrieved as JSON objects.

JSON data may also be returned to stdout, for use from the command line.

"""

from . import environment
import json
import os
import subprocess
import sys

# Cache directory
# ============================================================================

HOME = os.path.expanduser("~")


def user_directory(sub_directory):
    """ `$HOME/sub_directory` if it exists or else None. """
    result = None
    directory = os.path.join(HOME, sub_directory)
    if os.path.exists(directory):
        result = directory
    return result


CACHE_ROOT = (
    os.getenv("LocalAppData")
    or os.getenv("XDG_CACHE_HOME")
    or user_directory("AppData/Local")
    or user_directory("Local Settings/Application Data")
    or user_directory("Library/Caches")
    or user_directory(".cache")
    or "/tmp"
)

CACHE = os.path.join(CACHE_ROOT, "PostiATS")

# Scanned directories for prefilling
# ============================================================================

ROOTS = [
    environment.CWD,
    environment.PATSHOME,
    environment.PATSCONTRIB
]

# Other constants
# ============================================================================

JSON_EXT = ".json"
SATS_EXT = ".sats"
DATS_EXT = ".dats"
TIMEOUT_DELAY = 3
POSTIATS_ENCODING = "iso-8859-15"

HELP = """\
Usage: %s -h|--help|--to-stdout file|--prefill|--purge|--directory

Or else used as a Python3 module.

 * -h/--help: display this help.
 * --to-stdout file: for command line use, return the JSON object to stdout,
   where file, is a SATS or DATS file.
 * --prefill: prefill the cache with ATS files from the distribution and
   the current directory, recursively.
 * --purge: purge the cache directory, removing all JSON files and directories
   left empty.
 * --directory: print the cache directory path.

"""


# Testing file types
# ============================================================================

def file_ext(path):
    """ File extension of `path` including the leading dot. """
    result = os.path.splitext(path)[1]
    return result


def is_json_file(file_name):
    """ True if file extension is “.json”. """
    ext = file_ext(file_name)
    result = ext == JSON_EXT
    return result


def is_sats_file(file_name):
    """ True if file extension is “.sats”. """
    ext = file_ext(file_name)
    result = ext == SATS_EXT
    return result


def is_ats_file(file_name):
    """ True if file extension is “.sats” or “.dats”. """
    ext = file_ext(file_name)
    result = ext in [SATS_EXT, DATS_EXT]
    return result


# Resolving path
# ============================================================================

def path_elements(path):
    """ Elements of `path`.

    The list is never empty. The first element may be the empty string.

    """
    result = []
    (head, tail) = os.path.split(path)
    while tail != "":
        result.insert(0, tail)
        (head, tail) = os.path.split(head)
    result.insert(0, head)
    return result


def resolved_path(path):
    """ Path made absolute, with symbolic links resolve, and normalized. """
    path = os.path.abspath(path)
    elements = path_elements(path)
    result = ""
    for element in elements:
        segment = element
        segment_path = os.path.join(result, segment)
        if os.path.islink(segment_path):
            segment = os.readlink(segment_path)
        result = os.path.join(result, segment)
    result = os.path.normpath(result)
    return result


def clean_path(path):
    """ Path to be used for source and to derive cache path. """
    return resolved_path(path)


# Scanning directories for prefilling
# ============================================================================

def files_from_root(root, accept):
    """ Recursive list of files  in `root` for which `accept` is True. """
    for (dir_path, _dir_names, file_names) in os.walk(root, followlinks=True):
        for file_name in file_names:
            if accept(file_name):
                path = os.path.join(dir_path, file_name)
                yield path


def files_from_roots(roots, accept):
    """ `files_from_root` for each non-None root in `roots`. """
    for root in roots:
        if root is not None:
            yield from files_from_root(root, accept)


def ats_files():
    """ `files_from_roots(ROOTS, is_ats_file)`. """
    yield from files_from_roots(ROOTS, is_ats_file)


# Cached file names
# ============================================================================

def cached_ext(ext):
    """ Extension for cached JSON file, from original extension.

    “.(s|d)ats” will become “-(s|d)ats.json”, not “.(s|d)ats.json”. This is so
    because the files are not to be ATS files anymore, they are to be JSON
    files.

    """
    if ext == "":
        result = JSON_EXT
    elif ext[0] == ".":
        result = "-" + ext[1:] + JSON_EXT
    else:
        result = ext + JSON_EXT
    return result


def get_cached_file_name(file_name):
    """ Cached file name for `file_name`.

    `file_name` is supposed to be a `clean_path`. The function can be invoked
    on non-`clean_path`, but it will not be relevant.

    """
    (directory, base_name) = os.path.split(file_name)
    directory = os.path.relpath(directory, start="/")
    new_directory = os.path.join(CACHE, directory)
    (simple_name, ext) = os.path.splitext(base_name)
    new_base_name = simple_name + cached_ext(ext)
    result = os.path.join(new_directory, new_base_name)
    return result


# Generating JSON
# ============================================================================

def run(directory, command, encoding):
    """ Run `command` in `directory` using `encoding` for stdout and stderr.

    Return a tuple `(stdout, stderr, return_code)`. If `return_code` is None,
    then stdout is always None too while stderr may be None or a string. Even
    when `return_code` is zero, stderr may not be None or may be an empty
    string.

    """
    stdout = None
    stderr = None
    return_code = None
    result = None
    try:
        process = subprocess.Popen(
            command,
            cwd=directory,
            universal_newlines=False,
            stdin=None,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
        # pylint: disable=unexpected-keyword-arg
        (stdout, stderr) = process.communicate(timeout=TIMEOUT_DELAY)
        return_code = process.returncode
    except OSError:
        stdout = None
        stderr = None
        return_code = None
    except subprocess.TimeoutExpired as timeout:
        stderr = getattr(timeout, "stderr", "")
        process.kill()
        (_ignored, stderr_tail) = process.communicate()
        stderr += stderr_tail
        stdout = None
        return_code = None
    if stdout is not None:
        stdout = stdout.decode(encoding)
    if stderr is not None:
        stderr = stderr.decode(encoding)
    result = (stdout, stderr, return_code)
    return result


def make_cached_json(file_name):
    """ Invoke `patsopt --jsonize-2` on `file_name`.

    Backup the content in cache and return the content as a JSON object.

    `file_name` is assumed to be from `environment.which`.

    """
    result = None
    path = clean_path(file_name)
    working_directory = os.path.split(os.path.abspath(file_name))[0]
    file_type_switch = "-s" if is_sats_file(file_name) else "-d"
    command = []
    command.append("patsopt")
    command.append("--jsonize-2")
    command.append(file_type_switch)
    command.append(path)
    (stdout, _stderr, return_code) = run(
        working_directory,
        command,
        POSTIATS_ENCODING)
    if return_code == 0:
        cached_file_name = get_cached_file_name(path)
        cached_directory = os.path.split(cached_file_name)[0]
        if not os.path.exists(cached_directory):
            os.makedirs(cached_directory)
        output = open(cached_file_name, "w")
        output.write(stdout)
        output.close()
        result = json.loads(stdout)
    return result


# Retrieving JSON
# ============================================================================

def get_json_from_cache(file_name):
    """ Try to get JSON from cache or else return None.

    Check the JSON file is newer than the ATS file, so even if the file
    is in the cache, None may still be returned if the cache version is
    outdated.

    `file_name` is assumed to be from `environment.which`.

    """
    result = None
    path = clean_path(file_name)
    cached_file_name = get_cached_file_name(path)
    if os.path.exists(cached_file_name):
        time = os.path.getmtime(path)
        cached_time = os.path.getmtime(cached_file_name)
        if cached_time > time:
            try:
                source = open(cached_file_name, "r")
                try:
                    result = json.load(source)
                except ValueError:
                    pass
                source.close()
            except IOError:
                pass
            except OSError:
                pass
    return result


def get_json(file_name):
    """ Get JSON for `file_name`, from cache or (re-)generated.

    Return `None` of not found.

    Use `environment.which`.

    """
    result = None
    path = environment.which(file_name)
    if path is not None:
        result = get_json_from_cache(path)
        if result is None:
            result = make_cached_json(path)
    return result


def get_json_to_stdout(file_name):
    """ Print JSON data for `file_name` to stdout.

    Useful to use the cache from the command line too, not only from Python
    scripts importing this module.

    """
    json_object = get_json(file_name)
    if json_object is None:
        print("Failed to generate JSON", file=sys.stderr)
        sys.exit(1)
    json.dump(json_object, sys.stdout)
    print()


# Prefilling and purging
# ============================================================================

def prefill_cache():
    """ Cache jsonized ATS files from distribution and current directory. """
    print("Prefilling cache.")
    print("\rListing ATS files...", end="")
    file_names = list(ats_files())
    print("\rListing ATS files: done.")
    index = 0
    files_count = len(file_names)
    cached_count = 0
    for file_name in file_names:
        index += 1
        print("\rHandling ATS file #%i of %i" % (index, files_count), end="")
        if get_json(file_name) is not None:
            cached_count += 1
    print("\nDone: %i file(s) cached." % cached_count)


def purge_cache():
    """ Purge cache deleting JSON files and directories left empty. """
    for (dir_path, dir_names, file_names) in os.walk(CACHE, topdown=False):
        for file_name in file_names:
            if is_json_file(file_name):
                path = os.path.join(dir_path, file_name)
                print("Removing file “%s”" % path)
                os.remove(path)
        for directory in dir_names:
            path = os.path.join(dir_path, directory)
            if len(os.listdir(path)) == 0:
                print("Removing directory “%s”" % path)
                os.rmdir(path)


# Main
# ============================================================================

def main():

    """ Main. """

    my_name = os.path.split(sys.argv[0])[1]

    arg_error = True

    if len(sys.argv) == 2:
        arg1 = sys.argv[1]
        if arg1 in ["-h", "--help"]:
            arg_error = False
            print(HELP % my_name)
        elif arg1 == "--prefill":
            arg_error = False
            prefill_cache()
        elif arg1 == "--purge":
            arg_error = False
            purge_cache()
        elif arg1 == "--directory":
            arg_error = False
            print("Cache directory: %s" % CACHE)
    if len(sys.argv) == 3:
        arg1 = sys.argv[1]
        arg2 = sys.argv[2]
        if arg1 == "--to-stdout":
            arg_error = False
            get_json_to_stdout(arg2)

    if arg_error:
        print("ERROR: Invalid argument(s).", file=sys.stderr)
        print(HELP % my_name, file=sys.stderr)
        sys.exit(1)
