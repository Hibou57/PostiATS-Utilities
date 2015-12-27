#!/usr/bin/env python3
# -*- coding:utf-8; mode:python3; indent-tabs-mode:nil; tab-width:4; -*-

""" PostiATS text ranges/pointers. """

import collections

# PostiATS Text Ranges/Locations
# ============================================================================

# Types
# ----------------------------------------------------------------------------
LineColumn = collections.namedtuple("LineColumn", ["line", "column"])
Location = collections.namedtuple("Location", ["path", "start", "end"])

# Constants
# ----------------------------------------------------------------------------
# Sample location:
#     UTF_8.dats: 5235(line=167, offs=53) -- 5237(line=167, offs=55)

END_OF_PATH = ": "
LINE_TAG = "(line="
OFFS_TAG = ", offs="
END_OF_BEGIN = ") -- "
END_OF_END = ")"

# Given these tags, the above sample would be split like this:
#
#  * "UTF_8.dats"   Path
#  * ": "           END_OF_PATH
#  * "5235"         Start bytes
#  * "(line="       LINE_TAG
#  * "167"          Start line
#  * ", offs="      OFFS_TAG
#  * "53"           Start offset (column)
#  * ") -- "        END_OF_START
#  * "5237"         End bytes
#  * "(line="       LINE_TAG
#  * "167"          End line
#  * ", offs="      OFFS_TAG
#  * "55"           End offset (column)
#  * ")"            END_OF_END
#
# Tested and applied in this order (there are duplicates):
#
#  * END_OF_PATH
#  * LINE_TAG
#  * OFFS_TAG
#  * END_OF_START
#  * LINE_TAG
#  * OFFS_TAG
#  * END_OF_END


# Helper
# ----------------------------------------------------------------------------

def find_tag(text, tag, start):
    """ Tuple `(start, end)` of `tag` in `text` starting at `start`.

    If `tag` is not found, `(-1, end)` is returned.

    """
    i = text.find(tag, start)
    j = i + len(tag)
    result = (i, j)
    return result


# Methods
# ----------------------------------------------------------------------------

def is_location(text):
    """ True if text is a text range/location. """
    j = 0

    def test_tag(tag):
        """ Update (i,j) if i is not -1. """
        nonlocal j
        (i, j) = find_tag(text, tag, j)
        result = i != -1
        return result

    result = (
        test_tag(END_OF_PATH)
        and test_tag(LINE_TAG)
        and test_tag(OFFS_TAG)
        and test_tag(END_OF_BEGIN)
        and test_tag(LINE_TAG)
        and test_tag(OFFS_TAG)
        and test_tag(END_OF_END)
    )

    result = result and j == len(text)

    return result


def parse(text):
    """ Parse `text` as a `Location`. """
    assert is_location(text)

    i = 0
    j = 0
    k = 0

    (j, k) = find_tag(text, END_OF_PATH, k)
    path = text[i:j]
    i = k

    (j, k) = find_tag(text, LINE_TAG, k)
    # start_bytes = text[i:j]
    i = k

    (j, k) = find_tag(text, OFFS_TAG, k)
    start_line = int(text[i:j])
    i = k

    (j, k) = find_tag(text, END_OF_BEGIN, k)
    start_offs = int(text[i:j])
    i = k

    (j, k) = find_tag(text, LINE_TAG, k)
    # end_bytes = text[i:j]
    i = k

    (j, k) = find_tag(text, OFFS_TAG, k)
    end_line = int(text[i:j])
    i = k

    (j, k) = find_tag(text, END_OF_END, k)
    end_offs = int(text[i:j])
    i = k

    start = LineColumn(line=start_line, column=start_offs)
    end = LineColumn(line=end_line, column=end_offs)
    result = Location(path=path, start=start, end=end)

    return result
