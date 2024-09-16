import arcade
import arcade.gui # submódulo gui do arcade, que fornece componentes para criar interfaces gráficas.

from ..resources.constantes import LARGURA_TELA, ALTURA_TELA, AZUL, AMARELO, POPPINS, AGRANDIR

from ..telas.aguardar_jogadores import AguardarJogadores

import threading

# define a classe LoginView que herda de arcade.View. Cada classe View representa uma tela ou seção da aplicação.
class ResponderConvite(arcade.View): 
    def __init__(self, cliente, username_dono, id_partida,criar_partida_view, back_to_login):
        super().__init__() # chama o construtor da classe base (arcade.View) para garantir que a visão seja corretamente inicializada.
        self.gerencia_entrada = arcade.gui.UIManager() # cria uma instância do gerenciador de interface do usuário, que será usado para gerenciar os elementos gráficos
        self.logo = arcade.load_texture(f"interface_grafica/resources/widgets/logo.png")
        
        self.cliente = cliente
        self.username_dono = username_dono
        self.id_partida = id_partida   
        
        self.exibir_popup = True
        
        self.criar_partida_view = criar_partida_view
        self.back_to_login = back_to_login
        
        self.resposta = None
        
        self.setup() # chama o método setup para configurar a interface gráfica da visão.

    # define o método setup, que configura os componentes da interface gráfica.
    def setup(self):
        
        self.fundo_popup = arcade.load_texture("interface_grafica/resources/widgets/popup.png")

        self.logo = arcade.load_texture("interface_grafica/resources/widgets/logo.png")

        self.botoes = []
        self.b_recusar = arcade.load_texture("interface_grafica/resources/widgets/botoes/b-recusar.png")
        self.b_aceitar = arcade.load_texture("interface_grafica/resources/widgets/botoes/b-aceitar.png")
        self.botoes.append({
            'texture': self.b_recusar,
            'x': LARGURA_TELA//2 - 100,
            'y': ALTURA_TELA//2 - 90,
            'width': 150,
            'height': 60,
            'action': self.recusar_convite 
        })
        self.botoes.append({
            'texture': self.b_aceitar,
            'x': LARGURA_TELA//2 + 100,
            'y': ALTURA_TELA//2 - 90,
            'width': 150,
            'height': 60,
            'action': self.aceitar_convite 
        })
        
        # # cria um layout vertical para organizar os widgets (elementos gráficos)
        # vbox = arcade.gui.UIBoxLayout()
        
        # # campo de texto para mostrar mensagem
        # self.titulo = arcade.gui.UITextArea(
        #     text="Bora Jogar?", width=400, height=40, font_size=25, font_name=AGRANDIR, text_color=AMARELO
        # )
        # # adiciona o campo de texto ao layout vertical
        # vbox.add(self.titulo)

        # # campo de texto para mostrar mensagem
        # self.descricao = arcade.gui.UITextArea(
        #     text=f"{self.username_dono} convidou você para jogar.", width=400, height=40, font_size=14, font_name=POPPINS
        # )
        # # adiciona o campo de texto ao layout vertical
        # vbox.add(self.descricao)

        # # cria um campo de texto (UITextArea) que exibirá mensagens. define suas dimensões e o tamanho da fonte.
        # self.msg = arcade.gui.UITextArea(
        #     text="", width=450, height=40, font_size=14
        # )
        # vbox.add(self.msg)
        
        # aceitar_button = arcade.gui.UIFlatButton(
        #     text="ACEITAR", width=100, style={
        #                                     "font_name": POPPINS,
        #                                     "font_size": 14,
        #                                     "font_color": AZUL,
        #                                     "border_width": 3,
        #                                     "border_color": arcade.color.WHITE,
        #                                     "bg_color": AMARELO
        #                                 }
        # )

        # @aceitar_button.event
        # def on_click(event):
        #     self.resposta = "aceito"
        #     threading.Thread(target=self.enviar_resposta).start()
                        
        # vbox.add(aceitar_button)
        
        # recusar_button = arcade.gui.UIFlatButton(
        #     text="RECUSAR", width=100, style={
        #                                     "font_name": POPPINS,
        #                                     "font_size": 14,
        #                                     "font_color": AZUL,
        #                                     "border_width": 3,
        #                                     "border_color": arcade.color.WHITE,
        #                                     "bg_color": AMARELO
        #                                 }
        # )

        # @recusar_button.event
        # def on_click(event):
        #     self.resposta = "recuso"
        #     threading.Thread(target=self.enviar_resposta).start()
            
        # vbox.add(recusar_button)
        
        # # Adiciona o layout à interface do usuário
        # self.gerencia_entrada.add(
        #     arcade.gui.UIAnchorWidget(
        #         anchor_x="center_x", anchor_y="center_y", child=vbox
        #     )
        # )
    
    # define o método on_update, chamado a cada atualização do quadro, por exemplo atualiza algum atributo.
    def on_update(self, delta_time: float):
        if self.resposta:
            if self.resposta == "aceito":
                self.resposta = None
                self.window.show_view(AguardarJogadores(self.cliente, self.criar_partida_view, self.back_to_login))
                
            else:
                #se recusou: volta pra criar partida
                self.resposta = None
                self.window.show_view(self.criar_partida_view(self.cliente, self.back_to_login)) 
                     

    # define o método on_show_view, chamado quando a visão é exibida.
    def on_show_view(self):
        # define a cor de fundo da janela.
        arcade.set_background_color(AZUL)
        # habilita o gerenciador de interface, tornando os widgets interativos.
        self.gerencia_entrada.enable()
        
    # define o método on_hide_view, chamado quando a visão é escondida. Desativa o gerenciador de interface.
    def on_hide_view(self):
        # desativa o gerenciador de interface, tornando os widgets não interativos.
        self.gerencia_entrada.disable()

    # define o método on_draw, chamado a cada atualização da tela. Limpa a tela e desenha os widgets.
    def on_draw(self):
        # limpa o conteúdo da tela.
        self.clear()
                
        arcade.draw_texture_rectangle(0, 0, self.logo.width//100,
                                          self.logo.height//100, self.logo)
            
        self.gerencia_entrada.draw()
        
        if self.exibir_popup:
            self.desenhar_popup()

    def desenhar_popup(self):
        arcade.draw_texture_rectangle(LARGURA_TELA // 2, ALTURA_TELA // 2, 500, 350, self.fundo_popup)
        
        arcade.draw_text(f"{self.cliente.get_username()},", 
                    LARGURA_TELA // 2, ALTURA_TELA // 2 + 140, arcade.color.WHITE, 
                    font_size=15, font_name=POPPINS, anchor_x="center")

        arcade.draw_text("Bora Jogar?", LARGURA_TELA // 2, ALTURA_TELA // 2 + 90, AMARELO, 
                         font_size=25, font_name=AGRANDIR, anchor_x="center")
        
        arcade.draw_text(f"{self.username_dono} te convidou para", 
                         LARGURA_TELA // 2, ALTURA_TELA // 2 + 50, arcade.color.WHITE, 
                         font_size=15, font_name=POPPINS, anchor_x="center")
        arcade.draw_text(f"jogar uma partida!", 
                         LARGURA_TELA // 2, ALTURA_TELA // 2 + 25, arcade.color.WHITE, 
                         font_size=15, font_name=POPPINS, anchor_x="center")
        
        if self.logo:
            arcade.draw_texture_rectangle(LARGURA_TELA//2, ALTURA_TELA // 2 - 15, 150, 80, self.logo)        
            
        for botao in self.botoes:
            if 'texture' in botao:
                arcade.draw_texture_rectangle(botao['x'], botao['y'], botao['width'], botao['height'], 
                                              botao['texture'])
    
    def on_mouse_press(self, x, y, button, modifiers):
        for botao in self.botoes:
            if 'texture' in botao:
                if (botao['x'] - botao['width'] / 2 < x < botao['x'] + botao['width'] / 2 and
                        botao['y'] - botao['height'] / 2 < y < botao['y'] + botao['height'] / 2):
                    botao['action']()
                    break

        if (LARGURA_TELA // 2 - 100 < x < LARGURA_TELA // 2 + 100 and
                ALTURA_TELA // 2 - 25 < y < ALTURA_TELA // 2 + 25):
            self.exibir_popup = True

        self.on_draw()
    
    def aceitar_convite(self):
        self.resposta = "aceito"
        threading.Thread(target=self.enviar_resposta).start()

    def recusar_convite(self):
        self.resposta = "recuso"
        threading.Thread(target=self.enviar_resposta).start()
        # self.exibir_popup = False
    
    def enviar_resposta(self):
        self.cliente.responder_convite(self.resposta, self.id_partida)

