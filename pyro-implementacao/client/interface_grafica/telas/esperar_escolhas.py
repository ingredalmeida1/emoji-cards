import arcade
import arcade.gui # submódulo gui do arcade, que fornece componentes para criar interfaces gráficas.

from ..resources.constantes import LARGURA_TELA, ALTURA_TELA, AZUL, AMARELO, POPPINS, AGRANDIR

from ..telas.vencedor_turno import VencedorTurno

class EsperarEscolhas(arcade.View):
    def __init__(self, cliente, emocao, atributo_turno, pontuacao, id_partida, criar_partida_view, back_to_login, novo_turno):
        super().__init__()

        arcade.set_background_color(AZUL)
        
        self.cliente = cliente
        self.atributo = atributo_turno
        self.pontuacao = pontuacao
        self.id_partida = id_partida

        self.username_usuario = self.cliente.get_username()
        self.emocao_escolhida = emocao
         
        self.criar_partida_view = criar_partida_view
        self.back_to_login = back_to_login
        self.novo_turno = novo_turno

        self.centro = None
        self.esquerda = None
        self.direita = None
        
        self.outros_jogadores = [username for username in self.pontuacao.keys() if username != self.username_usuario ] 
        
        self.username_1 = self.username_usuario # usuario fica no meio
        self.username_2 = self.outros_jogadores[0]
        self.username_3 = self.outros_jogadores[1] 

        self.pontuacao_1 = self.pontuacao[self.username_1]
        self.pontuacao_2 = self.pontuacao[self.username_2]
        self.pontuacao_3 = self.pontuacao[self.username_3]

        self.fundo_atributo = arcade.load_texture("interface_grafica/resources/widgets/campo.png")

    def setup(self):
        #self.centro = arcade.load_texture(f"interface_grafica/resources/cartas/{self.emocao_escolhida}.png")
        self.centro = arcade.load_texture("interface_grafica/resources/cartas/carta-tras.png")
        self.esquerda = arcade.load_texture("interface_grafica/resources/cartas/carta-tras.png")
        self.direita = arcade.load_texture("interface_grafica/resources/cartas/carta-tras.png")
        
    def on_show(self):
        self.setup()     

    def on_draw(self):
        arcade.start_render()

        arcade.draw_texture_rectangle(LARGURA_TELA//2, ALTURA_TELA // 2 - 50, 180, 250, self.centro)
        arcade.draw_texture_rectangle(LARGURA_TELA//2 - 200, ALTURA_TELA // 2 - 50, 180, 250, self.esquerda)
        arcade.draw_texture_rectangle(LARGURA_TELA//2 + 200, ALTURA_TELA // 2 - 50, 180, 250, self.direita)
        
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
        


    # define o método on_update, chamado a cada atualização do quadro, por exemplo atualiza algum atributo.
    def on_update(self, delta_time: float):
        if self.cliente.mensagem_servidor:
            if self.cliente.mensagem_servidor.startswith("fim_turno"):
                
                #pega a mensagem e libera a variável compartilhada
                _, vencedor, novo_atributo, id_partida, escolhas_cada_jogador, pontuacao = self.cliente.mensagem_servidor.split(';')
                self.cliente.mensagem_servidor = None
                escolhas = eval(escolhas_cada_jogador)
                pontuacao = eval(pontuacao)
                
                self.window.show_view(VencedorTurno(self.cliente, self.atributo, vencedor, escolhas, pontuacao, id_partida, novo_atributo, self.criar_partida_view, self.back_to_login, self.novo_turno, ultimo=False, vencedor_partida='-', carta_adicionada='-'))
            
            elif self.cliente.mensagem_servidor.startswith("fim_partida"):    
                #pega a mensagem e libera a variável compartilhada

                _, vencedor_turno, novo_atributo, id_partida, escolhas_cada_jogador, pontuacao, vencedor_partida, carta_adicionada  = self.cliente.mensagem_servidor.split(';')
                self.cliente.mensagem_servidor = None
                escolhas = eval(escolhas_cada_jogador)
                pontuacao = eval(pontuacao)
                
                self.window.show_view(VencedorTurno(self.cliente, self.atributo, vencedor_turno, escolhas, pontuacao, id_partida, novo_atributo, self.criar_partida_view, self.back_to_login, self.novo_turno, ultimo=True, vencedor_partida=vencedor_partida, carta_adicionada=carta_adicionada))
                