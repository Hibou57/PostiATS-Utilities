Description of “json-ref.txt”
==============================================================================

Intro
------------------------------------------------------------------------------

“json-ref.txt” provides data for the interpretation of the nodes in the JSON
output from `patsopt`.

The data in this files may also be useful to study ATS2, since the JSON output
is close to an abstract syntax tree. Using JSON output with the help of this
documentation, may also allow program analyses, documentation and may be
creating tools to assist porting source from ATS2 to ATS3 in the future.


Format
------------------------------------------------------------------------------

“--” is a comment up to the end of line

A text line underlined by many “=====” is a heading, it’s like a comment.

JSON is made of dictionaries, lists and literals. In Patsopt JSON output,
lists may serves two purpose: a list as anyone understand it and a record just
like a dictionary, except with integer indexes instead of names. In the former
case, the list in “json-ref.txt” has a minimal and maximal length. In the
latter case, a list in “json-ref.txt” has a fixed length and its elements
appears as “[n]” just like if it was a key in a dictionary.

Each key, either as “foo” or “[n]” has a content which is described like if it
was a type. Types may be literal: bool, int, str. May be a dictionary made of
a set of fields which are all presents, each of them appearing as “+ name”.
May be a dictionary with a single key, and there may be multiple options for
this key, like if the key was a discriminant. These keys appears as “| name”.

Sometime an empty list or an empty dictionary appears, which means it’s always
an empty list of an empty dictionary in the JSON output. This may
be an omission of the JSON output or a case I could not meet.

Fake examples with explanations:


        function: -- a record of three indexed fields
           [0]: str -- member of type str
           [1]: -- record made of multiple components
              + argument1 -- this is always provided
              + argument2 -- this is always provided
           [2]: -- record made of either one of these single components
              | result -- this may be this
              | nothing -- or this

        argument1:
           [int] 0…n -- a list of int, without upper length, may be empty

        argument2:
           [int] 0…1 -- the list min/max length 0…1 is like an option type

        result:
            char

        nothing:
           []


Note each key is separately described, although it may have additional
comments where it occurs.

Note the description as type given in “json-ref.txt” are for the most general
cases, when a node appears in a precise context, its actual type may be a
subtype.

Where a question mark appears in a comment, it means more clarifications or
investigations would needed, but I failed to.

Data was inferred with analyses, testing and some comments ATS2 source.


Macro‑like nodes
------------------------------------------------------------------------------

Node names like “${abcd}” does not appear in JSON output, there are used
and defined like macro, since the same appears often at many places. As an
exemple, something like this often occurs in produced JSON data:

        foo:
           [0]: …
           [1]:
              + s2exp_node
              + s2exp_srt
           [2]: …

The type of “[1]” was turned into ${s2exp} in “json-ref.txt”, since if occurs
at multiple place, and it is somewhere defined like this:

        ${s2exp}:
           + s2ex_node
           + s2exp_srt

And instead of the former, you will see this:

        foo:
           [0]: …
           [1]: ${s2exp}
           [2]: …


Something similar in done with comments, as indicated in a comment at the top
of “json-ref.txt”


More on some nodes
------------------------------------------------------------------------------

The nodes name ending with “map”, are like symbol tables. There contains keys
whose name ends with “_stamp”. Do not mix stamps between table! The stamps
which appears directly in the table entries, defines the ID of the table
entries. When the stamps appears elsewhere, they are to be interpreted as
references to these table entries.

The node name ending with “_loc” has a string value of a special format. You
probably already since this format for source location in error messages
from Postiats. There is a module, `postiats/locations.py` in this repository,
to deal with this format.

Some node has special value to be further interpreted, like integers with
special meanings. The interpretation is given in comments and these special
values are listed in the module `postiats/constants.py`.

The dictionary keys appearing in JSON output from Postiats, are also listed
in `postiats/tags.py`.

The node “/” does not exists in JSON output, it just represents the root node.
