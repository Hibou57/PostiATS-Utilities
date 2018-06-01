# PostiATS-Utilities

Messages pretty printer, JSONized files cache and `which`‑like utility for ATS/Postiats.

Note this is not part of the official Postiats release and as much the repository name and the package name, use the name “PostiATS”, only to make their purpose clear. The use of this name here, does not imply any recommendation or endorsement.

## Help

### `pats-filter`

A filter for output from `patscc`. Convenient for more readable error output in a terminal or for easier integration in a text editor able to display error messages.

To use `pats-filter`, think to redirect `stderr` to `stdin`, since the filter reads from `stdin`.

Ex:
        patscc -o test test.dats 2>&1 | pats-filter

### `pats-which`

A `which` like command to locate an ATS source file by its name. The name is
the one which is expected to be used with an `#include`, `staload` or `dynload` directive. Hint: it handles `-IATS` arguments passed on its command line, the same way the ATS2 compiler would do. The optional `-IATS` arguments may be located anywhere in the arguments list.

If a single file is found, its full path is displayed on `stdout` and the exit code is `0`. If there are multiple candidats, the selected one is printed first and the others on the next lines with an “ (hidden)” at the end of their line. If it’s not found, “Not found.” is displayed on `stderr` and the exit code is `1`.

It is convenient for at least four purposes:

  * Check if a file can be found by the ATS2 compiler.
  * If there are multiple candidats, tell which one is used by the ATS2 compiler.
  * Open a staloaded/dynloaded/included file in a text editor.
  * When a file is not visible by ATS2, tell which file(s) of the same name, hide it.

Ex:

        pats-which share/atspre_staload.hats

### `pats-jsonized`

Manage a cache of jsonized ATS source files. The utilities is only one of the functions provided by the module `postiats/jsonized.py`. If you happen to use jsonized ATS source files, you may be worried about having to generate it each time
you need it even if the source file has not changed. This module exist to save this extraneous task, providing jsonized source files from cache.

Use `pats-jsonized --help` for more and have a look at `postiats/jsonized.py`.
