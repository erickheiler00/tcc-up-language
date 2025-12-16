# Linguagem UP 

A **Linguagem de programação UP** foi criada com foco em legibilidade e facilidade de escrita, com o intuito de facilitar o ensino de lógica de programação.

## Recursos
- Tipos: `int`, `float`, `string`, `boolean`, `list`
- Funções, laços de repetição, condicionais, operadores matemáticos
- Editor gráfico com destaque de sintaxe
- Interpretação direta (sem compilação)

## Estrutura do Projeto
```
Up/
├── core/           # Núcleo da linguagem (scanner, parser, interpreter)
├── exercicios/     # Exemplos e exercícios em UP, C e Python
├── gramatica/      # Especificação da gramática
├── editor.py       # Editor gráfico 
├── up.py           # Executador principal
└── ...
```

## Exemplo de Código
```up
int a = input_int("Digite o valor de A: ")
int b = input_int("Digite o valor de B: ")

int soma = a + b

print("Soma de A e B: ", soma)
```

## Como Executar
1. Instale Python 3.8+
2. Execute o editor gráfico:
   ```bash
   python3 editor.py
   ```
3. Ou rode um arquivo UP direto:
   ```bash
   python3 shell.py
   ```
   e execute
   ```bash
   run("caminho_do_arquivo/arquivo.up")
   ```

## Créditos
- Projeto desenvolvido por Erick José Heiler como Trabalho de Conclusão de Curso (TCC)


