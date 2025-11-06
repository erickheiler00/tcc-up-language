import up

# Loop infinito que ira ler a entrada bruta da janela do terminal
while True:
    # aguarda o usuario digitar uma linha de comando
    text = input('UP > ') 
    # Para nao dar erro ao pressionar enter sem ter digitado nada
    if text.strip() == "": continue
    # std como espaco reservado, pois o codigo nao vem de um arquivo real
    result, error = up.run('<stdin>', text) 
    
    # Se houver um erro iremos imprimi-lo, caso contrario imprimimos o resultado
    if error: 
        print(error.as_string())
    elif result: 
        # Quando ha apenas um resultado, mostramos apenas esse resultado
        if len(result.elements) == 1:
            print(repr(result.elements[0]))
        # Quando ha mais de um resultado, mostramos a lista inteira
        else:
            print(repr(result))

