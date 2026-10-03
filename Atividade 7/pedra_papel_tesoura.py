from secrets import choice

def pedra_papel_tesoura(jogador1: str, jogador2: str) -> str:
    jogador1 = jogador1.strip().lower()
    jogador2 = jogador2.strip().lower()

    opcoes_validas = ("pedra", "papel", "tesoura")

    if jogador1 not in opcoes_validas or jogador2 not in opcoes_validas:
        return "Escolha pedra, papel ou tesoura para jogar"

    if jogador1 == jogador2:
        return "empate"

    if jogador1 == "pedra" and jogador2 == "tesoura":
        return "jogador 01 ganhou"
    elif jogador1 == "papel" and jogador2 == "pedra":
        return "jogador 01 ganhou"
    elif jogador1 == "tesoura" and jogador2 == "papel":
        return "jogador 01 ganhou"
    elif jogador2 == "pedra" and jogador1 == "tesoura":
        return "jogador 02 ganhou"
    elif jogador2 == "papel" and jogador1 == "pedra":
        return "jogador 02 ganhou"
    elif jogador2 == "tesoura" and jogador1 == "papel":
        return "jogador 02 ganhou"

running = "sim"
soma_pontos_jogador1 = 0
soma_pontos_jogador2 = 0

while running == "sim":
    jogador1 = input("Escolha entre pedra, papel ou tesoura: ")
    jogador2 = choice(["pedra", "papel", "tesoura"])

    print(f"O computador escolheu: {jogador2}")

    resultado = pedra_papel_tesoura(jogador1, jogador2)
    print(resultado)

    if resultado == "jogador 01 ganhou":
        soma_pontos_jogador1 = soma_pontos_jogador1 + 1
    elif resultado == "jogador 02 ganhou":
        soma_pontos_jogador2 = soma_pontos_jogador2 + 1

    print(f"Placar: Jogador 01: {soma_pontos_jogador1} | Jogador 02: {soma_pontos_jogador2}")

    running = input("Deseja jogar novamente? Digite sim ou não: ").strip().lower()