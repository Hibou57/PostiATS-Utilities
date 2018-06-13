""" Text images of expressions. """

import sys

from . import declarations


# Helpers
# ============================================================================

def perror(message):
    """ Shorthand to print to `stderr`. """
    print(message, file=sys.stderr)


def error(message):
    """ `perror` and `sys.exit(1)`. """
    perror(message)
    sys.exit(1)


# Sort image
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
        if paren_if_fun:
            result += "("
        if inputs:
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
        result += sort_image(output)
        if paren_if_fun:
            result += ")"
    else:
        error("Unknown sort expression")
    return result


# Quantified expression image
# ============================================================================

def quantified_exp_image(node, key_image, open_close):
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


# Type image
# ============================================================================

# Special cases
# ----------------------------------------------------------------------------

def s2var_image(stamp):
    """ Static variable image. """
    den = declarations.get_def("s2var_stamp", stamp)
    if den is None:
        return "*ERROR*1*"
    return den.name + ": " + sort_image(den.sort)


def s2ecst_image(node, for_type):
    """ Image of a S2Ecst, either as type or sort.

    Type or sort, depending on `for_type`.

    """
    stamp = node[0]["s2cst_stamp"]
    den = declarations.get_def("s2cst_stamp", stamp)
    if den is None:
        return "*ERROR*2*"
    if for_type:
        return den.name
    return sort_image(den.sort)


def s2evar_image(node, for_type):
    """ Image of a S2Evar, either as type or sort.

    Type or sort, depending on `for_type`.

    """
    stamp = node[0]["s2var_stamp"]
    den = declarations.get_def("s2var_stamp", stamp)
    if den is None:
        return "*ERROR*3*"
    if for_type:
        return den.name
    return sort_image(den.sort)


# Specific
# ----------------------------------------------------------------------------

def s2eapp_image(node, key_image, _paren_if_fun, paren_if_app):
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
    result += image(function[key], paren_if_fun=True)
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


def s2eexi_image(node, key_image, _paren_if_fun, _paren_if_app):
    """ Image of an S2Eexi, either as type or sort.

    Type or sort, depending on `key_image`.

    Of an S2Eexi or of an S2Euni, depending on `open_close` characters.

    """
    return quantified_exp_image(node, key_image, open_close=("[", "]"))


def s2efun_image(node, key_image, paren_if_fun, _paren_if_app):
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


def s2erefarg_image(node, key_image, _paren_if_fun, _paren_if_app):
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


def s2etop_image(node, key_image, _paren_if_fun, paren_if_app):
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


def s2etyarr_image(node, key_image, _paren_if_fun, paren_if_app):
    """ Image of an S2Etyarr, either as type or sort.

    Type or sort, depending on `key_image`.

    """
    (key, image) = key_image  # `image` is a function.
    assert key == "s2exp_node" or key == "s2exp_srt"
    element_type = node[0]
    dimmensions = node[1]
    result = ""
    if paren_if_app:
        result += "("
    result += "@["
    result += image(element_type[key])
    result += "]"
    result += "["
    first = True
    for dimmension in dimmensions:
        if not first:
            result += ", "
        result += image(dimmension[key])
        first = False
    result += "]"
    if paren_if_app:
        result += ")"
    return result


def s2etyrec_image(node, key_image, _paren_if_fun, paren_if_app):
    """ Image of an S2Etyrec, either as type or sort.

    Type or sort, depending on `key_image`.

    """
    (key, image) = key_image  # `image` is a function.
    assert key == "s2exp_node" or key == "s2exp_srt"
    kind_tag = node[0]
    flat = True
    if "TYRECKINDbox" in kind_tag or "TYRECKINDbox_lin" in kind_tag:
        flat = False
    labels = node[2]
    result = ""
    if paren_if_app:
        result += "("
    if flat:
        result += "@{"
    else:
        result += "'{"
    first = True
    for label in labels:
        if not first:
            result += ", "
        label = label["SL0ABELED"]
        label_name = label[0]
        if "LABint" in label_name:
            result += str(label_name["LABint"])
        elif "LABsym" in label_name:
            result += label_name["LABsym"]
        else:
            error("Unknown label name type")
        result += "="
        result += image(label[2][key])
        first = False
    result += "}"
    if paren_if_app:
        result += ")"
    return result


def s2euni_image(node, key_image, _paren_if_fun, _paren_if_app):
    """ Image of an S2Euni, either as type or sort.

    Type or sort, depending on `key_image`.

    Of an S2Eexi or of an S2Euni, depending on `open_close` characters.

    """
    return quantified_exp_image(node, key_image, open_close=("{", "}"))


def s2ewthtype_image(node, key_image, _paren_if_fun, _paren_if_app):
    """ Image of an S2Ewthtype, either as type or sort.

    Type or sort, depending on `key_image`.

    """
    (key, image) = key_image  # `image` is a function.
    assert key == "s2exp_node" or key == "s2exp_srt"
    return image(node[0][key])


# Dispatch table
# ----------------------------------------------------------------------------

# There five special cases not in this table.

DISPATCH = {
    "S2Eapp": s2eapp_image,
    "S2Eexi": s2eexi_image,
    "S2Efun": s2efun_image,
    "S2Erefarg": s2erefarg_image,
    "S2Etop": s2etop_image,
    "S2Etyarr": s2etyarr_image,
    "S2Etyrec": s2etyrec_image,
    "S2Euni": s2euni_image,
    "S2Ewthtype": s2ewthtype_image}


# Main
# ============================================================================

def s2e_image(node, for_type, paren_if_fun=False, paren_if_app=False):
    """ Image of s2exp_node, either as type or sort. """
    if for_type:
        key_image = ("s2exp_node", type_image)
    else:
        key_image = ("s2exp_srt", sort_image)

    keys = list(node.keys())
    assert len(keys) == 1
    key = keys[0]
    sub_node = node[key]

    if key == "S2Ecst":
        result = s2ecst_image(sub_node, for_type)
    elif key == "S2Evar":
        result = s2evar_image(sub_node, for_type)
    elif key == "S2Eextkind":
        result = sub_node[0] if for_type else "?"
    elif key == "S2Eextype":
        result = sub_node[0] if for_type else "?"
    elif key == "S2Eintinf":
        result = sub_node[0] if for_type else "?"
    elif key in DISPATCH:
        method = DISPATCH[key]
        result = method(sub_node, key_image, paren_if_fun, paren_if_app)
    else:
        result = "?"
    return result


def type_image(node, paren_if_fun=False, paren_if_app=False):
    """ Dyn image. """
    return s2e_image(node, True, paren_if_fun, paren_if_app)


def type_sorts_image(node, paren_if_fun=False, paren_if_app=False):
    """ Dyn image. """
    return s2e_image(node, False, paren_if_fun, paren_if_app)
