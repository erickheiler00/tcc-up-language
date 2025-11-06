#include <stdio.h>

int main() {
    int i = 0;
    float valor, soma = 0.0, media;

    while (1) {
        printf("Digite um valor (0 para parar): ");
        scanf("%f", &valor);

        if (valor == 0) {
            break;
        }

        soma += valor;
        i++;
    }

    if (i != 0) {
        media = soma / i;
        printf("A média aritmética dos valores fornecidos é igual a %.2f\n", media);
    } else {
        printf("Erro: é necessário informar pelo menos um valor válido para calcular a média.\n");
    }

    return 0;
}