#!/usr/bin/env python3
# -*- coding:utf-8; mode:python3; indent-tabs-mode:nil; tab-width:4; -*-

""" Filter for PostiATS messages. """

import os
import sys

from collections import namedtuple
from enum import Enum

from . import locations

# Configuration (editable)
# ============================================================================

LINE_WIDTH = 78
SIMPLIFY = True
LOCATION_WITH_COLUMN = True


# PostiATS Messages
# ============================================================================

# Type
# ----------------------------------------------------------------------------
Message = namedtuple("Message", ["location", "level", "text"])

# Constants
# ----------------------------------------------------------------------------
# Sample message with location:
#     UTF_8.dats: 5235(line=167, offs=53) -- 5237(line=167, offs=55): \
#     error(3): static arity mismatch: more arguments are expected.
#
# Sample `showtype` or `$showtype` message:
#     **SHOWTYPE[UP]**(foo.dats: 768(line=46,\ offs=27) -- 769(line=46, \
#     offs=28)): S2Eapp(S2Ecst(T); S2EVar(0)): S2RTbas(S2RTBASimp(0; type))

END_OF_LOCATION = locations.END_OF_END  # ")"
START_OF_MSG_LEVEL = ": "
END_OF_MSG_LEVEL = ": "
SHOWTYPE_START = "**SHOWTYPE[UP]**("
SHOWTYPE_END = "): "


# Methods
# ----------------------------------------------------------------------------

def is_message_with_location(line):
    """ True if line is a message with location. """
    result = False
    i = line.find(END_OF_LOCATION + START_OF_MSG_LEVEL)
    if i != -1:
        i += len(END_OF_LOCATION)
        if locations.is_location(line[:i]):
            i += len(START_OF_MSG_LEVEL)
            i = line.find(END_OF_MSG_LEVEL, i)
            result = i != -1
    return result


def is_showtype_message(line):
    """ True if line is a showtype message (with location). """
    result = False
    if line.startswith(SHOWTYPE_START):
        i = line.find(SHOWTYPE_END)
        if i != -1:
            result = locations.is_location(line[len(SHOWTYPE_START):i])
    return result


def message_level_number(message_level):
    """ Level number from message level tag. """
    result = 0
    if message_level == "error(parsing)":
        result = 1
    if message_level == "error(2)":
        result = 2
    if message_level == "error(mac)":
        result = 2
    if message_level == "error(3)":
        result = 3
    return result


def parse_message_with_location(line):
    """ Parse `line` as a `Message`. """
    assert is_message_with_location(line)

    i = line.find(END_OF_LOCATION + START_OF_MSG_LEVEL)
    i += len(END_OF_LOCATION)
    location = locations.parse(line[:i])

    i += len(START_OF_MSG_LEVEL)
    j = line.find(END_OF_MSG_LEVEL, i)
    message_level = line[i:j]
    level = message_level_number(message_level)
    j += len(END_OF_MSG_LEVEL)

    text = line[j:]

    result = Message(
        location=location,
        level=level,
        text=text)
    return result


def parse_showtype_message(line):
    """ Parse `line` as a `Message`. """
    assert is_showtype_message(line)

    i = line.find(SHOWTYPE_END)
    location = locations.parse(line[len(SHOWTYPE_START):i])

    j = i + len(SHOWTYPE_END)
    level = 3

    text = "$showtype: " + line[j:]

    result = Message(
        location=location,
        level=level,
        text=text)
    return result


# Iterated String
# ============================================================================

class String(object):
    """ String iterator with indexes stack. """

    def __init__(self, string):
        """ Assign content to `string` and initializes index and stack. """
        self.string = string
        self.index = 0
        self.indexes = []
        self.len = len(string)

    def print_head(self):
        """ For debugging. """
        print(self.string[self.index:])

    def has_item(self):
        """ True if `item` is valid. """
        result = self.index < self.len
        return result

    def item(self):
        """ Character at index. """
        if not self.has_item():
            raise IndexError
        result = self.string[self.index]
        return result

    def has_ahead(self):
        """ True if `ahead` won't be `None`. """
        result = (self.index + 1) < self.len
        return result

    def ahead(self):
        """ Character next to actual `item` (may be `None`). """
        if not self.has_ahead():
            result = None
        else:
            result = self.string[self.index + 1]
        return result

    def consume(self):
        """ Consume current `item`: move index forward. """
        if not self.has_item():
            raise IndexError
        self.index += 1

    def push(self):
        """ Push current index on stack. """
        self.indexes.append(self.index)

    def unpush(self):
        """ Pop from stack not touching index. """
        if not self.indexes:
            raise IndexError
        self.indexes.pop()

    def pop(self):
        """ Pop current index from stack. """
        if not self.indexes:
            raise IndexError
        self.index = self.indexes.pop()

    def test_and_consume(self, string):
        """ True if `string` at index and skip, else False. """
        result = False
        i = self.index
        j = i + len(string)
        if self.string[i:j] == string:
            self.index = j
            result = True
        return result


# Parsing PostiATS's funny expressions
# ============================================================================

# Type
# ----------------------------------------------------------------------------
Node = namedtuple("Node", ["token", "kind", "nodes", "end"])

# Constants
# ----------------------------------------------------------------------------
KIND = Enum("KIND", "D2S2C3 LABEL NAME NAME_ID NUMERIC SYMBOL")
FOLLOWED_BY = Enum("FOLLOWED_BY", "SEMI_COLON COMMA ARROW END")


# Methods
# ----------------------------------------------------------------------------

# ### S2/C3 Name Token

def parse_d2s2c3_name(string):
    """ An S2Xxxx or a C3Xxxx or None. """
    # Ex. S2RTbas
    result = None
    prefix = None
    if string.test_and_consume("D2"):
        prefix = "D2"
    elif string.test_and_consume("S2"):
        prefix = "S2"
    elif string.test_and_consume("C3"):
        prefix = "C3"
    if prefix is not None:
        if string.has_item() and string.item().isalpha():
            result = prefix + string.item()
            string.consume()
            while string.has_item() and string.item().isalpha():
                result += string.item()
                string.consume()
    return result


# ### Numeric Token

def parse_numeric(string):
    """ A numeric or None. """
    # Ex. -123
    result = None
    string.push()
    if string.has_item():
        sign = +1
        if string.item() == "-":
            sign = -1
            string.consume()
        if string.has_item() and string.item().isnumeric():
            result = string.item()
            string.consume()
            while string.has_item() and string.item().isnumeric():
                result += string.item()
                string.consume()
            if sign == -1:
                result = "-" + result
    if result is None:
        string.pop()
    else:
        string.unpush()
    return result


# ### Name Token

def parse_name(string):
    """ A name or None. """
    # Ex. int or t@ype (but it is not selective!)

    def is_name_head_char(char):
        """ Alpha or _. """
        result = char.isalpha() or char == "_"
        return result

    def is_name_tail_char(char):
        """ Alnum or _ or @ or '. """
        result = char.isalnum() or char in {"_", "'", "@"}
        return result

    result = None
    if string.has_item() and is_name_head_char(string.item()):
        result = string.item()
        string.consume()
        while string.has_item() and is_name_tail_char(string.item()):
            result += string.item()
            string.consume()
    return result


# ### Label Token

def parse_label(string):
    """ A name= or None. """
    result = None
    string.push()
    name_part = parse_name(string)
    if name_part is not None:
        if string.test_and_consume("="):
            result = name_part
    if result is not None:
        string.unpush()
    else:
        string.pop()
    return result


# ### Name$ID Token

def parse_name_id(string):
    """ A name$id or None. """
    # Ex. foo$123
    result = None
    string.push()
    name_part = parse_name(string)
    if name_part is not None:
        if string.test_and_consume("$"):
            id_part = parse_numeric(string)
            if id_part is not None:
                result = name_part + "$" + id_part
    if result is not None:
        string.unpush()
    else:
        string.pop()
    return result


# ### Symbol Token

def is_symbol_char(char):
    """ True if `char` is a symbol. """
    # Also used by s2eapp_simplified_image.
    result = char in "[]<>.-+/%=~*&|"
    return result


def parse_symbol(string):
    """ A symbole or None. """
    # Ex. [ or --
    result = None
    if string.has_item() and is_symbol_char(string.item()):
        result = string.item()
        string.consume()
        while string.has_item() and is_symbol_char(string.item()):
            result += string.item()
            string.consume()
    return result


# ### Token

def parse_token(string):
    """ `(token, kind)` or None. """
    # Used by parse_node which do an higher level parsing using
    # the kind part.
    def try_token(method, kind):
        """ (token, kind) or None. """
        result = None
        token = method(string)
        if token is not None:
            result = (token, kind)
        return result

    result = (
        try_token(parse_d2s2c3_name, KIND.D2S2C3) or
        try_token(parse_label, KIND.LABEL) or
        try_token(parse_name_id, KIND.NAME_ID) or
        try_token(parse_name, KIND.NAME) or
        try_token(parse_numeric, KIND.NUMERIC) or
        try_token(parse_symbol, KIND.SYMBOL))
    return result


# ### Node

def get_end_kind(string):
    """ End kind. """
    result = None
    if string.test_and_consume("; "):
        result = FOLLOWED_BY.SEMI_COLON
    elif string.test_and_consume(", "):
        result = FOLLOWED_BY.COMMA
    elif string.test_and_consume("->"):
        result = FOLLOWED_BY.ARROW
    else:
        result = FOLLOWED_BY.END
    return result


def parse_node(string):
    """ A Node or None. """
    # High level parsing based on token kind.
    result = None
    token = None
    kind = False
    nodes = None
    end = None
    token_kind = parse_token(string)
    if token_kind is not None:
        (token, kind) = token_kind
        if kind == KIND.LABEL:
            nodes = parse_nodes(string)
            if nodes is not None:
                end = get_end_kind(string)
        elif string.test_and_consume("("):
            nodes = parse_nodes(string)
            if nodes is not None and string.test_and_consume(")"):
                end = get_end_kind(string)
        else:
            end = get_end_kind(string)
    if end is not None:
        result = Node(
            token=token,
            kind=kind,
            nodes=nodes,
            end=end)
    return result


def parse_nodes(string):
    """ Nodes or None. """
    # Iterate parse_node on string.
    result = []
    if string.item() != ")":
        while True:
            node = parse_node(string)
            if node is not None:
                result.append(node)
            else:
                result = None
                break
            if node.end == FOLLOWED_BY.END:
                break
    return result


# Words
# ============================================================================

# Type
# ----------------------------------------------------------------------------
Word = namedtuple("Word", ["text", "level", "kind"])

# Constants
# ----------------------------------------------------------------------------
WORD_TOKEN = 1
WORD_SEPARATOR = 2
WORD_OPERATOR = 3
WORD_OPEN = 4
WORD_CLOSE = 5


# Line
# ============================================================================

# Type
# ----------------------------------------------------------------------------
Line = namedtuple("Line", ["indent", "words"])


# Methods
# ----------------------------------------------------------------------------

def line_image(line):
    """ Image of line as string. """
    result = "  " * line.indent
    words = line.words
    i = 0
    first = 0
    last = len(words) - 1
    while i <= last:
        word = words[i]
        if word.kind == WORD_OPERATOR and i > first:
            result += " "
        result += word.text
        if word.kind == WORD_OPERATOR and i < last:
            result += " "
        if word.kind == WORD_SEPARATOR and i < last:
            result += " "
        i += 1
    return result


# Lines
# ============================================================================

def lines_image(lines):
    """ Image of lines as string. """
    result = ""
    for line in lines:
        result += line_image(line)
        result += "\n"
    return result


def append_words_as_line(result, words, indent):
    """ Helper. """
    if words:
        line = Line(indent, words)
        result.append(line)


def splitted_at_separator(line):
    """ Split line at separators kept at the end of each lines. """
    if line.words:
        indent = line.indent
        words = line.words
        level = words[0].level
        result = []
        line_words = []
        i = 0
        last = len(words) - 1
        while i <= last:
            word = words[i]
            line_words.append(word)
            if word.kind == WORD_SEPARATOR and word.level == level:
                line = Line(indent, line_words)
                result.append(line)
                line_words = []
            i += 1
        append_words_as_line(result, line_words, indent)
    else:
        result = [line]
    return result


def splitted_at_operator(line):
    """ Split line at operators kept at the start of each lines. """
    if line.words:
        indent = line.indent
        words = line.words
        level = words[0].level
        result = []
        line_words = []
        i = 0
        last = len(words) - 1
        while i <= last:
            word = words[i]
            if word.kind == WORD_OPERATOR and word.level == level:
                append_words_as_line(result, line_words, indent)
                line_words = []
            line_words.append(word)
            i += 1
        append_words_as_line(result, line_words, indent)
    else:
        result = [line]
    return result


def indented_on_next_level(line):
    """ Split line with indent on next level. """

    words = line.words
    if line.words:
        i = 0
        last = len(words) - 1
        level = words[0].level
        result = []

        def part(cond, indent):
            """ New line with `indent` with words while `cond`.

            `cond` is whether or not, `word.level == level`.

            """
            nonlocal words, i, last, level, result
            line_words = []
            while i <= last:
                word = words[i]
                if (word.level == level) != cond:
                    break
                line_words.append(word)
                i += 1
            append_words_as_line(result, line_words, indent)

        indent = line.indent
        while i <= last:
            part(True, indent)
            part(False, indent + 1)
    else:
        result = [line]
    return result


def format_lines(lines):
    """ Split and indent lines to fit max width. """
    changed = True
    result = lines
    while changed:
        lines = result
        result = []
        changed = False
        for line in lines:
            if len(line_image(line)) <= LINE_WIDTH:
                result.append(line)
                continue

            sublines = splitted_at_separator(line)
            if len(sublines) > 1:
                result += sublines
                changed = True
                continue

            sublines = splitted_at_operator(line)
            if len(sublines) > 1:
                result += sublines
                changed = True
                continue

            sublines = indented_on_next_level(line)
            if len(sublines) > 1:
                result += sublines
                changed = True
                continue
            result.append(line)
    return result


# Node Image as Word List
# ============================================================================

def append_end(node, level, acc):
    """ Helper. """
    if node.end == FOLLOWED_BY.SEMI_COLON:
        acc.append(Word(";", level, WORD_SEPARATOR))
    elif node.end == FOLLOWED_BY.COMMA:
        acc.append(Word(",", level, WORD_SEPARATOR))
    elif node.end == FOLLOWED_BY.ARROW:
        acc.append(Word("->", level, WORD_OPERATOR))
    elif node.end == FOLLOWED_BY.END:
        pass


def node_image(node, level, acc, with_end=True):
    """ Image of a node as word list. """
    result = acc
    if not simplified_image(node, level, result):
        result.append(Word(node.token, level, WORD_TOKEN))
        if node.kind == KIND.LABEL:
            result.append(Word("=", level, WORD_TOKEN))
            for subnode in node.nodes:
                result = node_image(subnode, level, result)
        elif node.nodes is not None:
            result.append(Word("(", level, WORD_OPEN))
            for subnode in node.nodes:
                result = node_image(subnode, level + 1, result)
            result.append(Word(")", level, WORD_CLOSE))
    if with_end:
        append_end(node, level, result)
    return result


# Node Image as a List of one Line
# ============================================================================

def node_lines_image(node):
    """ Image of node as lines. """
    words = []
    words = node_image(node, 0, words)
    result = [Line(0, words)]
    return result


# Node Image Simplification
# ============================================================================

# Constants
# ----------------------------------------------------------------------------

NAME_AS_OPERATOR = {
    "mul_int_int": "*",
    "add_int_int": "+",
    "sub_int_int": "*"}


# Helper
# ----------------------------------------------------------------------------

def is_empty_node(node):
    """ Node is empty (not the same as a leaf!). """
    result = node.nodes is not None and len(node.nodes) == 0
    return result


def single_child(node):
    """ The single child node or None. """
    result = None
    if node.nodes is not None and len(node.nodes) == 1:
        result = node.nodes[0]
    return result


def leaf_single_child(node):
    """ The single child leaf node or None. """
    result = None
    child = single_child(node)
    if child is not None and child.nodes is None:
        result = child
    return result


def int_single_child(node):
    """ The single child leaf node holding an integer or None. """
    result = None
    child = leaf_single_child(node)
    if child is not None and child.kind == KIND.NUMERIC:
        result = child
    return result


def empty_single_child(node):
    """ The single empty child node or None. """
    result = None
    child = single_child(node)
    if child is not None:
        if is_empty_node(child):
            result = child
    return result


# Methods
# ----------------------------------------------------------------------------

def s2eintinf_simplified_image(node, level, acc):
    """ S2Eintinf(number) --> number. """
    result = False
    if node.token == "S2Eintinf":
        leaf = int_single_child(node)
        if leaf is not None:
            acc.append(Word(leaf.token, level, WORD_TOKEN))
            result = True
    return result


def s2ecst_simplified_image(node, level, acc):
    """ S2Ecst(name) --> name | symbol. """
    result = False
    if node.token == "S2Ecst":
        leaf = leaf_single_child(node)
        if leaf is not None:
            token = leaf.token
            if token in NAME_AS_OPERATOR:
                operator = NAME_AS_OPERATOR[token]
                acc.append(Word(operator, level, WORD_OPERATOR))
            else:
                acc.append(Word(token, level, WORD_TOKEN))
            result = True
    return result


def d2s2evar_simplified_image(node, level, acc):
    """ (D2|S2)Evar(name(number)) --> name. """
    result = False
    if (node.token == "D2Evar") or (node.token == "S2Evar"):
        child = single_child(node)
        if child is not None:
            leaf = int_single_child(child)
            if leaf is not None:
                acc.append(Word(child.token, level, WORD_TOKEN))
                result = True
    return result


def s2eapp_simplified_image(node, level, acc):
    """ S2Eapp(name|sym; arg1, arg2) --> name(arg1, arg2) | (arg1 sym arg2).

    or S2Eapp(name|sym; arg1, … argn) --> name(arg1, … argn).

    """
    result = False
    if node.token == "S2Eapp":
        if node.nodes is not None and len(node.nodes) == 3:
            node1 = node.nodes[0]
            node2 = node.nodes[1]
            node3 = node.nodes[2]
            if (node1.end == FOLLOWED_BY.SEMI_COLON and
                    node2.end == FOLLOWED_BY.COMMA and
                    node3.end == FOLLOWED_BY.END):
                image1 = node_image(node1, level + 1, [], False)
                image2 = node_image(node2, level + 1, [], False)
                image3 = node_image(node3, level + 1, [], False)
                if len(image1) == 1 and is_symbol_char(image1[0].text[0]):
                    acc.append(Word("(", level, WORD_OPEN))
                    acc += image2
                    acc.append(Word(image1[0].text, level + 1, WORD_OPERATOR))
                    acc += image3
                    acc.append(Word(")", level, WORD_CLOSE))
                else:
                    acc += image1
                    acc.append(Word("(", level, WORD_OPEN))
                    acc += image2
                    acc.append(Word(",", level + 1, WORD_SEPARATOR))
                    acc += image3
                    acc.append(Word(")", level, WORD_CLOSE))
                result = True
        elif node.nodes is not None:
            node1 = node.nodes[0]
            if node1.end == FOLLOWED_BY.SEMI_COLON:
                image1 = node_image(node1, level + 1, [], False)
                acc += image1
                acc.append(Word("(", level, WORD_OPEN))
                first = True
                for i in range(1, len(node.nodes)):
                    noden = node.nodes[i]
                    noden_image = node_image(noden, level + 1, [], False)
                    if not first:
                        acc.append(Word(",", level + 1, WORD_SEPARATOR))
                    acc += noden_image
                    first = False
                acc.append(Word(")", level, WORD_CLOSE))
                result = True
    return result


def s2eeqeq_simplified_image(node, level, acc):
    """ S2Eeqeq(arg1, arg2) --> (arg1 == arg2). """
    result = False
    if node.token == "S2Eeqeq":
        if node.nodes is not None and len(node.nodes) == 2:
            node1 = node.nodes[0]
            node2 = node.nodes[1]
            if (node1.end == FOLLOWED_BY.SEMI_COLON and
                    node2.end == FOLLOWED_BY.END):
                image1 = node_image(node1, level + 1, [], False)
                image2 = node_image(node2, level + 1, [], False)
                acc.append(Word("(", level, WORD_OPEN))
                acc += image1
                acc.append(Word("==", level + 1, WORD_OPERATOR))
                acc += image2
                acc.append(Word(")", level, WORD_CLOSE))
                result = True
    return result


def s2effset_simplified_image(node, level, acc):
    """ S2EFFset(n) --> n. """
    result = False
    if node.token == "S2EFFset":
        if node.nodes is not None and len(node.nodes) == 1:
            node1 = node.nodes[0]
            image1 = node_image(node1, level, [], False)
            acc += image1
            result = True
    return result


def c3nstrprop_simplified_image(node, level, acc):
    """ C3NSTRprop(C3NSTRprop(); expression) --> expression. """
    result = False
    if node.token == "C3NSTRprop":
        nodes = node.nodes
        if nodes is not None and len(nodes) == 2:
            node1 = nodes[0]
            if node1.token == "C3TKmain" and is_empty_node(node1):
                node2 = nodes[1]
                node_image(node2, level, acc)
                result = True
    return result


def d2esymmac_simplified_image(node, level, acc):
    """ D2E(sym|mac)(name) --> name. """
    result = False
    if (node.token == "D2Esym") or (node.token == "D2Emac"):
        leaf = leaf_single_child(node)
        if leaf is not None:
            acc.append(Word(leaf.token, level, WORD_TOKEN))
            result = True
    return result


def name_simplified_image(node, level, acc):
    """ name(number) --> name. """
    result = False
    if node.kind == KIND.NAME:
        leaf = int_single_child(node)
        if leaf is not None:
            acc.append(Word(node.token, level, WORD_TOKEN))
            result = True
    return result


# Main
# ----------------------------------------------------------------------------

SIMPLIFIED_IMAGE_METHODS = [
    c3nstrprop_simplified_image,
    d2esymmac_simplified_image,
    d2s2evar_simplified_image,
    s2eapp_simplified_image,
    s2ecst_simplified_image,
    s2eeqeq_simplified_image,
    s2effset_simplified_image,
    s2eintinf_simplified_image,
    name_simplified_image]


def simplified_image(node, level, acc):
    """ Simplified node image. """
    result = False
    if SIMPLIFY:
        for method in SIMPLIFIED_IMAGE_METHODS:
            result = result or method(node, level, acc)
    return result


# Main
# ============================================================================

def is_root_node(node):
    """ True if node is a D2/S2/C3 node followed by end. """
    result = (
        node is not None and
        node.kind == KIND.D2S2C3 and
        node.end == FOLLOWED_BY.END)
    return result


def pretty_printed(string):
    """ String with Postiats expressions folded and re‑printed below. """
    fold_count = 0
    result = ""
    trees = []
    string = String(string)

    def append_folded_ref():
        """ Append a “[n]” in place of the parsed expression. """
        nonlocal fold_count, string, result
        # pylint: disable=unused-variable
        fold_count += 1
        if not string.has_item() or string.item() != "]":
            result += "[%i]" % fold_count
        else:
            result += "%i" % fold_count

    def append_folded_ref_target(lines):
        """ Append an “[n]:” before a pretty printed expression. """
        nonlocal fold_count, result
        # pylint: disable=unused-variable
        fold_count += 1
        result += "[%i]: " % fold_count
        if len(lines) > 1:
            result += "\n"

    while string.has_item():
        string.push()
        tree = parse_node(string)  # The magic is here
        if is_root_node(tree):
            string.unpush()
            append_folded_ref()
            trees.append(tree)
        else:
            string.pop()
            result += string.item()
            string.consume()

    result += "\n"
    fold_count = 0
    for tree in trees:
        lines = node_lines_image(tree)  # The magic is here
        lines = format_lines(lines)
        append_folded_ref_target(lines)
        result += lines_image(lines)
    return result


def main():
    """ Invoked by `../pats-filter`. """
    my_name = os.path.split(sys.argv[0])[1]
    if len(sys.argv) != 1:
        print("%s takes no parameter, just input." % my_name, file=sys.stderr)
        exit(1)
    message_before = False  # For managing additional blank lines.
    for line in sys.stdin:
        line = line.strip()
        if is_message_with_location(line):
            message = parse_message_with_location(line)
        elif is_showtype_message(line):
            message = parse_showtype_message(line)
        else:
            message = None
        if message:
            text = pretty_printed(message.text)
            location = message.location
            output = "%s: %s" % (
                locations.ide_formated(location, LOCATION_WITH_COLUMN),
                text)
            print()  # Separate messages with blank lines.
            print(output, end="")
            message_before = True
        else:
            output = pretty_printed(line)
            if message_before:
                print()  # Separate from messages with blank lines.
            print(output, end="")
            message_before = False
