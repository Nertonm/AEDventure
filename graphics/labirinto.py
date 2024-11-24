from random import shuffle, randrange, choice
from time import sleep
from PIL import ImageDraw
import pygame
from pygame import *
import sys
sys.setrecursionlimit(10000)


def fazer_caminho(tamanho, tela):
    x, y = tamanho
    caminho = [[x * 6 - 3, 3]]
    lugares_visitados = [[x * 6 - 3, 3]]
    linhas = []
    while [3, y * 6 - 3] not in lugares_visitados:
        escolhas = [0, 1, 2, 2, 3, 3]
        xx, yy = caminho[-1]
        parar = False
        while not parar:
            rdm = choice(escolhas)
            print(rdm)
            escolhas.remove(rdm)
            if rdm == 0:
                if [xx - 6, yy] not in lugares_visitados and xx - 6 > 0:
                    lugares_visitados.append([xx - 6, yy])
                    caminho.append([xx - 6, yy])
                    parar = True
            elif rdm == 1:
                if [xx, yy + 6] not in lugares_visitados and yy + 6 < y * 6:
                    lugares_visitados.append([xx, yy + 6])
                    caminho.append([xx, yy + 6])
                    parar = True
            elif rdm == 2:
                if [xx + 6, yy] not in lugares_visitados and xx + 6 < x * 6:
                    lugares_visitados.append([xx + 6, yy])
                    caminho.append([xx + 6, yy])
                    parar = True
            else:
                if [xx, yy - 6] not in lugares_visitados and yy - 6 > 0:
                    lugares_visitados.append([xx, yy - 6])
                    caminho.append([xx, yy - 6])
                    parar = True
        print(lugares_visitados)
        print(caminho)
        if not parar:
            caminho.pop()
    return caminho


class move():

    def esquerda(rgb, size, pos, id_jogador):
        r, g, b = rgb[pos[id_jogador][0][0] - size / 2, pos[id_jogador][0][1]]
        jogou = False
        if r == 0:
            jogou = True
            pos[id_jogador][0][0] -= size
        return pos, jogou

    def direita(rgb, size, pos, id_jogador):
        r, g, b = rgb[pos[id_jogador][0][0] + size / 2, pos[id_jogador][0][1]]
        jogou = False
        if r == 0:
            jogou = True
            pos[id_jogador][0][0] += size
        return pos, jogou

    def cima(rgb, size, pos, id_jogador):
        r, g, b = rgb[pos[id_jogador][0][0], pos[id_jogador][0][1] - size / 2]
        jogou = False
        if r == 0:
            jogou = True
            pos[id_jogador][0][1] -= size
        return pos, jogou

    def baixo(rgb, size, pos, id_jogador):
        r, g, b = rgb[pos[id_jogador][0][0], pos[id_jogador][0][1] + size / 2]
        jogou = False
        if r == 0:
            jogou = True
            pos[id_jogador][0][1] += size
        return pos, jogou


def posicionar_jogadores(tela, posicoes, size):
    for p in posicoes.values():
        cor = p[1]
        x, y = p[0]
        pygame.draw.rect(tela, cor, ((x - size / 2 + 1, y - size / 2 + 1), (size - 1, size - 1)))


def verificar_vitoria(posicao, tamanho, size):
    for ID, p in posicao.items():
        if p[0] == [size / 2, tamanho[1] * size - size / 2]:
            return True

    return False


def gerar_labirinto(w=10, h=10):
    vis = [[0] * w + [1] for _ in range(h)] + [[1] * (w + 1)]
    ver = [["|  "] * w + ['|'] for _ in range(h)] + [[]]
    hor = [["+--"] * w + ['+'] for _ in range(h + 1)]

    def walk(x, y):
        vis[y][x] = 1

        d = [(x - 1, y), (x, y + 1), (x + 1, y), (x, y - 1)]
        shuffle(d)
        for (xx, yy) in d:
            if vis[yy][xx]: continue
            if xx == x: hor[max(y, yy)][x] = "+  "
            if yy == y: ver[y][max(x, xx)] = "   "
            walk(xx, yy)

    walk(randrange(w), randrange(h))
    linhas_colunas = [[], []]
    for (a, b) in zip(hor, ver):
        # print(''.join(a + ['\n'] + b), flush=True)
        for l in a:
            if l == "+--":
                linhas_colunas[0].append(1)
            elif l == "+":
                pass
            else:
                linhas_colunas[0].append(0)
        if len(b) != 0:
            for c in b:
                if "|" in c:
                    linhas_colunas[1].append(1)
                else:
                    linhas_colunas[1].append(0)

    return linhas_colunas


def desenha_fim_pillow(tela, tamanho, size=11):
    (x, y) = tamanho
    # size += 1
    # inicio = pygame.Rect((x*6-5,1),(5,5))
    # fim = pygame.Rect((1,y*(size-1)-size+2),(size-2,size-2))
    # ponto = pygame.Rect((x*6-4,2),(3,3))
    # pygame.draw.rect(tela,(48,163,221), inicio)
    tela.rectangle((1, y * size - size + 1, size - 1, y * size - 1), fill=(255, 0, 0), outline=(255, 0, 0))


# pygame.draw.rect(tela,(255,0,0), ponto)


def desenhar_labirinto_pillow(img, tamanho, posicoes, size=11):
    (x, y) = tamanho
    size = size + 1
    contX = contY = 0
    cor = (255, 255, 255)
    for yy in range(0, y * size + 1, size):
        for xx in range(0, x * size + 1, size):
            try:
                if posicoes[0][contX] == 1:
                    img.line((xx, yy, xx + size, yy), fill=cor)
                if posicoes[1][contY] == 1:
                    img.line((xx, yy, xx, yy + size), fill=cor)
                contX += 1
                contY += 1
            except:
                pass
        contX -= 1
    desenha_fim_pillow(img, tamanho, size)


def avancar(tela, jogadas, todas_jogadas, rgb, ultima_jogada, x, y):
    j = jogadas[:]
    d_fim = [[j[0][-1][0] - 3, j[0][-1][1]],
             [j[0][-1][0], j[0][-1][1] + 3],
             [j[0][-1][0] + 3, j[0][-1][1]],
             [j[0][-1][0], j[0][-1][1] - 3]]

    for c in range(4):
        add = True
        var = 1
        cc = c
        r, g, b = rgb[(d_fim[c][0], d_fim[c][1])]
        if c == 0 and r != 0 and ultima_jogada != "D" and j[0] + [[d_fim[0][0] - 3, d_fim[0][1]]] not in todas_jogadas:
            var = [d_fim[0][0] - 3, d_fim[0][1]]
            pygame.draw.line(tela, (255, 0, 0), (j[0][-1]), var)
            ultima_jogada = "E"
            break
        elif c == 1 and r != 0 and ultima_jogada != "C" and j[0] + [
            [d_fim[1][0], d_fim[1][1] + 3]] not in todas_jogadas:
            var = [d_fim[1][0], d_fim[1][1] + 3]
            pygame.draw.line(tela, (255, 0, 0), (j[0][-1]), var)
            ultima_jogada = "B"
            # add = True
            break
        elif c == 2 and r != 0 and ultima_jogada != "E" and j[0] + [
            [d_fim[2][0] + 3, d_fim[2][1]]] not in todas_jogadas:
            var = [d_fim[2][0] + 3, d_fim[2][1]]
            pygame.draw.line(tela, (255, 0, 0), (j[0][-1]), var)
            ultima_jogada = "D"
            break
        elif c == 3 and r != 0 and ultima_jogada != "B" and j[0] + [
            [d_fim[3][0], d_fim[3][1] - 3]] not in todas_jogadas:
            var = [d_fim[3][0], d_fim[3][1] - 3]
            pygame.draw.line(tela, (255, 0, 0), (j[0][-1]), var)
            ultima_jogada = "C"
            break
        else:
            add = False

    if add:
        if var != 1:
            jogadas[1].append(ultima_jogada)
            jogadas[0].append(var)
    # print(jogadas)
    # print(jogadas[0])
    return ultima_jogada, jogadas[:], add, venceu(x, y, var)


def voltar(tela, jogadas, tamanho):
    inicio = jogadas[0][-1]
    fim = jogadas[0][-2]
    pygame.draw.line(tela, (255, 255, 255), inicio, fim)
    # print(jogadas[0])
    jogadas[0].pop()
    jogadas[1].pop()
    try:
        ultima_jogada = jogadas[1][-1]
    except:
        ultima_jogada = ""
        desenha_inicio_fim(tela, tamanho)
    # print(jogadas[0])
    return jogadas, True, ultima_jogada


def venceu(x, y, var, size=11):
    # print(var)
    size = size + 1
    # print([x*22-11,y*22-11])
    if var == [3, y * size - size / 2]:
        return True
    return False
