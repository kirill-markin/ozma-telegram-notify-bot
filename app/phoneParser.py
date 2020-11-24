import re

phoneRegex = r'\d{10,11}'
removeRegex = r'[\+\-\(\)\s\D]'

def parsePhone(phonestring):
    regex = re.compile(phoneRegex)

    phonestring = re.sub(removeRegex, '', phonestring)

    if (phonestring != '' and regex.match(phonestring)):
        return phonestring
    else:
        return None