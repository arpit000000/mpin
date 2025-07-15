import datetime
def check_mpin_strength(pin, dob_self, dob_spouse, anniversary):
    reasons = []

    if not pin.isdigit() or len(pin) not in [4, 6]:
        return "Invalid MPIN", ["INVALID_INPUT"]

    # Check common patterns
    if is_repeating_alternate(pin):
        reasons.append("COMMONLY_USED")

    if is_consecutive(pin):
        reasons.append("COMMONLY_USED")
    if has_repeated_digits(pin):
        reasons.append("COMMONLY_USED")

    # Check demographics if provided
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
def is_consecutive(pin):
    for i in range(len(pin) - 2):
        a, b, c = int(pin[i]), int(pin[i+1]), int(pin[i+2])
        if b - a == 1 and c - b == 1:
            return True
        if a - b == 1 and b - c == 1:
            return True
    return False
def has_repeated_digits(pin):
    return any(pin.count(d) > 2 for d in set(pin))
def check_common(pin):
    if not pin.isdigit() or len(pin) != 4:
        return "Invalid MPIN"
    if is_consecutive(pin) or has_repeated_digits(pin) or is_repeating_alternate(pin):
        return "WEAK: Commonly used MPIN"
    return "STRONG"
def is_repeating_alternate(pin):
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
    yy = yyyy[-2:]

    parts = set()

    # 4-digit patterns (forward and reverse)
    parts.update([
        dd + mm, mm + dd,
        dd + yy, yy + dd,
        mm + yy, yy + mm,
        yyyy,                    # normal YYYY
        yyyy[::-1],              # reversed YYYY
        dd + dd, mm + mm, yy + yy
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
# === TEST CASES ===

