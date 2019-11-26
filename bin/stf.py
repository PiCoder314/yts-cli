def pad(string, length, char):
    if not string:
        return str(string)
    l1 = len(string)
    res = string
    for _ in range(length-l1):
        res += char
    return res
