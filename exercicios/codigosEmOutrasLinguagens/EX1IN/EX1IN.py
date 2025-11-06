import math

a = int(input("Digite o valor de A: "))
b = int(input("Digite o valor de B: "))

soma = a + b
diferenca = a - b
produto = a * b
quociente = a / b
resto = a % b
logaritmo = math.log10(a)
potencia = a ** b

print("soma de A e B: ", soma)
print("diferença de A e B: ", diferenca)
print("produto de A por B: ", produto)
print("quociente de A por B: ", quociente)
print("resto da divisão de A por B: ", resto)
print("log10(A): ", logaritmo)
print("resultado de A elevado a B: ", potencia)