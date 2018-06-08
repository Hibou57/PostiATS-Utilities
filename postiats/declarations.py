""" Collect declarations. """

# This module is still work in progress, don’t care about the source.

import sys

from collections import namedtuple

from postiats import jsonized


Def = namedtuple("Def", ["table", "stamp", "name", "sort", "type", "cons"])
# Map is a Python built‑in, so table.
# The stamp key is used for table, it’s more straighforward.
# Sort, type and cons may be None.

Declaration = namedtuple("Declaration",
                         ["loc",
                          "name",
                          "construct",
                          "sort",
                          "type"])


DEFS = {
    "d2con_stamp": {},
    "d2cst_stamp": {},
    "d2var_stamp": {},
    "s2cst_stamp": {},
    "s2var_stamp": {}}
BASE_SORTS = set()
STATIC_CONSTANTS = {}
DECLARATIONS = []
STALOADED = set()


def clear():
    """ Clear generated data. """
    for table in DEFS.values():
        table.clear()
    BASE_SORTS.clear()
    STATIC_CONSTANTS.clear()
    DECLARATIONS.clear()
    STALOADED.clear()


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


# Base sorts
# ============================================================================

def collect_base_sorts(node):
    """ Fill BASE_SORTS. """
    if isinstance(node, dict):
        if "S2RTbas" in node:
            BASE_SORTS.add(node["S2RTbas"][0])
        else:
            for sub_node in node.values():
                collect_base_sorts(sub_node)
    elif isinstance(node, list):
        for sub_node in node:
            collect_base_sorts(sub_node)


# Stamps
# ============================================================================

def extract_def(entry, stamp_key, name_key, type_sort):
    """ Extract a `Def` from a JSON node given keys. """
    # type_sort is a function.
    (typ, sort) = type_sort(entry)
    stamp = entry[stamp_key]
    name = entry[name_key]
    return Def(stamp_key, stamp, name, sort, typ, None)


def add_def(den):
    """ Add `den` in `DEFS`. """
    table = DEFS[den.table]
    if den.stamp in table:
        error("Duplicated stamp: %s." % repr(den.stamp))
    table[den.stamp] = den


def extract_and_add_defs(
        root_node,
        section_key,
        stamp_key,
        name_key,
        type_sort):
    """ Extract and add defs given root node and keys. """
    # type_sort is a function.
    for entry in root_node[section_key]:
        den = extract_def(entry, stamp_key, name_key, type_sort)
        add_def(den)
        if section_key == "s2cstmap":
            STATIC_CONSTANTS[den.name] = den.sort


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


def d2con_type_sort(entry):
    """ Sort from d2conmap entry."""
    type_node = entry["d2con_type"]
    return (type_node["s2exp_node"], type_node["s2exp_srt"])


def d2cst_type_sort(entry):
    """ Sort from d2cstmap entry."""
    type_node = entry["d2cst_type"]
    return (type_node["s2exp_node"], type_node["s2exp_srt"])


def d2var_type_sort(_entry):
    """ Sort from d2varmap entry."""
    # May be provided in a D2Cvardecs.
    return (None, None)


def s2cst_type_sort(entry):
    """ Sort from s2cstmap entry."""
    # Static constant has a sort, no a type.
    return (None, entry["s2cst_srt"])


def s2var_type_sort(entry):
    """ Sort from s2varmap entry."""
    return (None, entry["s2var_srt"])


# Declarations: general
# ============================================================================

def add_declaration(
        stamp_key,
        stamp,
        loc,
        construct,
        name=None,
        sort=None,
        typ=None):
    """ Add a declaration given properties. """
    table = DEFS[stamp_key]
    if stamp in table:
        den = table[stamp]
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

    collect_base_sorts(root_node)
    collect_defs(root_node)
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
    construct = ["static", "data"]
    construct_tag = node[0]
    if construct_tag == 0:
        construct.append("datatype")
    elif construct_tag == 2:
        construct.append("datavtype")
    elif construct_tag == 5:
        construct.append("dataprop")
    elif construct_tag == 7:
        construct.append("dataview")
    else:
        error("Unknown data construction: %i" % construct_tag)
    for entry in node[1]:
        stamp = entry["s2cst_stamp"]
        add_declaration(
            stamp_key="s2cst_stamp",
            stamp=stamp,
            loc=loc,
            construct=construct)
        # Sort in Def but no type?


def handle_d2cdcstdecs(loc, node):
    """ Handle a D2Cdcstdecs. """
    # The loc argument is that of the keyword, not of the name, and there may
    # be multiple constant construction for an say extern keyword, as in val a
    # and b. Unfortunately, we can’t have the loc of the name, which would be
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
        stamp = entry["d2cst_stamp"]
        add_declaration(
            stamp_key="d2cst_stamp",
            stamp=stamp,
            loc=loc,
            construct=construct)
        # Type and sort informations are in the Def.


def handle_d2cexndecs(loc, node):
    """ Handle a D2Cexndecs. """
    # The loc argument is that of the keyword, not of the name, and there may
    # be multiple constant construction for an say extern keyword, as in
    # exception e1 and e2. Unfortunately, we can’t have the loc of the name,
    # which would be better.
    construct = ["dynamic", "constructor"]
    construct.append("exception")
    for item in node[0]:
        stamp = item["d2con_stamp"]
        add_declaration(
            stamp_key="d2con_stamp",
            stamp=stamp,
            loc=loc,
            construct=construct)
        # Type and sort informations are in the Def.


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
        stamp = entry["f2undec_var"]["d2var_stamp"]
        loc = entry["f2undec_loc"]
        add_declaration(
            stamp_key="d2var_stamp",
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
    # The _loc argument is that of the keyword, not of the name. We can have
    # the loc of the name, which is better, so the one passed is ignored.
    construct = ["dynamic", "implementation"]
    construct_tag = node[0]
    if construct_tag == 1:
        construct.append("implement")
    elif construct_tag == -1:
        construct.append("primplmnt")
    else:
        error("Unknown implementation construction: %i" % construct_tag)
    stamp = node[1]["i2mpdec_cst"]["d2cst_stamp"]
    # The stamp id is the same as that of the extern function declaration.
    loc = node[1]["i2mpdec_loc"]
    add_declaration(
        stamp_key="d2cst_stamp",
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
    # No stamp for the symbol.
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
            stamp_key=stamp_key,
            stamp=stamp,
            loc=loc,
            construct=construct,
            name=name)
        # Either type/sort from stamp (D2ITMcst) or none (D2ITMvar).


def handle_d2cstacsts(loc, node):
    """ Handle a D2Cstacsts. """
    # The loc argument is that of the keyword, not of the name, and there may
    # be multiple constant construction for an say extern keyword, as in
    # extern f(): int and g(): int. Unfortunately, we can’t have the loc of
    # the name, which would be better.
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
            construct.append("absvtype")
        elif construct_tag == 3:
            construct.append("absvt@ype")
        elif construct_tag == 5:
            construct.append("absprop")
        elif construct_tag == 7:
            construct.append("absview")
        else:
            error("Unknown static constant construct %i" % construct_tag)
        declarations = node[1]
    for declaration in declarations:
        stamp = declaration["s2cst_stamp"]
        add_declaration(
            stamp_key="s2cst_stamp",
            stamp=stamp,
            loc=loc,
            construct=construct)
        # Sort in Def but no type?


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
            stamp = var[0]["d2var_stamp"]
            add_declaration(
                stamp_key="d2var_stamp",
                stamp=stamp,
                loc=loc,
                construct=construct,
                sort=sort,
                typ=typ)
            # Type/sort retrieved from pattern if annotated.


def handle_d2cvardecs(_loc, node):
    """ Handle a D2Cvardecs. """
    for item in node[0]:
        loc = item["v2ardec_loc"]
        stamp = item["v2ardec_dvar"]["d2var_stamp"]
        typ = None
        sort = None
        type_node = item["v2ardec_type"]
        construct = ["dynamic", "var"]
        construct.append("var")
        if type_node:
            typ = type_node[0]["s2exp_node"]
            sort = type_node[0]["s2exp_srt"]
        add_declaration(
            stamp_key="d2var_stamp",
            stamp=stamp,
            loc=loc,
            construct=construct,
            sort=sort,
            typ=typ)
        # Type/sort available if annotated.
        construct = ["static", "var"]
        construct.append("var")
        stamp = item["v2ardec_svar"]["s2var_stamp"]
        add_declaration(
            stamp_key="s2var_stamp",
            stamp=stamp,
            loc=loc,
            construct=construct)
        # Sort available in stamp.


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
        error("Unknown case")
    return result


def sta_sort_image(node, paren_if_fun=False):
    """ Sort image. """
    return sort_image(node, paren_if_fun)


def s2var_image(stamp):
    """ Static variable image. """
    if stamp in DEFS:
        den = DEFS["s2var_stamp"][stamp]
        return den.name + ": " + sort_image(den.sort)
    return "*ERR*"


def dyn_image(node, for_type, paren_if_fun=False):
    """ Image of s2exp_node. """
    if for_type:
        key = "s2exp_node"
    else:
        key = "s2exp_srt"
    if for_type:
        image = dyn_type_image
    else:
        image = sort_image
    if "S2Ecst" in node:
        stamp = node["S2Ecst"][0]["s2cst_stamp"]
        table = DEFS["s2cst_stamp"]
        if stamp in table:
            den = table[stamp]
            if for_type:
                return den.name
            return sort_image(den.sort)
        return "*ERROR*"
    elif "S2Evar" in node:
        stamp = node["S2Evar"][0]["s2var_stamp"]
        table = DEFS["s2var_stamp"]
        if stamp in table:
            den = table[stamp]
            if for_type:
                return den.name
            return sort_image(den.sort)
        return "*ERROR*"
    elif "S2Eextkind" in node:
        return node["S2Eextkind"][0]
    elif "S2Eintinf" in node:
        return node["S2Eintinf"][0]
    elif "S2Efun" in node:
        node = node["S2Efun"]
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
        if paren_if_fun:
            result += ")"
        result += image(output[key])
    elif "S2Eapp" in node:
        node = node["S2Eapp"]
        function = node[0]
        arguments = node[1]
        result = image(function[key])
        result += "("
        first = True
        for item in arguments:
            if not first:
                result += ", "
            result += image(item[key])
            first = False
        result += ")"
    elif "S2Eexi" in node or "S2Euni" in node:
        if "S2Eexi" in node:
            node = node["S2Eexi"]
            begin = "["
            end = "]"
        else:
            node = node["S2Euni"]
            begin = "{"
            end = "}"
        variables = node[0]
        predicats = node[1]
        expression = node[2]
        result = begin
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
        result += end
        result += " "
        result += image(expression[key])
    else:
        for key in node.keys():
            return "?"
    return result


def dyn_type_image(node, paren_if_fun=False):
    """ Dyn image. """
    return dyn_image(node, True, paren_if_fun)


def dyn_sort_image(node, paren_if_fun=False):
    """ Dyn image. """
    return dyn_image(node, False, paren_if_fun)
