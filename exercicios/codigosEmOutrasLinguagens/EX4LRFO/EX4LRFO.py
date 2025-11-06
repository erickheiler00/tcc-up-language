for c in range(101):
    if c == 0:
        print("Celsius Fahrenheit")
        
    if c % 10 == 0:
        f = (c * 1.8) + 32
        print(c, "\t", f)