securityLevel = "user"


def someFunction():
    """
    This function tries change securityLevel, but it does it locally.
    """
    securityLevel = "admin"
    return print(securityLevel)


def otherFunction():
    """
    This function use global change,and after calling it
    """
    global securityLevel
    securityLevel = "admin"
    return print(securityLevel)


# shows global variable value
print(securityLevel)

# shows inside function "local" variable value
someFunction()
# shows global variable value same as previous
print(securityLevel)

# now variable is change by a function
otherFunction()
# shows global variable value - now it has new value
print(securityLevel)
