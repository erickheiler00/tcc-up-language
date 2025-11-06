#include <stdio.h>

void decimalParaBinario(int num) {
    int binario[32];
    int indice = 0;
    int i;

    if (num == 0) {
        printf("Binário: 0\n");
        return;
    }

    while (num > 0) {
        binario[indice] = num % 2;
        num = num / 2;
        indice++;
    }

    printf("Binário: ");

    for (i = indice - 1; i >= 0; i--) {
        printf("%d", binario[i]);
    }
    
    printf("\n");
}

int main() {
    int num;

    printf("Digite o 1º número inteiro positivo: ");
    scanf("%d", &num);
    decimalParaBinario(num);

    printf("Digite o 2º número inteiro positivo: ");
    scanf("%d", &num);
    decimalParaBinario(num);

    printf("Digite o 3º número inteiro positivo: ");
    scanf("%d", &num);
    decimalParaBinario(num);

    return 0;
}