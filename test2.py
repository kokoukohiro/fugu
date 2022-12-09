import re

a = "abcd"
line = "sdfsjiabcdsad"
b = re.findall(r'.*'+a+'.*',line)
print(b)