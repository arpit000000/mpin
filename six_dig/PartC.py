import datetime
def check_mpin_strength(pin, dob_self, dob_spouse, anniversary):
    reasons = []

    if not pin.isdigit() or len(pin) != 6:
        return "Invalid MPIN", ["INVALID_INPUT"]

    if isalternate(pin) or isconsecutive(pin) or isrepeated(pin) or ispallindrome(pin):
        reasons.append("COMMONLY_USED")

    if dob_self != "-1":
        if pin in extract_date_parts(dob_self):
            reasons.append("DEMOGRAPHIC_DOB_SELF")
    if dob_spouse != "-1":
        if pin in extract_date_parts(dob_spouse):
            reasons.append("DEMOGRAPHIC_DOB_SPOUSE")
    if anniversary != "-1":
        if pin in extract_date_parts(anniversary):
            reasons.append("DEMOGRAPHIC_ANNIVERSARY")

    strength = "WEAK" if reasons else "STRONG"
    return strength, reasons
def isconsecutive(pin):
    for i in range(len(pin) - 2):
        a, b, c = int(pin[i]), int(pin[i+1]), int(pin[i+2])
        if b - a == 1 and c - b == 1:
            return True
        if a - b == 1 and b - c == 1:
            return True
    return False
def isrepeated(pin):
    return any(pin.count(d) > 2 for d in set(pin))
def ispallindrome(pin):
    return pin == pin[::-1]

def isalternate(pin):
    return len(pin) == 6 and pin[0] == pin[2] and pin[1] == pin[3] and pin[4] == pin[5]
def extract_date_parts(date_str):
    if date_str == "-1":
        return set()

    try:
        date = datetime.datetime.strptime(date_str, "%d/%m/%Y")
    except ValueError:
        return set()

    dd = f"{date.day:02d}"
    mm = f"{date.month:02d}"
    yyyy = f"{date.year}"
    yyf = yyyy[-2:]
    yyb = yyyy[:2]

    parts = set()
    parts.update([
        dd + mm + yyf,dd + mm + yyb,mm + dd + yyf,
        mm + dd + yyb,dd + yyf + yyb,dd + yyb + yyf,yyf + dd + mm,
        yyb + dd + mm,mm + yyf + dd,mm + yyb + dd,
        yyf + mm + dd,yyb + mm + dd,
        yyf + yyf + yyf,yyb + yyb + yyb,
        dd + dd + dd,mm + mm + mm,
        yyyy + yyyy[::-1],yyyy[::-1] + yyyy
])


    return parts

test_cases = [
    ("111111", "20/12/2006", "15/03/2028", "28/10/2036", "WEAK", ["COMMONLY_USED"]),
    ("123456", "15/03/2008", "03/12/2022", "13/05/2026", "WEAK", ["COMMONLY_USED"]),
    ("654321", "15/06/2002", "12/11/2021", "17/12/2022", "WEAK", ["COMMONLY_USED"]),
    ("654321", "15/06/2002", "12/11/2021", "11/03/2026", "WEAK", ["COMMONLY_USED"]),
    ("122221", "12/08/2003", "03/03/2004", "-1", "WEAK", ["COMMONLY_USED"]),
    ("222333", "10/01/2001", "11/02/2002", "12/12/2012","WEAK", ["COMMONLY_USED"]),
    ("310303", "31/03/2003", "12/06/2028", "18/03/2024", "WEAK", ["DEMOGRAPHIC_DOB_SELF"]),
    ("300220", "31/03/2003", "03/03/2004", "11/04/2019","WEAK", ["COMMONLY_USED"]),
    ("121212", "-1", "12/12/2012", "-1", "WEAK", ["DEMOGRAPHIC_DOB_SPOUSE", "COMMONLY_USED"]),
    ("250998", "-1", "-1", "25/09/1998", "WEAK", ["DEMOGRAPHIC_ANNIVERSARY"]),
    ("000000", "03/03/2004", "11/04/2019", "13/12/2025", "WEAK", ["COMMONLY_USED"]),
    ("200331", "31/03/2003", "-1", "14/11/2022", "WEAK", ["DEMOGRAPHIC_DOB_SELF"]),
    ("739104", "10/01/2001", "11/02/2002", "12/12/2012", "STRONG", []),
    ("112233", "11/11/2000", "22/07/2009", "-1", "STRONG", []),
    ("947261", "-1", "-1", "-1", "STRONG", []),
    ("250998", "20/12/1980", "-1", "25/09/1998", "WEAK", ["DEMOGRAPHIC_ANNIVERSARY"]),
    ("200330", "31/03/2003", "-1", "-1", "WEAK", ["COMMONLY_USED"]),
    ("041195", "-1", "04/11/1995", "-1", "WEAK", ["DEMOGRAPHIC_DOB_SPOUSE"]),
    ("319004", "12/12/2001", "31/03/2003", "-1", "STRONG", []),
    ("032031", "31/03/2003", "-1", "-1", "WEAK", ["DEMOGRAPHIC_DOB_SELF"]),
    ("777321", "-1", "-1", "-1", "WEAK", ["COMMONLY_USED"])
]
for i, (pin, dob1, dob2, ann, expected_strength, expected_reasons) in enumerate(test_cases, 1):
    strength, reasons = check_mpin_strength(pin,dob1,dob2,ann)
    assert strength == expected_strength, f"Test {i} failed: strength"
    for r in expected_reasons:
        assert r in reasons, f"Test {i} failed: missing reason {r}"
    print(f"Test {i} passed.")

