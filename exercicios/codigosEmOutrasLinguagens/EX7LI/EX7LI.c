#include <stdio.h>
#include <string.h>
#include <ctype.h>

void tokenizacao(char expressao[], char lista_tokens[][50], int *qtd_tokens) {
    char nova_expressao[200] = "";
    char num[50] = "";
    char caractere_ant = '\0';
    int i = 0;
    int tamanho = strlen(expressao);
    
    for (i = 0; i < tamanho; i++) {
        if (expressao[i] != ' ') {
            int len = strlen(nova_expressao);
            nova_expressao[len] = expressao[i];
            nova_expressao[len + 1] = '\0';
        }
    }
    
    tamanho = strlen(nova_expressao);
    
    *qtd_tokens = 0;
    for (i = 0; i < tamanho; i++) {
        char caractere = nova_expressao[i];
        
        if (caractere == '(' || caractere == ')' || caractere == '*' || caractere == '/' || caractere == '^') {
            if (strlen(num) != 0) {
                strcpy(lista_tokens[*qtd_tokens], num);
                (*qtd_tokens)++;
                num[0] = '\0';
            }
            lista_tokens[*qtd_tokens][0] = caractere;
            lista_tokens[*qtd_tokens][1] = '\0';
            (*qtd_tokens)++;
        } 
        else if (caractere == '+' || (caractere == '-' && (isdigit(caractere_ant) || caractere_ant == ')'))) {
            if (isdigit(caractere_ant) || caractere_ant == ')') {
                if (strlen(num) != 0) {
                    strcpy(lista_tokens[*qtd_tokens], num);
                    (*qtd_tokens)++;
                    num[0] = '\0';
                }
                lista_tokens[*qtd_tokens][0] = caractere;
                lista_tokens[*qtd_tokens][1] = '\0';
                (*qtd_tokens)++;
            } 
        } 
        else {
            int len = strlen(num);
            num[len] = caractere;
            num[len + 1] = '\0';
        }
        
        caractere_ant = caractere;
    }
    
    if (strlen(num) != 0) {
        strcpy(lista_tokens[*qtd_tokens], num);
        (*qtd_tokens)++;
    }
}

int main() {
    char expressao[200];
    char lista_tokens[100][50];  
    int qtd_tokens;
    int i;
    
    printf("Digite uma expressão matemática: ");
    fgets(expressao, sizeof(expressao), stdin);
    
    if (expressao[strlen(expressao) - 1] == '\n') {
        expressao[strlen(expressao) - 1] = '\0';
    }
    
    tokenizacao(expressao, lista_tokens, &qtd_tokens);
    
    printf("Tokens:\n");
    for (i = 0; i < qtd_tokens; i++) {
        printf("%s\n", lista_tokens[i]);
    }
    
    return 0;
}