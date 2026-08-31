# Bom dia, professor, decidi fazer o código de 20 BANDEIRAS FÁCEIS

# 10 BANDEIRAS COM LISTRAS NA VERTICAL

# 1 - FRANÇA
# 2 - ITÁLIA
# 3 - BÉLGICA
# 4 - IRLANDA
# 5 - PERU
# 6 - ROMÊNIA
# 7 - MALI
# 8 - GUINÉ
# 9 - NIGÉRIA
# 10 - COSTA DO MARFIM


# 10 BANDEIRAS COM LISTRAS NA HORIZONTAL

# 11 - ALEMANHA
# 12 - RÚSSIA
# 13 - ÁUSTRIA
# 14 - ARMÊNIA
# 15 - HUNGRIA
# 16 - BULGÁRIA
# 17 - HOLANDA
# 18 - ESTÔNIA
# 19 - LITUÂNIA
# 20 - IÉMEN

from turtle import *
from time import sleep

screen = Screen()
screen.setup(width=1000, height=350)

t = Turtle()
t.shape("turtle")
t.speed(0)


# ============================================================
# 10 BANDEIRAS COM FAIXAS VERTICAIS
# Organização: 5 colunas x 2 linhas
# Cada bandeira: 180 x 120
# ============================================================


# --- BANDEIRA 1: FRANÇA ---

t.pu()
t.goto(-470, 50)
t.pd()

t.color("black")
t.fillcolor("#071F98")
t.begin_fill()
for cont in range(2):
    t.fd(60)
    t.lt(90)
    t.fd(120)
    t.lt(90)
t.end_fill()

t.pu()
t.goto(-410, 50)
t.pd()

t.fillcolor("#FFFFFF")
t.begin_fill()
for cont in range(2):
    t.fd(60)
    t.lt(90)
    t.fd(120)
    t.lt(90)
t.end_fill()

t.pu()
t.goto(-350, 50)
t.pd()

t.fillcolor("#E62E32")
t.begin_fill()
for cont in range(2):
    t.fd(60)
    t.lt(90)
    t.fd(120)
    t.lt(90)
t.end_fill()


# --- BANDEIRA 2: ITÁLIA ---

t.pu()
t.goto(-280, 50)
t.pd()

t.fillcolor("#008D45")
t.begin_fill()
for cont in range(2):
    t.fd(60)
    t.lt(90)
    t.fd(120)
    t.lt(90)
t.end_fill()

t.pu()
t.goto(-220, 50)
t.pd()

t.fillcolor("#FFFFFF")
t.begin_fill()
for cont in range(2):
    t.fd(60)
    t.lt(90)
    t.fd(120)
    t.lt(90)
t.end_fill()

t.pu()
t.goto(-160, 50)
t.pd()

t.fillcolor("#D3222B")
t.begin_fill()
for cont in range(2):
    t.fd(60)
    t.lt(90)
    t.fd(120)
    t.lt(90)
t.end_fill()


# --- BANDEIRA 3: BÉLGICA ---

t.pu()
t.goto(-90, 50)
t.pd()

t.fillcolor("#000000")
t.begin_fill()
for cont in range(2):
    t.fd(60)
    t.lt(90)
    t.fd(120)
    t.lt(90)
t.end_fill()

t.pu()
t.goto(-30, 50)
t.pd()

t.fillcolor("#FDDA25")
t.begin_fill()
for cont in range(2):
    t.fd(60)
    t.lt(90)
    t.fd(120)
    t.lt(90)
t.end_fill()

t.pu()
t.goto(30, 50)
t.pd()

t.fillcolor("#EF3340")
t.begin_fill()
for cont in range(2):
    t.fd(60)
    t.lt(90)
    t.fd(120)
    t.lt(90)
t.end_fill()


# --- BANDEIRA 4: IRLANDA ---

t.pu()
t.goto(100, 50)
t.pd()

t.fillcolor("#179B62")
t.begin_fill()
for cont in range(2):
    t.fd(60)
    t.lt(90)
    t.fd(120)
    t.lt(90)
t.end_fill()

t.pu()
t.goto(160, 50)
t.pd()

t.fillcolor("#FFFFFF")
t.begin_fill()
for cont in range(2):
    t.fd(60)
    t.lt(90)
    t.fd(120)
    t.lt(90)
t.end_fill()

t.pu()
t.goto(220, 50)
t.pd()

t.fillcolor("#FF883D")
t.begin_fill()
for cont in range(2):
    t.fd(60)
    t.lt(90)
    t.fd(120)
    t.lt(90)
t.end_fill()


# --- BANDEIRA 5: PERU ---

t.pu()
t.goto(290, 50)
t.pd()

t.fillcolor("#D90F23")
t.begin_fill()
for cont in range(2):
    t.fd(60)
    t.lt(90)
    t.fd(120)
    t.lt(90)
t.end_fill()

t.pu()
t.goto(350, 50)
t.pd()

t.fillcolor("#FFFFFF")
t.begin_fill()
for cont in range(2):
    t.fd(60)
    t.lt(90)
    t.fd(120)
    t.lt(90)
t.end_fill()

t.pu()
t.goto(410, 50)
t.pd()

t.fillcolor("#D90F23")
t.begin_fill()
for cont in range(2):
    t.fd(60)
    t.lt(90)
    t.fd(120)
    t.lt(90)
t.end_fill()


# ============================================================
# SEGUNDA LINHA
# ============================================================


# --- BANDEIRA 6: ROMÊNIA ---

t.pu()
t.goto(-470, -80)
t.pd()

t.fillcolor("#002B80")
t.begin_fill()
for cont in range(2):
    t.fd(60)
    t.lt(90)
    t.fd(120)
    t.lt(90)
t.end_fill()

t.pu()
t.goto(-410, -80)
t.pd()

t.fillcolor("#FCD215")
t.begin_fill()
for cont in range(2):
    t.fd(60)
    t.lt(90)
    t.fd(120)
    t.lt(90)
t.end_fill()

t.pu()
t.goto(-350, -80)
t.pd()

t.fillcolor("#CE1126")
t.begin_fill()
for cont in range(2):
    t.fd(60)
    t.lt(90)
    t.fd(120)
    t.lt(90)
t.end_fill()


# --- BANDEIRA 7: MALI ---

t.pu()
t.goto(-280, -80)
t.pd()

t.fillcolor("#15B53A")
t.begin_fill()
for cont in range(2):
    t.fd(60)
    t.lt(90)
    t.fd(120)
    t.lt(90)
t.end_fill()

t.pu()
t.goto(-220, -80)
t.pd()

t.fillcolor("#FCD116")
t.begin_fill()
for cont in range(2):
    t.fd(60)
    t.lt(90)
    t.fd(120)
    t.lt(90)
t.end_fill()

t.pu()
t.goto(-160, -80)
t.pd()

t.fillcolor("#CE1126")
t.begin_fill()
for cont in range(2):
    t.fd(60)
    t.lt(90)
    t.fd(120)
    t.lt(90)
t.end_fill()


# --- BANDEIRA 8: GUINÉ ---

t.pu()
t.goto(-90, -80)
t.pd()

t.fillcolor("#CE1126")
t.begin_fill()
for cont in range(2):
    t.fd(60)
    t.lt(90)
    t.fd(120)
    t.lt(90)
t.end_fill()

t.pu()
t.goto(-30, -80)
t.pd()

t.fillcolor("#FCD215")
t.begin_fill()
for cont in range(2):
    t.fd(60)
    t.lt(90)
    t.fd(120)
    t.lt(90)
t.end_fill()

t.pu()
t.goto(30, -80)
t.pd()

t.fillcolor("#009460")
t.begin_fill()
for cont in range(2):
    t.fd(60)
    t.lt(90)
    t.fd(120)
    t.lt(90)
t.end_fill()


# --- BANDEIRA 9: NIGÉRIA ---

t.pu()
t.goto(100, -80)
t.pd()

t.fillcolor("#008751")
t.begin_fill()
for cont in range(2):
    t.fd(60)
    t.lt(90)
    t.fd(120)
    t.lt(90)
t.end_fill()

t.pu()
t.goto(160, -80)
t.pd()

t.fillcolor("#FFFFFF")
t.begin_fill()
for cont in range(2):
    t.fd(60)
    t.lt(90)
    t.fd(120)
    t.lt(90)
t.end_fill()

t.pu()
t.goto(220, -80)
t.pd()

t.fillcolor("#008751")
t.begin_fill()
for cont in range(2):
    t.fd(60)
    t.lt(90)
    t.fd(120)
    t.lt(90)
t.end_fill()


# --- BANDEIRA 10: COSTA DO MARFIM ---

t.pu()
t.goto(290, -80)
t.pd()

t.fillcolor("#FF8201")
t.begin_fill()
for cont in range(2):
    t.fd(60)
    t.lt(90)
    t.fd(120)
    t.lt(90)
t.end_fill()

t.pu()
t.goto(350, -80)
t.pd()

t.fillcolor("#FFFFFF")
t.begin_fill()
for cont in range(2):
    t.fd(60)
    t.lt(90)
    t.fd(120)
    t.lt(90)
t.end_fill()

t.pu()
t.goto(410, -80)
t.pd()

t.fillcolor("#019A44")
t.begin_fill()
for cont in range(2):
    t.fd(60)
    t.lt(90)
    t.fd(120)
    t.lt(90)
t.end_fill()


# As 10 bandeiras permanecem juntas na tela por 5 segundos
sleep(5)

# Apaga todas de uma vez
t.clear()

# ============================================================
# 10 BANDEIRAS COM FAIXAS HORIZONTAIS
# Organização: 5 colunas x 2 linhas
# Cada bandeira: 180 x 120
# ============================================================


# --- BANDEIRA 11: ALEMANHA ---

t.pu()
t.goto(-470, 170)
t.pd()

t.color("black")
t.fillcolor("#000000")
t.begin_fill()
for cont in range(2):
    t.fd(180)
    t.rt(90)
    t.fd(40)
    t.rt(90)
t.end_fill()

t.pu()
t.goto(-470, 130)
t.pd()

t.fillcolor("#DD0000")
t.begin_fill()
for cont in range(2):
    t.fd(180)
    t.rt(90)
    t.fd(40)
    t.rt(90)
t.end_fill()

t.pu()
t.goto(-470, 90)
t.pd()

t.fillcolor("#FFCE01")
t.begin_fill()
for cont in range(2):
    t.fd(180)
    t.rt(90)
    t.fd(40)
    t.rt(90)
t.end_fill()


# --- BANDEIRA 12: RÚSSIA ---

t.pu()
t.goto(-280, 170)
t.pd()

t.fillcolor("#FFFFFF")
t.begin_fill()
for cont in range(2):
    t.fd(180)
    t.rt(90)
    t.fd(40)
    t.rt(90)
t.end_fill()

t.pu()
t.goto(-280, 130)
t.pd()

t.fillcolor("#0039A6")
t.begin_fill()
for cont in range(2):
    t.fd(180)
    t.rt(90)
    t.fd(40)
    t.rt(90)
t.end_fill()

t.pu()
t.goto(-280, 90)
t.pd()

t.fillcolor("#D52B1E")
t.begin_fill()
for cont in range(2):
    t.fd(180)
    t.rt(90)
    t.fd(40)
    t.rt(90)
t.end_fill()


# --- BANDEIRA 13: ÁUSTRIA ---

t.pu()
t.goto(-90, 170)
t.pd()

t.fillcolor("#C8112E")
t.begin_fill()
for cont in range(2):
    t.fd(180)
    t.rt(90)
    t.fd(40)
    t.rt(90)
t.end_fill()

t.pu()
t.goto(-90, 130)
t.pd()

t.fillcolor("#FFFFFF")
t.begin_fill()
for cont in range(2):
    t.fd(180)
    t.rt(90)
    t.fd(40)
    t.rt(90)
t.end_fill()

t.pu()
t.goto(-90, 90)
t.pd()

t.fillcolor("#C8112E")
t.begin_fill()
for cont in range(2):
    t.fd(180)
    t.rt(90)
    t.fd(40)
    t.rt(90)
t.end_fill()


# --- BANDEIRA 14: ARMÊNIA ---

t.pu()
t.goto(100, 170)
t.pd()

t.fillcolor("#D90113")
t.begin_fill()
for cont in range(2):
    t.fd(180)
    t.rt(90)
    t.fd(40)
    t.rt(90)
t.end_fill()

t.pu()
t.goto(100, 130)
t.pd()

t.fillcolor("#0033A0")
t.begin_fill()
for cont in range(2):
    t.fd(180)
    t.rt(90)
    t.fd(40)
    t.rt(90)
t.end_fill()

t.pu()
t.goto(100, 90)
t.pd()

t.fillcolor("#F2A800")
t.begin_fill()
for cont in range(2):
    t.fd(180)
    t.rt(90)
    t.fd(40)
    t.rt(90)
t.end_fill()


# --- BANDEIRA 15: HUNGRIA ---

t.pu()
t.goto(290, 170)
t.pd()

t.fillcolor("#CE2939")
t.begin_fill()
for cont in range(2):
    t.fd(180)
    t.rt(90)
    t.fd(40)
    t.rt(90)
t.end_fill()

t.pu()
t.goto(290, 130)
t.pd()

t.fillcolor("#FFFFFF")
t.begin_fill()
for cont in range(2):
    t.fd(180)
    t.rt(90)
    t.fd(40)
    t.rt(90)
t.end_fill()

t.pu()
t.goto(290, 90)
t.pd()

t.fillcolor("#477050")
t.begin_fill()
for cont in range(2):
    t.fd(180)
    t.rt(90)
    t.fd(40)
    t.rt(90)
t.end_fill()


# ============================================================
# SEGUNDA LINHA
# ============================================================


# --- BANDEIRA 16: BULGÁRIA ---

t.pu()
t.goto(-470, 30)
t.pd()

t.fillcolor("#FFFFFF")
t.begin_fill()
for cont in range(2):
    t.fd(180)
    t.rt(90)
    t.fd(40)
    t.rt(90)
t.end_fill()

t.pu()
t.goto(-470, -10)
t.pd()

t.fillcolor("#00966E")
t.begin_fill()
for cont in range(2):
    t.fd(180)
    t.rt(90)
    t.fd(40)
    t.rt(90)
t.end_fill()

t.pu()
t.goto(-470, -50)
t.pd()

t.fillcolor("#D62612")
t.begin_fill()
for cont in range(2):
    t.fd(180)
    t.rt(90)
    t.fd(40)
    t.rt(90)
t.end_fill()


# --- BANDEIRA 17: HOLANDA ---

t.pu()
t.goto(-280, 30)
t.pd()

t.fillcolor("#AE1C28")
t.begin_fill()
for cont in range(2):
    t.fd(180)
    t.rt(90)
    t.fd(40)
    t.rt(90)
t.end_fill()

t.pu()
t.goto(-280, -10)
t.pd()

t.fillcolor("#FFFFFF")
t.begin_fill()
for cont in range(2):
    t.fd(180)
    t.rt(90)
    t.fd(40)
    t.rt(90)
t.end_fill()

t.pu()
t.goto(-280, -50)
t.pd()

t.fillcolor("#21468B")
t.begin_fill()
for cont in range(2):
    t.fd(180)
    t.rt(90)
    t.fd(40)
    t.rt(90)
t.end_fill()


# --- BANDEIRA 18: ESTÔNIA ---

t.pu()
t.goto(-90, 30)
t.pd()

t.fillcolor("#0072CE")
t.begin_fill()
for cont in range(2):
    t.fd(180)
    t.rt(90)
    t.fd(40)
    t.rt(90)
t.end_fill()

t.pu()
t.goto(-90, -10)
t.pd()

t.fillcolor("#000000")
t.begin_fill()
for cont in range(2):
    t.fd(180)
    t.rt(90)
    t.fd(40)
    t.rt(90)
t.end_fill()

t.pu()
t.goto(-90, -50)
t.pd()

t.fillcolor("#FFFFFF")
t.begin_fill()
for cont in range(2):
    t.fd(180)
    t.rt(90)
    t.fd(40)
    t.rt(90)
t.end_fill()


# --- BANDEIRA 19: LITUÂNIA ---

t.pu()
t.goto(100, 30)
t.pd()

t.fillcolor("#FDB913")
t.begin_fill()
for cont in range(2):
    t.fd(180)
    t.rt(90)
    t.fd(40)
    t.rt(90)
t.end_fill()

t.pu()
t.goto(100, -10)
t.pd()

t.fillcolor("#006A44")
t.begin_fill()
for cont in range(2):
    t.fd(180)
    t.rt(90)
    t.fd(40)
    t.rt(90)
t.end_fill()

t.pu()
t.goto(100, -50)
t.pd()

t.fillcolor("#C1272D")
t.begin_fill()
for cont in range(2):
    t.fd(180)
    t.rt(90)
    t.fd(40)
    t.rt(90)
t.end_fill()


# --- BANDEIRA 20: IÉMEN ---

t.pu()
t.goto(290, 30)
t.pd()

t.fillcolor("#CE1126")
t.begin_fill()
for cont in range(2):
    t.fd(180)
    t.rt(90)
    t.fd(40)
    t.rt(90)
t.end_fill()

t.pu()
t.goto(290, -10)
t.pd()

t.fillcolor("#FFFFFF")
t.begin_fill()
for cont in range(2):
    t.fd(180)
    t.rt(90)
    t.fd(40)
    t.rt(90)
t.end_fill()

t.pu()
t.goto(290, -50)
t.pd()

t.fillcolor("#000000")
t.begin_fill()
for cont in range(2):
    t.fd(180)
    t.rt(90)
    t.fd(40)
    t.rt(90)
t.end_fill()


# As 10 bandeiras permanecem juntas por 5 segundos
sleep(5)

# Apaga todas de uma vez
t.clear()

mainloop()