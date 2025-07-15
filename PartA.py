def is_consecutive(pin):
    for i in range(len(pin) - 2):
        a, b, c = int(pin[i]), int(pin[i+1]), int(pin[i+2])
        if b - a == 1 and c - b == 1:  # Ascending
            return True
        if a - b == 1 and b - c == 1:  # Descending
            return True
    return False

def has_repeated_digits(pin):
    return any(pin.count(d) >= 2 for d in set(pin))
def is_repeating_alternate(pin):
    return len(pin) == 4 and pin[0] == pin[2] and pin[1] == pin[3]
def check_common(pin):
    if not pin.isdigit() or len(pin) != 4:
        return "Invalid MPIN"
    if is_consecutive(pin) or has_repeated_digits(pin) or is_repeating_alternate(pin):
        return "WEAK: Commonly used MPIN"
    return "STRONG"
s = 1
while(s==1):
    user_input = input("Enter a 4-digit MPIN: ")
    result = check_common(user_input)
    print(result)
    s = int(input("Enter s "))