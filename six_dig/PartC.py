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
def check_common(pin):
    if not pin.isdigit() or len(pin) != 4:
        return "Invalid MPIN"
    if isconsecutive(pin) or isrepeated(pin) or isalternate(pin):
        return "WEAK: Commonly used MPIN"
    return "STRONG"
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
        dd + mm + yyf,dd + mm + yyb,mm + dd + yyf,
        mm + dd + yyb,dd + yyf + yyb,dd + yyb + yyf,yyf + dd + mm,
        yyb + dd + mm,mm + yyf + dd,mm + yyb + dd,
        yyf + mm + dd,yyb + mm + dd,
        yyf + yyf + yyf,yyb + yyb + yyb,
        dd + dd + dd,mm + mm + mm,
        yyyy + yyyy[::-1],yyyy[::-1] + yyyy
])


    return parts

pin = input("Enter your 6 digit MPIN: ")

print("\nNow enter dates in DD/MM/YYYY format or enter -1 if not applicable.")

dob_self = input("Enter your DOB (Self): ")
dob_spouse = input("Enter your Spouse DOB: ")
anniversary = input("Enter your Wedding Anniversary: ")

strength, reasons = check_mpin_strength(pin, dob_self, dob_spouse, anniversary)

print("\n🧾 MPIN Analysis Result:")
print("Strength:", strength)
print("Reasons:", reasons if reasons else "[] (No weakness found)")

