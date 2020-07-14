# -*- coding: utf-8 -*-
import numpy

# Promp the user for a base number
while True:
    base = input("Enter number x: ")
    try:
        base = int(base)
        break
    except:
        # continue asking until the user enters a number
        continue

# Promp the user for an exponent number
while True:
    exponent = input("Enter number y: ")
    try:
        exponent = int(exponent)
        break
    except:
        # continue asking until the user enters a number
        continue

# Print x^y
print("X**y = " + str(base**exponent))

# Print log(base 2) of x
print("log(x) = " + str(numpy.log2(base)))
