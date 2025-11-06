#include <stdio.h>
#include <math.h>

int main() {
    int a, b, soma, diferenca, produto, resto;
    double quociente, logaritmo, potencia;
    
    printf("Digite o valor de A: ");
    scanf("%d", &a);

    printf("Digite o valor de B: ");
    scanf("%d", &b);

    soma = a + b;
    diferenca = a - b;
    produto = a * b;
    quociente = (double)a / b;
    resto = a % b;
    logaritmo = log10((double)a);
    potencia = pow(a, b);

    printf("soma de A e B: %d\n", soma);
    printf("diferença de A e B: %d\n", diferenca);
    printf("produto de A por B: %d\n", produto);
    printf("quociente de A por B: %f\n", quociente);
    printf("resto da divisão de A por B: %d\n", resto);
    printf("log10(A): %f\n", logaritmo);
    printf("resultado de A elevado a B: %f\n", potencia);

    return 0;
}