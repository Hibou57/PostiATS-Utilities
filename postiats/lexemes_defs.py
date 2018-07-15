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


# Non‑terminals
# ----------------------------------------------------------------------------

class NonTerm(Enum):

    """ Non terminal lexical products. """

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


# Terminals
# ----------------------------------------------------------------------------

class Term(Enum):

    """ Terminal lexical products. """

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


# Translation of non‑terminals to terminals
# ----------------------------------------------------------------------------

NONTERMS_TRANSL = {
    NonTerm.ABSPROP: Term.T_ABSTYPE,
    NonTerm.ABST0YPE: Term.T_ABSTYPE,
    NonTerm.ABSTYPE: Term.T_ABSTYPE,
    NonTerm.ABSVIEWT0YPE: Term.T_ABSTYPE,
    NonTerm.ABSVIEW: Term.T_ABSTYPE,
    NonTerm.ABSVIEWTYPE: Term.T_ABSTYPE,
    NonTerm.CASE_neg: Term.T_CASE,
    NonTerm.CASE_pos: Term.T_CASE,
    NonTerm.CASE: Term.T_CASE,
    NonTerm.CASTFN: Term.T_FUN,
    NonTerm.COMMENT_block_c: Term.T_COMMENT_block,
    NonTerm.COMMENT_block_ml: Term.T_COMMENT_block,
    NonTerm.DATAPROP: Term.T_DATATYPE,
    NonTerm.DATATYPE: Term.T_DATATYPE,
    NonTerm.DATAVIEW: Term.T_DATATYPE,
    NonTerm.DATAVTYPE: Term.T_DATATYPE,
    NonTerm.DLRDELAY: Term.T_DLRDELAY,
    NonTerm.DLREFFMASK_ALL: Term.T_DLREFFMASK_ARG,
    NonTerm.DLREFFMASK_EXN: Term.T_DLREFFMASK_ARG,
    NonTerm.DLREFFMASK_NTM: Term.T_DLREFFMASK_ARG,
    NonTerm.DLREFFMASK_REF: Term.T_DLREFFMASK_ARG,
    NonTerm.DLREFFMASK_WRT: Term.T_DLREFFMASK_ARG,
    NonTerm.DLRLDELAY: Term.T_DLRDELAY,
    NonTerm.DLRLST: Term.T_DLRLST,
    NonTerm.DLRLST_T: Term.T_DLRLST,
    NonTerm.DLRLST_VT: Term.T_DLRLST,
    NonTerm.DLRREC: Term.T_DLRREC,
    NonTerm.DLRREC_T: Term.T_DLRREC,
    NonTerm.DLRREC_VT: Term.T_DLRREC,
    NonTerm.DLRTUP: Term.T_DLRTUP,
    NonTerm.DLRTUP_T: Term.T_DLRTUP,
    NonTerm.DLRTUP_VT: Term.T_DLRTUP,
    NonTerm.DLRVCOPYENV_V: Term.T_DLRVCOPYENV,
    NonTerm.DLRVCOPYENV_VT: Term.T_DLRVCOPYENV,
    NonTerm.FIXAT: Term.T_FIX,
    NonTerm.FIX: Term.T_FIX,
    NonTerm.FN: Term.T_FUN,
    NonTerm.FNX: Term.T_FUN,
    NonTerm.FUN: Term.T_FUN,
    NonTerm.IMPLEMENT: Term.T_IMPLEMENT,
    NonTerm.IMPLMNT: Term.T_IMPLEMENT,
    NonTerm.INFIXL: Term.T_FIXITY,
    NonTerm.INFIXR: Term.T_FIXITY,
    NonTerm.INFIX: Term.T_FIXITY,
    NonTerm.LAMAT: Term.T_LAM,
    NonTerm.LAM: Term.T_LAM,
    NonTerm.LLAMAT: Term.T_LAM,
    NonTerm.LLAM: Term.T_LAM,
    NonTerm.MACDEF: Term.T_MACDEF,
    NonTerm.MACRODEF: Term.T_MACDEF,
    NonTerm.POSTFIX: Term.T_FIXITY,
    NonTerm.PRAXI: Term.T_FUN,
    NonTerm.PREFIX: Term.T_FIXITY,
    NonTerm.PRFN: Term.T_FUN,
    NonTerm.PRFUN: Term.T_FUN,
    NonTerm.PRIMPLMNT: Term.T_IMPLEMENT,
    NonTerm.PROPDEF: Term.T_TYPEDEF,
    NonTerm.PROP_neg: Term.T_TYPE,
    NonTerm.PROP_pos: Term.T_TYPE,
    NonTerm.PROP: Term.T_TYPE_OR_IDENT,
    NonTerm.PRVAL: Term.T_VAL,
    NonTerm.PRVAR: Term.T_VAR,
    NonTerm.T0YPE_neg: Term.T_TYPE,
    NonTerm.T0YPE_pos: Term.T_TYPE,
    NonTerm.T0YPE: Term.T_TYPE,
    NonTerm.TYPEDEF: Term.T_TYPEDEF,
    NonTerm.TYPE_neg: Term.T_TYPE,
    NonTerm.TYPE_pos: Term.T_TYPE,
    NonTerm.TYPE: Term.T_TYPE_OR_IDENT,
    NonTerm.VAL_neg: Term.T_VAL,
    NonTerm.VAL_pos: Term.T_VAL,
    NonTerm.VAL: Term.T_VAL,
    NonTerm.VAR: Term.T_VAR,
    NonTerm.VIEWDEF: Term.T_TYPEDEF,
    NonTerm.VIEW_neg: Term.T_TYPE,
    NonTerm.VIEW_pos: Term.T_TYPE,
    NonTerm.VIEWT0YPE_neg: Term.T_TYPE,
    NonTerm.VIEWT0YPE_pos: Term.T_TYPE,
    NonTerm.VIEWT0YPE: Term.T_TYPE,
    NonTerm.VIEW: Term.T_TYPE_OR_IDENT,
    NonTerm.VIEWTYPEDEF: Term.T_TYPEDEF,
    NonTerm.VIEWTYPE_neg: Term.T_TYPE,
    NonTerm.VIEWTYPE_pos: Term.T_TYPE,
    NonTerm.VIEWTYPE: Term.T_TYPE_OR_IDENT,
    NonTerm.WITHPROP: Term.T_WITHTYPE,
    NonTerm.WITHTYPE: Term.T_WITHTYPE,
    NonTerm.WITHVIEW: Term.T_WITHTYPE,
    NonTerm.WITHVIEWTYPE: Term.T_WITHTYPE}


assert all(isinstance(x, NonTerm) for x in NONTERMS_TRANSL)
assert all(isinstance(x, Term) for x in NONTERMS_TRANSL.values())
assert all(x in NONTERMS_TRANSL for x in NonTerm)


# Translation of some idents to products
# ----------------------------------------------------------------------------

IDENTS_TRANSL = {

    # Terminals

    "and": Term.T_AND,
    "as": Term.T_AS,
    "assume": Term.T_ASSUME,
    "absimpl": Term.T_ASSUME,
    "@": Term.T_AT_OR_SIDENT,
    "!": Term.T_BANG_OR_IDENT,
    "|": Term.T_BAR,
    "begin": Term.T_BEGIN,
    "`": Term.T_BQUOTE,
    "classdec": Term.T_CLASSDEC,
    ":": Term.T_COLON,
    "datasort": Term.T_DATASORT,
    "$arrpsz": Term.T_DLRARRPSZ,
    "$arrptrsize": Term.T_DLRARRPSZ,
    "$break": Term.T_DLRBREAK,
    "$continue": Term.T_DLRCONTINUE,
    "$d2ctype": Term.T_DLRD2CTYPE,
    "$effmask": Term.T_DLREFFMASK,
    "$extern": Term.T_DLREXTERN,
    "$extfcall": Term.T_DLREXTFCALL,
    "$extkind": Term.T_DLREXTKIND,
    "$extmcall": Term.T_DLREXTMCALL,
    "$extval": Term.T_DLREXTVAL,
    "$extype": Term.T_DLREXTYPE,
    "$extype_struct": Term.T_DLREXTYPE_STRUCT,
    "$literal": Term.T_DLRLITERAL,
    "$myfilename": Term.T_DLRMYFILENAME,
    "$myfunction": Term.T_DLRMYFUNCTION,
    "$mylocation": Term.T_DLRMYLOCATION,
    "$raise": Term.T_DLRRAISE,
    "$showtype": Term.T_DLRSHOWTYPE,
    "$solver_assert": Term.T_DLRSOLASSERT,
    "$solver_verify": Term.T_DLRSOLVERIFY,
    "$tempenver": Term.T_DLRTEMPENVER,
    "$tyrep": Term.T_DLRTYREP,
    "$vararg": Term.T_DLRVARARG,
    "do": Term.T_DO,
    "$": Term.T_DOLLAR,
    ".": Term.T_DOT,
    "..": Term.T_DOTDOT,
    "...": Term.T_DOTDOTDOT,
    ".<>.": Term.T_DOTLTGTDOT,
    ".<": Term.T_DOTLT,
    "else": Term.T_ELSE,
    "end": Term.T_END,
    "=": Term.T_EQ_OR_DIDENT,
    "=>": Term.T_EQGT,
    "=>>": Term.T_EQGTGT,
    "=<": Term.T_EQLT,
    "=<>": Term.T_EQLTGT,
    "=/=>": Term.T_EQSLASHEQGT,
    "=/=>>": Term.T_EQSLASHEQGTGT,
    "exception": Term.T_EXCEPTION,
    "extern": Term.T_EXTERN,
    "extvar": Term.T_EXTVAR,
    "extype": Term.T_EXTYPE,
    ">.": Term.T_GTDOT,
    ">": Term.T_GT_OR_IDENT,
    "><": Term.T_GTLT_OR_DIDENT,
    "#": Term.T_HASH,
    "ifcase": Term.T_IFCASE,
    "if": Term.T_IF,
    "import": Term.T_IMPORT,
    "in": Term.T_IN,
    "let": Term.T_LET,
    "local": Term.T_LOCAL,
    "<": Term.T_LT_OR_IDENT,
    "->": Term.T_MINUSGT_OR_SIDENT,
    "-<": Term.T_MINUSLT,
    "-<>": Term.T_MINUSLTGT,
    "nonfix": Term.T_NONFIX,
    "of": Term.T_OF,
    "op": Term.T_OP,
    "overload": Term.T_OVERLOAD,
    "%": Term.T_PERCENT_OR_IDENT,
    "?": Term.T_QMARK_OR_IDENT,
    "reassume": Term.T_REASSUME,
    "absreimpl": Term.T_REASSUME,
    "rec": Term.T_REC,
    "scase": Term.T_SCASE,
    "sif": Term.T_SIF,
    "sortdef": Term.T_SORTDEF,
    "#assert": Term.T_SRPASSERT,
    "#codegen2": Term.T_SRPCODEGEN2,
    "#define": Term.T_SRPDEFINE,
    "dynload": Term.T_SRPDYNLOAD,
    "#dynload": Term.T_SRPDYNLOAD,
    "#elifdef": Term.T_SRPELIFDEF,
    "#elif": Term.T_SRPELIF,
    "#elifndef": Term.T_SRPELIFNDEF,
    "#else": Term.T_SRPELSE,
    "#endif": Term.T_SRPENDIF,
    "#error": Term.T_SRPERROR,
    "#ifdef": Term.T_SRPIFDEF,
    "#if": Term.T_SRPIF,
    "#ifndef": Term.T_SRPIFNDEF,
    "#include": Term.T_SRPINCLUDE,
    "#pragma": Term.T_SRPPRAGMA,
    "#prerr": Term.T_SRPPRERR,
    "#print": Term.T_SRPPRINT,
    "#require": Term.T_SRPREQUIRE,
    "staload": Term.T_SRPSTALOAD,
    "#staload": Term.T_SRPSTALOAD,
    "#then": Term.T_SRPTHEN,
    "#undef": Term.T_SRPUNDEF,
    "sta": Term.T_STACST,
    "stacst": Term.T_STACST,
    "stadef": Term.T_STADEF,
    "static": Term.T_STATIC,
    "symelim": Term.T_SYMELIM,
    "symintr": Term.T_SYMINTR,
    "then": Term.T_THEN,
    "~": Term.T_TILDE_OR_IDENT,
    "tkindef": Term.T_TKINDEF,
    "try": Term.T_TRY,
    "when": Term.T_WHEN,
    "where": Term.T_WHERE,
    "with": Term.T_WITH,

    # Non‑terminals

    "absprop": NonTerm.ABSPROP,
    "abst0ype": NonTerm.ABST0YPE,
    "abstflat": NonTerm.ABST0YPE,
    "abstbox": NonTerm.ABSTYPE,
    "abstype": NonTerm.ABSTYPE,
    "absview": NonTerm.ABSVIEW,
    "absviewt0ype": NonTerm.ABSVIEWT0YPE,
    "absvt0ype": NonTerm.ABSVIEWT0YPE,
    "absvtflat": NonTerm.ABSVIEWT0YPE,
    "absviewtype": NonTerm.ABSVIEWTYPE,
    "absvtbox": NonTerm.ABSVIEWTYPE,
    "absvtype": NonTerm.ABSVIEWTYPE,
    "castfn": NonTerm.CASTFN,
    "dataprop": NonTerm.DATAPROP,
    "datatype": NonTerm.DATATYPE,
    "dataview": NonTerm.DATAVIEW,
    "dataviewtype": NonTerm.DATAVTYPE,
    "datavtype": NonTerm.DATAVTYPE,
    "$delay": NonTerm.DLRDELAY,
    "$effmask_all": NonTerm.DLREFFMASK_ALL,
    "$effmask_exn": NonTerm.DLREFFMASK_EXN,
    "$effmask_ntm": NonTerm.DLREFFMASK_NTM,
    "$effmask_ref": NonTerm.DLREFFMASK_REF,
    "$effmask_wrt": NonTerm.DLREFFMASK_WRT,
    "$ldelay": NonTerm.DLRLDELAY,
    "$list": NonTerm.DLRLST,
    "$lst": NonTerm.DLRLST,
    "$list_t": NonTerm.DLRLST_T,
    "$lst_t": NonTerm.DLRLST_T,
    "$list_vt": NonTerm.DLRLST_VT,
    "$lst_vt": NonTerm.DLRLST_VT,
    "$rec": NonTerm.DLRREC,
    "$record": NonTerm.DLRREC,
    "$record_t": NonTerm.DLRREC_T,
    "$rec_t": NonTerm.DLRREC_T,
    "$record_vt": NonTerm.DLRREC_VT,
    "$rec_vt": NonTerm.DLRREC_VT,
    "$tuple_t": NonTerm.DLRTUP_T,
    "$tup_t": NonTerm.DLRTUP_T,
    "$tup": NonTerm.DLRTUP,
    "$tuple": NonTerm.DLRTUP,
    "$tuple_vt": NonTerm.DLRTUP_VT,
    "$tup_vt": NonTerm.DLRTUP_VT,
    "$vcopyenv_vt": NonTerm.DLRVCOPYENV_VT,
    "$vcopyenv_v": NonTerm.DLRVCOPYENV_V,
    "fn": NonTerm.FN,
    "fnx": NonTerm.FNX,
    "fun": NonTerm.FUN,
    "implement": NonTerm.IMPLEMENT,
    "implmnt": NonTerm.IMPLMNT,
    "infix": NonTerm.INFIX,
    "infixl": NonTerm.INFIXL,
    "infixr": NonTerm.INFIXR,
    "macdef": NonTerm.MACDEF,
    "macrodef": NonTerm.MACRODEF,
    "postfix": NonTerm.POSTFIX,
    "praxi": NonTerm.PRAXI,
    "prefix": NonTerm.PREFIX,
    "prfn": NonTerm.PRFN,
    "prfun": NonTerm.PRFUN,
    "primplement": NonTerm.PRIMPLMNT,
    "primplmnt": NonTerm.PRIMPLMNT,
    "propdef": NonTerm.PROPDEF,
    "prval": NonTerm.PRVAL,
    "prvar": NonTerm.PRVAR,
    "typedef": NonTerm.TYPEDEF,
    "var": NonTerm.VAR,
    "viewdef": NonTerm.VIEWDEF,
    "viewtypedef": NonTerm.VIEWTYPEDEF,
    "vtypedef": NonTerm.VIEWTYPEDEF,
    "withprop": NonTerm.WITHPROP,
    "withtype": NonTerm.WITHTYPE,
    "withviewtype": NonTerm.WITHVIEWTYPE,
    "withvtype": NonTerm.WITHVIEWTYPE,
    "withview": NonTerm.WITHVIEW,

    # Added

    "case": NonTerm.CASE,
    "prop": NonTerm.PROP,
    "type": NonTerm.TYPE,
    "t0ype": NonTerm.T0YPE,
    "vtype": NonTerm.VIEWTYPE,
    "vt0ype": NonTerm.VIEWT0YPE,
    "view": NonTerm.VIEW,
    "viewtype": NonTerm.VIEWTYPE,
    "viewt0ype": NonTerm.VIEWT0YPE,
    "val": NonTerm.VAL,
    "for": Term.T_FOR,
    "while": Term.T_WHILE,
    "addr": Term.T_ADDR_OR_IDENT,
    "fold": Term.T_FOLD_OR_IDENT,
    "free": Term.T_FREE_OR_IDENT,
    "lam": NonTerm.LAM,
    "llam": NonTerm.LLAM,
    "fix": NonTerm.FIX}

assert all(isinstance(x, str) for x in IDENTS_TRANSL)
assert all(isinstance(x, (Term, NonTerm)) for x in IDENTS_TRANSL.values())


def ident_translation(ident, default):
    """ Ident possibly translated after IDENTS_TRANSL. """
    return IDENTS_TRANSL[ident] if ident in IDENTS_TRANSL else default


# Prefixes
# ----------------------------------------------------------------------------

# ### Types

class TreeNode:

    """ Prefix table as a tree. """

    __slots__ = ["next", "product"]

    def __init__(self):

        self.next = dict()  # char -> TreeNode.
        self.product = None  # Term, NonTerm, Start or None.


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
    assert isinstance(product, (Term, Start)) or product in NONTERMS_TRANSL
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

add_prefix(EOF, Term.T_EOF)

# Term, sorted by "XX"

add_prefix("0", Term.T_INTZERO)
add_prefix("addr@", Term.T_ADDRAT)
add_prefix("fold@", Term.T_FOLDAT)
add_prefix("for*", Term.T_FORSTAR)
add_prefix("free@", Term.T_FREEAT)
add_prefix("view@", Term.T_VIEWAT)
add_prefix("while*", Term.T_WHILESTAR)
add_prefix("@{", Term.T_ATLBRACE)
add_prefix("@[", Term.T_ATLBRACKET)
add_prefix("@(", Term.T_ATLPAREN)
add_prefix("\\", Term.T_BACKSLASH_OR_IDENT)
add_prefix("`(", Term.T_BQUOTELPAREN)
add_prefix(":<", Term.T_COLONLT)
add_prefix(",", Term.T_COMMA)
add_prefix(",(", Term.T_COMMALPAREN)
add_prefix("#[", Term.T_HASHLBRACKET)
add_prefix("$", Term.T_IDENT_sym)
add_prefix("{", Term.T_LBRACE)
add_prefix("[", Term.T_LBRACKET)
add_prefix("(", Term.T_LPAREN)
add_prefix("%(", Term.T_PERCENTLPAREN)
add_prefix("'{", Term.T_QUOTELBRACE)
add_prefix("'[", Term.T_QUOTELBRACKET)
add_prefix("'(", Term.T_QUOTELPAREN)
add_prefix("}", Term.T_RBRACE)
add_prefix("]", Term.T_RBRACKET)
add_prefix(")", Term.T_RPAREN)
add_prefix(";", Term.T_SEMICOLON)

# NonTerm, Sorted by "XX"

add_prefix("abst@ype", NonTerm.ABST0YPE)
add_prefix("absviewt@ype", NonTerm.ABSVIEWT0YPE)
add_prefix("absvt@ype", NonTerm.ABSVIEWT0YPE)
add_prefix("case-", NonTerm.CASE_neg)
add_prefix("case+", NonTerm.CASE_pos)
add_prefix("fix@", NonTerm.FIXAT)
add_prefix("lam@", NonTerm.LAMAT)
add_prefix("llam@", NonTerm.LLAMAT)
add_prefix("prop-", NonTerm.PROP_neg)
add_prefix("prop+", NonTerm.PROP_pos)
add_prefix("t0ype-", NonTerm.T0YPE_neg)
add_prefix("t0ype+", NonTerm.T0YPE_pos)
add_prefix("t@ype", NonTerm.T0YPE)
add_prefix("t@ype-", NonTerm.T0YPE_neg)
add_prefix("t@ype+", NonTerm.T0YPE_pos)
add_prefix("type-", NonTerm.TYPE_neg)
add_prefix("type+", NonTerm.TYPE_pos)
add_prefix("val-", NonTerm.VAL_neg)
add_prefix("val+", NonTerm.VAL_pos)
add_prefix("view-", NonTerm.VIEW_neg)
add_prefix("view+", NonTerm.VIEW_pos)
add_prefix("viewt0ype-", NonTerm.VIEWT0YPE_neg)
add_prefix("viewt0ype+", NonTerm.VIEWT0YPE_pos)
add_prefix("viewt@ype", NonTerm.VIEWT0YPE)
add_prefix("viewt@ype-", NonTerm.VIEWT0YPE_neg)
add_prefix("viewt@ype+", NonTerm.VIEWT0YPE_pos)
add_prefix("viewtype-", NonTerm.VIEWTYPE_neg)
add_prefix("viewtype+", NonTerm.VIEWTYPE_pos)
add_prefix("vt0ype-", NonTerm.VIEWT0YPE_neg)
add_prefix("vt0ype+", NonTerm.VIEWT0YPE_pos)
add_prefix("vt@ype", NonTerm.VIEWT0YPE)
add_prefix("vt@ype-", NonTerm.VIEWT0YPE_neg)
add_prefix("vtype-", NonTerm.VIEWTYPE_neg)
add_prefix("vt@ype+", NonTerm.VIEWT0YPE_pos)
add_prefix("vtype+", NonTerm.VIEWTYPE_pos)

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

COMMENTS = {Term.T_COMMENT_block, Term.T_COMMENT_line, Term.T_COMMENT_rest}

ERRORS = {Term.T_IDENT_srp}

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
