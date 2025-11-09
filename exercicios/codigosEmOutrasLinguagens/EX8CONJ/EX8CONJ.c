#include <stdio.h>
#include <string.h>
#include <stdbool.h>

bool letras_unicas(char palavra[]) {
    char repetidas[256] = ""; 
    int conjunto[256] = {0}; 
    int i;

    for (i = 0; i < strlen(palavra); i++) {
        char caractere = palavra[i];
        if (conjunto[(int)caractere] == 0) {
            conjunto[(int)caractere] = 1;
        } else {
            return false;
        }
    }

    return true;
}

int main() {
    char palavra[100];

    printf("Digite uma palavra: ");
    scanf("%s", palavra);

    printf("%s\n", letras_unicas(palavra) ? "True" : "False");

    return 0;
}