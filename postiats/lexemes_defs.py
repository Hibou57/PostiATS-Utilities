""" Lexemes base definitions for the lexemes module. """

from enum import Enum


# Definitions
# ============================================================================

# Characters
# ----------------------------------------------------------------------------

def char_range(first, last):
    """ Set of characters first..last. """
    return set(chr(c) for c in range(ord(first), ord(last) + 1))


EOF = chr(26)
EOL = "\n"
SPACE = set("\n\r\v\f\t ")
ESCAPED1 = set("ntvbrfa")
ESCAPED2 = set("\\?'\"()[]{}")
ESCAPED = ESCAPED1 | ESCAPED2
OCTAL = char_range("0", "7")
DIGIT = OCTAL | {"8", "9"}
XDIGIT2 = char_range("A", "F")
XDIGIT3 = char_range("a", "f")
XDIGIT = DIGIT | XDIGIT2 | XDIGIT3
IDENTFST1 = char_range("a", "z")
IDENTFST2 = char_range("A", "Z")
IDENTFST3 = {"_"}
IDENTFST = IDENTFST1 | IDENTFST2 | IDENTFST3
IDENTRST3 = {"'", "$"}
IDENTRST = IDENTFST | DIGIT | IDENTRST3
SYMBOLIC = set("%&+-./:=@~`^|*!?<>#")
X = set("xX")
P = set("pP")
E = set("eE")
SIGN = set("-+")
FL = set("fFlL")
LU = set("LlUu")
EXTCODE_TAG = set("#$^")
OTHERS = set("()[]{},;")


# Non‑finals
# ----------------------------------------------------------------------------

class NonFin(Enum):

    """ Non‑final lexical products. """

    ABSPROP = "ABSPROP"
    ABST0YPE = "ABST0YPE"
    ABSTYPE = "ABSTYPE"
    ABSVIEW = "ABSVIEW"
    ABSVIEWT0YPE = "ABSVIEWT0YPE"
    ABSVIEWTYPE = "ABSVIEWTYPE"
    CASE = "CASE"
    CASE_neg = "CASE_neg"
    CASE_pos = "CASE_pos"
    CASTFN = "CASTFN"
    COMMENT_block_c = "COMMENT_block_c"
    COMMENT_block_ml = "COMMENT_block_ml"
    DATAPROP = "DATAPROP"
    DATATYPE = "DATATYPE"
    DATAVIEW = "DATAVIEW"
    DATAVTYPE = "DATAVTYPE"
    DLRDELAY = "DLRDELAY"
    DLREFFMASK_ALL = "DLREFFMASK_ALL"
    DLREFFMASK_EXN = "DLREFFMASK_EXN"
    DLREFFMASK_NTM = "DLREFFMASK_NTM"
    DLREFFMASK_REF = "DLREFFMASK_REF"
    DLREFFMASK_WRT = "DLREFFMASK_WRT"
    DLRLDELAY = "DLRLDELAY"
    DLRLST = "DLRLST"
    DLRLST_T = "DLRLST_T"
    DLRLST_VT = "DLRLST_VT"
    DLRREC = "DLRREC"
    DLRREC_T = "DLRREC_T"
    DLRREC_VT = "DLRREC_VT"
    DLRTUP = "DLRTUP"
    DLRTUP_T = "DLRTUP_T"
    DLRTUP_VT = "DLRTUP_VT"
    DLRVCOPYENV_V = "DLRVCOPYENV_V"
    DLRVCOPYENV_VT = "DLRVCOPYENV_VT"
    FIX = "FIX"
    FIXAT = "FIXAT"
    FN = "FN"
    FNX = "FNX"
    FUN = "FUN"
    IMPLEMENT = "IMPLEMENT"
    IMPLMNT = "IMPLMNT"
    INFIX = "INFIX"
    INFIXL = "INFIXL"
    INFIXR = "INFIXR"
    LAM = "LAM"
    LAMAT = "LAMAT"
    LLAM = "LLAM"
    LLAMAT = "LLAMAT"
    MACDEF = "MACDEF"
    MACRODEF = "MACRODEF"
    POSTFIX = "POSTFIX"
    PRAXI = "PRAXI"
    PREFIX = "PREFIX"
    PRFN = "PRFN"
    PRFUN = "PRFUN"
    PRIMPLMNT = "PRIMPLMNT"
    PROP = "PROP"
    PROPDEF = "PROPDEF"
    PROP_neg = "PROP_neg"
    PROP_pos = "PROP_pos"
    PRVAL = "PRVAL"
    PRVAR = "PRVAR"
    T0YPE = "T0YPE"
    T0YPE_neg = "T0YPE_neg"
    T0YPE_pos = "T0YPE_pos"
    TYPE = "TYPE"
    TYPEDEF = "TYPEDEF"
    TYPE_neg = "TYPE_neg"
    TYPE_pos = "TYPE_pos"
    VAL = "VAL"
    VAL_neg = "VAL_neg"
    VAL_pos = "VAL_pos"
    VAR = "VAR"
    VIEW = "VIEW"
    VIEWDEF = "VIEWDEF"
    VIEW_neg = "VIEW_neg"
    VIEW_pos = "VIEW_pos"
    VIEWT0YPE = "VIEWT0YPE"
    VIEWT0YPE_neg = "VIEWT0YPE_neg"
    VIEWT0YPE_pos = "VIEWT0YPE_pos"
    VIEWTYPE = "VIEWTYPE"
    VIEWTYPEDEF = "VIEWTYPEDEF"
    VIEWTYPE_neg = "VIEWTYPE_neg"
    VIEWTYPE_pos = "VIEWTYPE_pos"
    WITHPROP = "WITHPROP"
    WITHTYPE = "WITHTYPE"
    WITHVIEW = "WITHVIEW"
    WITHVIEWTYPE = "WITHVIEWTYPE"


# Finals
# ----------------------------------------------------------------------------

class Fin(Enum):

    """ Final lexical products. """

    T_ABSTYPE = "T_ABSTYPE"
    T_ADDRAT = "T_ADDRAT"
    T_ADDR_OR_IDENT = "T_ADDR_OR_IDENT"  # Renamed
    T_AND = "T_AND"
    T_ASSUME = "T_ASSUME"
    T_AS = "T_AS"
    T_ATLBRACE = "T_ATLBRACE"
    T_ATLBRACKET = "T_ATLBRACKET"
    T_ATLPAREN = "T_ATLPAREN"
    T_AT_OR_SIDENT = "T_AT_OR_SIDENT"  # Renamed
    T_BACKSLASH_OR_IDENT = "T_BACKSLASH_OR_IDENT"  # Renamed
    T_BANG_OR_IDENT = "T_BANG_OR_IDENT"  # Renamed
    T_BAR = "T_BAR"
    T_BEGIN = "T_BEGIN"
    T_BQUOTELPAREN = "T_BQUOTELPAREN"
    T_BQUOTE = "T_BQUOTE"
    T_CASE = "T_CASE"
    T_CHAR = "T_CHAR"
    T_CLASSDEC = "T_CLASSDEC"
    T_COLONLT = "T_COLONLT"
    T_COLON = "T_COLON"
    T_COMMALPAREN = "T_COMMALPAREN"
    T_COMMA = "T_COMMA"
    T_COMMENT_block = "T_COMMENT_block"
    T_COMMENT_line = "T_COMMENT_line"
    T_COMMENT_rest = "T_COMMENT_rest"
    T_DATASORT = "T_DATASORT"
    T_DATATYPE = "T_DATATYPE"
    T_DLRARRPSZ = "T_DLRARRPSZ"
    T_DLRBREAK = "T_DLRBREAK"
    T_DLRCONTINUE = "T_DLRCONTINUE"
    T_DLRD2CTYPE = "T_DLRD2CTYPE"
    T_DLRDELAY = "T_DLRDELAY"
    T_DLREFFMASK_ARG = "T_DLREFFMASK_ARG"
    T_DLREFFMASK = "T_DLREFFMASK"
    T_DLREXTERN = "T_DLREXTERN"
    T_DLREXTFCALL = "T_DLREXTFCALL"
    T_DLREXTKIND = "T_DLREXTKIND"
    T_DLREXTMCALL = "T_DLREXTMCALL"
    T_DLREXTVAL = "T_DLREXTVAL"
    T_DLREXTYPE_STRUCT = "T_DLREXTYPE_STRUCT"
    T_DLREXTYPE = "T_DLREXTYPE"
    T_DLRLITERAL = "T_DLRLITERAL"
    T_DLRLST = "T_DLRLST"
    T_DLRMYFILENAME = "T_DLRMYFILENAME"
    T_DLRMYFUNCTION = "T_DLRMYFUNCTION"
    T_DLRMYLOCATION = "T_DLRMYLOCATION"
    T_DLRRAISE = "T_DLRRAISE"
    T_DLRREC = "T_DLRREC"
    T_DLRSHOWTYPE = "T_DLRSHOWTYPE"
    T_DLRSOLASSERT = "T_DLRSOLASSERT"
    T_DLRSOLVERIFY = "T_DLRSOLVERIFY"
    T_DLRTEMPENVER = "T_DLRTEMPENVER"
    T_DLRTUP = "T_DLRTUP"
    T_DLRTYREP = "T_DLRTYREP"
    T_DLRVARARG = "T_DLRVARARG"
    T_DLRVCOPYENV = "T_DLRVCOPYENV"
    T_DOLLAR = "T_DOLLAR"
    T_DO = "T_DO"
    T_DOTDOTDOT = "T_DOTDOTDOT"
    T_DOTDOT = "T_DOTDOT"
    T_DOTINT = "T_DOTINT"
    T_DOTLTGTDOT = "T_DOTLTGTDOT"
    T_DOTLT = "T_DOTLT"
    T_DOT = "T_DOT"
    T_ELSE = "T_ELSE"
    T_END = "T_END"
    T_EOF = "T_EOF"
    T_EQGTGT = "T_EQGTGT"
    T_EQGT = "T_EQGT"
    T_EQLTGT = "T_EQLTGT"
    T_EQLT = "T_EQLT"
    T_EQSLASHEQGTGT = "T_EQSLASHEQGTGT"
    T_EQSLASHEQGT = "T_EQSLASHEQGT"
    T_EQ_OR_DIDENT = "T_EQ_OR_DIDENT"  # Renamed
    T_ERR = "T_ERR"
    T_EXCEPTION = "T_EXCEPTION"
    T_EXTCODE = "T_EXTCODE"
    T_EXTERN = "T_EXTERN"
    T_EXTVAR = "T_EXTVAR"
    T_EXTYPE = "T_EXTYPE"
    T_FIXITY = "T_FIXITY"
    T_FIX = "T_FIX"
    T_FLOAT = "T_FLOAT"
    T_FOLDAT = "T_FOLDAT"
    T_FOLD_OR_IDENT = "T_FOLD_OR_IDENT"  # Renamed
    T_FORSTAR = "T_FORSTAR"
    T_FOR = "T_FOR"
    T_FREEAT = "T_FREEAT"
    T_FREE_OR_IDENT = "T_FREE_OR_IDENT"  # Renamed
    T_FUN = "T_FUN"
    T_GTDOT = "T_GTDOT"
    T_GTLT_OR_DIDENT = "T_GTLT_OR_DIDENT"  # Renamed
    T_GT_OR_IDENT = "T_GT_OR_IDENT"  # Renamed
    T_HASHLBRACKET = "T_HASHLBRACKET"
    T_HASH = "T_HASH"
    T_IDENT_alp = "T_IDENT_alp"
    T_IDENT_arr = "T_IDENT_arr"
    T_IDENT_dlr = "T_IDENT_dlr"
    T_IDENT_ext = "T_IDENT_ext"
    T_IDENT_srp = "T_IDENT_srp"
    T_IDENT_sym = "T_IDENT_sym"
    T_IDENT_tmp = "T_IDENT_tmp"
    T_IFCASE = "T_IFCASE"
    T_IF = "T_IF"
    T_IMPLEMENT = "T_IMPLEMENT"
    T_IMPORT = "T_IMPORT"
    T_INT = "T_INT"
    T_IN = "T_IN"
    T_INTZERO = "T_INTZERO"
    T_LAM = "T_LAM"
    T_LBRACE = "T_LBRACE"
    T_LBRACKET = "T_LBRACKET"
    T_LET = "T_LET"
    T_LOCAL = "T_LOCAL"
    T_LPAREN = "T_LPAREN"
    T_LT_OR_IDENT = "T_LT_OR_IDENT"  # Renamed
    T_MACDEF = "T_MACDEF"
    T_MINUSGT_OR_SIDENT = "T_MINUSGT_OR_SIDENT"  # Renamed
    T_MINUSLTGT = "T_MINUSLTGT"
    T_MINUSLT = "T_MINUSLT"
    T_NONFIX = "T_NONFIX"
    T_OF = "T_OF"
    T_OP = "T_OP"
    T_OVERLOAD = "T_OVERLOAD"
    T_PERCENTLPAREN = "T_PERCENTLPAREN"
    T_PERCENT_OR_IDENT = "T_PERCENT_OR_IDENT"  # Renamed
    T_QMARK_OR_IDENT = "T_QMARK_OR_IDENT"  # Renamed
    T_QUOTELBRACE = "T_QUOTELBRACE"
    T_QUOTELBRACKET = "T_QUOTELBRACKET"
    T_QUOTELPAREN = "T_QUOTELPAREN"
    T_RBRACE = "T_RBRACE"
    T_RBRACKET = "T_RBRACKET"
    T_REASSUME = "T_REASSUME"
    T_REC = "T_REC"
    T_RPAREN = "T_RPAREN"
    T_SCASE = "T_SCASE"
    T_SEMICOLON = "T_SEMICOLON"
    T_SIF = "T_SIF"
    T_SORTDEF = "T_SORTDEF"
    T_SPACE = "T_SPACE"
    T_SRPASSERT = "T_SRPASSERT"
    T_SRPCODEGEN2 = "T_SRPCODEGEN2"
    T_SRPDEFINE = "T_SRPDEFINE"
    T_SRPDYNLOAD = "T_SRPDYNLOAD"
    T_SRPELIFDEF = "T_SRPELIFDEF"
    T_SRPELIFNDEF = "T_SRPELIFNDEF"
    T_SRPELIF = "T_SRPELIF"
    T_SRPELSE = "T_SRPELSE"
    T_SRPENDIF = "T_SRPENDIF"
    T_SRPERROR = "T_SRPERROR"
    T_SRPIFDEF = "T_SRPIFDEF"
    T_SRPIFNDEF = "T_SRPIFNDEF"
    T_SRPIF = "T_SRPIF"
    T_SRPINCLUDE = "T_SRPINCLUDE"
    T_SRPPRAGMA = "T_SRPPRAGMA"
    T_SRPPRERR = "T_SRPPRERR"
    T_SRPPRINT = "T_SRPPRINT"
    T_SRPREQUIRE = "T_SRPREQUIRE"
    T_SRPSTALOAD = "T_SRPSTALOAD"
    T_SRPTHEN = "T_SRPTHEN"
    T_SRPUNDEF = "T_SRPUNDEF"
    T_STACST = "T_STACST"
    T_STADEF = "T_STADEF"
    T_STATIC = "T_STATIC"
    T_STRING = "T_STRING"
    T_SYMELIM = "T_SYMELIM"
    T_SYMINTR = "T_SYMINTR"
    T_THEN = "T_THEN"
    T_TILDE_OR_IDENT = "T_TILDE_OR_IDENT"  # Renamed
    T_TKINDEF = "T_TKINDEF"
    T_TRY = "T_TRY"
    T_TYPEDEF = "T_TYPEDEF"
    T_TYPE = "T_TYPE"
    T_TYPE_OR_IDENT = "T_TYPE_OR_IDENT"  # Added
    T_VAL = "T_VAL"
    T_VAR = "T_VAR"
    T_VIEWAT = "T_VIEWAT"
    T_WHEN = "T_WHEN"
    T_WHERE = "T_WHERE"
    T_WHILESTAR = "T_WHILESTAR"
    T_WHILE = "T_WHILE"
    T_WITH = "T_WITH"
    T_WITHTYPE = "T_WITHTYPE"


# Translation of non‑finals to finals
# ----------------------------------------------------------------------------

NONFINS_TRANSL = {
    NonFin.ABSPROP: Fin.T_ABSTYPE,
    NonFin.ABST0YPE: Fin.T_ABSTYPE,
    NonFin.ABSTYPE: Fin.T_ABSTYPE,
    NonFin.ABSVIEWT0YPE: Fin.T_ABSTYPE,
    NonFin.ABSVIEW: Fin.T_ABSTYPE,
    NonFin.ABSVIEWTYPE: Fin.T_ABSTYPE,
    NonFin.CASE_neg: Fin.T_CASE,
    NonFin.CASE_pos: Fin.T_CASE,
    NonFin.CASE: Fin.T_CASE,
    NonFin.CASTFN: Fin.T_FUN,
    NonFin.COMMENT_block_c: Fin.T_COMMENT_block,
    NonFin.COMMENT_block_ml: Fin.T_COMMENT_block,
    NonFin.DATAPROP: Fin.T_DATATYPE,
    NonFin.DATATYPE: Fin.T_DATATYPE,
    NonFin.DATAVIEW: Fin.T_DATATYPE,
    NonFin.DATAVTYPE: Fin.T_DATATYPE,
    NonFin.DLRDELAY: Fin.T_DLRDELAY,
    NonFin.DLREFFMASK_ALL: Fin.T_DLREFFMASK_ARG,
    NonFin.DLREFFMASK_EXN: Fin.T_DLREFFMASK_ARG,
    NonFin.DLREFFMASK_NTM: Fin.T_DLREFFMASK_ARG,
    NonFin.DLREFFMASK_REF: Fin.T_DLREFFMASK_ARG,
    NonFin.DLREFFMASK_WRT: Fin.T_DLREFFMASK_ARG,
    NonFin.DLRLDELAY: Fin.T_DLRDELAY,
    NonFin.DLRLST: Fin.T_DLRLST,
    NonFin.DLRLST_T: Fin.T_DLRLST,
    NonFin.DLRLST_VT: Fin.T_DLRLST,
    NonFin.DLRREC: Fin.T_DLRREC,
    NonFin.DLRREC_T: Fin.T_DLRREC,
    NonFin.DLRREC_VT: Fin.T_DLRREC,
    NonFin.DLRTUP: Fin.T_DLRTUP,
    NonFin.DLRTUP_T: Fin.T_DLRTUP,
    NonFin.DLRTUP_VT: Fin.T_DLRTUP,
    NonFin.DLRVCOPYENV_V: Fin.T_DLRVCOPYENV,
    NonFin.DLRVCOPYENV_VT: Fin.T_DLRVCOPYENV,
    NonFin.FIXAT: Fin.T_FIX,
    NonFin.FIX: Fin.T_FIX,
    NonFin.FN: Fin.T_FUN,
    NonFin.FNX: Fin.T_FUN,
    NonFin.FUN: Fin.T_FUN,
    NonFin.IMPLEMENT: Fin.T_IMPLEMENT,
    NonFin.IMPLMNT: Fin.T_IMPLEMENT,
    NonFin.INFIXL: Fin.T_FIXITY,
    NonFin.INFIXR: Fin.T_FIXITY,
    NonFin.INFIX: Fin.T_FIXITY,
    NonFin.LAMAT: Fin.T_LAM,
    NonFin.LAM: Fin.T_LAM,
    NonFin.LLAMAT: Fin.T_LAM,
    NonFin.LLAM: Fin.T_LAM,
    NonFin.MACDEF: Fin.T_MACDEF,
    NonFin.MACRODEF: Fin.T_MACDEF,
    NonFin.POSTFIX: Fin.T_FIXITY,
    NonFin.PRAXI: Fin.T_FUN,
    NonFin.PREFIX: Fin.T_FIXITY,
    NonFin.PRFN: Fin.T_FUN,
    NonFin.PRFUN: Fin.T_FUN,
    NonFin.PRIMPLMNT: Fin.T_IMPLEMENT,
    NonFin.PROPDEF: Fin.T_TYPEDEF,
    NonFin.PROP_neg: Fin.T_TYPE,
    NonFin.PROP_pos: Fin.T_TYPE,
    NonFin.PROP: Fin.T_TYPE_OR_IDENT,
    NonFin.PRVAL: Fin.T_VAL,
    NonFin.PRVAR: Fin.T_VAR,
    NonFin.T0YPE_neg: Fin.T_TYPE,
    NonFin.T0YPE_pos: Fin.T_TYPE,
    NonFin.T0YPE: Fin.T_TYPE,
    NonFin.TYPEDEF: Fin.T_TYPEDEF,
    NonFin.TYPE_neg: Fin.T_TYPE,
    NonFin.TYPE_pos: Fin.T_TYPE,
    NonFin.TYPE: Fin.T_TYPE_OR_IDENT,
    NonFin.VAL_neg: Fin.T_VAL,
    NonFin.VAL_pos: Fin.T_VAL,
    NonFin.VAL: Fin.T_VAL,
    NonFin.VAR: Fin.T_VAR,
    NonFin.VIEWDEF: Fin.T_TYPEDEF,
    NonFin.VIEW_neg: Fin.T_TYPE,
    NonFin.VIEW_pos: Fin.T_TYPE,
    NonFin.VIEWT0YPE_neg: Fin.T_TYPE,
    NonFin.VIEWT0YPE_pos: Fin.T_TYPE,
    NonFin.VIEWT0YPE: Fin.T_TYPE,
    NonFin.VIEW: Fin.T_TYPE_OR_IDENT,
    NonFin.VIEWTYPEDEF: Fin.T_TYPEDEF,
    NonFin.VIEWTYPE_neg: Fin.T_TYPE,
    NonFin.VIEWTYPE_pos: Fin.T_TYPE,
    NonFin.VIEWTYPE: Fin.T_TYPE_OR_IDENT,
    NonFin.WITHPROP: Fin.T_WITHTYPE,
    NonFin.WITHTYPE: Fin.T_WITHTYPE,
    NonFin.WITHVIEW: Fin.T_WITHTYPE,
    NonFin.WITHVIEWTYPE: Fin.T_WITHTYPE}


assert all(isinstance(x, NonFin) for x in NONFINS_TRANSL)
assert all(isinstance(x, Fin) for x in NONFINS_TRANSL.values())
assert all(x in NONFINS_TRANSL for x in NonFin)


# Translation of some idents to products
# ----------------------------------------------------------------------------

IDENTS_TRANSL = {

    # Finals

    "and": Fin.T_AND,
    "as": Fin.T_AS,
    "assume": Fin.T_ASSUME,
    "absimpl": Fin.T_ASSUME,
    "@": Fin.T_AT_OR_SIDENT,
    "!": Fin.T_BANG_OR_IDENT,
    "|": Fin.T_BAR,
    "begin": Fin.T_BEGIN,
    "`": Fin.T_BQUOTE,
    "classdec": Fin.T_CLASSDEC,
    ":": Fin.T_COLON,
    "datasort": Fin.T_DATASORT,
    "$arrpsz": Fin.T_DLRARRPSZ,
    "$arrptrsize": Fin.T_DLRARRPSZ,
    "$break": Fin.T_DLRBREAK,
    "$continue": Fin.T_DLRCONTINUE,
    "$d2ctype": Fin.T_DLRD2CTYPE,
    "$effmask": Fin.T_DLREFFMASK,
    "$extern": Fin.T_DLREXTERN,
    "$extfcall": Fin.T_DLREXTFCALL,
    "$extkind": Fin.T_DLREXTKIND,
    "$extmcall": Fin.T_DLREXTMCALL,
    "$extval": Fin.T_DLREXTVAL,
    "$extype": Fin.T_DLREXTYPE,
    "$extype_struct": Fin.T_DLREXTYPE_STRUCT,
    "$literal": Fin.T_DLRLITERAL,
    "$myfilename": Fin.T_DLRMYFILENAME,
    "$myfunction": Fin.T_DLRMYFUNCTION,
    "$mylocation": Fin.T_DLRMYLOCATION,
    "$raise": Fin.T_DLRRAISE,
    "$showtype": Fin.T_DLRSHOWTYPE,
    "$solver_assert": Fin.T_DLRSOLASSERT,
    "$solver_verify": Fin.T_DLRSOLVERIFY,
    "$tempenver": Fin.T_DLRTEMPENVER,
    "$tyrep": Fin.T_DLRTYREP,
    "$vararg": Fin.T_DLRVARARG,
    "do": Fin.T_DO,
    "$": Fin.T_DOLLAR,
    ".": Fin.T_DOT,
    "..": Fin.T_DOTDOT,
    "...": Fin.T_DOTDOTDOT,
    ".<>.": Fin.T_DOTLTGTDOT,
    ".<": Fin.T_DOTLT,
    "else": Fin.T_ELSE,
    "end": Fin.T_END,
    "=": Fin.T_EQ_OR_DIDENT,
    "=>": Fin.T_EQGT,
    "=>>": Fin.T_EQGTGT,
    "=<": Fin.T_EQLT,
    "=<>": Fin.T_EQLTGT,
    "=/=>": Fin.T_EQSLASHEQGT,
    "=/=>>": Fin.T_EQSLASHEQGTGT,
    "exception": Fin.T_EXCEPTION,
    "extern": Fin.T_EXTERN,
    "extvar": Fin.T_EXTVAR,
    "extype": Fin.T_EXTYPE,
    ">.": Fin.T_GTDOT,
    ">": Fin.T_GT_OR_IDENT,
    "><": Fin.T_GTLT_OR_DIDENT,
    "#": Fin.T_HASH,
    "ifcase": Fin.T_IFCASE,
    "if": Fin.T_IF,
    "import": Fin.T_IMPORT,
    "in": Fin.T_IN,
    "let": Fin.T_LET,
    "local": Fin.T_LOCAL,
    "<": Fin.T_LT_OR_IDENT,
    "->": Fin.T_MINUSGT_OR_SIDENT,
    "-<": Fin.T_MINUSLT,
    "-<>": Fin.T_MINUSLTGT,
    "nonfix": Fin.T_NONFIX,
    "of": Fin.T_OF,
    "op": Fin.T_OP,
    "overload": Fin.T_OVERLOAD,
    "%": Fin.T_PERCENT_OR_IDENT,
    "?": Fin.T_QMARK_OR_IDENT,
    "reassume": Fin.T_REASSUME,
    "absreimpl": Fin.T_REASSUME,
    "rec": Fin.T_REC,
    "scase": Fin.T_SCASE,
    "sif": Fin.T_SIF,
    "sortdef": Fin.T_SORTDEF,
    "#assert": Fin.T_SRPASSERT,
    "#codegen2": Fin.T_SRPCODEGEN2,
    "#define": Fin.T_SRPDEFINE,
    "dynload": Fin.T_SRPDYNLOAD,
    "#dynload": Fin.T_SRPDYNLOAD,
    "#elifdef": Fin.T_SRPELIFDEF,
    "#elif": Fin.T_SRPELIF,
    "#elifndef": Fin.T_SRPELIFNDEF,
    "#else": Fin.T_SRPELSE,
    "#endif": Fin.T_SRPENDIF,
    "#error": Fin.T_SRPERROR,
    "#ifdef": Fin.T_SRPIFDEF,
    "#if": Fin.T_SRPIF,
    "#ifndef": Fin.T_SRPIFNDEF,
    "#include": Fin.T_SRPINCLUDE,
    "#pragma": Fin.T_SRPPRAGMA,
    "#prerr": Fin.T_SRPPRERR,
    "#print": Fin.T_SRPPRINT,
    "#require": Fin.T_SRPREQUIRE,
    "staload": Fin.T_SRPSTALOAD,
    "#staload": Fin.T_SRPSTALOAD,
    "#then": Fin.T_SRPTHEN,
    "#undef": Fin.T_SRPUNDEF,
    "sta": Fin.T_STACST,
    "stacst": Fin.T_STACST,
    "stadef": Fin.T_STADEF,
    "static": Fin.T_STATIC,
    "symelim": Fin.T_SYMELIM,
    "symintr": Fin.T_SYMINTR,
    "then": Fin.T_THEN,
    "~": Fin.T_TILDE_OR_IDENT,
    "tkindef": Fin.T_TKINDEF,
    "try": Fin.T_TRY,
    "when": Fin.T_WHEN,
    "where": Fin.T_WHERE,
    "with": Fin.T_WITH,

    # Non‑finals

    "absprop": NonFin.ABSPROP,
    "abst0ype": NonFin.ABST0YPE,
    "abstflat": NonFin.ABST0YPE,
    "abstbox": NonFin.ABSTYPE,
    "abstype": NonFin.ABSTYPE,
    "absview": NonFin.ABSVIEW,
    "absviewt0ype": NonFin.ABSVIEWT0YPE,
    "absvt0ype": NonFin.ABSVIEWT0YPE,
    "absvtflat": NonFin.ABSVIEWT0YPE,
    "absviewtype": NonFin.ABSVIEWTYPE,
    "absvtbox": NonFin.ABSVIEWTYPE,
    "absvtype": NonFin.ABSVIEWTYPE,
    "castfn": NonFin.CASTFN,
    "dataprop": NonFin.DATAPROP,
    "datatype": NonFin.DATATYPE,
    "dataview": NonFin.DATAVIEW,
    "dataviewtype": NonFin.DATAVTYPE,
    "datavtype": NonFin.DATAVTYPE,
    "$delay": NonFin.DLRDELAY,
    "$effmask_all": NonFin.DLREFFMASK_ALL,
    "$effmask_exn": NonFin.DLREFFMASK_EXN,
    "$effmask_ntm": NonFin.DLREFFMASK_NTM,
    "$effmask_ref": NonFin.DLREFFMASK_REF,
    "$effmask_wrt": NonFin.DLREFFMASK_WRT,
    "$ldelay": NonFin.DLRLDELAY,
    "$list": NonFin.DLRLST,
    "$lst": NonFin.DLRLST,
    "$list_t": NonFin.DLRLST_T,
    "$lst_t": NonFin.DLRLST_T,
    "$list_vt": NonFin.DLRLST_VT,
    "$lst_vt": NonFin.DLRLST_VT,
    "$rec": NonFin.DLRREC,
    "$record": NonFin.DLRREC,
    "$record_t": NonFin.DLRREC_T,
    "$rec_t": NonFin.DLRREC_T,
    "$record_vt": NonFin.DLRREC_VT,
    "$rec_vt": NonFin.DLRREC_VT,
    "$tuple_t": NonFin.DLRTUP_T,
    "$tup_t": NonFin.DLRTUP_T,
    "$tup": NonFin.DLRTUP,
    "$tuple": NonFin.DLRTUP,
    "$tuple_vt": NonFin.DLRTUP_VT,
    "$tup_vt": NonFin.DLRTUP_VT,
    "$vcopyenv_vt": NonFin.DLRVCOPYENV_VT,
    "$vcopyenv_v": NonFin.DLRVCOPYENV_V,
    "fn": NonFin.FN,
    "fnx": NonFin.FNX,
    "fun": NonFin.FUN,
    "implement": NonFin.IMPLEMENT,
    "implmnt": NonFin.IMPLMNT,
    "infix": NonFin.INFIX,
    "infixl": NonFin.INFIXL,
    "infixr": NonFin.INFIXR,
    "macdef": NonFin.MACDEF,
    "macrodef": NonFin.MACRODEF,
    "postfix": NonFin.POSTFIX,
    "praxi": NonFin.PRAXI,
    "prefix": NonFin.PREFIX,
    "prfn": NonFin.PRFN,
    "prfun": NonFin.PRFUN,
    "primplement": NonFin.PRIMPLMNT,
    "primplmnt": NonFin.PRIMPLMNT,
    "propdef": NonFin.PROPDEF,
    "prval": NonFin.PRVAL,
    "prvar": NonFin.PRVAR,
    "typedef": NonFin.TYPEDEF,
    "var": NonFin.VAR,
    "viewdef": NonFin.VIEWDEF,
    "viewtypedef": NonFin.VIEWTYPEDEF,
    "vtypedef": NonFin.VIEWTYPEDEF,
    "withprop": NonFin.WITHPROP,
    "withtype": NonFin.WITHTYPE,
    "withviewtype": NonFin.WITHVIEWTYPE,
    "withvtype": NonFin.WITHVIEWTYPE,
    "withview": NonFin.WITHVIEW,

    # Added

    "case": NonFin.CASE,
    "prop": NonFin.PROP,
    "type": NonFin.TYPE,
    "t0ype": NonFin.T0YPE,
    "vtype": NonFin.VIEWTYPE,
    "vt0ype": NonFin.VIEWT0YPE,
    "view": NonFin.VIEW,
    "viewtype": NonFin.VIEWTYPE,
    "viewt0ype": NonFin.VIEWT0YPE,
    "val": NonFin.VAL,
    "for": Fin.T_FOR,
    "while": Fin.T_WHILE,
    "addr": Fin.T_ADDR_OR_IDENT,
    "fold": Fin.T_FOLD_OR_IDENT,
    "free": Fin.T_FREE_OR_IDENT,
    "lam": NonFin.LAM,
    "llam": NonFin.LLAM,
    "fix": NonFin.FIX}

assert all(isinstance(x, str) for x in IDENTS_TRANSL)
assert all(isinstance(x, (Fin, NonFin)) for x in IDENTS_TRANSL.values())


def ident_translation(ident, default, in_feffs):
    """ Ident possibly translated after IDENTS_TRANSL. """
    if in_feffs:
        # Only apply this single translation when in function effects.
        if default == Fin.T_IDENT_sym and ident == ">":
            return Fin.T_GT_OR_IDENT
        return default
    return IDENTS_TRANSL[ident] if ident in IDENTS_TRANSL else default


# Prefixes
# ----------------------------------------------------------------------------

# ### Types

class TreeNode:

    """ Prefix table as a tree. """

    __slots__ = ["next", "product"]

    def __init__(self):

        self.next = dict()  # char -> TreeNode.
        self.product = None  # Fin, NonFin, Start or None.


def add_to_tree(tree, prefix, product):
    """ Add prefix as a branch of tree. """
    node = tree
    for c in prefix:
        if c not in node.next:
            node.next[c] = TreeNode()
        node = node.next[c]
    assert node.product is None  # Unique definitions: no ambigous prefixes.
    node.product = product


def tree_step(node, c):
    """ Step in tree by c from node (transition on c). """
    if c not in node.next:
        return None
    return node.next[c]


# ### Further processing interpretation

class Start(Enum):

    """ Interpretations of some prefixes. """

    CHAR_start = "CHAR_start"
    COMMENT_block_c_start = "COMMENT_block_c_start"
    COMMENT_block_ml_start = "COMMENT_block_ml_start"
    COMMENT_line_start = "COMMENT_line_start"
    COMMENT_rest_start = "COMMENT_rest_start"
    DOTINT_start = "DOTINT_start"
    FLOAT_dec_start = "FLOAT_dec_start"
    IDENT_dlr_start = "IDENT_dlr_start"
    IDENT_srp_start = "IDENT_srp_start"
    IDENT_sym_start = "IDENT_sym_start"
    IDENT_xx_start = "IDENT_xx_start"
    INT_oct_start = "INT_oct_start"
    QMARKGT_start = "QMARKGT_start"
    STRING_start = "STRING_start"
    XX_dec_start = "XX_dec_start"
    XX_hex_start = "XX_hex_start"


# ### Prefixes lookup table as a tree

TREE = TreeNode()


def add_prefix(prefix, product):
    """ Add to TREE. """
    assert isinstance(product, (Fin, Start)) or product in NONFINS_TRANSL
    add_to_tree(TREE, prefix, product)


def add_prefixes2(char1, char2_set, product):
    """ Add "c1" + "c21".."c2n" to TREE. """
    for char2 in char2_set:
        add_prefix(char1 + char2, product)


def add_prefixes1(char1_set, product):
    """ Add "c11".."c1n" to TREE. """
    for char1 in char1_set:
        add_prefix(char1, product)


# Some prefixes are a product on their own, some prefix starts a product.

add_prefix(EOF, Fin.T_EOF)

# Fin, sorted by "XX"

add_prefix("0", Fin.T_INTZERO)
add_prefix("addr@", Fin.T_ADDRAT)
add_prefix("fold@", Fin.T_FOLDAT)
add_prefix("for*", Fin.T_FORSTAR)
add_prefix("free@", Fin.T_FREEAT)
add_prefix("view@", Fin.T_VIEWAT)
add_prefix("while*", Fin.T_WHILESTAR)
add_prefix("@{", Fin.T_ATLBRACE)
add_prefix("@[", Fin.T_ATLBRACKET)
add_prefix("@(", Fin.T_ATLPAREN)
add_prefix("\\", Fin.T_BACKSLASH_OR_IDENT)
add_prefix("`(", Fin.T_BQUOTELPAREN)
add_prefix(":<", Fin.T_COLONLT)
add_prefix(",", Fin.T_COMMA)
add_prefix(",(", Fin.T_COMMALPAREN)
add_prefix("#[", Fin.T_HASHLBRACKET)
add_prefix("$", Fin.T_IDENT_sym)
add_prefix("{", Fin.T_LBRACE)
add_prefix("[", Fin.T_LBRACKET)
add_prefix("(", Fin.T_LPAREN)
add_prefix("%(", Fin.T_PERCENTLPAREN)
add_prefix("'{", Fin.T_QUOTELBRACE)
add_prefix("'[", Fin.T_QUOTELBRACKET)
add_prefix("'(", Fin.T_QUOTELPAREN)
add_prefix("}", Fin.T_RBRACE)
add_prefix("]", Fin.T_RBRACKET)
add_prefix(")", Fin.T_RPAREN)
add_prefix(";", Fin.T_SEMICOLON)

# NonFin, Sorted by "XX"

add_prefix("abst@ype", NonFin.ABST0YPE)
add_prefix("absviewt@ype", NonFin.ABSVIEWT0YPE)
add_prefix("absvt@ype", NonFin.ABSVIEWT0YPE)
add_prefix("case-", NonFin.CASE_neg)
add_prefix("case+", NonFin.CASE_pos)
add_prefix("fix@", NonFin.FIXAT)
add_prefix("lam@", NonFin.LAMAT)
add_prefix("llam@", NonFin.LLAMAT)
add_prefix("prop-", NonFin.PROP_neg)
add_prefix("prop+", NonFin.PROP_pos)
add_prefix("t0ype-", NonFin.T0YPE_neg)
add_prefix("t0ype+", NonFin.T0YPE_pos)
add_prefix("t@ype", NonFin.T0YPE)
add_prefix("t@ype-", NonFin.T0YPE_neg)
add_prefix("t@ype+", NonFin.T0YPE_pos)
add_prefix("type-", NonFin.TYPE_neg)
add_prefix("type+", NonFin.TYPE_pos)
add_prefix("val-", NonFin.VAL_neg)
add_prefix("val+", NonFin.VAL_pos)
add_prefix("view-", NonFin.VIEW_neg)
add_prefix("view+", NonFin.VIEW_pos)
add_prefix("viewt0ype-", NonFin.VIEWT0YPE_neg)
add_prefix("viewt0ype+", NonFin.VIEWT0YPE_pos)
add_prefix("viewt@ype", NonFin.VIEWT0YPE)
add_prefix("viewt@ype-", NonFin.VIEWT0YPE_neg)
add_prefix("viewt@ype+", NonFin.VIEWT0YPE_pos)
add_prefix("viewtype-", NonFin.VIEWTYPE_neg)
add_prefix("viewtype+", NonFin.VIEWTYPE_pos)
add_prefix("vt0ype-", NonFin.VIEWT0YPE_neg)
add_prefix("vt0ype+", NonFin.VIEWT0YPE_pos)
add_prefix("vt@ype", NonFin.VIEWT0YPE)
add_prefix("vt@ype-", NonFin.VIEWT0YPE_neg)
add_prefix("vtype-", NonFin.VIEWTYPE_neg)
add_prefix("vt@ype+", NonFin.VIEWT0YPE_pos)
add_prefix("vtype+", NonFin.VIEWTYPE_pos)

# Start, Sorted by Start.XX

add_prefix("'", Start.CHAR_start)
add_prefix("/*", Start.COMMENT_block_c_start)
add_prefix("(*", Start.COMMENT_block_ml_start)
add_prefix("//", Start.COMMENT_line_start)
add_prefix("////", Start.COMMENT_rest_start)
add_prefixes2(".", DIGIT, Start.DOTINT_start)
add_prefix("0.", Start.FLOAT_dec_start)
add_prefixes2("0", E, Start.FLOAT_dec_start)
add_prefixes2("$", IDENTFST, Start.IDENT_dlr_start)
add_prefixes2("#", IDENTFST, Start.IDENT_srp_start)
add_prefixes2("$", SYMBOLIC, Start.IDENT_sym_start)
add_prefixes1(SYMBOLIC, Start.IDENT_sym_start)
add_prefixes1(IDENTFST, Start.IDENT_xx_start)
add_prefixes2("0", OCTAL, Start.INT_oct_start)
add_prefix('?>', Start.QMARKGT_start)
add_prefix('"', Start.STRING_start)
add_prefixes1(DIGIT - {"0"}, Start.XX_dec_start)  # "0" is another prefix.
add_prefixes2("0", X, Start.XX_hex_start)


# Additions
# ============================================================================

COMMENTS = {Fin.T_COMMENT_block, Fin.T_COMMENT_line, Fin.T_COMMENT_rest}

ERRORS = {Fin.T_IDENT_srp}

IDENT_EXTS = {
    "car!",
    "cdr!",
    "fprint!",
    "fprintln!",
    "gprint!",
    "gprintln!",
    "iscons!",
    "islist!",
    "isnil!",
    "prerr!",
    "prerrln!",
    "print!",
    "println!",
    "tupz!"}
