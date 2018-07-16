""" Lexicalisation of ATS2 sources. """

from . import lexemes_defs as d

from .lexemes_defs import (Term, NonTerm, Start)


# Types
# ============================================================================

class Input:

    """ Input string with current pos. """

    __slots__ = ["source", "length", "pos"]

    def __init__(self, source):
        self.source = source
        self.length = len(source)
        self.pos = 0

    def char(self, offset=0):
        """ Character at pos or EOF is at end of string. """
        i = self.pos + offset
        if i < self.length:
            return self.source[i]
        if i == self.length:
            return d.EOF
        raise ValueError

    def consume(self, count=1):
        """ Increment pos. """
        assert self.pos + count <= self.length
        self.pos += count

    def string(self, start, end=None):
        """ String from start to pos excluded. """
        if end is None:
            end = self.pos
        return self.source[start:self.pos]

    def at(self, text):
        """ True if string at current position. """
        i = self.pos
        j = i + len(text)
        return self.source[i:j] == text


def file_input(path):
    """ Input from file. """
    source_file = open(path, encoding="iso-8859-15")
    source_text = source_file.read()
    source_file.close()
    return Input(source_text)


# Helpers
# ============================================================================

def get_ident(source):
    """ Try to read `IDENTFST` `IDENTRST`*. """
    result = None
    c = source.char()
    if c in d.IDENTFST:
        result = c
        while True:
            c = source.char(len(result))
            if c not in d.IDENTRST:
                break
            result += c
    if result is not None:
        source.consume(len(result))
    return result


def get_chars_of_category(source, category, count=-1):
    """ Try to read category+. """
    result = ""
    count_down = count
    c = source.char()
    while c in category and count_down != 0:
        count_down -= 1
        result += c
        c = source.char(len(result))
    source.consume(len(result))
    return result if result else None


def get_char_of_category(source, category):
    """ Read category?. """
    result = ""
    c = source.char()
    if c in category:
        result = c
    source.consume(len(result))
    return result if result else None


def get_char(source, c):
    """ Read c?. """
    result = ""
    if source.char() == c:
        result = c
    source.consume(len(result))
    return result if result else None


def get_symbol(source):
    """ Try to read `SYMBOLIC`+. """
    return get_chars_of_category(source, d.SYMBOLIC)


def get_oct(source):
    """ Try to read `OCTAL`+. """
    return get_chars_of_category(source, d.OCTAL)


def get_dec(source):
    """ Try to read `DIGIT`+. """
    return get_chars_of_category(source, d.DIGIT)


def get_hex(source):
    """ Try to read `XDIGIT`+. """
    return get_chars_of_category(source, d.XDIGIT)


def get_p(source):
    """ Try to read `P`?. """
    return get_char_of_category(source, d.P)


def get_e(source):
    """ Try to read `E`?. """
    return get_char_of_category(source, d.E)


def get_sign(source):
    """ Try to read `SIGN`?. """
    return get_char_of_category(source, d.SIGN)


def get_fl(source):
    """ Try to read `FL`?. """
    return get_char_of_category(source, d.FL)


def get_lu(source):
    """ Try to read `LU`?. """
    return get_char_of_category(source, d.LU)


# Specials
# ============================================================================

# Space
# ----------------------------------------------------------------------------

def get_space(source):
    """ Try to read `SPACE`+. """
    return get_chars_of_category(source, d.SPACE)


# Space float dec
# ----------------------------------------------------------------------------

def space_float_dec_cond(space, source, consume):
    """ SPACE . DIGIT """
    result = (
        space is not None and
        source.char(0) == "." and
        source.char(1) in d.DIGIT)
    if result and consume:
        source.consume(2)
    return result


def space_float_dec(source):
    """ T_FLOAT

    Prefix: SAPCE .

    SPACE . DIGIT+ (E SIGN? DIGIT+)? FL?

    Note SPACE is already consumed, source is at the dot.

    """
    assert source.at(".")
    assert source.char(1) in d.DIGIT
    source.consume()
    _fractional = get_dec(source)  # Not empty.
    if get_e(source):
        _sign = get_sign(source)
        exponent = get_dec(source)
        if exponent is None:
            return Term.T_ERR
    _fl = get_fl(source)
    return Term.T_FLOAT


# Extcode
# ----------------------------------------------------------------------------

def get_extcode_tag(source):
    """ Try to read `EXTCODE_TAG`?. """
    return get_char_of_category(source, d.EXTCODE_TAG)


def extcode_cond(sol, source, consume):
    """ SOL % { """
    result = sol and source.char(0) == "%" and source.char(1) == "{"
    if result and consume:
        source.consume(2)
    return result


def extcode(source):
    """ T_EXTCODE.

    Prefix: SOL %{

    SOL %{ (# | ^ 2? | $ 2?)? IC* SOL %}

    Note SOL space is already consumed, source is at the percent‑sign.

    """
    assert source.at("%{")
    end_string = d.EOL + "%}"
    tag = get_extcode_tag(source)
    if tag == "$" or tag == "^":
        _sub_tag = get_char(source, "2")
    while True:
        if source.at(end_string):
            source.consume(len(end_string))
            break
        c = source.char()
        if c == d.EOF:
            return Term.T_ERR
        source.consume()
    return Term.T_EXTCODE


# Prefix handlers
# ============================================================================

# Prefix
# ----------------------------------------------------------------------------

def get_prefix_product(source):
    """ Try to get prefix product at source. """
    node = d.TREE
    product = None
    size = 0
    while True:
        c = source.char(size)
        node = d.tree_step(node, c)
        if node is None:
            break
        if node.product is not None:
            product = node.product
        if c == d.EOF:
            break
        size += 1
    source.consume(size)
    return product


# CHAR_start
# ----------------------------------------------------------------------------

def char_escaped(source):
    """ Helper for char. """
    c = source.char()
    if c in d.ESCAPED:
        source.consume()
        return c
    if c == "0" and source.char(1) in d.X:
        source.consume(2)
        hex_digits = get_hex(source)
        return hex_digits if hex_digits else Term.T_ERR
    if c in d.OCTAL:
        oct_digits = get_oct(source)
        return oct_digits
    return Term.T_ERR


def char(source):
    r""" T_CHAR

    Prefix: '

    '\ ESCAPED '
    ' IC_LQ '
    '\ OCTAL+ '
    '\ X XDIGIT+ '

    """
    assert source.at("'")
    source.consume()
    c = source.char()
    if c == "\\":
        source.consume()
        escaped = char_escaped(source)
        if escaped == Term.T_ERR:
            return Term.T_ERR
    else:
        if c == d.EOF:
            return Term.T_ERR
        source.consume()
    c = get_char(source, "'")
    if c is None:
        return Term.T_ERR
    return Term.T_CHAR


# COMMENT_block_c_start
# ----------------------------------------------------------------------------

def comment_block_c(source):
    """ COMMENT_block_c

    Prefix: /*

    /* IC* */

    """
    assert source.at("/*")
    end_string = "*/"
    while True:
        if source.at(end_string):
            source.consume(len(end_string))
            break
        c = source.char()
        if c == d.EOF:
            return Term.T_ERR
        source.consume()
    return NonTerm.COMMENT_block_c


# COMMENT_block_ml_start
# ----------------------------------------------------------------------------

def comment_block_ml(source):
    """ COMMENT_block_ml

    Prefix: (*

    (* IC* COMMENT_block_ml IC* *)

    """
    assert source.at("(*")
    start_string = "(*"
    end_string = "*)"
    level = 0
    while True:
        if source.at(start_string):
            source.consume(len(start_string))
            level += 1
        elif source.at(end_string):
            source.consume(len(end_string))
            level -= 1
            if level == 0:
                break
        else:
            c = source.char()
            if c == d.EOF:
                return Term.T_ERR
            source.consume()
    return NonTerm.COMMENT_block_ml


# COMMENT_line_start
# ----------------------------------------------------------------------------

def comment_line(source):
    """ T_COMMENT_line

    Prefix: //

    // IC_LEOL* (EOL|EOF)

    """
    assert source.at("//")
    while True:
        c = source.char()
        if c == d.EOL or c == d.EOF:
            # Don’t consume EOL nor EOF
            break
        source.consume()
    return Term.T_COMMENT_line


# COMMENT_rest_start
# ----------------------------------------------------------------------------

def comment_rest(source):
    """ T_COMMENT_rest

    Prefix: ////

    //// IC* EOF

    """
    assert source.at("////")
    while True:
        c = source.char()
        if c == d.EOF:
            # Don’t consume EOF
            break
        source.consume()
    return Term.T_COMMENT_rest


# DOTINT_start
# ----------------------------------------------------------------------------

def dotint(source):
    """ T_DOTINT

    Prefix: . DIGIT

    . DIGIT+

    """
    assert source.at(".")
    source.consume()
    _int_ident = get_dec(source)
    return Term.T_DOTINT


# FLOAT_dec_start
# ----------------------------------------------------------------------------

def float_dec(source):
    """ T_FLOAT

    Prefix: 0.
    Prefix: 0 E

    0. DIGIT* (E SIGN? DIGIT+)? FL?
    0 E SIGN? DIGIT+ FL?

    """
    assert source.at("0")
    assert source.char(1) in d.E | {"."}
    source.consume()
    if get_char(source, "."):
        _fractional = get_dec(source)
        # No need to check for empty, the integral part is not.
    if get_e(source):
        _sign = get_sign(source)
        exponent = get_dec(source)
        if not exponent:
            return Term.T_ERR
    _fl = get_fl(source)
    return Term.T_FLOAT


# IDENT_dlr_start
# ----------------------------------------------------------------------------

def ident_dlr(source):
    """ T_IDENT_dlr

    Prefix: $ IDENTFST

    $ IDENTFST IDENTRST*

    T_IDENT_dlr is possibly translated.

    """
    assert source.at("$")
    assert source.char(1) in d.IDENTFST
    source.consume()
    rest = get_ident(source)
    ident = "$" + rest
    return d.ident_translation(ident, Term.T_IDENT_dlr)


# IDENT_srp_start
# ----------------------------------------------------------------------------

def ident_srp(source):
    """ T_IDENT_srp

    Prefix: # IDENTFST

    # IDENTFST IDENTRST*

    T_IDENT_srp is possibly translated.

    """
    assert source.at("#")
    assert source.char(1) in d.IDENTFST
    source.consume()
    rest = get_ident(source)
    ident = "#" + rest
    return d.ident_translation(ident, Term.T_IDENT_srp)


# IDENT_sym_start
# ----------------------------------------------------------------------------

def ident_sym(source):
    """ T_IDENT_sym

    Prefix: $ SYMBOLIC
    Prefix: SYMBOLIC

    $ SYMBOLIC*
    SYMBOLIC+

    T_IDENT_sym is possibly translated.

    """
    assert source.char() in d.SYMBOLIC | {"$"}
    ident = ""
    if get_char(source, "$"):
        ident += "$"
    ident += get_symbol(source)
    return d.ident_translation(ident, Term.T_IDENT_sym)


# IDENT_xx_start
# ----------------------------------------------------------------------------

def ident_xx(source):
    """ T_IDENT_arr, T_IDENT_ext, T_IDENT_tmp, T_IDENT_alp

    Prefix: IDENTFST

    IDENTFST IDENTRST* [
    IDENTFST IDENTRST* !
    IDENTFST IDENTRST* <
    IDENTFST IDENTRST*

    T_IDENT_alp is possibly translated.

    """
    assert source.char() in d.IDENTFST
    ident = get_ident(source)
    c = source.char()
    if c == "[":
        source.consume()
        return Term.T_IDENT_arr
    if c == "!":
        source.consume()
        return Term.T_IDENT_ext
    if c == "<":
        source.consume()
        return Term.T_IDENT_tmp
    return d.ident_translation(ident, Term.T_IDENT_alp)


# INT_oct_start
# ----------------------------------------------------------------------------

def int_oct(source):
    """ T_INT

    Prefix: 0 OCTAL

    0 OCTAL+ LU?

    """
    assert source.at("0")
    _oct = get_oct(source)
    _lu = get_lu(source)
    return Term.T_INT


# QMARKGT_start
# ----------------------------------------------------------------------------

def qmarkgt(source):
    """ T_IDENT_sym

    Prefix: ?>

    T_IDENT_sym is translated.

    """
    assert source.at("?>")
    source.consume(1)  # Not 2!
    ident = "?"
    return d.ident_translation(ident, Term.T_IDENT_sym)


# STRING_start
# ----------------------------------------------------------------------------

def get_oct3(source):
    """ Try to read `OCTAL`+. """
    return get_chars_of_category(source, d.OCTAL, count=3)


def get_hex2(source):
    """ Try to read `XDIGIT`+. """
    return get_chars_of_category(source, d.XDIGIT, count=2)


def string_escaped(source):
    """ Helper for string. """
    c = source.char()
    if c in d.ESCAPED or c == "\n":
        source.consume()
        return c
    if c == "0" and source.char(1) in d.X:
        source.consume(2)
        hex_digits = get_hex2(source)
        return hex_digits if hex_digits else Term.T_ERR
    if c in d.OCTAL:
        oct_digits = get_oct3(source)
        return oct_digits
    return Term.T_ERR


def string(source):
    r""" T_STRING

    Prefix: "

    " (\ EOL | \ ESCAPED | \ X XDIGIT{1,2} | \ OCTAL{1,3} | IC_LDQ)* "

    """
    assert source.at('"')
    source.consume()
    while True:
        c = source.char()
        if c == "\\":
            source.consume()
            escaped = string_escaped(source)
            if escaped == Term.T_ERR:
                return Term.T_ERR
        elif c == '"':
            source.consume()
            break
        else:
            source.consume()
        if c == d.EOF:
            return Term.T_ERR
    return Term.T_STRING


# XX_dec_start
# ----------------------------------------------------------------------------

def xx_dec(source):
    """ T_FLOAT, T_INT

    Prefix: 1-9

    DIGIT+ . DIGIT* (E SIGN? DIGIT+)? FL?
    DIGIT+ E SIGN? DIGIT+ FL?
    DIGIT+ LU?

    """
    assert source.char() in d.DIGIT
    a_float = False
    _integral = get_dec(source)
    if get_char(source, "."):
        a_float = True
        _fractional = get_dec(source)
        # No need to check for empty, the integral part is not.
    if get_e(source):
        a_float = True
        _sign = get_sign(source)
        exponent = get_dec(source)
        if not exponent:
            return Term.T_ERR
    if a_float:
        _fl = get_fl(source)
        return Term.T_FLOAT
    _lu = get_lu(source)
    return Term.T_INT


# XX_hex_start
# ----------------------------------------------------------------------------

def xx_hex(source):
    """ T_FLOAT, T_INT

    Prefix: 0 X

    0 X . XDIGIT+ P SIGN? DIGIT+ FL?
    0 X XDIGIT+ P SIGN? DIGIT+ FL?
    0 X XDIGIT+ . XDIGIT* P SIGN? DIGIT+ FL?
    0 X XDIGIT+ LU?

    """
    assert source.at("0x") or source.at("0X")
    source.consume(2)
    a_float = False
    integral = get_hex(source)  # May be empty
    fractional = None
    if get_char(source, "."):
        a_float = True
        fractional = get_hex(source)
    if get_p(source):
        a_float = True
        _sign = get_sign(source)
        exponent = get_hex(source)
        if not exponent:
            return Term.T_ERR
    elif a_float:
        return Term.T_ERR
    if a_float:
        if not integral and not fractional:
            return Term.T_ERR
        _fl = get_fl(source)
        return Term.T_FLOAT
    if not integral:
        return Term.T_ERR
    _lu = get_lu(source)
    return Term.T_INT


# Dispatch
# ----------------------------------------------------------------------------

DISPATCH = {
    Start.CHAR_start: char,
    Start.COMMENT_block_c_start: comment_block_c,
    Start.COMMENT_block_ml_start: comment_block_ml,
    Start.COMMENT_line_start: comment_line,
    Start.COMMENT_rest_start: comment_rest,
    Start.DOTINT_start: dotint,
    Start.FLOAT_dec_start: float_dec,
    Start.IDENT_dlr_start: ident_dlr,
    Start.IDENT_srp_start: ident_srp,
    Start.IDENT_sym_start: ident_sym,
    Start.IDENT_xx_start: ident_xx,
    Start.INT_oct_start: int_oct,
    Start.QMARKGT_start: qmarkgt,
    Start.STRING_start: string,
    Start.XX_dec_start: xx_dec,
    Start.XX_hex_start: xx_hex}

assert all(isinstance(x, Start) for x in DISPATCH)


# Main
# ============================================================================

def raw(source):
    """ Unfiltered lexemes. """

    def term(kind):
        """ (pos, kind, string) """
        assert isinstance(kind, Term)
        return (kind, pos, source.pos, source.string(pos))

    sol = True
    while True:
        pos = source.pos
        space = get_space(source)
        if space is not None:
            sol = space[-1] == d.EOL
            yield term(Term.T_SPACE)
        # Don’t set sol to False when there is no space, not here: at start
        # of file, we have an sol and no space.
        pos = source.pos
        if space_float_dec_cond(space, source, consume=False):
            product = space_float_dec(source)
            yield term(product)
        elif extcode_cond(sol, source, consume=False):
            product = extcode(source)
            yield term(product)
        else:
            product = get_prefix_product(source)
            if product is not None:
                if isinstance(product, Start):
                    source.pos = pos
                    product = DISPATCH[product](source)
                if isinstance(product, NonTerm):  # Not elif!
                    product = d.NONTERMS_TRANSL[product]
                yield term(product)
            else:
                source.consume()
                product = Term.T_ERR
                yield term(product)
        sol = False
        # Suppose no product is empty except T_EOF and no product consumes
        # the EOL except T_SPACE.
        if product == Term.T_EOF:
            # Don’t check source pos is at end, it is not the same: when
            # a token ends with EOF, it gives no chance to generate a
            # T_EOF.
            break


def filtered(source):
    """ Filtered lexemes. """

    def error(lexeme):
        """ Lexeme as T_ERR. """
        return (lexeme[0], Term.T_ERR, lexeme[2])

    for lexeme in raw(source):
        kind = lexeme[1]
        if kind == Term.T_ERR:
            yield lexeme
            break
        elif kind == Term.T_SPACE:
            pass
        elif kind in d.COMMENTS:
            pass
        elif kind in d.ERRORS:
            yield error(lexeme)
            break
        elif kind == Term.T_IDENT_ext:
            name = lexeme[2]
            if name not in d.IDENT_EXTS:
                yield error(lexeme)
                break
        else:
            yield lexeme
