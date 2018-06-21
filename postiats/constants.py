""" Special values in JSON. """

NO_PF = -1

# c2lau_neg
REACHABLE = 0  # => and =>>
UNREACHABLE = 1  # =/=> and =/=>>

# c2lau_seq
PARALLEL = 0  # => and =/=>
SEQUENTIAL = 1  # =>> and =/=>>

# D2Cdatdecs[0]
DATATYPE = 0
DATAVIEWTYPE = 2
DATAPROP = 5
DATAVIEW = 7

# D2Cdcstdecs[1]
DCKCASTFN = "DCKcastfn"
DCKFUN = "DCKfun"
DCKPRAXI = "DCKpraxi"
DCKPRFUN = "DCKprfun"
DCKVAL = "DCKval"

# D2Cfundecs[0]
FK_FN = "FK_fn"
FK_FNX = "FK_fnx"
FK_FUN = "FK_fun"
FK_PRFN = "FK_prfn"
FK_PRFUN = "FK_prfun"

# D2Cimpdec[0]
IMPLEMENT = 1
PRIMPLEMENT = -1

# D2Cstacsts[0]
ABSTYPE = 0
ABST0YPE = 1
ABSVIEWTYPE = 2
ABSVIEWT0YPE = 3
ABSPROP = 5
ABSVIEW = 7

# DCSTEXTDEFnone[0]
STATIC = 0
EXTERN = 1

# D2Cvaldecs[0]
VK_PRVAL = "VK_prval"
VK_VAL = "VK_val"
VK_VAL_NEG = "VK_val_neg"  # val-
VK_VAL_POS = "VK_val_pos"  # val/val+

# D2Ecasehead[0]
CK_CASE = "CK_case"
CK_CASE_NEG = "CK_case_neg"  # case-
CK_CASE_POS = "CK_case_pos"  # case/case+

# D2Erec[0], D2Etup[0]
UNBOXED = 0  # @(…) / @{…}
BOXED = 1  # '(…) / '{…} / $tup(…) / $rec{…}

# funclo_name
FUNCLOCLO = "FUNCLOclo"
FUNCLOFUN = "FUNCLOfun"

# P2Tcon[0]
PCKCON = "PCKcon"
PCKFREE = "PCKfree"
PCKUNFOLD = "PCKunfold"

# S2Erefarg[0]
BY_VALUE = 0  # !arg
BY_REFERENCE = 1  # &arg

# S2Etop[0]
UNINITIALIZED = 0
INITIALIZED = 1

# v2ardec_knd
VAR = 0
PTR = 1

