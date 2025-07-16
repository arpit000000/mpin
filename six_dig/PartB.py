import datetime

def checkmpin(pin, dob_self, dob_spouse, anniversary):
    if not pin.isdigit() or len(pin) != 6:
        return "Invalid MPIN"
    
    if isalternate(pin):
        return "WEAK"
    if isconsecutive(pin):
        return "WEAK"
    if isrepeated(pin):
        return "WEAK"
    if ispallindrome(pin):
        return "WEAK"
    
    if dob_self != "-1" and pin in extract_date_parts(dob_self):
        return "WEAK"
    if dob_spouse != "-1" and pin in extract_date_parts(dob_spouse):
        return "WEAK"
    if anniversary != "-1" and pin in extract_date_parts(anniversary):
        return "WEAK"

    return "STRONG"
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
    return any(pin.count(d) > 2 for d in set(pin))

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

pin = input("Enter your 6 digit MPIN: ")

print("\nNow enter dates in DD/MM/YYYY format or enter -1 if not applicable.")

dob_self = input("Enter your DOB (Self): ")
dob_spouse = input("Enter your Spouse DOB: ")
anniversary = input("Enter your Wedding Anniversary: ")

strength = checkmpin(pin, dob_self, dob_spouse, anniversary)

print("\n🧾 MPIN Analysis Result:")
print("Strength:", strength)
# test_cases = [
#     # Format: (pin, dob_self, dob_spouse, anniversary, expected_result)

#     #Valid strong pins (no issues)
#     ("2764", "-1", "-1", "-1", "STRONG"),
#     ("5830", "-1", "-1", "-1", "STRONG"),
#     ("9173", "-1", "-1", "-1", "STRONG"),

#     # Consecutive numbers
#     ("1234", "-1", "-1", "-1", "WEAK"),
#     ("4321", "-1", "-1", "-1", "WEAK"),

#     # Repeated digits
#     ("1112", "-1", "-1", "-1", "WEAK"),
#     ("9999", "-1", "-1", "-1", "WEAK"),

#     # Repeating alternate pattern
#     ("4343", "-1", "-1", "-1", "WEAK"),
#     ("1212", "-1", "-1", "-1", "WEAK"),

#     # Matches DOB self
#     ("2202", "22/02/1997", "-1", "-1", "WEAK"),
#     ("1997", "22/02/1997", "-1", "-1", "WEAK"),
#     ("7991", "22/02/1997", "-1", "-1", "WEAK"),  # Reversed YYYY

#     # Matches DOB spouse
#     ("1507", "-1", "15/07/1995", "-1", "WEAK"),
#     ("9515", "-1", "15/07/1995", "-1", "WEAK"),  # Reversed YYYY + DD

#     # Matches anniversary
#     ("2508", "-1", "-1", "25/08/2010", "WEAK"),
#     ("2010", "-1", "-1", "25/08/2010", "WEAK"),
#     ("0102", "-1", "-1", "02/01/2001", "WEAK"),

#     # Invalid PIN length
#     ("123", "-1", "-1", "-1", "Invalid MPIN"),
#     ("12345", "-1", "-1", "-1", "Invalid MPIN"),
#     ("abcd", "-1", "-1", "-1", "Invalid MPIN"),

#     # Strong pin even with demographics
#     ("7864", "15/08/1997", "17/09/1999", "01/01/2022", "STRONG")
# ]

# # === RUN TESTS ===

# passed = 0
# for i, (pin, dob1, dob2, ann, expected) in enumerate(test_cases, 1):
#     result = checkmpin(pin, dob1, dob2, ann)
#     status = "PASS" if result == expected else "FAIL"
#     print(f"Test {i:02d}: {status} → MPIN: {pin}, Expected: {expected}, Got: {result}")
#     if status.startswith("PASS"):
#         passed += 1

# print(f"\n{passed}/{len(test_cases)} tests passed.")