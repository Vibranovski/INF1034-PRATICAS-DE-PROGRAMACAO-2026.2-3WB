from random import choice

def substitui_palavra_oculta(palavra_aleatoria, palavra_oculta, letra, vida):
    if letra in palavra_aleatoria:
        for i in range(len(palavra_aleatoria)):
            if letra == palavra_aleatoria[i]:
                #substituir o "_ " na palavra oculta pela letra
                palavra_oculta = palavra_oculta[:2*i] + letra + palavra_oculta[2*i+1:]
        print(f"{palavra_oculta}")
    else:
        print("Errou")
        vida = vida - 1
        print(f"Você tem {vida} vidas restantes.")

def validar_letra(letra):
    while not letra.isalpha():
        print("Entrada inválida! Digite apenas letras, sem números ou caracteres especiais.")
        letra = input("Digite uma letra ou a palavra inteira: ").lower()

reiniciar = "sim"

while reiniciar == "sim":

    # 1° passo: gerar aleatoriamente a palavra
    lista = ["banana", "laranja", "maca", "abacaxi", "kiwi"]
    palavra_aleatoria = choice(lista)

    palavra_oculta = "_ " * len(palavra_aleatoria)

    vida = 6
    palavra_auxiliar = palavra_oculta

    while palavra_auxiliar != palavra_aleatoria and vida > 0:
        letra = input("Digite uma letra ou a palavra inteira: ").lower()
        validar_letra(letra)     
        if len(letra) == 1:
            substitui_palavra_oculta(palavra_aleatoria, palavra_oculta, letra, vida)
        else:
            if letra == palavra_aleatoria: # quando o jogador acerta a palavra inteira
                palavra_oculta = palavra_aleatoria
                palavra_auxiliar = palavra_aleatoria
            else:
                print("Você errou a palavra!")
                vida = vida - 1
                print(f"Você tem {vida} vidas restantes.")
        palavra_auxiliar = palavra_oculta.replace(" ", "")

    if vida == 0:
        print("Forca! Você perdeu!")
    else:
        print("Parabéns! Você acertou a palavra!")

    print(palavra_oculta, "\n\n")

    reiniciar = input("Deseja jogar novamente? (sim/não): ")