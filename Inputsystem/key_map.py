from typing import Optional

DIRECT_KEYS = {}


def create_direct_key_hash(key_id: str, key_repr: str, key_code: Optional[bytes], assign_to_dict=True):
    key_hash = {"id": key_id, "repr": key_repr, "code": key_code}
    if assign_to_dict:
        DIRECT_KEYS[key_code] = key_hash
    return key_hash


PARENT_000 = create_direct_key_hash("__/0/PARENT_000/__", "Parent 000", b'\x00', False)
PARENT_224 = create_direct_key_hash("__/0/PARENT_224/__", "Parent 224", b'\xe0', False)
UNKNOWN_KEY = create_direct_key_hash("__/!/UNKNOWN_KEY/__", "Unknown", None, False)

EXTENDED_KEYS = {PARENT_000: {}, PARENT_224: {}}


def create_extended_key_hash(key_id: str, key_name: str, key_repr: str, key_code: bytes, parent_hash: dict):
    key_hash = {"id": key_id, "name": key_name, "repr": key_repr, 
                "code": key_code, "parent": parent_hash}
    EXTENDED_KEYS[parent_hash][key_code] = key_hash
    return key_hash


SMALL_A = create_direct_key_hash("__/1/SMALL_A/__", "[a]", b"a")
SMALL_B = create_direct_key_hash("__/1/SMALL_B/__", "[b]", b"b")
SMALL_C = create_direct_key_hash("__/1/SMALL_C/__", "[c]", b"c")
SMALL_D = create_direct_key_hash("__/1/SMALL_D/__", "[d]", b"d")
SMALL_E = create_direct_key_hash("__/1/SMALL_E/__", "[e]", b"e")
SMALL_F = create_direct_key_hash("__/1/SMALL_F/__", "[f]", b"f")
SMALL_G = create_direct_key_hash("__/1/SMALL_G/__", "[g]", b"g")
SMALL_H = create_direct_key_hash("__/1/SMALL_H/__", "[h]", b"h")
SMALL_I = create_direct_key_hash("__/1/SMALL_I/__", "[i]", b"i")
SMALL_J = create_direct_key_hash("__/1/SMALL_J/__", "[j]", b"j")
SMALL_K = create_direct_key_hash("__/1/SMALL_K/__", "[k]", b"k")
SMALL_L = create_direct_key_hash("__/1/SMALL_L/__", "[l]", b"l")
SMALL_M = create_direct_key_hash("__/1/SMALL_M/__", "[m]", b"m")
SMALL_N = create_direct_key_hash("__/1/SMALL_N/__", "[n]", b"n")
SMALL_O = create_direct_key_hash("__/1/SMALL_O/__", "[o]", b"o")
SMALL_P = create_direct_key_hash("__/1/SMALL_P/__", "[p]", b"p")
SMALL_Q = create_direct_key_hash("__/1/SMALL_Q/__", "[q]", b"q")
SMALL_R = create_direct_key_hash("__/1/SMALL_R/__", "[r]", b"r")
SMALL_S = create_direct_key_hash("__/1/SMALL_S/__", "[s]", b"s")
SMALL_T = create_direct_key_hash("__/1/SMALL_T/__", "[t]", b"t")
SMALL_U = create_direct_key_hash("__/1/SMALL_U/__", "[u]", b"u")
SMALL_V = create_direct_key_hash("__/1/SMALL_V/__", "[v]", b"v")
SMALL_W = create_direct_key_hash("__/1/SMALL_W/__", "[w]", b"w")
SMALL_X = create_direct_key_hash("__/1/SMALL_X/__", "[x]", b"x")
SMALL_Y = create_direct_key_hash("__/1/SMALL_Y/__", "[y]", b"y")
SMALL_Z = create_direct_key_hash("__/1/SMALL_Z/__", "[z]", b"z")

CAPITAL_A = create_direct_key_hash("__/2/CAPITAL_A/__", "[A]", b"A")
CAPITAL_B = create_direct_key_hash("__/2/CAPITAL_B/__", "[B]", b"B")
CAPITAL_C = create_direct_key_hash("__/2/CAPITAL_C/__", "[C]", b"C")
CAPITAL_D = create_direct_key_hash("__/2/CAPITAL_D/__", "[D]", b"D")
CAPITAL_E = create_direct_key_hash("__/2/CAPITAL_E/__", "[E]", b"E")
CAPITAL_F = create_direct_key_hash("__/2/CAPITAL_F/__", "[F]", b"F")
CAPITAL_G = create_direct_key_hash("__/2/CAPITAL_G/__", "[G]", b"G")
CAPITAL_H = create_direct_key_hash("__/2/CAPITAL_H/__", "[H]", b"H")
CAPITAL_I = create_direct_key_hash("__/2/CAPITAL_I/__", "[I]", b"I")
CAPITAL_J = create_direct_key_hash("__/2/CAPITAL_J/__", "[J]", b"J")
CAPITAL_K = create_direct_key_hash("__/2/CAPITAL_K/__", "[K]", b"K")
CAPITAL_L = create_direct_key_hash("__/2/CAPITAL_L/__", "[L]", b"L")
CAPITAL_M = create_direct_key_hash("__/2/CAPITAL_M/__", "[M]", b"M")
CAPITAL_N = create_direct_key_hash("__/2/CAPITAL_N/__", "[N]", b"N")
CAPITAL_O = create_direct_key_hash("__/2/CAPITAL_O/__", "[O]", b"O")
CAPITAL_P = create_direct_key_hash("__/2/CAPITAL_P/__", "[P]", b"P")
CAPITAL_Q = create_direct_key_hash("__/2/CAPITAL_Q/__", "[Q]", b"Q")
CAPITAL_R = create_direct_key_hash("__/2/CAPITAL_R/__", "[R]", b"R")
CAPITAL_S = create_direct_key_hash("__/2/CAPITAL_S/__", "[S]", b"S")
CAPITAL_T = create_direct_key_hash("__/2/CAPITAL_T/__", "[T]", b"T")
CAPITAL_U = create_direct_key_hash("__/2/CAPITAL_U/__", "[U]", b"U")
CAPITAL_V = create_direct_key_hash("__/2/CAPITAL_V/__", "[V]", b"V")
CAPITAL_W = create_direct_key_hash("__/2/CAPITAL_W/__", "[W]", b"W")
CAPITAL_X = create_direct_key_hash("__/2/CAPITAL_X/__", "[X]", b"X")
CAPITAL_Y = create_direct_key_hash("__/2/CAPITAL_Y/__", "[Y]", b"Y")
CAPITAL_Z = create_direct_key_hash("__/2/CAPITAL_Z/__", "[Z]", b"Z")

# NOTE: Numpad keys and Alpha keys are not distinguished, so they are simply number keys
NUMBER_1 = create_direct_key_hash("__/3/NUMBER_1/__", "[1]", b"1")
NUMBER_2 = create_direct_key_hash("__/3/NUMBER_2/__", "[2]", b"2")
NUMBER_3 = create_direct_key_hash("__/3/NUMBER_3/__", "[3]", b"3")
NUMBER_4 = create_direct_key_hash("__/3/NUMBER_4/__", "[4]", b"4")
NUMBER_5 = create_direct_key_hash("__/3/NUMBER_5/__", "[5]", b"5")
NUMBER_6 = create_direct_key_hash("__/3/NUMBER_6/__", "[6]", b"6")
NUMBER_7 = create_direct_key_hash("__/3/NUMBER_7/__", "[7]", b"7")
NUMBER_8 = create_direct_key_hash("__/3/NUMBER_8/__", "[8]", b"8")
NUMBER_9 = create_direct_key_hash("__/3/NUMBER_9/__", "[9]", b"9")
NUMBER_0 = create_direct_key_hash("__/3/NUMBER_0/__", "[0]", b"0")

# Special Symbols
EXCLAMATION   = create_direct_key_hash("__/4/!_or_(SHIFT+1)/__", "[!]", b'!')
AT            = create_direct_key_hash("__/4/@_or_(SHIFT+2)/__", "[@]", b'@')
HASH          = create_direct_key_hash("__/4/#_or_(SHIFT+3)/__", "[#]", b'#')
DOLLAR        = create_direct_key_hash("__/4/$_or_(SHIFT+4)/__", "[$]", b'$')
PERCENT       = create_direct_key_hash("__/4/%_or_(SHIFT+5)/__", "[%]", b'%')
EXPONENT      = create_direct_key_hash("__/4/^_or_(SHIFT+6)/__", "[^]", b'^')
AND           = create_direct_key_hash("__/4/&_or_(SHIFT+7)/__", "[&]", b'&')
ASTERISK      = create_direct_key_hash("__/4/*_or_(SHIFT+8)/__", "[*]", b'*')

OPEN_PARENTHESIS     = create_direct_key_hash("__/4/(_or_(SHIFT+9)/__",        "['(']", b'(')
CLOSE_PARENTHESIS    = create_direct_key_hash("__/4/)_or_(SHIFT+0)/__",        "[')']", b')')
OPEN_CURLY_BRACES    = create_direct_key_hash("__/10/OPEN_CURLY_BRACES/__",    "['{']", b'{')
CLOSE_CURLY_BRACES   = create_direct_key_hash("__/10/CLOSE_CURLY_BRACES/__",   "['}']", b'}')
OPEN_SQUARE_BRACKET  = create_direct_key_hash("__/10/OPEN_SQUARE_BRACKET/__",  "['[']", b'[')
CLOSE_SQUARE_BRACKET = create_direct_key_hash("__/10/CLOSE_SQUARE_BRACKET/__", "[']']", b']')

# Function Keys
F1  = create_extended_key_hash("__/5/F1_KEY/__",  "F1 Key",  "[F1]",  b';', PARENT_000)
F2  = create_extended_key_hash("__/5/F2_KEY/__",  "F2 Key",  "[F2]",  b'<', PARENT_000)
F3  = create_extended_key_hash("__/5/F3_KEY/__",  "F3 Key",  "[F3]",  b'=', PARENT_000)
F4  = create_extended_key_hash("__/5/F4_KEY/__",  "F4 Key",  "[F4]",  b'>', PARENT_000)
F5  = create_extended_key_hash("__/5/F5_KEY/__",  "F5 Key",  "[F5]",  b'?', PARENT_000)
F6  = create_extended_key_hash("__/5/F6_KEY/__",  "F6 Key",  "[F6]",  b'@', PARENT_000)
F7  = create_extended_key_hash("__/5/F7_KEY/__",  "F7 Key",  "[F7]",  b'A', PARENT_000)
F8  = create_extended_key_hash("__/5/F8_KEY/__",  "F8 Key",  "[F8]",  b'B', PARENT_000)
F9  = create_extended_key_hash("__/5/F9_KEY/__",  "F9 Key",  "[F9]",  b'C', PARENT_000)
F10 = create_extended_key_hash("__/5/F10_KEY/__", "F10 Key", "[F10]", b'D', PARENT_000)
F11 = ...   # TODO: add F11 key_hash
F12 = ...   # TODO: add F12 key_hash

# Arrow Keys
UP_ARROW    = create_extended_key_hash("__/6/UP_ARROW_KEY/__",    "Up Key",    "[up]",    b'H', PARENT_224)
DOWN_ARROW  = create_extended_key_hash("__/6/DOWN_ARROW_KEY/__",  "Down Key",  "[down]",  b'P', PARENT_224)
LEFT_ARROW  = create_extended_key_hash("__/6/LEFT_ARROW_KEY/__",  "Left Key",  "[left]",  b'K', PARENT_224)
RIGHT_ARROW = create_extended_key_hash("__/6/RIGHT_ARROW_KEY/__", "Right Key", "[right]", b'M', PARENT_224)

# Other Navigation keys
HOME      = create_extended_key_hash("__/7/HOME_KEY/__",      "Home Key",      "[home]",   b'G', PARENT_224)
PAGE_UP   = create_extended_key_hash("__/7/PAGE_UP_KEY/__",   "Page Up Key",   "[pg up]",  b'I', PARENT_224)
PAGE_DOWN = create_extended_key_hash("__/7/PAGE_DOWN_KEY/__", "Page Down Key", "[pg dn]",  b'Q', PARENT_224)
END       = create_extended_key_hash("__/7/END_KEY/__",       "End Key",       "[end]",    b'O', PARENT_224)
INSERT    = create_extended_key_hash("__/7/INSERT_KEY/__",    "Insert Key",    "[insert]", b'R', PARENT_224)
DELETE    = create_extended_key_hash("__/7/DELETE_KEY/__",    "Delete Key",    "[del]",    b'S', PARENT_224)

# Control Keys
ENTER     = create_direct_key_hash("__/8/ENTER_KEY/__",     "[enter]",     b'\r')
TAB       = create_direct_key_hash("__/8/TAB_KEY/__",       "[tab]",       b'\t')
BACKSPACE = create_direct_key_hash("__/8/BACKSPACE_KEY/__", "[backspace]", b'\x08')
ESCAPE    = create_direct_key_hash("__/8/ESCAPE_KEY/__",    "[esc]",       b'\x1b')
SPACE     = create_direct_key_hash("__/8/SPACE_KEY/__",     "[space]",     b' ')

# Math Symbols
MINUS_SIGN  = create_direct_key_hash("__/9/MINUS_SIGN/__",  "[-]", b'-')
PLUS_SIGN   = create_direct_key_hash("__/9/PLUS_SIGN/__",   "[+]", b'+')
EQUALS_SIGN = create_direct_key_hash("__/9/EQUALS_SIGN/__", "[=]", b'=')
# multiplication_sign(asterisk) and division_sign(slash) covered in other sections

UNDERSCORE = create_direct_key_hash("__/10/UNDERSCORE_KEY/__", "[_]", b'_')
PIPE_KEY   = create_direct_key_hash("__/10/PIPE_KEY/__",       "[|]", b'|')

BACKSLASH_KEY     = create_direct_key_hash("__/10/BACKSLASH_KEY/__",    r"[\]", b'\\')
FORWARD_SLASH_KEY = create_direct_key_hash("__/10/FORWARD_SLASH_KEY/__", "[/]", b'/')

SEMICOLON_KEY = create_direct_key_hash("__/10/SEMICOLON_KEY/__", "[;]", b';')
COLON_KEY     = create_direct_key_hash("__/10/COLON_KEY/__",     "[:]", b':')

SINGLE_QUOTES = create_direct_key_hash("__/10/SINGLE_QUOTES_KEY/__", "[']", b"'")
DOUBLE_QUOTES = create_direct_key_hash("__/10/DOUBLE_QUOTES_KEY/__", '["]', b'"')

COMMA  = create_direct_key_hash("__/10/COMMA_KEY/__",  "[,]", b',')
PERIOD = create_direct_key_hash("__/10/PERIOD_KEY/__", "[.]", b'.')

LESS_THAN    = create_direct_key_hash("__/10/LESS_THAN_KEY/__",    "[<]", b'<')
GREATER_THAN = create_direct_key_hash("__/10/GREATER_THAN_KEY/__", "[>]", b'>')

QUESTION_MARK = create_direct_key_hash("__/10/QUESTION_MARK/__", "[?]", b'?')

BACKTICK_KEY = create_direct_key_hash("__/10/BACKTICK_KEY/__", "[`]", b'`')
TILDE_KEY    = create_direct_key_hash("__/10/TILDE_KEY/__",    "[~]", b'~')
