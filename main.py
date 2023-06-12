# bibliotecas utilizadas
import numpy as np
import pygame
import math

# linhas e colunas do tabuleiro
linha = 8
coluna = 8
#tamanho do tabuleiro
tamanhoQuadrado = 70
# cor do tabuleiro
verdeClaro = (0, 128, 0)
# peças
branca = (255, 255, 255)
preto = (0, 0, 0)

#carregando imagens
pecaBranca = pygame.image.load("pecaBranca.png")
pecaBrancaImagem = pygame.transform.scale(pecaBranca, (65, 65))
pecaPreta = pygame.image.load("pecaPreta.png")
pecaPretaImagem = pygame.transform.scale(pecaPreta, (70, 70))

# iniciando o pygame
pygame.init()
# criando a tela
screen = pygame.display.set_mode((578, 685))
# titulo
pygame.display.set_caption("Reversi")


#retorna as coordenadas da peça como x e y
def matrizCoordenada(i, j):
    # cria lista de posição
    pos = [0, 0]
    # calcula a coordenada y
    pos[0] = tamanhoQuadrado * j + (2 * (j + 1))
    # calcula a coordenada x
    pos[1] = 90 + (tamanhoQuadrado * i) + (2 * i)
    # retorna a posição
    return pos

# retorna a posição do tabuleiro como i e j
def coordenadaMatriz(x, y):
    # cria lista de posição
    index = [0, 0]
    # calcula j
    index[0] = int(math.floor((x - 2) / (tamanhoQuadrado + 2)))
    # calcula i
    index[1] = math.floor((y - 90) / (tamanhoQuadrado + 2))
    #retorna a posição
    return index

def tabuleiro():
    #criando o tabuleiro
    #1 = peça branca
    #2 = peça preta
    tabuleiro = np.zeros((linha, coluna))
    tabuleiro[3][3] = 1
    tabuleiro[3][4] = 2
    tabuleiro[4][3] = 2
    tabuleiro[4][4] = 1
    return tabuleiro

def dicaPossiveisMovimentos(tabuleiro, vez):
    # criando uma matriz de dicas
    # utilizada para armazenar dicas de possiveis movimentos
    # 1 é valido e 0 é invalido
    dicas = np.zeros((linha, coluna))
    # criando matriz de movimentos possiveis
    # utilizada para armazenar os movimentos possiveis
    movimentosPossiveis = []
    for i in range(8):
        for j in range(8):
            #verifica se o movimento é valido utilizando a função
            if movimentoValido(tabuleiro, i, j, vez):
                # acrescenta 1 na matriz de dicas
                dicas[i][j] = 1
                # acrescenta o movimento na matriz de movimentos possiveis
                movimentosPossiveis.append([i, j])
    # retorna as dicas e os movimentos possiveis
    return dicas, movimentosPossiveis

def desenharTabuleiro():
    #desenhando o tabuleiro
    for j in range(coluna):
        for i in range(linha):
            #desenhando o tabuleiro
            #screen é a janela de exibição
            #verdeClaro é a cor do tabuleiro
            # as contas utilizadas são para que os quadrados sejam criados um ao lado do outro
            pygame.draw.rect(screen, verdeClaro,
                             (j * tamanhoQuadrado + 2 * (j + 1), (i * tamanhoQuadrado) + (2 * i) + 90, tamanhoQuadrado, tamanhoQuadrado))

    for j in range(coluna):
        for i in range(linha):
            #verifica se há uma peça branca na posição
            if tabuleiro[i][j] == 1:
                #verifica a posição da peça
                pos = matrizCoordenada(i, j)
                #desenha a peça
                screen.blit(pecaPretaImagem, (pos[0], pos[1]))
            # verifica se há uma peça preta na posição
            elif tabuleiro[i][j] == 2:
                # verifica a posição da peça
                pos = matrizCoordenada(i, j)
                # desenha a peça
                screen.blit(pecaBrancaImagem, (pos[0], pos[1]))
            # verifica se há uma dica na posição
            if dicas[i][j] == 1:
                # colore os possiveis espaços de jogada
                pygame.draw.rect(screen, (152 ,251,152),
                                 (j * tamanhoQuadrado + 2 * (j + 1), (i * tamanhoQuadrado) + (2 * i) + 90, tamanhoQuadrado,
                                  tamanhoQuadrado))
                pass

def desenharPontuacao(vez):
    #verifica de quem é a vez
    if vez == 1:
        v = "Preto"
    else:
        v = "Branco"
    #armazena a pontuação obtida
    pontuacoes = pontuacao()
    #tamanho da fonte
    font = pygame.font.SysFont(None, 30)
    #cria o texto
    pretaPontuacao = font.render("Preta Pontuação : " + str(pontuacoes[0]), True, (255, 255, 255))
    brancaPontuacao = font.render("Branca Pontuação : " + str(pontuacoes[1]), True, (255, 255, 255))
    vezJogador = font.render("Vez : " + v, True, (255, 255, 255))
    #desenha o texto
    screen.blit(pretaPontuacao, (10, 10))
    screen.blit(brancaPontuacao, (10, 40))
    screen.blit(vezJogador, (10, 70))

    pass

#calcula a pontuação
def pontuacao():
    pontuacoes = [0, 0]
    #percorre o tabuleiro
    for i in range(8):
        for j in range(8):
            #verifica se há uma peça branca
            if tabuleiro[i][j] == 1:
                #acrescenta 1 na pontuação
                pontuacoes[0] += 1
                # verifica se há uma peça preta
            elif tabuleiro[i][j] == 2:
                # acrescenta 1 na pontuação
                pontuacoes[1] += 1
    #retorna a pontuação
    return pontuacoes


def movimentoValido(tabuleiro, x, y, vez):
    #verifica se a posição está vazia
    if tabuleiro[x][y] != 0:
        return False
    
    #verifica se o movimento é valido
    direcoes = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, -1), (-1, 1)]
    #armazena as peças que serão giradas
    pecasGirar = []

    #percorre as direções
    for dx, dy in direcoes:
        #armazena a posição
        i, j = x + dx, y + dy
        #armazena as peças
        pecas = []

        #percorre as peças
        while 0 <= i < 8 and 0 <= j < 8:
            #verifica se a peça é do jogador
            if tabuleiro[i][j] == vez:
                #verifica se há peças para girar
                pecasGirar.extend(pecas)
                break
            #verifica se a peça é vazia
            if tabuleiro[i][j] == 0:
                break
            #adiciona a peça
            pecas.append((i, j))
            #atualiza a posição
            i += dx
            j += dy

    #verifica se há peças para girar
    if not pecasGirar:
        return False
    
    #retorna as peças para girar
    return pecasGirar


#verifica se o jogo acabou
def game_over():
    #tamanho da fonte
    fonte = pygame.font.SysFont(None, 90)
    for i in range(8):
        #verifica se há movimentos possiveis
        for j in range(8):
            if movimentoValido(tabuleiro, i, j, 1) != False or movimentoValido(tabuleiro, i, j, 2) != False:
                #se houver, retorna falso
                return False
    pontuacoes = pontuacao()
    #verifica quem ganhou
    if pontuacoes[0] > pontuacoes[1]:
        #escreve na tela
        gameOver = fonte.render("PRETO VENCEU", True, (0, 0, 0), (255, 255, 255))
        #imprime no console
        print("Peça preta venceu!")
        #desenha na tela
        screen.blit(gameOver, (10, 350))

    #se não, verifica se empatou
    elif pontuacoes[0] == pontuacoes[1]:
        #escreve na tela
        gameOver = fonte.render("EMPATE", True, (159, 158, 158), (0, 0, 0))
        #imprime no console
        print("Empate!")
        #desenha na tela
        screen.blit(gameOver, (10, 350))

    #se não, verifica se o branco ganhou
    else:
        #escreve na tela
        gameOver = fonte.render("BRANCO VENCEU", True, (255, 255, 255), (0, 0, 0))
        #imprime no console
        print("Peça branca venceu!")
        #desenha na tela
        screen.blit(gameOver, (10, 350))

    return True

def gerador(tabuleiro):
    #matriz com a heuristica de cada posição do tabuleiro
    heuristica = np.array([[1000, -10, 10, 10, 10, 10, -10, 1000],
                          [-10, -10, 1, 1, 1, 1, -10, -10],
                          [10, 1, 1, 1, 1, 1, 1, 10],
                          [10, 1, 1, 1, 1, 1, 1, 10],
                          [10, 1, 1, 1, 1, 1, 1, 10],
                          [10, 1, 1, 1, 1, 1, 1, 10],
                          [-10, -10, 1, 1, 1, 1, -10, -10],
                          [1000, -10, 10, 10, 10, 10, -10, 1000]])
    # inicialização das variáveis de pontuação e peso
    pontuacaoHumano = 0
    pontuacaoIA = 0
    pesoJogador = 0
    pesoIA = 0
    vazio = 0
    # percorre todas as posições do tabuleiro
    for i in range(8):
        for j in range(8):
            #verifica se a posição está vazia
            if tabuleiro[i][j] == 0:
                #acrescenta 1 na variavel vazio
                vazio += 1
            #verifica se a posição contém uma peça do jogador humano
            if tabuleiro[i][j] == 1:
                #acrescenta 1 na pontuação
                pontuacaoHumano += 1
                #acrescenta o peso da posição
                pesoJogador += heuristica[i][j]
            #verifica se a posição contém uma peça do jogador humano
            if tabuleiro[i][j] == 2:
                #acrescenta 1 na pontuação
                pontuacaoIA += 1
                #acrescenta o peso da posição
                pesoIA += heuristica[i][j]
    # verifica se ainda há posições vazias no tabuleiro
    if vazio > 0:
        # retorna os pesos do jogador e da IA
        return pesoIA, pesoJogador
    else:
        # retorna as pontuações do jogador e da IA
        return pontuacaoIA, pontuacaoHumano
    
def fazerMelhorMovimento(mover):
    #armazena o melhor movimento
    melhorMovimento[0] = mover[0]
    melhorMovimento[1] = mover[1]


def girar(tabuleiro, pecas, vez):
    #verifica se há peças para girar
    for i in range(len(pecas)):
        # obtém as coordenadas da peça atual
        #atualiza a posição no tabuleiro com a cor do jogador atual
        tabuleiro[pecas[i][0]][pecas[i][1]] = vez
    pass

def minimax_minimizer(tabuleiro, vez, profundidade, alpha, beta):
    ## Obtém a lista de movimentos possíveis para o jogador atual
    movimentos_possiveis = dicaPossiveisMovimentos(tabuleiro, vez)[1]
    # Verifica as condições de parada: se não há mais movimentos possíveis,
    # se o jogo não está em andamento ou se atingiu a profundidade máxima
    if len(movimentos_possiveis) == 0 or running == False or profundidade == 0:
        # obtém a pontuação do tabuleiro atual
        pontos = gerador(tabuleiro)
        # verifica a vez do jogador para determinar a pontuação final
        if vez == 2:
            pontos = pontos[0] - pontos[1]
            return pontos
        else:
            pontos = pontos[1] - pontos[0]
            return pontos
    else:
        # alterna a vez do jogador
        if vez == 1:
            proximo = 2
        else:
            proximo = 1

    # inicializa a pontuação mínima como infinito
    pontuacao_minima = math.inf
    # percorre todos os movimentos possíveis
    for movimento in movimentos_possiveis:
        # cria uma cópia do tabuleiro
        novo_tabuleiro = np.copy(tabuleiro)
        # obtém as peças que serão giradas pelo movimento atual
        pecasGirar = movimentoValido(tabuleiro, movimento[0], movimento[1], vez)
        # atualiza o tabuleiro com o movimento atual
        novo_tabuleiro[movimento[0]][movimento[1]] = vez
        girar(novo_tabuleiro, pecasGirar, vez)
        # chama a função minimax_maximizer para o próximo jogador
        pontos = minimax_maximizer(novo_tabuleiro, proximo, profundidade - 1, alpha, beta)
        # atualiza a pontuação mínima, se necessário
        if pontos < pontuacao_minima:
            pontuacao_minima = pontos
        # atualiza o valor de beta com a pontuação mínima encontrada até o momento
        beta = min(beta, pontos)
        # realiza o corte alpha-beta
        if beta <= alpha:
            break
    # retorna a pontuação mínima encontrada
    return pontuacao_minima


def minimax_maximizer(tabuleiro, vez, profundidade, alpha, beta):
    # Obtém a lista de movimentos possíveis para o jogador atual
    movimentos_possiveis = dicaPossiveisMovimentos(tabuleiro, vez)[1]
    # Verifica as condições de parada: se não há mais movimentos possíveis,
    # se o jogo não está em andamento ou se atingiu a profundidade máxima
    if len(movimentos_possiveis) == 0 or running == False or profundidade == 0:
        # obtém a pontuação do tabuleiro atual
        pontos = gerador(tabuleiro)
        # verifica a vez do jogador para determinar a pontuação final
        if vez == 2:
            pontos = pontos[0] - pontos[1]
            return pontos
        else:
            pontos = pontos[1] - pontos[0]
            return pontos
    else:
        # alterna a vez do jogador
        if vez == 1:
            proximo = 2
        else:
            proximo = 1
    # inicializa a pontuação máxima como -infinito
    pontuaçao_maxima = -math.inf
    # percorre todos os movimentos possíveis
    for mover in movimentos_possiveis:
        # cria uma cópia do tabuleiro
        novo_tabuleiro = np.copy(tabuleiro)
        # obtém as peças que serão giradas pelo movimento atual
        pecasGirar = movimentoValido(tabuleiro, mover[0], mover[1], vez)
        # atualiza o tabuleiro com o movimento atual
        novo_tabuleiro[mover[0]][mover[1]] = vez
        girar(novo_tabuleiro, pecasGirar, vez)
        # chama a função minimax_minimizer para o próximo jogador
        pontos = minimax_minimizer(novo_tabuleiro, proximo, profundidade - 1, alpha, beta)
        # atualiza a pontuação máxima, se necessário
        if pontos > pontuaçao_maxima:
            pontuaçao_maxima = pontos
            # verifica se a profundidade atual é igual à profundidade da IA
            # se sim, imprime o movimento como o melhor movimento atual
            if profundidade == profundidadeIA:
                print("Melhor movimento: " + str(mover))
                fazerMelhorMovimento(mover) 
        # atualiza o valor de alpha com a pontuação máxima encontrada até o momento
        alpha = max(alpha, pontos)
        # realiza o corte alpha-beta, se necessário
        if beta <= alpha:
            break
    # retorna a pontuação máxima encontrada
    return pontuaçao_maxima


# inicialização das variáveis
melhorMovimento = [0, 0] # variável para armazenar o melhor movimento
vez = 1 # variável para controlar a vez do jogador (1 para o jogador preto, 2 para o jogador branco)
tabuleiro = tabuleiro() # criação do tabuleiro
running = True #Variável para controlar o loop principal do jogo, se está rodando ou não
profundidadeIA = 2 # profundidade máxima para a busca do algoritmo minimax

while running:
    screen.fill((0, 0, 0)) # preenche a tela com uma cor de fundo
    dicas = dicaPossiveisMovimentos(tabuleiro, vez)[0] # obtém as dicas de possíveis movimentos
    movimentos_possiveis = dicaPossiveisMovimentos(tabuleiro, vez)[1] # obtém os movimentos possíveis

    desenharTabuleiro() # desenha o tabuleiro
    desenharPontuacao(vez) # desenha a pontuação

    #verifica se o jogo acabou
    if game_over():
        running = False
        # desenha a pontuação final
        desenharPontuacao(vez)
        pygame.display.update()
        # espera 5 segundos
        pygame.time.wait(5000)

    # verifica se há movimentos possíveis para o jogador atual e troca a vez
    if len(movimentos_possiveis) == 0:
        if vez == 1:
            print("Peça preta não pode fazer nenhum movimento! Próximo jogador!")
            vez = 2
        else:
            print("Peça branca não pode fazer nenhum movimento! Próximo jogador!")
            vez = 1

    # trata os eventos do pygame
    for event in pygame.event.get():
        # verifica se o usuário clicou no botão de fechar a janela
        if event.type == pygame.QUIT:
            running = False
        # verifica se o usuário clicou em alguma posição do tabuleiro
        if event.type == pygame.MOUSEBUTTONDOWN:
            # obtém as coordenadas do mouse
            x = event.pos[0]
            y = event.pos[1]
            j, i = coordenadaMatriz(x, y)

            #v verifica se a vez é do jogador branco
            if vez == 1:
                # verifica se o movimento é válido
                pecasGirar = movimentoValido(tabuleiro, i, j, 1)
                # se for, atualiza o tabuleiro e gira as peças
                if pecasGirar:
                    tabuleiro[i][j] = 1
                    girar(tabuleiro, pecasGirar, vez)
                    # reseta as dicas
                    dicas = np.zeros((linha, coluna))
                    # desenha o tabuleiro
                    desenharTabuleiro()
                    # atualiza a pontuação
                    pygame.display.update()
                    # troca a vez
                    vez = 2
    # verifica se a vez é do jogador preto
    if vez == 2:
        # espera 1 segundo
        pygame.time.wait(1000)
        # inicializa as variáveis alpha e beta
        alpha = -math.inf
        beta = math.inf
        # chama a função minimax_maximizer para o jogador atual
        minimax_maximizer(tabuleiro, vez, profundidadeIA, alpha, beta)  #encontra o melhor movimento
        # verifica se o movimento é válido
        pecasGirar = movimentoValido(tabuleiro, melhorMovimento[0], melhorMovimento[1], 2)
        # se for, atualiza o tabuleiro e gira as peças
        if pecasGirar:
            tabuleiro[melhorMovimento[0]][melhorMovimento[1]] = 2
            girar(tabuleiro, pecasGirar, vez)
        #troca a vez
        vez = 1
    # atualiza a tela
    pygame.display.update()