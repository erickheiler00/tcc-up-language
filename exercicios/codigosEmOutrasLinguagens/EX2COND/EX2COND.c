#include <stdio.h>

int main() {
    int a, b, c, temp;

    printf("Digite o primeiro número: ");
    scanf("%d", &a);

    printf("Digite o segundo número: ");
    scanf("%d", &b);

    printf("Digite o terceiro número: ");
    scanf("%d", &c);

    if (a <= b && b <= c) {
        printf("Números em ordem crescente: %d %d %d\n", a, b, c);
    }

    else if (a <= c && c <= b) {
        printf("Números em ordem crescente: %d %d %d\n", a, c, b);
    }

    else if (b <= c && c <= a) {
        printf("Números em ordem crescente: %d %d %d\n", b, c, a);
    }

    else if (c <= a && a <= b) {
        printf("Números em ordem crescente: %d %d %d\n", c, a, b);
    }

    else if (c <= b && b <= a) {
        printf("Números em ordem crescente: %d %d %d\n", c, b, a);
    }

    else {    
        printf("Números em ordem crescente: %d %d %d\n", b, a, c);
    }

    return 0;
}