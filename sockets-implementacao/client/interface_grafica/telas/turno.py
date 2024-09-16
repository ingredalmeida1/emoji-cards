import arcade
import arcade.gui # submódulo gui do arcade, que fornece componentes para criar interfaces gráficas.

from ..resources.constantes import LARGURA_TELA, ALTURA_TELA, AZUL, AMARELO, POPPINS, AGRANDIR

import threading
from ..telas.esperar_escolhas import EsperarEscolhas

class Turno(arcade.View):
    def __init__(self, cliente, atributo_turno, pontuacao, id_partida, criar_partida_view, back_to_login):
        super().__init__()
                
        self.cliente = cliente
        self.atributo = atributo_turno.replace('_',' ').replace('qtd','').upper()
        self.pontuacao = pontuacao
        self.id_partida = id_partida
        
        self.username_usuario = self.cliente.get_username()
        
        #atualizar contador turnos
        self.cliente.count_turnos += 1
        
        self.criar_partida_view = criar_partida_view
        self.back_to_login = back_to_login

        arcade.set_background_color(AZUL)

        self.esquerda_centro = None
        self.esquerda_esquerda = None
        self.esquerda_direita = None
        self.esquerda_p_esquerda = None
        self.esquerda_p_direita = None

        self.direita_centro = None
        self.direita_esquerda = None
        self.direita_direita = None
        self.direita_p_esquerda = None
        self.direita_p_direita = None
        
        self.outros_jogadores = [username for username in self.pontuacao.keys() if username != self.username_usuario ] 
        
        #mostrar pontuacao
        self.username_1 = self.username_usuario # usuario fica no meio
        self.username_2 = self.outros_jogadores[0]
        self.username_3 = self.outros_jogadores[1]

        self.pontuacao_1 = str(self.pontuacao[self.username_1])
        self.pontuacao_2 = str(self.pontuacao[self.username_2])
        self.pontuacao_3 = str(self.pontuacao[self.username_3])

        self.fundo_atributo = arcade.load_texture("interface_grafica/resources/widgets/campo.png")

        self.centro_esquerda = None
        self.centro_direita = None

        self.botoes = []

        # preenchendo cartas principais da rodada provisoriamente
        print('baralho escolhido = ',self.cliente.baralho_escolhido)
        emocao_1 = self.cliente.baralho_escolhido[0]
        self.carta_1 = arcade.load_texture(f"interface_grafica/resources/cartas/{emocao_1}.png")
        self.botoes.append({
            'texture': self.carta_1,
            'x': LARGURA_TELA // 2 - 183,
            'y': 125,
            'width': 160,
            'height': 230,
            'action': lambda:  self.selecionar_carta(0)
        })

        emocao_2 = self.cliente.baralho_escolhido[1]
        self.carta_2 = arcade.load_texture(f"interface_grafica/resources/cartas/{emocao_2}.png")
        self.botoes.append({
            'texture': self.carta_2,
            'x': LARGURA_TELA // 2,
            'y': 125,
            'width': 160,
            'height': 230,
            'action': lambda:  self.selecionar_carta(1)
        })
        
        emocao_3 = self.cliente.baralho_escolhido[2]
        self.carta_3 = arcade.load_texture(f"interface_grafica/resources/cartas/{emocao_3}.png")
        self.botoes.append({
            'texture': self.carta_3,
            'x': LARGURA_TELA // 2 + 183,
            'y': 125,
            'width': 160,
            'height': 230,
            'action': lambda:  self.selecionar_carta(2)
        })

    def setup(self):
        self.esquerda_centro = arcade.load_texture("interface_grafica/resources/cartas/carta-tras.png")
        self.esquerda_esquerda = arcade.load_texture("interface_grafica/resources/cartas/carta-tras.png")
        self.esquerda_direita = arcade.load_texture("interface_grafica/resources/cartas/carta-tras.png")
        self.esquerda_p_esquerda = arcade.load_texture("interface_grafica/resources/cartas/carta-tras.png")
        self.esquerda_p_direita = arcade.load_texture("interface_grafica/resources/cartas/carta-tras.png")

        self.direita_centro = arcade.load_texture("interface_grafica/resources/cartas/carta-tras.png")
        self.direita_esquerda = arcade.load_texture("interface_grafica/resources/cartas/carta-tras.png")
        self.direita_direita = arcade.load_texture("interface_grafica/resources/cartas/carta-tras.png")
        self.direita_p_esquerda = arcade.load_texture("interface_grafica/resources/cartas/carta-tras.png")
        self.direita_p_direita = arcade.load_texture("interface_grafica/resources/cartas/carta-tras.png")
        
        self.centro_direita = arcade.load_texture("interface_grafica/resources/cartas/carta-tras.png")
        self.centro_esquerda = arcade.load_texture("interface_grafica/resources/cartas/carta-tras.png")
        
    def on_show(self):
        self.setup()     

    def on_draw(self):
        arcade.start_render()
        
        arcade.draw_text(f"Turno {self.cliente.count_turnos}", 10, 580,
            AMARELO, font_size=12, font_name=POPPINS,  anchor_x="left")


        arcade.draw_texture_rectangle(63, ALTURA_TELA // 2, 90, 126, self.esquerda_centro, angle=270)
        arcade.draw_texture_rectangle(63, ALTURA_TELA // 2 + 95, 90, 126, self.esquerda_esquerda, angle=270)
        arcade.draw_texture_rectangle(63, ALTURA_TELA // 2 - 95, 90, 126, self.esquerda_direita, angle=270)
        arcade.draw_texture_rectangle(43, ALTURA_TELA // 2 + 175, 60, 86, self.esquerda_p_esquerda, angle=270)
        arcade.draw_texture_rectangle(43, ALTURA_TELA // 2 - 175, 60, 86, self.esquerda_p_direita, angle=270)

        arcade.draw_texture_rectangle(LARGURA_TELA - 63, ALTURA_TELA // 2, 90, 126, self.direita_centro, angle=90)
        arcade.draw_texture_rectangle(LARGURA_TELA - 63, ALTURA_TELA // 2 + 95, 90, 126, self.direita_esquerda, angle=90)
        arcade.draw_texture_rectangle(LARGURA_TELA - 63, ALTURA_TELA // 2 - 95, 90, 126, self.direita_direita, angle=90)
        arcade.draw_texture_rectangle(LARGURA_TELA - 43, ALTURA_TELA // 2 + 175, 60, 86, self.direita_p_esquerda, angle=90)
        arcade.draw_texture_rectangle(LARGURA_TELA - 43, ALTURA_TELA // 2 - 175, 60, 86, self.direita_p_direita, angle=90)

        arcade.draw_texture_rectangle(LARGURA_TELA//2 - 312, 50, 72, 96, self.centro_esquerda)
        arcade.draw_texture_rectangle(LARGURA_TELA//2 + 312, 50, 72, 96, self.centro_direita)

        # if self.username_1 and self.pontuacao_1:
        arcade.draw_text(self.username_1, LARGURA_TELA//2, 570, arcade.color.WHITE, 
                        font_size=15, font_name=POPPINS, anchor_x="center")
        arcade.draw_text(self.pontuacao_1, LARGURA_TELA//2, 530, arcade.color.WHITE, 
                        font_size=15, font_name=POPPINS, anchor_x="center")
            
        # if self.username_2 and self.pontuacao_2:
        arcade.draw_text(self.username_2, LARGURA_TELA//2 - 180, 570, AMARELO, 
                        font_size=15, font_name=POPPINS, anchor_x="center")
        arcade.draw_text(self.pontuacao_2, LARGURA_TELA//2 - 180, 530, AMARELO, 
                        font_size=15, font_name=POPPINS, anchor_x="center")
            
        # if self.username_3 and self.pontuacao_3:
        arcade.draw_text(self.username_3, LARGURA_TELA//2 + 180, 570, AMARELO, 
                        font_size=15, font_name=POPPINS, anchor_x="center")
        arcade.draw_text(self.pontuacao_3, LARGURA_TELA//2 + 180, 530, AMARELO, 
                        font_size=15, font_name=POPPINS, anchor_x="center")
            
        if self.fundo_atributo and self.atributo:
            arcade.draw_texture_rectangle(LARGURA_TELA//2, ALTURA_TELA// 2 + 150, 350, 60, self.fundo_atributo)
            arcade.draw_text(self.atributo, LARGURA_TELA//2, ALTURA_TELA// 2 + 143, arcade.color.WHITE, 
                         font_size=15, font_name=POPPINS, anchor_x="center")
            
        for botao in self.botoes:
            if 'texture' in botao:
                arcade.draw_texture_rectangle(botao['x'], botao['y'], botao['width'], botao['height'], botao['texture'])
            
    def on_mouse_press(self, x, y, button, modifiers):
        for botao in self.botoes:
            if 'texture' in botao:
                if (botao['x'] - botao['width'] / 2 < x < botao['x'] + botao['width'] / 2 and
                        botao['y'] - botao['height'] / 2 < y < botao['y'] + botao['height'] / 2):
                    botao['action']()
                    break

    def selecionar_carta(self, indice): 
        print(self.cliente.baralho_escolhido)
        #remove a carta selecionada do baralho
        emocao = self.cliente.baralho_escolhido.pop(indice)
        print("Selecionou", emocao )
        print(self.cliente.baralho_escolhido)
        
        #avisa pro servidor qual foi a carta
        self.cliente.responder_jogada_turno(emocao, self.id_partida)
        
        #mudar para tela de aguardar
        self.window.show_view(EsperarEscolhas(self.cliente, emocao, self.atributo, self.pontuacao, self.id_partida, self.criar_partida_view, self.back_to_login, Turno)) 

