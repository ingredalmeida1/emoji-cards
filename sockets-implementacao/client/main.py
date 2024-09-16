import arcade 
from interface_grafica.telas.login import Login

from interface_grafica.resources.constantes import LARGURA_TELA, ALTURA_TELA, TITULO

from client import Client

def main():
    # cria uma instância da janela com 800x600 pixels, o título configurado para incluir o nome do cliente, e permite que a janela seja redimensionada.
    window = arcade.Window(LARGURA_TELA, ALTURA_TELA, TITULO, resizable=False)
    
    cliente = Client()
    
    # cria uma instância da visão principal 
    main_view = Login(cliente)
    
    #Define a main_view como a visão que deve ser exibida na janela.
    window.show_view(main_view)
    
    #inicia o loop principal do arcade, que mantém a aplicação em execução e atualiza a tela.
    arcade.run()

if __name__ == "__main__":
    main()