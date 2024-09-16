import arcade
import arcade.gui # submódulo gui do arcade, que fornece componentes para criar interfaces gráficas.

from ..resources.constantes import LARGURA_TELA, ALTURA_TELA, AZUL, AMARELO, POPPINS, AGRANDIR

import threading

from ..telas.perfil import Perfil
from ..telas.aguardar_jogadores import AguardarJogadores
from ..telas.responder_convite import ResponderConvite

class CriarPartida(arcade.View):
    def __init__(self, cliente, login_view):
        super().__init__()

        arcade.set_background_color(AZUL)
        
        self.back_to_login = login_view

        self.botoes = []
        self.fundo_campo_jogador1 = None
        self.fundo_campo_jogador2 = None

        self.gerencia_entrada = arcade.gui.UIManager()
        
        #atributos comunicacao:
        self.cliente = cliente
        self.mensagem = None
        
        self.setup() # chama o método setup para configurar a interface gráfica da visão.

    def setup(self):
        
        self.campo_jogador1 = arcade.gui.UIInputText(
            text = '',
            width = 280,
            text_color = arcade.color.WHITE,
            font_name = POPPINS
        )
        
        self.gerencia_entrada.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="left",
                anchor_y="bottom",
                align_x=LARGURA_TELA//2 - 140,
                align_y=338,
                child=self.campo_jogador1
            )
        )

        self.campo_jogador2 = arcade.gui.UIInputText(
            text='',
            width=280,
            text_color = arcade.color.WHITE,
            font_name = POPPINS
        )

        self.gerencia_entrada.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="left",
                anchor_y="bottom",
                align_x=LARGURA_TELA//2 - 140,
                align_y=238,
                child=self.campo_jogador2
            )
        )
        
        self.b_partida = arcade.load_texture("interface_grafica/resources/widgets/botoes/b-partida.png")
        self.b_perfil = arcade.load_texture("interface_grafica/resources/widgets/botoes/b-perfil.png")
        self.fundo_campo_jogador1 = arcade.load_texture("interface_grafica/resources/widgets/campo.png")
        self.fundo_campo_jogador2 = arcade.load_texture("interface_grafica/resources/widgets/campo.png")

        self.botoes.append({
            'texture': self.b_partida,
            'x': LARGURA_TELA//2,
            'y': 200,
            'width': 290,
            'height': 70,
            'action': self.criar_partida
        })
        self.botoes.append({
            'texture': self.b_perfil,
            'x': 970,
            'y': 570,
            'width': 35,
            'height': 35,
            'action': self.perfil
        })
        
        #auxiliar:
        vbox = arcade.gui.UIBoxLayout()
        self.msg = arcade.gui.UITextArea(
            text="", height=40, font_size=12, font_name=POPPINS, text_color=arcade.color.RED
        )
        vbox.add(self.msg)
        
        self.gerencia_entrada.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center", anchor_y="top", child=vbox
            )
        )

    def on_draw(self):
        arcade.start_render()
        
        for botao in self.botoes:
            if 'texture' in botao:
                arcade.draw_texture_rectangle(botao['x'], botao['y'], botao['width'], botao['height'], 
                                              botao['texture'])

        if self.fundo_campo_jogador1:
            arcade.draw_texture_rectangle(LARGURA_TELA//2, 380, 350, 
                                          60, self.fundo_campo_jogador1)
        if self.fundo_campo_jogador2:
            arcade.draw_texture_rectangle(LARGURA_TELA//2, 280, 350, 
                                          60, self.fundo_campo_jogador2)
            
        arcade.draw_text(self.cliente.get_username(), 950, 560,
                         AMARELO, font_size=12, font_name=POPPINS,  anchor_x="right")
        
        arcade.draw_text("username 1", LARGURA_TELA//2, 415,
                         arcade.color.WHITE, font_size=15, font_name=POPPINS, anchor_x="center")
        arcade.draw_text("username 2", LARGURA_TELA//2, 315,
                         arcade.color.WHITE, font_size=15, font_name=POPPINS, anchor_x="center")

        self.gerencia_entrada.draw()
                
    def on_mouse_press(self, x, y, button, modifiers):
        self.msg.text = ""

        for botao in self.botoes:
            if 'texture' in botao:
                if (botao['x'] - botao['width'] / 2 < x < botao['x'] + botao['width'] / 2 and
                        botao['y'] - botao['height'] / 2 < y < botao['y'] + botao['height'] / 2):
                    botao['action']()
                    break
           
    def on_update(self, delta_time: float):
        if self.mensagem:
            if self.mensagem == "Inicia Criacao Partida":
                self.window.show_view(AguardarJogadores(self.cliente, CriarPartida, self.back_to_login))
            
            self.msg.text = self.mensagem
            self.mensagem = None
        
        if self.cliente.mensagem_servidor:
            if self.cliente.mensagem_servidor.startswith("convite"):
                _,username_dono,id_partida = self.cliente.mensagem_servidor.split(',')
                self.window.show_view(ResponderConvite(self.cliente,username_dono,id_partida, CriarPartida, self.back_to_login))
            
            #se não for, exibe a mensagem pro usuário
            self.msg.text = self.cliente.mensagem_servidor
            self.cliente.mensagem_servidor = None
            self.mensagem = None
                    
    def on_show_view(self):
        # habilita o gerenciador de interface, tornando os widgets interativos.
        self.gerencia_entrada.enable()     

    def on_hide_view(self):
        # desativa o gerenciador de interface, tornando os widgets não interativos.
        self.gerencia_entrada.disable()        
    
    # ações a serem executadas quando a janela é fechada
    def on_close(self):
        self.cliente.logout()

    def perfil(self):
    #     threading.Thread(target=self.comunicar_info_perfil).start()
    # def comunicar_info_perfil(self):
        s, msg = self.cliente.exibir_perfil()
        if s == True:
            info_perfil = msg
            '''
            info_perfil = {
                    'colecao_cartas': colecao_cartas,
                    'baralhos': baralhos,
                    'qtd_baralhos': qtd_baralhos
            }
            '''
            self.window.show_view(Perfil(self.cliente, info_perfil, self.back_to_login, CriarPartida)) 
        else:
            #ocorreu algum erro
            self.mensagem = msg
            
    def criar_partida(self):
        threading.Thread(target=self.comunicar_criar_partida).start()

    def comunicar_criar_partida(self):
        username1 = self.campo_jogador1.text
        username2 = self.campo_jogador2.text      
        if username1 != "" and username2 != "":
            self.mensagem = "Inicia Criacao Partida"
            self.cliente.criar_partida(username1, username2)
        else:
            self.mensagem = "Preencha Todos os Campos!"