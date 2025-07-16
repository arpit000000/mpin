import datetime
def check_mpin_strength(pin, dob_self, dob_spouse, anniversary):
    reasons = []

    if not pin.isdigit() or len(pin) != 4:
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
def ispallindrome(pin):
    return pin == pin[::-1]
def isconsecutive(pin):
    for i in range(len(pin) - 2):
        a, b, c = int(pin[i]), int(pin[i+1]), int(pin[i+2])
        if b - a == 1 and c - b == 1:
            return True
        if a - b == 1 and b - c == 1:
            return True
    return False
def isrepeated(pin):
    return any(pin.count(d) >= 2 for d in set(pin))
def isalternate(pin):
    return len(pin) == 4 and pin[0] == pin[2] and pin[1] == pin[3]
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
        dd + mm, mm + dd,
        dd + yyf, yyf + dd,
        dd+yyb,yyb+dd,
        mm + yyf, yyf + mm,
        yyb+mm,mm+yyb,
        yyyy,                    
        yyyy[::-1],              
        dd + dd, mm + mm, yyf + yyb
    ])

    return parts

# pin = input("Enter your 4 digit MPIN: ")

# print("\nNow enter dates in DD/MM/YYYY format or enter -1 if not applicable.")

# dob_self = input("Enter your DOB (Self): ")
# dob_spouse = input("Enter your Spouse DOB: ")
# anniversary = input("Enter your Wedding Anniversary: ")

# strength, reasons = check_mpin_strength(pin, dob_self, dob_spouse, anniversary)

# print("\n🧾 MPIN Analysis Result:")
# print("Strength:", strength)
# print("Reasons:", reasons if reasons else "[] (No weakness found)")

test_cases = [
    ("1111", "20/12/2006", "15/03/2028", "28/10/2036", "WEAK", ["COMMONLY_USED"]),
    ("1234", "15/03/2008", "03/12/2022", "13/05/2026", "WEAK", ["COMMONLY_USED"]),
    ("6543", "15/06/2002", "12/11/2021", "17/12/2022", "WEAK", ["COMMONLY_USED"]),
    ("6543", "15/06/2002", "12/11/2021", "11/03/2026", "WEAK", ["COMMONLY_USED"]),
    ("1221", "12/08/2003", "03/03/2004", "-1", "WEAK", ["COMMONLY_USED"]),
    ("2233", "10/01/2001", "11/02/2002", "12/12/2012","WEAK", ["COMMONLY_USED"]),
    ("3103", "31/03/2003", "12/06/2028", "18/03/2024", "WEAK", ["DEMOGRAPHIC_DOB_SELF"]),
    ("3020", "31/03/2003", "03/03/2004", "11/04/2019","WEAK", ["COMMONLY_USED"]),
    ("1212", "-1", "12/12/2012", "-1", "WEAK", ["COMMONLY_USED","DEMOGRAPHIC_DOB_SPOUSE"]),
    ("2998", "-1", "-1", "25/09/1998", "WEAK", ["COMMONLY_USED"]),
    ("0000", "03/03/2004", "11/04/2019", "13/12/2025", "WEAK", ["COMMONLY_USED"]),
    ("2031", "31/03/2003", "-1", "14/11/2022", "WEAK", ["DEMOGRAPHIC_DOB_SELF"]),
    ("7304", "10/01/2001", "11/02/2002", "12/12/2012", "STRONG", []),
    ("1123", "11/11/2000", "22/07/2009", "-1", "WEAK", ["COMMONLY_USED"]),
    ("9421", "-1", "-1", "-1", "STRONG", []),
    ("2598", "-1", "-1", "25/09/1998", "WEAK", ["DEMOGRAPHIC_ANNIVERSARY"]),
    ("2030", "31/03/2003", "-1", "-1", "WEAK", ["COMMONLY_USED"]),
    ("0415", "-1", "04/11/1995", "-1", "STRONG",[]),
    ("3104", "12/12/2001", "31/03/2003", "-1", "STRONG", []),
    ("0331", "31/03/2003", "-1", "-1", "WEAK", ["DEMOGRAPHIC_DOB_SELF"]),
    ("7321", "-1", "-1", "-1", "WEAK", ["COMMONLY_USED"])
]
for i, (pin, dob1, dob2, ann, expected_strength, expected_reasons) in enumerate(test_cases, 1):
    strength, reasons = check_mpin_strength(pin,dob1,dob2,ann)
    assert strength == expected_strength, f"Test {i} failed: strength"
    for r in expected_reasons:
        assert r in reasons, f"Test {i} failed: missing reason {r}"
    print(f"Test {i} passed.")



