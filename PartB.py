import datetime

def check_mpin_strength(pin, dob_self, dob_spouse, anniversary):
    if not pin.isdigit() or len(pin) not in [4, 6]:
        return "Invalid MPIN"

    # Check common patterns
    if is_repeating_alternate(pin):
        return "WEAK"
    if is_consecutive(pin):
        return "WEAK"
    if has_repeated_digits(pin):
        return "WEAK"

    # Check demographics if provided
    if dob_self != "-1" and pin in extract_date_parts(dob_self):
        return "WEAK"
    if dob_spouse != "-1" and pin in extract_date_parts(dob_spouse):
        return "WEAK"
    if anniversary != "-1" and pin in extract_date_parts(anniversary):
        return "WEAK"

    return "STRONG"
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

# strength = check_mpin_strength(pin, dob_self, dob_spouse, anniversary)

# print("\n🧾 MPIN Analysis Result:")
# print("Strength:", strength)
test_cases = [
    # Format: (pin, dob_self, dob_spouse, anniversary, expected_result)

    # ✅ Valid strong pins (no issues)
    ("2764", "-1", "-1", "-1", "STRONG"),
    ("5830", "-1", "-1", "-1", "STRONG"),
    ("9173", "-1", "-1", "-1", "STRONG"),

    # ❌ Consecutive numbers
    ("1234", "-1", "-1", "-1", "WEAK"),
    ("4321", "-1", "-1", "-1", "WEAK"),

    # ❌ Repeated digits
    ("1112", "-1", "-1", "-1", "WEAK"),
    ("9999", "-1", "-1", "-1", "WEAK"),

    # ❌ Repeating alternate pattern
    ("4343", "-1", "-1", "-1", "WEAK"),
    ("1212", "-1", "-1", "-1", "WEAK"),

    # ❌ Matches DOB self
    ("2202", "22/02/1997", "-1", "-1", "WEAK"),
    ("1997", "22/02/1997", "-1", "-1", "WEAK"),
    ("7991", "22/02/1997", "-1", "-1", "WEAK"),  # Reversed YYYY

    # ❌ Matches DOB spouse
    ("1507", "-1", "15/07/1995", "-1", "WEAK"),
    ("9515", "-1", "15/07/1995", "-1", "WEAK"),  # Reversed YYYY + DD

    # ❌ Matches anniversary
    ("2508", "-1", "-1", "25/08/2010", "WEAK"),
    ("2010", "-1", "-1", "25/08/2010", "WEAK"),
    ("0102", "-1", "-1", "02/01/2001", "WEAK"),

    # ❌ Invalid PIN length
    ("123", "-1", "-1", "-1", "Invalid MPIN"),
    ("12345", "-1", "-1", "-1", "Invalid MPIN"),
    ("abcd", "-1", "-1", "-1", "Invalid MPIN"),

    # ✅ Strong pin even with demographics
    ("7864", "15/08/1997", "17/09/1999", "01/01/2022", "STRONG")
]

# === RUN TESTS ===

passed = 0
for i, (pin, dob1, dob2, ann, expected) in enumerate(test_cases, 1):
    result = check_mpin_strength(pin, dob1, dob2, ann)
    status = "✅ PASS" if result == expected else "❌ FAIL"
    print(f"Test {i:02d}: {status} → MPIN: {pin}, Expected: {expected}, Got: {result}")
    if status.startswith("✅"):
        passed += 1

print(f"\n✅ {passed}/{len(test_cases)} tests passed.")