#include <stdio.h>

void exibir_invertido(int n) {
    if (n == 0) {
        return;
    }

    int numero;
    scanf("%d", &numero);
    exibir_invertido(n - 1);
    printf("%d\n", numero);
}

int main() {
    int n;

    printf("Quantos números você deseja informar? ");
    scanf("%d", &n);

    printf("Digite os números e veja-os na ordem inversa:\n");
    exibir_invertido(n);

    return 0;
}