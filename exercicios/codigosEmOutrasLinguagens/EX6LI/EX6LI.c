#include <stdio.h>

int divisores(int num, int lista_divisores[]) {
    int contador = 0;
    for (int i = 1; i < num+1; i++) {
        if (num % i == 0) {
            lista_divisores[contador] = i;
            contador++;
        }
    }

    return contador;
}

int main() {
    int num;
    int lista_divisores[100]; 
    int quantidade;

    printf("Digite um número para saber seus divisores: ");
    scanf("%d", &num);

    quantidade = divisores(num, lista_divisores);
    printf("Os divisores do número %d são: ", num);
    for (int i = 0; i < quantidade; i++) {
        printf("%d ", lista_divisores[i]);
    }
    printf("\n");

    return 0;
}