# PostiATS-Utilities

Messages pretty printer, JSONized files cache, `which`‑like, an `ls`‑like and a `whatis`‑like utilities for ATS/Postiats (the latter may get a better name).

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

List the top‑level declarations in an ATS source file. Declarations from `#include` are treated as top‑level, although only the ones referenced from the file including the other will be listed, due to a “limitation” of the JSON data used. Similarly, `typedef`, `infix` declarations and others, are not listed for the same reason; however, some are listed in the list of static constants, but only it it’s actually referred to by the source file. Ex. `typedef t = int` will appears as `t: t@ype` in the static constants list if something in the source file refers to this type alias. Ability to extract type definition will be added in a future revision.

When available, sort and type informations are displayed. Availability of these informations depends on the way the ATS source is written. With `val` and `var`, including with pattern matching, the defined entities need to be explicitly type annotated. With function, these informations appears only for an extern definition or its implementation. Although not primarily intended, this may be seen as an incentive to write separate declarations and implementations.

The output format is self explanatory. Just note the two lists which appears at the beginning, are a list of the base sorts and a list of the static constants referred by the ATS source file. The static constants list shows their name and sort.

Where type is displayed, a type expression or sub‑expression may be replaced by a question mark, “?”. This means producing a text image for the expression, is not already supported. If you happen to miss one and have too many of these “?”, please, feel free to fill an issue with a sample ATS source file where such a declaration appears. Sometimes, “\*ERROR\*” may appears in place of a type expression ; this means the static constant expression is missing from the JSON data.

Note sometimes the location displayed is that of the keyword introducing an entity declaration, not that of the name of the declared entity. This notably happens with constructors defined by say `datatype`.

With the `-r` option, the listing can be recursive through `staload`.

`pats-ls` handles `-IATS` options and file path resolution the same way as `pats-which` do, which is the same way the ATS2 compiler do.

This utility may be useful as a quick documentation tool to be used from a text editor. It is also expected to be useful to help reading ATS source files. In the future, a search command based on this listing, will be added as another utility based on this one. Also, another tool will come to further help reading and search deeper.

Ex.

        pats-ls prelude/basics_gen.sats


### `pats-whatis`

Tells what you have in the most inner span at a text position, then at the enclosing span, then at the outer enclosing span, and so on. The result is displayed on `stdout`, from most inner to most outer span, with source file locations and a readable designation of the ATS2 construct at each span.

The utility was started as an attempt to aid reading ATS2 source file. However, although it may be used for that purpose, it lacks details to really aid reading. Still, it’s useful to navigate locally in a source file.

File names are handled the same way as with `pats-which`. Next to the file name, it takes two additional integer argument, for line and column.

Ex. Suppose you have a `sample.dats` file containing this:

        prval
          (a, b) =
            (true, 1 == 1)


The following invokation will give the quoted results on `stdout`.

`pats-whatis sample.dats 3 8`:

  * sample.dats:3:6: constant (dynamic)
  * sample.dats:3:5: tuple
  * sample.dats:1:1: value declaration(s)

`pats-whatis sample.dats 3 15`:

  * sample.dats:3:14: overloaded symbol (dynamic)
  * sample.dats:3:12: function application
  * sample.dats:3:5: tuple
  * sample.dats:1:1: value declaration(s)

Note it includes implicit declarations `patsopt` may produce, like function effect annotation even if there is none is the source, and also note `patsopt` erase or ignore some things, which is also indicated as such. This utility does no syntactic analyses, it relies on JSON data produce by the ATS2 compiler.

It’s obviously more intended to be invoked from an IDE or text editor rather than from the command line. Some IDE or editor, allows to invoke an external program with the current line and column as parameters.

If the first line tells something like “** Unsupported Xyz **”, you can tell about, opening an issue with a short source sample triggering this message, so that I can add support for the designated language construct.


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
