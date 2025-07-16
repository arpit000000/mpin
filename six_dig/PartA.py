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
def check(pin):
    if not pin.isdigit() or len(pin) != 6:
        return "Invalid MPIN"
    if isconsecutive(pin) or isrepeated(pin) or isalternate(pin) or ispallindrome(pin):
        return "WEAK: Commonly used MPIN"
    return "STRONG"
s = 1
while(s==1):
    user_input = input("Enter a 6-digit MPIN: ")
    result = check(user_input)
    print(result)
    s = int(input("Enter s enter 1 for continue -1 for exit."))