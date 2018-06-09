# PostiATS-Utilities

Messages pretty printer, JSONized files cache, `which`‑like and `ls`‑like utilities for ATS/Postiats.

Note this is not part of the official Postiats release and as much the repository name and the package name, use the name “PostiATS”, only to make their purpose clear. The use of this name here, does not imply any recommendation or endorsement.


## Help


### `install-ats2-on-debian-ubuntu.sh`

Variation of [githwxi/C9-ATS2-install.sh](https://gist.github.com/githwxi/7e31f4fd4df92125b73c). See comments at the top of `install-ats2-on-debian-ubuntu.sh`. In particular, there are configuration variables one may need to edit.


### `pats-filter`

A filter for output from `patscc`. Convenient for more readable error output in a terminal or for easier integration in a text editor able to display error messages.

To use `pats-filter`, think to redirect `stderr` to `stdin`, since the filter reads from `stdin`.

Ex:

        patscc -o test test.dats 2>&1 | pats-filter


### `pats-jsonized`

Manage a cache of jsonized ATS source files, with base sorts and static constants as a reminder and overview of a source file’s domain. The utilities is only one of the functions provided by the module `postiats/jsonized.py`. If you happen to use jsonized ATS source files, you may be worried about having to generate it each time
you need it even if the source file has not changed. This module exist to save this process invocation, providing jsonized source files from cache.

**Please note** it is not aware of source files dependencies. If `foo.dats` depends on `foo.hats` or `foo.sats` and `foo.hats` or `foo.sats` was changed, it will not understand `foo.dats` is obsolete. Since most of time only the files in a directory will change, an option to refresh the cache for a directory, will be added in the future.

Use `pats-jsonized --help` for more and have a look at `postiats/jsonized.py`. Since it does not generate immediately readable output, no example command line will be given here.


### `pats-ls`

List the top‑level declarations in an ATS source file. Declarations from `#include` are treated as top‑level, although only the ones referenced from the file including the other will be listed, due to a “limitation” of the JSON data used. Similarly, `typedef`, `infix` declarations and others, are not listed for the same reason; however, some are listed in the list of static constants, but only it it’s actually referred to by the source file. Ex. `typedef t = int` will appears as `t: t@ype` in the static constants list if something in the source file refers to this type definition. Ability to extract type definition will be added in a future revision.

When available, sort and type informations are displayed. Availability of these informations depends on the way the ATS source is written. With `val` and `var`, including with pattern matching, the defined entities need to be explicitly type annotated. With function, these informations appears only for an extern definition or its implementation. Although not primarily intended, this may be seen as an incentive to write separate declarations and implementations.

The output format is self explanatory. Just note the two lists which appears at the beginning, are a list of the base sorts and a list of the static constants referred by the ATS source file. The static constants list shows their name and sort.

Where type is displayed, a type expression or sub‑expression may be replaced by a question mark, “?”. This means producing a text image for the expression, is not already supported. If you happen to miss one and have too many of these “?”, please, feel free to file an issue with a sample ATS source file where such a declaration appears. Sometimes, “*ERROR*” may appears in place of a type expression ; this means the static constant expression is missing from the JSON data.

Note sometimes the location displayed is that of the keyword introducing an entity declaration, not that of the name of the declared entity. This notably happens with constructors defined by say `datatype`.

With the `-r` option, the listing can be recursive through `staload`.

`pats-ls` handles `-IATS` options and file path resolution the same way as `pats-which` do, which is the same way the ATS2 compiler do.

This utility may be useful as a quick documentation tool to be used from a text editor. It is also expected to be useful to help reading ATS source files. In the future, a search command based on this listing, will be added as another utility based on this one. Also, another tool will come to further help reading and search deeper.

Ex.

        pats-ls prelude/basics_gen.sats


### `pats-which`

A `which` like command to locate an ATS source file by its name. The name is
the one which is expected to be used with an `#include`, `staload` or `dynload` directive. Hint: it handles `-IATS` arguments passed on its command line, the same way the ATS2 compiler would do. The optional `-IATS` arguments may be located anywhere on the arguments list.

Warning: the current working directory comes first in the search path, but when a DATS files refers to a SATS file, it needs to do so using a dotted relative path. Ex. if `foo.dats` staload `foo.sats` in the same directory as `foo.dats`, it needs to do `staload "./foo.sats"`, because the current working directory is not that of the DATS file. If `foo.dats` do `staload "foo.sats"`, it will only work if compiled from within its own directory. It is safer to always use dotted relative path to refer a file relatively to its own directory.

If a single file is found, its full path is displayed on `stdout` and the exit code is `0`. If there are multiple candidates, the selected one is printed first and the others on the next lines with an “ (hidden)” at the end of their line. If it’s not found, “Not found.” is displayed on `stderr` and the exit code is `1`.

It is convenient for at least three purposes:

  * Check if a file can be found by the ATS2 compiler.
  * Open a staloaded/dynloaded/included file in a text editor.
  * When a file is not visible by ATS2, tell which file(s) of the same name may hide it.

Ex:

        pats-which share/atspre_staload.hats
