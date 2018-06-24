""" Special values in JSON. """

NO_PF = -1

# c2lau_neg
REACHABLE_CLAUSE = 0  # => and =>>
UNREACHABLE_CLAUSE = 1  # =/=> and =/=>>

# c2lau_seq
PARALLEL_CLAUSE = 0  # => and =/=>
SEQUENTIAL_CLAUSE = 1  # =>> and =/=>>

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

# D2Cinclude[0]
INCLUDE_IN_STATIC = 0
INCLUDE_IN_DYNAMIC = 1

# D2Cfundecs[0]
FK_FN = "FK_fn"
FK_FNX = "FK_fnx"
FK_FUN = "FK_fun"
FK_PRFN = "FK_prfn"
FK_PRFUN = "FK_prfun"

# D2Cimpdec[0]
IMPLEMENT = 1
IMPLMNT = 0
PRIMPLEMENT = -1

# D2Cstacsts[0]
ABSTYPE = 0
ABST0YPE = 1
ABSVIEWTYPE = 2
ABSVIEWT0YPE = 3
ABSPROP = 5
ABSVIEW = 7

# D2Cvaldecs[0]
VK_PRVAL = "VK_prval"
VK_VAL = "VK_val"
VK_VAL_NEG = "VK_val_neg"  # val-
VK_VAL_POS = "VK_val_pos"  # val/val+

# D2Ecasehead[0]
CK_CASE = "CK_case"
CK_CASE_NEG = "CK_case_neg"  # case-
CK_CASE_POS = "CK_case_pos"  # case/case+

# D2Erec[0], D2Etup[0], P2Trec[0]
FLAT = 0  # @(…) / @{…}
BOXED = 1  # '(…) / '{…} / $tup(…) / $rec{…}

# DCSTEXTDEFnone[0]
IMPLIED_STA = 0  # Rarely used, using an explicit "sta#…" is more common.
EXTERN = 1  # Explicit extern or implied by staload

# funclo_arglst[0]
CLOREF = -1
CLOPTR = 1

# funclo_name
FUNCLOCLO = "FUNCLOclo"  # -<cloref>, closure
FUNCLOFUN = "FUNCLOfun"  # -<fun>, non‑closure

# P2Tcon[0]
PCKCON = "PCKcon"  # normal constructor
PCKFREE = "PCKfree"  # freeing, prefixed with a tild sign
# PCKLINCON = "PCKlincon"  # linear constructor, should not occur in JSON
PCKUNFOLD = "PCKunfold"  # unfold, prefixed with an at sign

# S2Erefarg[0]
BY_VALUE = 0  # !arg
BY_REFERENCE = 1  # &arg

# S2Etop[0]
NO_DATA_PART = 0
DATA_PART = 1

# v2ardec_knd
VAR = 0
PTR = 1
