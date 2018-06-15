""" Collect declarations. """

import sys

from collections import namedtuple

from . import constants as c
from . import jsonized
from . import tags as t


# Data
# ============================================================================

Def = namedtuple("Def", [
    "stamp_key",
    "stamp",
    "name",
    "sort",
    "type",
    "conss"])
# The stamp key is used to designate the map, it’s more straighforward. Since
# map is a Python built‑in, the map variables will be named table. Sort, type
# and conss may be None. Conss is a list of constructors (many cons).

Declaration = namedtuple("Declaration", [
    "loc",
    "name",
    "construct",
    "sort",
    "type"])


DEFS = {
    t.D2CON_STAMP: {},  # From d2conmap.
    t.D2CST_STAMP: {},  # From d2cstmap.
    t.D2VAR_STAMP: {},  # From d2varmap.
    t.S2CST_STAMP: {},  # From s2cstmap.
    t.S2VAR_STAMP: {}}  # From s2varmap.

BASE_SORTS = set()
STATIC_CONSTANTS = {}
DECLARATIONS = []
STALOADED = set()


# Methods
# ----------------------------------------------------------------------------

def clear():
    """ Clear generated data. """
    for table in DEFS.values():
        table.clear()
    BASE_SORTS.clear()
    STATIC_CONSTANTS.clear()
    DECLARATIONS.clear()
    STALOADED.clear()


def add_def(den):
    """ Add `den` in `DEFS`. """
    table = DEFS[den.stamp_key]
    if den.stamp in table:
        error("Duplicated stamp: %s." % repr(den.stamp))
    table[den.stamp] = den


def get_def(stamp_key, stamp):
    """ Entry in `DEFS`; may be `None` if missing stamp. """
    table = DEFS[stamp_key]
    return table[stamp] if stamp in table else None


def update_def(den, new_def):
    """ Substitue `new_den` for `den` in `DEFS`. """
    table = DEFS[den.stamp_key]
    if den.stamp not in table:
        error("Missing stamp: %s." % repr(den.stamp))
    table[den.stamp] = new_def


def collect_static_constants():
    """ Fillup `STATIC_CONSTANTS` from previously collected defs.

    `DEFS` needs to be populated, although it may still be empty after that.

    """
    for den in DEFS[t.S2CST_STAMP].values():
        STATIC_CONSTANTS[den.name] = den.sort


def add_declaration(
        stamp_key,
        stamp,
        loc,
        construct,
        name=None,
        sort=None,
        typ=None):
    """ Add a declaration possibly complented by a referred def.

    `DEFS` needs to be populated, since `stamp_key` and `stamp` are used
    as a reference in `DEFS`.

    """
    den = get_def(stamp_key, stamp)
    if den is not None:
        declaration = Declaration(
            loc=loc,
            name=name or den.name,
            construct=construct,
            sort=sort or den.sort,
            type=typ or den.type)
        DECLARATIONS.append(declaration)
    else:
        # error("Missing stamp: %i" % stamp)
        # #include is buggy with stamps.
        pass


def add_staloaded(path):
    """ Register a new source reference encoutered in a file. """
    # Invoked from handle_d2cstaload.
    STALOADED.add(path)


# Helpers
# ============================================================================

def perror(message):
    """ Shorthand to print to `stderr`. """
    print(message, file=sys.stderr)


def error(message):
    """ `perror` and `sys.exit(1)`. """
    perror(message)
    sys.exit(1)


# Base sorts
# ============================================================================

def collect_base_sorts(node):
    """ Fillup `BASE_SORTS`. """
    if isinstance(node, dict):
        if t.S2RTBAS in node:
            BASE_SORTS.add(node[t.S2RTBAS][0])
        else:
            for sub_node in node.values():
                collect_base_sorts(sub_node)
    elif isinstance(node, list):
        for sub_node in node:
            collect_base_sorts(sub_node)


# Maps (x2xxxmap)
# ============================================================================

# General
# ----------------------------------------------------------------------------

def extract_def(entry, stamp_key, name_key, type_sort):
    """ Extract a `Def` from a JSON node given keys. """
    # type_sort is a function.
    (typ, sort, conss) = type_sort(entry)
    stamp = entry[stamp_key]
    name = entry[name_key]
    return Def(stamp_key, stamp, name, sort, typ, conss)


def extract_and_add_defs(
        root_node,
        section_key,
        stamp_key,
        name_key,
        type_sort):
    """ Extract and add defs iteratively from root node. """
    # type_sort is a function.
    for entry in root_node[section_key]:
        den = extract_def(entry, stamp_key, name_key, type_sort)
        add_def(den)


def collect_defs(root_node):
    """ Collect defs: their stamp, name, sort and type. """

    extract_and_add_defs(
        root_node=root_node,
        section_key=t.D2CONMAP,
        stamp_key=t.D2CON_STAMP,
        name_key=t.D2CON_SYM,
        type_sort=d2con_type_sort)

    extract_and_add_defs(
        root_node=root_node,
        section_key=t.D2CSTMAP,
        stamp_key=t.D2CST_STAMP,
        name_key=t.D2CST_SYM,
        type_sort=d2cst_type_sort)

    extract_and_add_defs(
        root_node=root_node,
        section_key=t.D2VARMAP,
        stamp_key=t.D2VAR_STAMP,
        name_key=t.D2VAR_SYM,
        type_sort=d2var_type_sort)

    extract_and_add_defs(
        root_node=root_node,
        section_key=t.S2CSTMAP,
        stamp_key=t.S2CST_STAMP,
        name_key=t.S2CST_SYM,
        type_sort=s2cst_type_sort)

    extract_and_add_defs(
        root_node=root_node,
        section_key=t.S2VARMAP,
        stamp_key=t.S2VAR_STAMP,
        name_key=t.S2VAR_SYM,
        type_sort=s2var_type_sort)


# Specific (x2xxx_type_sort)
# ----------------------------------------------------------------------------

def d2con_type_sort(entry):
    """ Sort and type from d2conmap entry."""
    type_node = entry[t.D2CON_TYPE]
    return (type_node[t.S2EXP_NODE], type_node[t.S2EXP_SRT], None)


def d2cst_type_sort(entry):
    """ Sort and type from d2cstmap entry."""
    type_node = entry[t.D2CST_TYPE]
    return (type_node[t.S2EXP_NODE], type_node[t.S2EXP_SRT], None)


def d2var_type_sort(_entry):
    """ `(None, None, None)` from d2varmap entry."""
    # Sort and type may be provided later in a D2Cvardecs.
    return (None, None, None)


def s2cst_type_sort(entry):
    """ Sort and constructors list from s2cstmap entry."""
    # Static constant has a sort, no a type.
    cond_cons = entry[t.S2CST_DCONLST]
    conss = cond_cons[0] if cond_cons else None
    return (None, entry[t.S2CST_SRT], conss)


def s2var_type_sort(entry):
    """ Sort from s2varmap entry."""
    return (None, entry[t.S2VAR_SRT], None)


# Declarations
# ============================================================================

# General
# ----------------------------------------------------------------------------

def collect_declarations(root_node):
    """ Collect declarations. """
    # Also used by handle_d2cinclude.
    for entry in root_node:
        loc = entry[t.D2ECL_LOC]
        node = entry[t.D2ECL_NODE]
        dispatch_declaration(loc, node)


def collect_top_level_declarations(root_node):
    """ Collect declarations. """
    collect_declarations(root_node[t.D2ECLIST])


def dispatch_declaration(loc, wrapper_node):
    """ Dispatch by “D2Cxxx”. """
    keys = list(wrapper_node.keys())
    if len(keys) != 1:
        error("Broken “d2ecl_node”")
    discriminant = keys[0]
    node = wrapper_node[discriminant]
    if discriminant not in DISPATCH_TABLE:
        error("Unknon D2Cxxx: %s" % discriminant)
    DISPATCH_TABLE[discriminant](loc, node)
    # The dispatch table is defined later, after each handler is defined.


# Specific
# ----------------------------------------------------------------------------

def complete_var_def(stamp_key, stamp, sort, typ):
    """ Workaround lack of type information in d2varmap. """
    assert stamp_key == t.D2VAR_STAMP
    den = get_def(stamp_key, stamp)
    assert den is not None
    new_def = Def(
        stamp_key=den.stamp_key,
        stamp=den.stamp,
        name=den.name,
        sort=sort,
        type=typ,
        conss=den.conss)
    update_def(den, new_def)


def handle_d2cdatdecs(loc, node):
    """ Handle a D2Cdatdecs. """
    # The loc argument is that of the keyword, not of the name, and there may
    # be multiple data construction for a say datatype keyword, as in datatype
    # T and U and V. Unfortunately, we can’t have the loc of the name, which
    # would be better.
    construct = ["static", "data"]
    construct_tag = node[0]
    if construct_tag == c.DATATYPE:
        construct.append("datatype")
    elif construct_tag == c.DATAVIEWTYPE:
        construct.append("dataviewtype")
    elif construct_tag == c.DATAPROP:
        construct.append("dataprop")
    elif construct_tag == c.DATAVIEW:
        construct.append("dataview")
    else:
        error("Unknown data construction: %i" % construct_tag)
    for entry in node[1]:
        stamp_key = t.S2CST_STAMP
        stamp = entry[stamp_key]
        add_declaration(
            stamp_key=stamp_key,
            stamp=stamp,
            loc=loc,
            construct=construct)
        # Sort in referred def, but no type.
        den = get_def(stamp_key, stamp)
        if den is not None:
            conss = den.conss
            if conss is not None:
                construct = construct.copy()
                construct[0] = "dynamic"  # Constructors not in the static.
                construct[1] = "constructor"
                stamp_key = t.D2CON_STAMP
                for cons in conss:
                    stamp = cons[stamp_key]
                    add_declaration(
                        stamp_key=stamp_key,
                        stamp=stamp,
                        loc=loc,
                        construct=construct)


def handle_d2cdcstdecs(loc, node):
    """ Handle a D2Cdcstdecs. """
    # The loc argument is that of the keyword, not of the name, and there may
    # be multiple constant construction for a say val keyword, as in val a and
    # b. Unfortunately, we can’t have the loc of the name, which would be
    # better.
    construct = ["dynamic", "constant"]
    construct_tag = node[1]
    if construct_tag == c.DCKCASTFN:
        construct.append("castfn")
    elif construct_tag == c.DCKFUN:
        construct.append("fun")
    elif construct_tag == c.DCKPRAXI:
        construct.append("praxi")
    elif construct_tag == c.DCKPRFUN:
        construct.append("prfun")
    elif construct_tag == c.DCKVAL:
        construct.append("val")
    else:
        error("Unknown constant construction: %s" % construct_tag)
    for entry in node[2]:
        stamp_key = t.D2CST_STAMP
        stamp = entry[stamp_key]
        add_declaration(
            stamp_key=stamp_key,
            stamp=stamp,
            loc=loc,
            construct=construct)
        # Type and sort informations are in the referred def.


def handle_d2cexndecs(loc, node):
    """ Handle a D2Cexndecs. """
    # The loc argument is that of the keyword, not of the name, but there
    # is a single name per exception construct.
    construct = ["dynamic", "constructor"]  # Exception is a () -> type.
    construct.append("exception")
    for item in node[0]:
        stamp_key = t.D2CON_STAMP
        stamp = item[stamp_key]
        add_declaration(
            stamp_key=stamp_key,
            stamp=stamp,
            loc=loc,
            construct=construct)
        # Type and sort informations are in the referred def.


def handle_d2cextcode(_loc, _node):
    """ Handle a D2Cextcode. """
    # Not a declaration.
    pass


def handle_d2cextvar(_loc, _node):
    """ Handle a D2Cextvar. """
    # No stamp and not a declaration anyway, rather an assignment.
    pass


def handle_d2cfundecs(_loc, node):
    """ Handle a D2Cfundecs. """
    # The _loc argument is that of the keyword, not of the name, and there may
    # be multiple functions for a say fun keyword, as in fun x and y and z.
    # Luckyly, we can have the loc of the name, which is better, so the one
    # passed is ignored.
    construct = ["dynamic", "function"]
    construct_tag = node[0]
    if construct_tag == c.FK_FN:
        construct.append("fn")
    elif construct_tag == c.FK_FNX:
        construct.append("fnx")
    elif construct_tag == c.FK_FUN:
        construct.append("fun")
    elif construct_tag == c.FK_PRFN:
        construct.append("prfn")
    elif construct_tag == c.FK_PRFUN:
        construct.append("prfun")
    else:
        error("Unknown function construction: %s" % construct_tag)
    for entry in node[2]:
        stamp_key = t.D2VAR_STAMP
        stamp = entry[t.F2UNDEC_VAR][stamp_key]
        loc = entry[t.F2UNDEC_LOC]
        add_declaration(
            stamp_key=stamp_key,
            stamp=stamp,
            loc=loc,
            construct=construct)
        # No type/sort informations, but could be derived, but too complicated
        # while easier to write a declaration.


def handle_d2cignored(_loc, _node):
    """ Handle a D2Cignored. """
    # Lost.
    pass


def handle_d2cimpdec(_loc, node):
    """ Handle a D2Cimpdec. """
    # The _loc argument is that of the keyword, not of the name. Luckyly, we
    # can have the loc of the name, which is better, so the one passed is
    # ignored.
    construct = ["dynamic", "implementation"]
    construct_tag = node[0]
    if construct_tag == c.IMPLEMENT:
        construct.append("implement")
    elif construct_tag == c.PRIMPLEMENT:
        construct.append("primplement")
    else:
        error("Unknown implementation construction: %i" % construct_tag)
    stamp_key = t.D2CST_STAMP
    stamp = node[1][t.I2MPDEC_CST][stamp_key]
    # The stamp id is the same as that of the extern function declaration.
    loc = node[1][t.I2MPDEC_LOC]
    add_declaration(
        stamp_key=stamp_key,
        stamp=stamp,
        loc=loc,
        construct=construct)
    # Type and sort informations are in the Def.


def handle_d2cinclude(_loc, node):
    """ Handle a D2Cinclude. """
    # Not a declaration.
    collect_declarations(node[1])


def handle_d2clist(_loc, _node):
    """ Handle a D2Clist. """
    # Not a declaration.
    pass


def handle_d2clocal(_loc, _node):
    """ Handle a D2C_local. """
    # Not a declaration.
    pass


def handle_d2cnone(_loc, _node):
    """ Handle a D2Cnone. """
    # Nothing.
    pass


def handle_d2coverload(loc, node):
    """ Handle a D2Coverload. """
    # The stamp (if there is one) is that of the overladed symbol, not of the
    # ouverloading one.
    construct = ["dynamic", "alias"]
    stamp_key = None
    stamp = None
    name = node[0]
    sub_node = node[2][0]  # There are never many, isn’t it?
    if t.D2ITMCST in sub_node:
        stamp_key = t.D2CST_STAMP
        stamp = sub_node[t.D2ITMCST][0][stamp_key]
    elif t.D2ITMVAR in sub_node:
        stamp_key = t.D2VAR_STAMP
        stamp = sub_node[t.D2ITMVAR][0][stamp_key]
    elif t.D2ITMIGNORED in sub_node:
        pass
    else:
        error("Unknow overload case")
    construct.append("overload")
    if stamp is not None:
        add_declaration(
            stamp_key=stamp_key,  # Of the overloaded entity.
            stamp=stamp,
            loc=loc,
            construct=construct,
            name=name)
        # Either type and sort from referred def, if D2ITMcst or none if
        # D2ITMvar.


def handle_d2cstacsts(loc, node):
    """ Handle a D2Cstacsts. """
    # The loc argument is that of the keyword, not of the name, and there may
    # be multiple constant constructions for a say abstype keyword, as in
    # abstype T = a and U = b. Unfortunately, we can’t have the loc of the
    # name, which would be better.
    construct = ["static", "constant"]
    if len(node) == 1:
        construct.append("stacst")
        declarations = node[0]
    else:
        construct_tag = node[0]
        if construct_tag == c.ABSTYPE:
            construct.append("abstype")
        elif construct_tag == c.ABST0YPE:
            construct.append("abst@ype")
        elif construct_tag == c.ABSVIEWTYPE:
            construct.append("absviewtype")
        elif construct_tag == c.ABSVIEWT0YPE:
            construct.append("absviewt@ype")
        elif construct_tag == c.ABSPROP:
            construct.append("absprop")
        elif construct_tag == c.ABSVIEW:
            construct.append("absview")
        else:
            error("Unknown static constant construct %i" % construct_tag)
        declarations = node[1]
    for declaration in declarations:
        stamp_key = t.S2CST_STAMP
        stamp = declaration[stamp_key]
        add_declaration(
            stamp_key=stamp_key,
            stamp=stamp,
            loc=loc,
            construct=construct)
        # Sort in the referred def but no type.


def handle_d2cstaload(_loc, node):
    """ Handle a D2Cstaload. """
    # Not a declaration, but record it.
    path = node[1]
    add_staloaded(path)


def handle_d2cvaldecs(_loc, node):
    """ Handle a D2Cvaldecs. """
    construct = ["dynamic", "value"]
    construct_tag = node[0]
    if construct_tag == c.VK_PRVAL:
        construct.append("prval")
    elif construct_tag == c.VK_VAL:
        construct.append("val")
    elif construct_tag == c.VK_VAL_NEG:
        construct.append("val-")
    elif construct_tag == c.VK_VAL_POS:
        construct.append("val+")
    else:
        error("Unknown function construction: %s" % construct)
    for item in node[1]:
        for (loc, var, typ, sort) in p2at_node_p2tvars(item[t.V2ALDEC_PAT]):
            stamp_key = t.D2VAR_STAMP
            stamp = var[0][stamp_key]
            add_declaration(
                stamp_key=stamp_key,
                stamp=stamp,
                loc=loc,
                construct=construct,
                sort=sort,
                typ=typ)
            # Type and sort retrieved from pattern if annotated.
            if sort is not None:
                complete_var_def(stamp_key, stamp, sort, typ)
                # For possible later references.


def handle_d2cvardecs(_loc, node):
    """ Handle a D2Cvardecs. """
    for item in node[0]:
        loc = item[t.V2ARDEC_LOC]
        stamp_key = t.D2VAR_STAMP
        stamp = item[t.V2ARDEC_DVAR][stamp_key]
        typ = None
        sort = None
        type_node = item[t.V2ARDEC_TYPE]
        construct = ["dynamic", "value"]
        construct.append("var")
        if type_node:
            typ = type_node[0][t.S2EXP_NODE]
            sort = type_node[0][t.S2EXP_SRT]
        add_declaration(
            stamp_key=stamp_key,
            stamp=stamp,
            loc=loc,
            construct=construct,
            sort=sort,
            typ=typ)
        # Type and sort available if annotated.
        if sort is not None:
            complete_var_def(stamp_key, stamp, sort, typ)
            # For possible later references.
        construct = ["static", "value"]
        construct.append("var")
        stamp_key = t.S2VAR_STAMP
        stamp = item[t.V2ARDEC_SVAR][stamp_key]
        add_declaration(
            stamp_key=stamp_key,
            stamp=stamp,
            loc=loc,
            construct=construct)
        # Sort available in the referred def.


# Dispatch table
# ----------------------------------------------------------------------------

DISPATCH_TABLE = {
    t.D2CDATDECS: handle_d2cdatdecs,
    t.D2CDCSTDECS: handle_d2cdcstdecs,
    t.D2CEXNDECS: handle_d2cexndecs,
    t.D2CEXTCODE: handle_d2cextcode,
    t.D2CEXTVAR: handle_d2cextvar,
    t.D2CFUNDECS: handle_d2cfundecs,
    t.D2CIGNORED: handle_d2cignored,
    t.D2CIMPDEC: handle_d2cimpdec,
    t.D2CINCLUDE: handle_d2cinclude,
    t.D2CLIST: handle_d2clist,
    t.D2CLOCAL: handle_d2clocal,
    t.D2CNONE: handle_d2cnone,
    t.D2COVERLOAD: handle_d2coverload,
    t.D2CSTACSTS: handle_d2cstacsts,
    t.D2CSTALOAD: handle_d2cstaload,
    t.D2CVALDECS: handle_d2cvaldecs,
    t.D2CVARDECS: handle_d2cvardecs}


# Inner nodes
# ============================================================================

def p2at_node_p2tvars(node, type_sort=None):
    """ Yield variables from pattern. """
    # Node is a {p2at_loc, p2at_node}
    # Passed type_sort is an initial value.
    loc = node[t.P2AT_LOC]
    node = node[t.P2AT_NODE]
    if t.P2TANN in node:
        if not type_sort:
            type_sort = node[t.P2TANN][1]
        yield from p2at_node_p2tvars(node[t.P2TANN][0], type_sort)
    elif t.P2TREC in node:
        nodes = node[t.P2TREC][2]
        for item in nodes:
            yield from p2at_node_p2tvars(item[t.LABP2ATNORM][1], type_sort)
    elif t.P2TVAR in node:
        node = node[t.P2TVAR]
        typ = None
        sort = None
        if type_sort:
            typ = type_sort[t.S2EXP_NODE]
            sort = type_sort[t.S2EXP_SRT]
        yield (loc, node, typ, sort)
    else:
        # No pattern variables here.
        pass


# Main
# ============================================================================

def handle_source_file(path):
    """ Collect declarations and others for one source file.

    Clear before starting to collect.

    The path is that of an ATS source file, as the compiler would expect it.

    """
    root_node = jsonized.get_json(path)
    if root_node is None:
        error("Failed to evaluate %s" % path)
    clear()
    collect_base_sorts(root_node)
    collect_defs(root_node)
    collect_static_constants()  # From previously collected defs.
    collect_top_level_declarations(root_node)
