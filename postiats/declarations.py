""" Collect declarations. """

import sys

from collections import namedtuple

from postiats import jsonized


Stamp = namedtuple("Stamp", ["id", "name", "sort"])  # Sort may be None.

Declaration = namedtuple("Declaration",
                         ["construct",
                          "name",
                          "loc",
                          "type",
                          "sort"])


STAMPS = {}
DECLARATIONS = []
STALOADED = set()


# Helpers
# ============================================================================

def perror(message):
    """ Shorthand to print to `stderr`. """
    print(message, file=sys.stderr)


def error(message):
    """ `perror` and `sys.exit(1)`. """
    perror(message)
    sys.exit(1)


def add_staloaded(path):
    """ Register a new added source. """
    STALOADED.add(path)


# Stamps
# ============================================================================

def extract_stamp(entry, stamp_key, name_key, sort):
    """ Extract a `Stamp` from a JSON node given keys. """
    # Sort is a function.
    stamp_id = entry[stamp_key]
    name = entry[name_key]
    return Stamp(stamp_id, name, sort(entry))


def add_stamp(stamp):
    """ Add `stamp` in `STAMPS`. """
    if stamp.id in STAMPS:
        error("Warning: duplicated stamp: %s." % repr(stamp))
    STAMPS[stamp.id] = stamp


def extract_and_add_stamps(root_node, section_key, stamp_key, name_key, sort):
    """ Extract and add stamps given root node and keys. """
    # Sort is a function.
    for entry in root_node[section_key]:
        stamp = extract_stamp(entry, stamp_key, name_key, sort)
        add_stamp(stamp)


def collect_stamps(root_node):
    """ Collect stamps: their stamp id, name and sort. """

    extract_and_add_stamps(
        root_node=root_node,
        section_key="d2conmap",
        stamp_key="d2con_stamp",
        name_key="d2con_sym",
        sort=d2con_sort)

    extract_and_add_stamps(
        root_node=root_node,
        section_key="d2cstmap",
        stamp_key="d2cst_stamp",
        name_key="d2cst_sym",
        sort=d2cst_sort)

    extract_and_add_stamps(
        root_node=root_node,
        section_key="d2varmap",
        stamp_key="d2var_stamp",
        name_key="d2var_sym",
        sort=d2var_sort)

    extract_and_add_stamps(
        root_node=root_node,
        section_key="s2cstmap",
        stamp_key="s2cst_stamp",
        name_key="s2cst_sym",
        sort=s2cst_sort)

    extract_and_add_stamps(
        root_node=root_node,
        section_key="s2varmap",
        stamp_key="s2var_stamp",
        name_key="s2var_sym",
        sort=s2var_sort)


def d2con_sort(entry):
    """ Sort from d2conmap entry."""
    return entry["d2con_type"]["s2exp_srt"]


def d2cst_sort(entry):
    """ Sort from d2cstmap entry."""
    return entry["d2cst_type"]["s2exp_srt"]


def d2var_sort(_entry):
    """ Sort from d2varmap entry."""
    # May be provided in a D2Cvardecs.
    return None


def s2cst_sort(entry):
    """ Sort from s2cstmap entry."""
    return entry["s2cst_srt"]


def s2var_sort(entry):
    """ Sort from s2varmap entry."""
    return entry["s2var_srt"]


# Declarations: general
# ============================================================================

def add_declaration(construct, stamp_id, loc, typ=None, sort=None, name=None):
    """ Add a declaration given properties. """
    if stamp_id in STAMPS:
        stamp = STAMPS[stamp_id]
        declaration = Declaration(
            construct=construct,
            name=name or stamp.name,
            loc=loc,
            type=typ,
            sort=sort or stamp.sort)
        DECLARATIONS.append(declaration)
    else:
        # error("Missing stamp id: %i" % stamp_id)
        # #include is buggy with stamps.
        pass


def collect_declarations(root_node):
    """ Collect declarations. """
    for entry in root_node:
        loc = entry["d2ecl_loc"]
        node = entry["d2ecl_node"]
        dispatch_declaration(loc, node)


def collect_main_declarations(root_node):
    """ Collect declarations. """
    collect_declarations(root_node["d2eclist"])


def handle_source_file(path):
    """ Handle one source file. """
    root_node = jsonized.get_json(path)
    if root_node is None:
        error("Failed to evaluate %s" % path)

    collect_stamps(root_node)
    collect_main_declarations(root_node)


# Declarations: specific
# ============================================================================

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


def handle_d2cdatdecs(loc, node):
    """ Handle a D2Cdatdecs. """
    # The loc argument is that of the keyword, not of the name, and there may
    # be multiple data construction for an say datatype keyword, as in
    # datatype T and U and V. Unfortunately, we can’t have the loc of the
    # name, which would be better.
    construct = node[0]
    if construct == 0:
        construct = "datatype"
    elif construct == 2:
        construct = "datavtype"
    elif construct == 5:
        construct = "dataprop"
    elif construct == 7:
        construct = "dataview"
    else:
        error("Unknown data construction: %i" % construct)
    construct = "data: " + construct
    for entry in node[1]:
        stamp_id = entry["s2cst_stamp"]
        add_declaration(
            construct=construct,
            stamp_id=stamp_id,
            loc=loc)


def handle_d2cdcstdecs(loc, node):
    """ Handle a D2Cdcstdecs. """
    # The loc argument is that of the keyword, not of the name, and there may
    # be multiple constant construction for an say extern keyword, as in val a
    # and b. Unfortunately, we can’t have the loc of the name, which would be
    # better.
    construct = node[1]
    if construct == "DCKcastfn":
        construct = "castfn"
    elif construct == "DCKfun":
        construct = "fun"
    elif construct == "DCKpraxi":
        construct = "praxi"
    elif construct == "DCKprfun":
        construct = "prfun"
    elif construct == "DCKval":
        construct = "val"
    else:
        error("Unknown constant construction: %s" % construct)
    construct = "constant: " + construct
    for entry in node[2]:
        stamp_id = entry["d2cst_stamp"]
        add_declaration(
            construct=construct,
            stamp_id=stamp_id,
            loc=loc)


def handle_d2cexndecs(loc, node):
    """ Handle a D2Cexndecs. """
    # The loc argument is that of the keyword, not of the name, and there may
    # be multiple constant construction for an say extern keyword, as in
    # exception e1 and e2. Unfortunately, we can’t have the loc of the name,
    # which would be better.
    for item in node[0]:
        stamp_id = item["d2con_stamp"]
        add_declaration(
            construct="exception",
            stamp_id=stamp_id,
            loc=loc)


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
    # be multiple functions for an say fun keyword, as in fun x and y and z.
    # We can have the loc of the name, which is better, so the one passed is
    # ignored.
    construct = node[0]
    if construct == "FK_fn":
        construct = "fn"
    elif construct == "FK_fnx":
        construct = "fnx"
    elif construct == "FK_fun":
        construct = "fun"
    elif construct == "FK_prfn":
        construct = "prfn"
    elif construct == "FK_prfun":
        construct = "prfun"
    else:
        error("Unknown function construction: %s" % construct)
    construct = "function: " + construct
    for entry in node[2]:
        stamp_id = entry["f2undec_var"]["d2var_stamp"]
        loc = entry["f2undec_loc"]
        add_declaration(
            construct=construct,
            stamp_id=stamp_id,
            loc=loc)


def handle_d2cignored(_loc, _node):
    """ Handle a D2Cignored. """
    # Lost.
    pass


def handle_d2cimpdec(_loc, node):
    """ Handle a D2Cimpdec. """
    # The _loc argument is that of the keyword, not of the name. We can have
    # the loc of the name, which is better, so the one passed is ignored.
    construct = node[0]
    if construct == 1:
        construct = "implement"
    elif construct == -1:
        construct = "primplmnt"
    else:
        error("Unknown case")
    construct = "implementation: " + construct
    stamp_id = node[1]["i2mpdec_cst"]["d2cst_stamp"]
    loc = node[1]["i2mpdec_loc"]
    add_declaration(
        construct=construct,
        stamp_id=stamp_id,
        loc=loc)


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
    # No stamp for the symbol.
    stamp_id = None
    name = node[0]
    sub_node = node[2][0]  # There are never many, isn’t it?
    if "D2ITMcst" in sub_node:
        stamp_id = sub_node["D2ITMcst"][0]["d2cst_stamp"]
    elif "D2ITMvar" in sub_node:
        stamp_id = sub_node["D2ITMvar"][0]["d2var_stamp"]
    elif "D2ITMignored" in sub_node:
        pass
    else:
        error("Unknow case")
    if stamp_id is not None:
        add_declaration(
            construct="overload",
            stamp_id=stamp_id,
            loc=loc,
            name=name)


def handle_d2cstacsts(loc, node):
    """ Handle a D2Cstacsts. """
    # The loc argument is that of the keyword, not of the name, and there may
    # be multiple constant construction for an say extern keyword, as in
    # extern f(): int and g(): int. Unfortunately, we can’t have the loc of
    # the name, which would be better.
    if len(node) == 1:
        construct = "stacst"
        declarations = node[0]
    else:
        construct = node[0]
        if construct == 0:
            construct = "abstype"
        elif construct == 1:
            construct = "abst@ype"
        elif construct == 2:
            construct = "absvtype"
        elif construct == 3:
            construct = "absvt@ype"
        elif construct == 5:
            construct = "absprop"
        elif construct == 7:
            construct = "absview"
        else:
            error("Unknown static constant construct %i" % construct)
        declarations = node[1]
    construct = "static constant: " + construct
    for declaration in declarations:
        stamp_id = declaration["s2cst_stamp"]
        add_declaration(
            construct=construct,
            stamp_id=stamp_id,
            loc=loc)


def handle_d2cstaload(_loc, node):
    """ Handle a D2Cstaload. """
    # Not a declaration, but record it.
    path = node[1]
    add_staloaded(path)


def handle_d2cvaldecs(_loc, node):
    """ Handle a D2Cvaldecs. """

    construct = node[0]
    if construct == "VK_prval":
        construct = "prval"
    elif construct == "VK_val":
        construct = "val"
    elif construct == "VK_val_neg":
        construct = "val-"
    elif construct == "VK_val_pos":
        construct = "val+"
    else:
        error("Unknown function construction: %s" % construct)
    construct = "value: " + construct
    for item in node[1]:
        for (loc, var, sort) in p2at_node_p2tvars(item["v2aldec_pat"]):
            stamp_id = var[0]["d2var_stamp"]
            add_declaration(
                construct=construct,
                stamp_id=stamp_id,
                loc=loc,
                sort=sort)


def handle_d2cvardecs(_loc, node):
    """ Handle a D2Cvardecs. """
    construct = "var"
    for item in node[0]:
        loc = item["v2ardec_loc"]
        stamp_id = item["v2ardec_dvar"]["d2var_stamp"]
        type_node = item["v2ardec_type"]
        sort = type_node[0]["s2exp_srt"] if type_node else None
        add_declaration(
            construct=construct,
            stamp_id=stamp_id,
            loc=loc,
            sort=sort)


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
    "D2Cvardecs": handle_d2cvardecs
}


# Inner nodes
# ============================================================================

def p2at_node_p2tvars(node, sort=None):
    """ Yield variables from pattern. """
    # Node is a {p2at_loc, p2at_node}
    loc = node["p2at_loc"]
    node = node["p2at_node"]
    if "P2Tann" in node:
        if not sort:
            sort = node["P2Tann"][1]["s2exp_srt"]
        yield from p2at_node_p2tvars(node["P2Tann"][0], sort)
    elif "P2Trec" in node:
        nodes = node["P2Trec"][2]
        for item in nodes:
            yield from p2at_node_p2tvars(item["LABP2ATnorm"][1], sort)
    elif "P2Tvar" in node:
        node = node["P2Tvar"]
        yield (loc, node, sort)


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
                result += sort_image(item, paren_if_fun=not marny_args)
                if not first:
                    result += ", "
                first = False
            if marny_args:
                result += ")"
            result += " -> "
            if paren_if_fun:
                result += ")"
        result += sort_image(output)
    else:
        error("Unknown case")
    return result
