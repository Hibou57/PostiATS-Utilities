""" Collect declarations. """

import sys

from collections import namedtuple

from postiats import jsonized


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
    "d2con_stamp": {},  # From d2conmap.
    "d2cst_stamp": {},  # From d2cstmap.
    "d2var_stamp": {},  # From d2varmap.
    "s2cst_stamp": {},  # From s2cstmap.
    "s2var_stamp": {}}  # From s2varmap.

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
    for den in DEFS["s2cst_stamp"].values():
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
        if "S2RTbas" in node:
            BASE_SORTS.add(node["S2RTbas"][0])
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
        section_key="d2conmap",
        stamp_key="d2con_stamp",
        name_key="d2con_sym",
        type_sort=d2con_type_sort)

    extract_and_add_defs(
        root_node=root_node,
        section_key="d2cstmap",
        stamp_key="d2cst_stamp",
        name_key="d2cst_sym",
        type_sort=d2cst_type_sort)

    extract_and_add_defs(
        root_node=root_node,
        section_key="d2varmap",
        stamp_key="d2var_stamp",
        name_key="d2var_sym",
        type_sort=d2var_type_sort)

    extract_and_add_defs(
        root_node=root_node,
        section_key="s2cstmap",
        stamp_key="s2cst_stamp",
        name_key="s2cst_sym",
        type_sort=s2cst_type_sort)

    extract_and_add_defs(
        root_node=root_node,
        section_key="s2varmap",
        stamp_key="s2var_stamp",
        name_key="s2var_sym",
        type_sort=s2var_type_sort)


# Specific (x2xxx_type_sort)
# ----------------------------------------------------------------------------

def d2con_type_sort(entry):
    """ Sort and type from d2conmap entry."""
    type_node = entry["d2con_type"]
    return (type_node["s2exp_node"], type_node["s2exp_srt"], None)


def d2cst_type_sort(entry):
    """ Sort and type from d2cstmap entry."""
    type_node = entry["d2cst_type"]
    return (type_node["s2exp_node"], type_node["s2exp_srt"], None)


def d2var_type_sort(_entry):
    """ `(None, None, None)` from d2varmap entry."""
    # Sort and type may be provided later in a D2Cvardecs.
    return (None, None, None)


def s2cst_type_sort(entry):
    """ Sort and constructors list from s2cstmap entry."""
    # Static constant has a sort, no a type.
    cond_cons = entry["s2cst_dconlst"]
    conss = cond_cons[0] if cond_cons else None
    return (None, entry["s2cst_srt"], conss)


def s2var_type_sort(entry):
    """ Sort from s2varmap entry."""
    return (None, entry["s2var_srt"], None)


# Declarations
# ============================================================================

# General
# ----------------------------------------------------------------------------

def collect_declarations(root_node):
    """ Collect declarations. """
    # Also used by handle_d2cinclude.
    for entry in root_node:
        loc = entry["d2ecl_loc"]
        node = entry["d2ecl_node"]
        dispatch_declaration(loc, node)


def collect_top_level_declarations(root_node):
    """ Collect declarations. """
    collect_declarations(root_node["d2eclist"])


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
    assert stamp_key == "d2var_stamp"
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
    if construct_tag == 0:
        construct.append("datatype")
    elif construct_tag == 2:
        construct.append("dataviewtype")
    elif construct_tag == 5:
        construct.append("dataprop")
    elif construct_tag == 7:
        construct.append("dataview")
    else:
        error("Unknown data construction: %i" % construct_tag)
    for entry in node[1]:
        stamp_key = "s2cst_stamp"
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
                stamp_key = "d2con_stamp"
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
    if construct_tag == "DCKcastfn":
        construct.append("castfn")
    elif construct_tag == "DCKfun":
        construct.append("fun")
    elif construct_tag == "DCKpraxi":
        construct.append("praxi")
    elif construct_tag == "DCKprfun":
        construct.append("prfun")
    elif construct_tag == "DCKval":
        construct.append("val")
    else:
        error("Unknown constant construction: %s" % construct_tag)
    for entry in node[2]:
        stamp_key = "d2cst_stamp"
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
        stamp_key = "d2con_stamp"
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
    # No stamp.
    pass


def handle_d2cfundecs(_loc, node):
    """ Handle a D2Cfundecs. """
    # The _loc argument is that of the keyword, not of the name, and there may
    # be multiple functions for a say fun keyword, as in fun x and y and z.
    # Luckyly, we can have the loc of the name, which is better, so the one
    # passed is ignored.
    construct = ["dynamic", "function"]
    construct_tag = node[0]
    if construct_tag == "FK_fn":
        construct.append("fn")
    elif construct_tag == "FK_fnx":
        construct.append("fnx")
    elif construct_tag == "FK_fun":
        construct.append("fun")
    elif construct_tag == "FK_prfn":
        construct.append("prfn")
    elif construct_tag == "FK_prfun":
        construct.append("prfun")
    else:
        error("Unknown function construction: %s" % construct_tag)
    for entry in node[2]:
        stamp_key = "d2var_stamp"
        stamp = entry["f2undec_var"][stamp_key]
        loc = entry["f2undec_loc"]
        add_declaration(
            stamp_key=stamp_key,
            stamp=stamp,
            loc=loc,
            construct=construct)
        # No type/sort informations, but could be derived.


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
    if construct_tag == 1:
        construct.append("implement")
    elif construct_tag == -1:
        construct.append("primplement")
    else:
        error("Unknown implementation construction: %i" % construct_tag)
    stamp_key = "d2cst_stamp"
    stamp = node[1]["i2mpdec_cst"][stamp_key]
    # The stamp id is the same as that of the extern function declaration.
    loc = node[1]["i2mpdec_loc"]
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
    if "D2ITMcst" in sub_node:
        stamp_key = "d2cst_stamp"
        stamp = sub_node["D2ITMcst"][0][stamp_key]
    elif "D2ITMvar" in sub_node:
        stamp_key = "d2var_stamp"
        stamp = sub_node["D2ITMvar"][0][stamp_key]
    elif "D2ITMignored" in sub_node:
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
        if construct_tag == 0:
            construct.append("abstype")
        elif construct_tag == 1:
            construct.append("abst@ype")
        elif construct_tag == 2:
            construct.append("absviewtype")
        elif construct_tag == 3:
            construct.append("absviewt@ype")
        elif construct_tag == 5:
            construct.append("absprop")
        elif construct_tag == 7:
            construct.append("absview")
        else:
            error("Unknown static constant construct %i" % construct_tag)
        declarations = node[1]
    for declaration in declarations:
        stamp_key = "s2cst_stamp"
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
    if construct_tag == "VK_prval":
        construct.append("prval")
    elif construct_tag == "VK_val":
        construct.append("val")
    elif construct_tag == "VK_val_neg":
        construct.append("val-")
    elif construct_tag == "VK_val_pos":
        construct.append("val+")
    else:
        error("Unknown function construction: %s" % construct)
    for item in node[1]:
        for (loc, var, typ, sort) in p2at_node_p2tvars(item["v2aldec_pat"]):
            stamp_key = "d2var_stamp"
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
        loc = item["v2ardec_loc"]
        stamp_key = "d2var_stamp"
        stamp = item["v2ardec_dvar"][stamp_key]
        typ = None
        sort = None
        type_node = item["v2ardec_type"]
        construct = ["dynamic", "value"]
        construct.append("var")
        if type_node:
            typ = type_node[0]["s2exp_node"]
            sort = type_node[0]["s2exp_srt"]
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
        stamp_key = "s2var_stamp"
        stamp = item["v2ardec_svar"][stamp_key]
        add_declaration(
            stamp_key=stamp_key,
            stamp=stamp,
            loc=loc,
            construct=construct)
        # Sort available in the referred def.


# Dispatch table
# ----------------------------------------------------------------------------

DISPATCH_TABLE = {
    "D2Cdatdecs": handle_d2cdatdecs,
    "D2Cdcstdecs": handle_d2cdcstdecs,
    "D2Cexndecs": handle_d2cexndecs,
    "D2Cextcode": handle_d2cextcode,
    "D2Cextvar": handle_d2cextvar,
    "D2Cfundecs": handle_d2cfundecs,
    "D2Cignored": handle_d2cignored,
    "D2Cimpdec": handle_d2cimpdec,
    "D2Cinclude": handle_d2cinclude,
    "D2Clist": handle_d2clist,
    "D2Clocal": handle_d2clocal,
    "D2Cnone": handle_d2cnone,
    "D2Coverload": handle_d2coverload,
    "D2Cstacsts": handle_d2cstacsts,
    "D2Cstaload": handle_d2cstaload,
    "D2Cvaldecs": handle_d2cvaldecs,
    "D2Cvardecs": handle_d2cvardecs}


# Inner nodes
# ============================================================================

def p2at_node_p2tvars(node, type_sort=None):
    """ Yield variables from pattern. """
    # Node is a {p2at_loc, p2at_node}
    # Passed type_sort is an initial value.
    loc = node["p2at_loc"]
    node = node["p2at_node"]
    if "P2Tann" in node:
        if not type_sort:
            type_sort = node["P2Tann"][1]
        yield from p2at_node_p2tvars(node["P2Tann"][0], type_sort)
    elif "P2Trec" in node:
        nodes = node["P2Trec"][2]
        for item in nodes:
            yield from p2at_node_p2tvars(item["LABP2ATnorm"][1], type_sort)
    elif "P2Tvar" in node:
        node = node["P2Tvar"]
        typ = None
        sort = None
        if type_sort:
            typ = type_sort["s2exp_node"]
            sort = type_sort["s2exp_srt"]
        yield (loc, node, typ, sort)
    else:
        # No pattern variables here.
        pass


# Image of type and sort
# ============================================================================

def sort_image(node, paren_if_fun=False):
    """ Image of s2xxx_srt and S2RTfun[0][n]. """
    # Node is a {S2RTbas}|{S2RTfun}
    if "S2RTbas" in node:
        result = node["S2RTbas"][0]
    elif "S2RTfun" in node:
        node = node["S2RTfun"]
        inputs = node[0]
        output = node[1]
        result = ""
        if inputs:
            if paren_if_fun:
                result += "("
            marny_args = len(inputs) > 1
            if marny_args:
                result += "("
            first = True
            for item in inputs:
                if not first:
                    result += ", "
                result += sort_image(item, paren_if_fun=not marny_args)
                first = False
            if marny_args:
                result += ")"
            elif first:
                result += "()"
            result += " -> "
            if paren_if_fun:
                result += ")"
        result += sort_image(output)
    else:
        error("Unknown sort expression")
    return result


def sta_sort_image(node, paren_if_fun=False):
    """ Sort image. """
    return sort_image(node, paren_if_fun)


def s2var_image(stamp):
    """ Static variable image. """
    if stamp in DEFS:
        den = DEFS["s2var_stamp"][stamp]
        return den.name + ": " + sort_image(den.sort)
    return "*ERROR*"


def s2ecst_image(node, for_type):
    """ Image of a S2Ecst, either as type or sort.

    Type or sort, depending on `for_type`.

    """
    stamp = node[0]["s2cst_stamp"]
    den = get_def("s2cst_stamp", stamp)
    if den is None:
        return "*ERROR*"
    if for_type:
        return den.name
    return sort_image(den.sort)


def s2evar_image(node, for_type):
    """ Image of a S2Evar, either as type or sort.

    Type or sort, depending on `for_type`.

    """
    stamp = node[0]["s2var_stamp"]
    den = get_def("s2var_stamp", stamp)
    if den is None:
        return "*ERROR*"
    if for_type:
        return den.name
    return sort_image(den.sort)


def s2eapp_image(node, key_image, paren_if_app):
    """ Image of an S2Eapp, either as type or sort.

    Type or sort, depending on `key_image`.

    """
    (key, image) = key_image  # `image` is a function.
    assert key == "s2exp_node" or key == "s2exp_srt"
    function = node[0]
    arguments = node[1]
    result = ""
    if paren_if_app:
        result += "("
    result += image(function[key])
    result += "("
    first = True
    for item in arguments:
        if not first:
            result += ", "
        result += image(item[key])
        first = False
    result += ")"
    if paren_if_app:
        result += ")"
    return result


def s2efun_image(node, key_image, paren_if_fun):
    """ Image of a S2Efun, either as type or sort.

    Type or sort, depending on `key_image`.

    """
    (key, image) = key_image  # `image` is a function.
    assert key == "s2exp_node" or key == "s2exp_srt"
    inputs = node[1]
    output = node[2]
    result = ""
    if paren_if_fun:
        result += "("
    marny_args = len(inputs) > 1
    if marny_args:
        result += "("
    first = True
    for item in inputs:
        if not first:
            result += ", "
        result += image(item[key], not marny_args)
        first = False
    if marny_args:
        result += ")"
    elif first:
        result += "()"
    result += " -> "
    result += image(output[key])
    if paren_if_fun:
        result += ")"
    return result


def s2erefarg_image(node, key_image):
    """ Image of a S2Erefarg, either as type or sort.

    Type or sort, depending on `key_image`.

    """
    (key, image) = key_image  # `image` is a function.
    assert key == "s2exp_node" or key == "s2exp_srt"
    passing_style = node[0]
    if passing_style == 0:
        # By value
        prefix = "!"
    elif passing_style == 1:
        # By reference
        prefix = "&"
    else:
        error("Unknown argument passing style: %i" % passing_style)
    return prefix + image(node[1][key], paren_if_fun=True, paren_if_app=True)


def quantifier_image(node, key_image, open_close):
    """ Image of an S2Eexi or of an S2Euni, either as type or sort.

    Type or sort, depending on `key_image`.

    Of an S2Eexi or of an S2Euni, depending on `open_close` characters.

    """
    (key, image) = key_image  # `image` is a function.
    assert key == "s2exp_node" or key == "s2exp_srt"
    (opn, close) = open_close  # Two paired characters.
    variables = node[0]
    predicats = node[1]
    expression = node[2]
    result = opn
    first = True
    for variable in variables:
        if not first:
            result += "; "
        result += s2var_image(variable["s2var_stamp"])
        first = False
    if predicats:
        if variables:
            result += " | "
        first = True
        for predicat in predicats:
            if not first:
                result += "; "
            result += image(predicat[key])
            first = False
    result += close
    result += " "
    result += image(expression[key])
    return result


def s2ewthtype_image(node, key_image):
    """ Image of an S2Ewthtype, either as type or sort.

    Type or sort, depending on `key_image`.

    """
    (key, image) = key_image  # `image` is a function.
    assert key == "s2exp_node" or key == "s2exp_srt"
    return image(node[0][key])


def s2etop_image(node, key_image, paren_if_app):
    """ Image of an S2Etop, either as type or sort.

    Type or sort, depending on `key_image`.

    """
    (key, image) = key_image  # `image` is a function.
    assert key == "s2exp_node" or key == "s2exp_srt"
    view_status = node[0]
    if view_status == 0:
        # Uninitialized
        postfix = "?"
    elif view_status == 1:
        # Initialized
        postfix = "?!"
    else:
        error("Unknown view status: %i" % view_status)
    result = ""
    if paren_if_app:
        result += "("
    result += image(node[1][key], paren_if_app=True)
    result += postfix
    if paren_if_app:
        result += ")"
    return result


def dyn_image(node, for_type, paren_if_fun=False, paren_if_app=False):
    """ Image of s2exp_node, either as type or sort. """
    if for_type:
        key_image = ("s2exp_node", dyn_type_image)
    else:
        key_image = ("s2exp_srt", sort_image)

    keys = list(node.keys())
    assert len(keys) == 1
    key = keys[0]
    node = node[key]

    if key == "S2Ecst":
        result = s2ecst_image(node, for_type)
    elif key == "S2Evar":
        result = s2evar_image(node, for_type)
    elif key == "S2Eextkind":
        assert for_type
        result = node[0]
    elif key == "S2Eintinf":
        assert for_type
        result = node[0]
    elif key == "S2Eapp":
        result = s2eapp_image(node, key_image, paren_if_app)
    elif key == "S2Efun":
        result = s2efun_image(node, key_image, paren_if_fun)
    elif key == "S2Eexi":
        open_close = ("[", "]")
        result = quantifier_image(node, key_image, open_close)
    elif key == "S2Euni":
        open_close = ("{", "}")
        result = quantifier_image(node, key_image, open_close)
    elif key == "S2Erefarg":
        result = s2erefarg_image(node, key_image)
    elif key == "S2Ewthtype":
        result = s2ewthtype_image(node, key_image)
    elif key == "S2Etop":
        result = s2etop_image(node, key_image, paren_if_app)
    else:
        result = "?"
    return result


def dyn_type_image(node, paren_if_fun=False, paren_if_app=False):
    """ Dyn image. """
    return dyn_image(node, True, paren_if_fun, paren_if_app)


def dyn_sort_image(node, paren_if_fun=False, paren_if_app=False):
    """ Dyn image. """
    return dyn_image(node, False, paren_if_fun, paren_if_app)


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
