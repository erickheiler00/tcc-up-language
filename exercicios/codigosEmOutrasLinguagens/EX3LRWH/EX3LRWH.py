soma = 0.0
i = 0

while True:
    valor = float(input("Digite um valor (0 para parar): "))
    
    if valor == 0:
        break
    
    soma += valor
    i += 1

if i != 0:
    media = soma / i
    print("A média aritmética dos valores fornecidos é igual a", media)
else:
    print("Erro: é necessário informar pelo menos um valor válido para calcular a média.")