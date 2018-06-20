""" Text images of expressions. """

import sys

from . import constants as c
from . import declarations
from . import tags as t


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
    if t.S2RTBAS in node:
        result = node[t.S2RTBAS][0]
    elif t.S2RTFUN in node:
        node = node[t.S2RTFUN]
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
    elif t.S2RTTUP in node:
        node = node[t.S2RTTUP]
        items = node[0]
        result = "("
        first = True
        for item in items:
            if not first:
                result += ", "
            result += sort_image(item)
            first = False
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
    assert key == t.S2EXP_NODE or key == t.S2EXP_SRT
    (opn, close) = open_close  # Two paired characters.
    variables = node[0]
    predicats = node[1]
    expression = node[2]
    result = opn
    first = True
    for variable in variables:
        if not first:
            result += "; "
        result += s2var_image(variable[t.S2VAR_STAMP])
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
    den = declarations.get_def(t.S2VAR_STAMP, stamp)
    if den is None:
        return "*ERROR*1*"
    return den.name + ": " + sort_image(den.sort)


def s2ecst_image(node, for_type):
    """ Image of a S2Ecst, either as type or sort.

    Type or sort, depending on `for_type`.

    """
    stamp = node[0][t.S2CST_STAMP]
    den = declarations.get_def(t.S2CST_STAMP, stamp)
    if den is None:
        return "*ERROR*2*"
    if for_type:
        return den.name
    return sort_image(den.sort)


def s2evar_image(node, for_type):
    """ Image of a S2Evar, either as type or sort.

    Type or sort, depending on `for_type`.

    """
    stamp = node[0][t.S2VAR_STAMP]
    den = declarations.get_def(t.S2VAR_STAMP, stamp)
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
    assert key == t.S2EXP_NODE or key == t.S2EXP_SRT
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
    assert key == t.S2EXP_NODE or key == t.S2EXP_SRT
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
    assert key == t.S2EXP_NODE or key == t.S2EXP_SRT
    passing_style = node[0]
    if passing_style == c.BY_VALUE:
        prefix = "!"
    elif passing_style == c.BY_REFERENCE:
        prefix = "&"
    else:
        error("Unknown argument passing style: %i" % passing_style)
    return prefix + image(node[1][key], paren_if_fun=True, paren_if_app=True)


def s2etop_image(node, key_image, _paren_if_fun, paren_if_app):
    """ Image of an S2Etop, either as type or sort.

    Type or sort, depending on `key_image`.

    """
    (key, image) = key_image  # `image` is a function.
    assert key == t.S2EXP_NODE or key == t.S2EXP_SRT
    view_status = node[0]
    if view_status == c.UNINITIALIZED:
        postfix = "?"
    elif view_status == c.INITIALIZED:
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
    assert key == t.S2EXP_NODE or key == t.S2EXP_SRT
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
    assert key == t.S2EXP_NODE or key == t.S2EXP_SRT
    kind_tag = node[0]
    flat = True
    if t.TYRECKINDBOX in kind_tag or t.TYRECKINDBOX_LIN in kind_tag:
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
        label = label[t.SL0ABELED]
        label_name = label[0]
        if t.LABINT in label_name:
            result += str(label_name[t.LABINT])
        elif t.LABSYM in label_name:
            result += label_name[t.LABSYM]
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
    assert key == t.S2EXP_NODE or key == t.S2EXP_SRT
    return image(node[0][key])


# Dispatch table
# ----------------------------------------------------------------------------

# There five special cases not in this table.

DISPATCH = {
    t.S2EAPP: s2eapp_image,
    t.S2EEXI: s2eexi_image,
    t.S2EFUN: s2efun_image,
    t.S2EREFARG: s2erefarg_image,
    t.S2ETOP: s2etop_image,
    t.S2ETYARR: s2etyarr_image,
    t.S2ETYREC: s2etyrec_image,
    t.S2EUNI: s2euni_image,
    t.S2EWTHTYPE: s2ewthtype_image}


# Main
# ============================================================================

def s2e_image(node, for_type, paren_if_fun=False, paren_if_app=False):
    """ Image of s2exp_node, either as type or sort. """
    if for_type:
        key_image = (t.S2EXP_NODE, type_image)
    else:
        key_image = (t.S2EXP_SRT, sort_image)

    keys = list(node.keys())
    assert len(keys) == 1
    key = keys[0]
    sub_node = node[key]

    if key == t.S2ECST:
        result = s2ecst_image(sub_node, for_type)
    elif key == t.S2EVAR:
        result = s2evar_image(sub_node, for_type)
    elif key == t.S2EEXTKIND:
        result = sub_node[0] if for_type else "?"
    elif key == t.S2EEXTYPE:
        result = sub_node[0] if for_type else "?"
    elif key == t.S2EINTINF:
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
