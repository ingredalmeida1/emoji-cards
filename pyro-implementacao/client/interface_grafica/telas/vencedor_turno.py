import arcade
import arcade.gui # submódulo gui do arcade, que fornece componentes para criar interfaces gráficas.

from ..resources.constantes import LARGURA_TELA, ALTURA_TELA, AZUL, AMARELO, POPPINS, AGRANDIR

import threading
from ..telas.vencedor_partida import VencedorPartida

class VencedorTurno(arcade.View):
    def __init__(self, cliente, atributo, vencedor, escolhas, pontuacao, id_partida, atributo_novo_turno, criar_partida_view, back_to_login, novo_turno, ultimo, vencedor_partida, carta_adicionada):
        super().__init__()

        arcade.set_background_color(AZUL)
    
        self.cliente = cliente
        self.atributo = atributo
        self.vencedor = vencedor
        self.escolhas = escolhas
        self.pontuacao = pontuacao
        self.id_partida = id_partida
        self.atributo_novo_turno = atributo_novo_turno
        
        self.ultimo = ultimo
        self.vencedor_partida = vencedor_partida
        self.carta_adicionada = carta_adicionada
         
        self.username_usuario = self.cliente.get_username()

        self.criar_partida_view = criar_partida_view
        self.back_to_login = back_to_login
        self.novo_turno = novo_turno

        self.centro = None
        self.esquerda = None
        self.direita = None
        
        self.resultado = None   
        
        self.outros_jogadores = [username for username in self.pontuacao.keys() if username != self.username_usuario ] 
        
        self.username_1 = self.username_usuario # usuario fica no meio
        self.username_2 = self.outros_jogadores[0]
        self.username_3 = self.outros_jogadores[1] 
        
        self.usernames = [self.username_1,self.username_2,self.username_3]    
        
        if self.vencedor == "empate":
    
            self.resultado = "Empatou ;)"
            
            self.cores = [arcade.color.WHITE,arcade.color.WHITE,arcade.color.WHITE]
            

        else:            
            self.resultado = f"{self.vencedor} venceu com a emocao {self.escolhas[self.vencedor]}!"
            
            self.cores = []
            for username in self.usernames:
                if username == self.vencedor:
                    self.cores.append(AMARELO)
                else:
                    self.cores.append(arcade.color.WHITE)
            
        self.pontuacao_1 = str(self.pontuacao[self.username_1])
        self.pontuacao_2 = str(self.pontuacao[self.username_2])
        self.pontuacao_3 = str(self.pontuacao[self.username_3])
        
        self.escolha_1 = str(self.escolhas[self.username_1])
        self.escolha_2 = str(self.escolhas[self.username_2])
        self.escolha_3 = str(self.escolhas[self.username_3])       

        self.fundo_atributo = arcade.load_texture("interface_grafica/resources/widgets/campo.png")

        self.botoes = []

        self.b_proximo = arcade.load_texture("interface_grafica/resources/widgets/botoes/b-proximo.png")
        self.botoes.append({
            'texture': self.b_proximo,
            'x': LARGURA_TELA - 100,
            'y': 50,
            'width': 120,
            'height': 30,
            'action': self.mudar_tela
        })

    def setup(self):
        self.centro = arcade.load_texture(f"interface_grafica/resources/cartas/{self.escolha_1}.png")
        self.esquerda = arcade.load_texture(f"interface_grafica/resources/cartas/{self.escolha_2}.png")
        self.direita = arcade.load_texture(f"interface_grafica/resources/cartas/{self.escolha_3}.png")
        
    def on_show(self):
        self.setup()     

    def on_draw(self):
        arcade.start_render()

        arcade.draw_texture_rectangle(LARGURA_TELA//2, ALTURA_TELA // 2 - 50, 180, 250, self.centro)
        arcade.draw_text(self.username_1, LARGURA_TELA//2, 100, self.cores[0], 
                         font_size=15, font_name=POPPINS, anchor_x="center")
        
        arcade.draw_texture_rectangle(LARGURA_TELA//2 - 200, ALTURA_TELA // 2 - 50, 180, 250, self.esquerda)
        arcade.draw_text(self.username_2, LARGURA_TELA//2 - 200, 100,  self.cores[1], 
                         font_size=15, font_name=POPPINS, anchor_x="center")
        
        arcade.draw_texture_rectangle(LARGURA_TELA//2 + 200, ALTURA_TELA // 2 - 50, 180, 250, self.direita)
        arcade.draw_text(self.username_3, LARGURA_TELA//2 + 200, 100,  self.cores[2], 
                         font_size=15, font_name=POPPINS, anchor_x="center")

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
        
        arcade.draw_text(self.resultado, LARGURA_TELA//2,  50, AMARELO, 
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

    def mudar_tela(self):
        if (self.ultimo == True):
                self.window.show_view(VencedorPartida(self.cliente, self.vencedor_partida, self.carta_adicionada, self.pontuacao, self.criar_partida_view, self.back_to_login)) 
        
        else:
            self.window.show_view(self.novo_turno(self.cliente, self.atributo_novo_turno, self.pontuacao, self.id_partida, self.criar_partida_view,self.back_to_login)) 
