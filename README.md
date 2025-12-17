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
├── core/                                    # Núcleo da linguagem
│   ├── errors/                              # Tratamento de erros
│   │   ├── errors.py                        # Definições de erros léxicos, sintáticos e semânticos
│   │   └── runtime.py                       # Erros em tempo de execução
│   │
│   ├── interpreter/                         # Interpretador da linguagem
│   │   ├── context.py                       # Contexto de execução
│   │   ├── interpreter.py                   # Lógica principal do interpretador
│   │   └── symbolTable.py                   # Tabela de símbolos
│   │
│   ├── parser/                              # Analisador sintático
│   │   ├── nodes.py                         # Nós da árvore sintática abstrata (AST)
│   │   ├── parser.py                        # Implementação do parser
│   │   └── parseResult.py                   # Resultado do processo de parsing
│   │
│   └── scanner/                             # Analisador léxico
│       ├── scanner.py                       # Implementação do scanner
│       └── tokens.py                        # Definição dos tokens
│ 
├── exercicios/                              # Exemplos e exercícios
│   ├── codigosEmOutrasLinguagens/           # Códigos em Python e C
│   └── codigosEmUp/                         # Códigos escritos em UP
│   └── listasDeExercicios/                  # Listas de exercícios
│       ├── lista_de_exercicios_base.pdf     # Listas utilizadas como base para a lista principal
│       └── lista_de_exercicios_impl.pdf     # Lista de exercícios selecionados para implementação
│
├── gramatica/                               # Especificação da linguagem
│   └── grammar.txt                          # Gramática da linguagem UP
│
├── editor.py                                # Editor gráfico da linguagem
├── shell.py                                 # Shell interativo (REPL) da UP
├── strings_with_arrows.py                   # Utilitário para destacar erros no código
├── up.py                                    # Executador principal da linguagem
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


