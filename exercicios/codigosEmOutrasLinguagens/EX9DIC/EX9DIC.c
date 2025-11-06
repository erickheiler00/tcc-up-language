#include <stdio.h>
#include <string.h>

#define MAX_SIZE 100

void buscaReversa(char chaves[MAX_SIZE][MAX_SIZE], char valores[MAX_SIZE][MAX_SIZE], int tamanho, char valor_buscado[MAX_SIZE]) {
    int i;
    printf("\nChaves que possuem o valor buscado '%s':\n", valor_buscado);
    
    for (i = 0; i < tamanho; i++) {
        if (strcmp(valores[i], valor_buscado) == 0) {
            printf("%s\n", chaves[i]);
        }
    }
}

int main() {
    char chaves[MAX_SIZE][MAX_SIZE];
    char valores[MAX_SIZE][MAX_SIZE];
    int tamanho = 0;
    
    char chave[MAX_SIZE], valor[MAX_SIZE];
    
    while (1) {
        printf("Digite uma chave para ser armazenada no dicionário (enter para parar): ");
        fgets(chave, MAX_SIZE, stdin);
        chave[strcspn(chave, "\n")] = 0; 
        
        if (strlen(chave) == 0) break;
        
        printf("Digite um valor para ser armazenado no dicionário: ");
        fgets(valor, MAX_SIZE, stdin);
        valor[strcspn(valor, "\n")] = 0; 
        
        strcpy(chaves[tamanho], chave);
        strcpy(valores[tamanho], valor);
        tamanho++;
    }
    
    char valor_buscado[MAX_SIZE];
    printf("\nPor fim, digite um valor a ser buscado: ");
    fgets(valor_buscado, MAX_SIZE, stdin);
    valor_buscado[strcspn(valor_buscado, "\n")] = 0; 
    
    buscaReversa(chaves, valores, tamanho, valor_buscado);
    
    return 0;
}