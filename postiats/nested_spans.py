# -*- mode:python3 -*-

""" Nested spans from text position.

From a point defined as a file name, line and column, get the list
of nested span from outer to innest span including the text position.

The stack of nested spans gives location in the corresponding file with
a readable name for the ATS2 constructs corresponding to the spans.

"""

from . import declarations
from . import jsonized
from . import locations
from . import tags as t


# Helpers
# ============================================================================

def get_loc(node, key):
    """ Parsed loc at node[key]. """
    loc_str = node[key]
    return locations.parse(loc_str)


def get_merged_locs(node, key):
    """ Parsed and merged locs at node. """
    path = None
    start_char = 0
    start_line = 0
    start_column = 0
    end_char = 0
    end_line = 0
    end_column = 0
    first = True
    for item in node:
        loc_str = item[key]
        loc = locations.parse(loc_str)
        if first:
            path = loc.path
            start_char = loc.start.char
            start_line = loc.start.line
            start_column = loc.start.column
            end_char = loc.end.char
            end_line = loc.end.line
            end_column = loc.end.column
            first = False
        elif loc.start.char < start_char:
            start_char = loc.start.char
            start_line = loc.start.line
            start_column = loc.start.column
        elif loc.end.char > end_char:
            end_char = loc.end.char
            end_line = loc.end.line
            end_column = loc.end.column
    start = locations.Position(
        char=start_char,
        line=start_line,
        column=start_column)
    end = locations.Position(
        char=end_char,
        line=end_line,
        column=end_column)
    return locations.Location(path=path, start=start, end=end)


def single_key(node):
    """ Single key of node dict. """
    count = 0
    key = None  # Avoid pylint warning
    for key in node:
        count += 1
    assert count == 1
    return key


def in_loc(line, col, loc):
    """ If line‑col is in loc. """
    result = False
    if loc.start.line <= line and line <= loc.end.line:
        result = True
        if loc.start.line == line:
            result = result and (col >= loc.start.column)
        if loc.end.line == line:
            result = result and (col < loc.end.column)
    return result


# Common
# ============================================================================

def d2exp_loc_node(node):
    """ Next loc and node from {d2exp_loc, d2exp_node}. """
    loc = get_loc(node, t.D2EXP_LOC)
    sub_node = node[t.D2EXP_NODE]
    key = single_key(sub_node)
    next_node = sub_node[key]
    yield (loc, next_node, key)


def p2at_loc_node(node):
    """ Next locs and nodes from {p2at_loc, p2at_node}. """
    loc = get_loc(node, t.P2AT_LOC)
    sub_node = node[t.P2AT_NODE]
    key = single_key(sub_node)
    next_node = sub_node[key]
    yield (loc, next_node, key)


# Root
# ============================================================================

def d2eclist_locs_nodes(node):
    """ Next locs and nodes. """
    for item in node:
        loc = get_loc(item, t.D2ECL_LOC)
        sub_node = item[t.D2ECL_NODE]
        key = single_key(sub_node)
        next_node = sub_node[key]
        yield (loc, next_node, key)


# Specific
# ============================================================================

def c2lau_pat_locs_nodes(node):
    """ Next locs and nodes. """
    for item in node:
        yield from p2at_loc_node(item)


def d2cfundecs_locs_nodes(node):
    """ Next locs and nodes. """
    sub_node = node[2]
    for item in sub_node:
        loc = get_loc(item, t.F2UNDEC_LOC)
        key = t.F2UNDEC_DEF
        next_node = item[key]
        yield (loc, next_node, key)


def d2cimpdec_loc_node(node):
    """ Next locs and nodes. """
    sub_node = node[1]
    loc = get_loc(sub_node, t.I2MPDEC_LOC)
    key = t.I2MPDEC_DEF
    next_node = sub_node[key]
    yield (loc, next_node, key)


def d2clocal_locs_nodes(node):
    """ Next locs and nodes. """
    sub_node = node[0]
    yield from d2eclist_locs_nodes(sub_node)
    sub_node = node[1]
    yield from d2eclist_locs_nodes(sub_node)


def d2cvaldecs_locs_nodes(node):
    """ Next locs and nodes. """
    for item in node[1]:

        sub_node = item[t.V2ALDEC_PAT]
        yield from p2at_loc_node(sub_node)

        sub_node = item[t.V2ALDEC_DEF]
        yield from d2exp_loc_node(sub_node)


def d2cvardecs_locs_nodes(node):
    """ Next locs and nodes. """
    sub_node = node[0]
    for item in sub_node:
        loc = get_loc(item, t.V2ARDEC_LOC)
        key = t.V2ARDEC_INIT
        next_node = item[key]
        yield (loc, next_node, key)


def d2eann_funclo_loc_node(node):
    """ Next locs and nodes. """
    sub_node = node[0]
    yield from d2exp_loc_node(sub_node)


def d2eann_seff_dyn_loc_node(node):
    """ Next locs and nodes. """
    sub_node = node[0]
    yield from d2exp_loc_node(sub_node)


def d2eann_type_loc_node(node):
    """ Next locs and nodes. """
    sub_node = node[0]
    yield from d2exp_loc_node(sub_node)


def d2eapplst_locs_nodes(node):
    """ Next locs and nodes. """
    sub_node = node[0]
    yield from d2exp_loc_node(sub_node)
    for item in node[1]:
        # We have no loc, retrieve it from inner nodes.
        key = single_key(item)
        assert key in {t.D2EXPARGDYN, t.D2EXPARGSTA}
        if key == t.D2EXPARGDYN:
            next_node = item[key]
            loc = get_merged_locs(next_node[2], t.D2EXP_LOC)
            yield (loc, next_node, key)


def d2eassgn_locs_nodes(node):
    """ Next locs and nodes. """
    sub_node = node[0]
    yield from d2exp_loc_node(sub_node)
    sub_node = node[1]
    yield from d2exp_loc_node(sub_node)


def d2ecasehead_locs_nodes(node):
    """ Next locs and nodes. """
    sub_node = node[2]
    for item in sub_node:
        yield from d2exp_loc_node(item)
    sub_node = node[3]
    for item in sub_node:
        # loc = get_loc(item, t.C2LAU_LOC)
        # C2LAU_LOC spans both guard and body, one would prevent to match the
        # other, so locs are retrieved from inner nodes.
        key = t.C2LAU_BODY
        next_node = item[key]
        loc = get_loc(next_node, t.D2EXP_LOC)
        yield(loc, next_node, key)
        key = t.C2LAU_PAT
        next_node = item[key]
        loc = get_merged_locs(next_node, t.P2AT_LOC)
        yield(loc, next_node, key)


def d2ederef_loc_node(node):
    """ Next locs and nodes. """
    sub_node = node[1]
    yield from d2exp_loc_node(sub_node)


def d2eifhead_locs_nodes(node):
    """ Next locs and nodes. """
    sub_node = node[1]
    yield from d2exp_loc_node(sub_node)
    sub_node = node[2]
    yield from d2exp_loc_node(sub_node)
    sub_node = node[3]
    if sub_node:
        sub_node = sub_node[0]
        yield from d2exp_loc_node(sub_node)


def d2elam_dyn_locs_nodes(node):
    """ Next locs and nodes. """
    sub_node = node[2]
    for item in sub_node:
        yield from p2at_loc_node(item)
    sub_node = node[3]
    yield from d2exp_loc_node(sub_node)


def d2elam_met_loc_node(node):
    """ Next locs and nodes. """
    sub_node = node[1]
    yield from d2exp_loc_node(sub_node)


def d2elam_sta_loc_node(node):
    """ Next locs and nodes. """
    sub_node = node[2]
    yield from d2exp_loc_node(sub_node)


def d2elet_locs_nodes(node):
    """ Next locs and nodes. """
    sub_node = node[0]
    yield from d2eclist_locs_nodes(sub_node)
    sub_node = node[1]
    yield from d2exp_loc_node(sub_node)


def d2elist_locs_nodes(node):
    """ Next locs and nodes. """
    sub_node = node[1]
    for item in sub_node:
        yield from d2exp_loc_node(item)


def d2eseq_locs_nodes(node):
    """ Next locs and nodes. """
    sub_node = node[0]
    for item in sub_node:
        yield from d2exp_loc_node(item)


def d2esing_loc_node(node):
    """ Next locs and nodes. """
    sub_node = node[0]
    yield from d2exp_loc_node(sub_node)


def d2expargdyn_locs_nodes(node):
    """ Next locs and nodes. """
    for item in node[2]:
        yield from d2exp_loc_node(item)


def p2tann_loc_node(node):
    """ Next locs and nodes. """
    sub_node = node[0]
    yield from p2at_loc_node(sub_node)


def p2tcon_locs_nodes(node):
    """ Next locs and nodes. """
    sub_node = node[5]
    for item in sub_node:
        yield from p2at_loc_node(item)


def p2trec_locs_nodes(node):
    """ Next locs and nodes. """
    sub_node = node[2]
    for item in sub_node:
        sub_item = item[t.LABP2ATNORM][1]
        yield from p2at_loc_node(sub_item)


def v2ardec_init_loc_node(node):
    """ Next locs and nodes. """
    sub_node = node[0]
    yield from d2exp_loc_node(sub_node)


LOCS_NODES = {
    t.C2LAU_BODY: d2exp_loc_node,
    t.C2LAU_PAT: c2lau_pat_locs_nodes,
    t.D2CFUNDECS: d2cfundecs_locs_nodes,
    t.D2CIMPDEC: d2cimpdec_loc_node,
    t.D2CLOCAL: d2clocal_locs_nodes,
    t.D2CVALDECS: d2cvaldecs_locs_nodes,
    t.D2CVARDECS: d2cvardecs_locs_nodes,
    t.D2EANN_FUNCLO: d2eann_funclo_loc_node,
    t.D2EANN_SEFF: d2eann_seff_dyn_loc_node,
    t.D2EANN_TYPE: d2eann_type_loc_node,
    t.D2EAPPLST: d2eapplst_locs_nodes,
    t.D2EASSGN: d2eassgn_locs_nodes,
    t.D2ECASEHEAD: d2ecasehead_locs_nodes,
    t.D2EDEREF: d2ederef_loc_node,
    t.D2EIFHEAD: d2eifhead_locs_nodes,
    t.D2ELAM_DYN: d2elam_dyn_locs_nodes,
    t.D2ELAM_MET: d2elam_met_loc_node,
    t.D2ELAM_STA: d2elam_sta_loc_node,
    t.D2ELET: d2elet_locs_nodes,
    t.D2ELIST: d2elist_locs_nodes,
    t.D2ESEQ: d2eseq_locs_nodes,
    t.D2ESING: d2esing_loc_node,
    t.D2EXPARGDYN: d2expargdyn_locs_nodes,
    t.F2UNDEC_DEF: d2exp_loc_node,
    t.I2MPDEC_DEF: d2exp_loc_node,
    t.P2TANN: p2tann_loc_node,
    t.P2TCON: p2tcon_locs_nodes,
    t.P2TREC: p2trec_locs_nodes,
    t.V2ARDEC_INIT: v2ardec_init_loc_node,
}


# Leafs (no loc inside)
# ============================================================================

LEAFS = {
    t.D2CDATDECS,
    t.D2CDCSTDECS,
    t.D2CEXNDECS,
    t.D2CNONE,
    t.D2COVERLOAD,
    t.D2CSTACSTS,
    t.D2ECST,
    t.D2EEMPTY,
    t.D2EI0NT,
    t.D2EIGNORED,
    t.D2ESYM,
    t.D2EVAR,
    t.P2TANY,
    t.P2TBOOL,
    t.P2TEMPTY,
    t.P2TVAR,
}


# Readable labels
# ============================================================================

LABELS = {
    t.C2LAU_BODY: "matching clause body",
    t.C2LAU_PAT: "matching clause guard",
    t.D2CDATDECS: "dataxxx declaration(s)",
    t.D2CDCSTDECS: "constant declaration(s) (dynamic)",
    t.D2CEXNDECS: "exception declaration",
    t.D2CFUNDECS: "function declaration(s)",
    t.D2CIMPDEC: "impementation declaration",
    t.D2CLOCAL: "local declaration(s)",
    t.D2CNONE: "erased (by pasopt)",
    t.D2COVERLOAD: "overload definition",
    t.D2CSTACSTS: "absxxx declaration(s)",
    t.D2CVALDECS: "value declaration(s)",
    t.D2CVARDECS: "variable declaration(s)",
    t.D2EANN_FUNCLO: "closure annotation",
    t.D2EANN_SEFF: "effect(s) annotation",
    t.D2EANN_TYPE: "type annotation",
    t.D2EAPPLST: "function application",
    t.D2EASSGN: "assignment",
    t.D2ECASEHEAD: "case expression (dynamic)",
    t.D2ECST: "constant (dynamic)",
    t.D2EDEREF: "dereference",
    t.D2EEMPTY: "void",
    t.D2EI0NT: "integer",
    t.D2EIFHEAD: "conditional (dynamic)",
    t.D2EIGNORED: "ignored (by patsopt)",
    t.D2ELAM_DYN: "lambda (dynamic, boxed)",
    t.D2ELAM_MET: "lambda with termination metric",
    t.D2ELAM_STA: "lambda (static)",
    t.D2ELET: "let expression",
    t.D2ELIST: "tuple",
    t.D2ESEQ: "sequence of expressions",
    t.D2ESING: "singleton",
    t.D2ESYM: "overloaded symbol (dynamic)",
    t.D2EVAR: "variable (dynamic)",
    t.D2EXPARGDYN: "dynamic argument(s)",
    t.F2UNDEC_DEF: "function definition",
    t.I2MPDEC_DEF: "implementation definition",
    t.P2TANN: "pattern element (annotated)",
    t.P2TANY: "wildcard pattern",
    t.P2TBOOL: "boolean",
    t.P2TCON: "constructor application",
    t.P2TEMPTY: "empty pattern",
    t.P2TREC: "pattern record",
    t.P2TVAR: "pattern variable",
    t.V2ARDEC_INIT: "variable initialisation",
}


# Sanity check
# ============================================================================

# LOCS_NODES and LEAFS don’t intersects
assert all(k not in LOCS_NODES for k in LEAFS)

# LABELS covers LOCS_NODES and LEAFS
assert all(k in LABELS for k in LOCS_NODES)
assert all(k in LABELS for k in LEAFS)


# Main
# ============================================================================

def append(result, loc, key):
    """ Append to result. """
    if key in LABELS:
        label = LABELS[key]
        text = locations.ide_formated(loc) + ": " + label
        result.insert(0, text)


def main(path, line, col):
    """ Main. """

    result = []

    root_node = jsonized.get_json(path)
    if root_node is None:
        declarations.error("Failed to evaluate %s" % path)
    node = root_node["d2eclist"]
    locs_nodes = d2eclist_locs_nodes
    found = True
    while found and locs_nodes:
        found = False
        for (loc, next_node, key) in locs_nodes(node):
            if in_loc(line, col, loc):
                found = True
                node = next_node
                append(result, loc, key)
                if key in LOCS_NODES:
                    locs_nodes = LOCS_NODES[key]
                elif key in LEAFS:
                    locs_nodes = None
                else:
                    result.insert(0, "** Unsupported %s **" % key)
                    locs_nodes = None
                break
        if not found:
            pass

    return result
