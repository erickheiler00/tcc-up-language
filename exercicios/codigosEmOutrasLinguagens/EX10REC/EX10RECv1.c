#include <stdio.h>
#include <stdlib.h>

int main() {
    int n, i;

    printf("Quantos números você deseja informar? ");
    scanf("%d", &n);

    int *numeros = malloc(n * sizeof(int));
    if (numeros == NULL) {
        printf("Erro ao alocar memória.\n");
        return 1;
    }

    printf("Digite os números:\n");
    for (i = 0; i < n; i++) {
        scanf("%d", &numeros[i]);
    }

    printf("\nOrdem inversa:\n");
    for (i = n - 1; i >= 0; i--) {
        printf("%d\n", numeros[i]);
    }

    free(numeros);
    return 0;
}