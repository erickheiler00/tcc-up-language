#include <stdio.h>

int main() {
    int num, indice, i;
    int binario[32];

    // Primeiro número
    printf("Digite o 1º número inteiro positivo: ");
    scanf("%d", &num);

    indice = 0;
    if (num == 0) {
        printf("Binário: 0\n");
    } else {
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

    // Segundo número
    printf("Digite o 2º número inteiro positivo: ");
    scanf("%d", &num);

    indice = 0;
    if (num == 0) {
        printf("Binário: 0\n");
    } else {
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

    // Terceiro número
    printf("Digite o 3º número inteiro positivo: ");
    scanf("%d", &num);

    indice = 0;
    if (num == 0) {
        printf("Binário: 0\n");
    } else {
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

    return 0;
}