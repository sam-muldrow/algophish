import re

def convert_to_ascii(string):
  return re.sub(r'[^\x00-\x7F]', '', string)


print(convert_to_ascii("asdasd812o831283<x1312>"))