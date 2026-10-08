import pygame

## Definições de funções
# def valida_email(email):
#     sufixo = email[-8:]
#     if sufixo == "@puc.com":
#         return True
#     else:
#         return False

def valida_email(email):
    return email[-8:] == "@puc.com"

def possui_maiuscula(senha):
    for carac in senha:
        if 'A' <= carac <= 'Z':
            return True
    return False

def possui_minuscula(senha):
    for carac in senha:
        if 'a' <= carac <= 'z':
            return True
    return False

def possui_numero(senha):
    for carac in senha:
        if carac.isnumeric():
            return True
    return False

def valida_senha(senha):
    if len(senha) < 8:
        return False
    if not possui_maiuscula(senha):
        return False
    if not possui_minuscula(senha):
        return False
    if not possui_numero(senha):
        return False
    
    return True

def criptografa(senha):
    senha_cripto = ""
    for carac in senha:
        if carac.isalpha():
            pos_alpha = ord(carac) - ord('a')
            pos_alpha = (pos_alpha + 3) % 26
            pos_ascii = pos_alpha + ord('a')
            senha_cripto += chr(pos_ascii)
    return senha_cripto

# ## Configurar e utilizar o pygame
# pygame.init()
# screen = pygame.display.set_mode((1280, 720))
# running = True

# input_string = ""
# valid_email = False
# pressed_enter = False
# fonte = pygame.font.Font(size=50)
# fonte_validation = pygame.font.Font(size=25)

# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#         if event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_BACKSPACE:
#                 input_string = input_string[:-1]
#             elif event.key == pygame.K_RETURN:
#                 pressed_enter = True
#                 valid_email = valida_email(input_string)
#             else:
#                 input_string += event.unicode

#     screen.fill("white")
#     pygame.draw.rect(screen, "black", (100, 100, 500, 50), 3)
#     input_text = fonte.render(input_string, True, "#000000")
#     screen.blit(input_text, (120, 105))
#     if pressed_enter:
#         if valid_email:
#             valid_text = fonte_validation.render("Parabéns, o seu e-mail é válido!", True, "green")
#             screen.blit(valid_text, (120, 180))
#         else:
#             valid_text = fonte_validation.render("O seu e-mail não é válido. Digite novamente!", True, "red")
#             screen.blit(valid_text, (120, 180))

#     pygame.display.update()




email_valido = False
senha_valida = False
caracter_valido = False

while email_valido is not True:
    email = input("Digite seu e-mail: ")
    email_valido = valida_email(email)
    if email_valido:
        print("E-mail válido!")
    else:
        print("E-mail inválido. Digite novamente.")

while senha_valida is not True:
    senha = input("Digite sua senha: ")
    senha_valida = valida_senha(senha)

    for carac in senha:
        if ('0' <= carac <= '9') or ('A' <= carac <= 'Z') or ('a' <= carac <= 'z'):
            pass
        else:
            senha_valida = False
            break

    if senha_valida:
        print("Senha válida!")
    else:
        print("Senha inválida. Digite novamente.")


resultado = criptografa(senha)
print("Senha criptografada: ", resultado)
