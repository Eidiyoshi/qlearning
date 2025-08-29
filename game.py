#python -m pip install -U pgzero
import pgzrun
import numpy as np
import random

TILE_SIZE = 64
WIDTH_SIZE = 9
HEIGHT_SIZE = 9
WIDTH = TILE_SIZE * WIDTH_SIZE
HEIGHT = TILE_SIZE * HEIGHT_SIZE
np.set_printoptions(formatter={'float': lambda x: "{0:0.3f}".format(x)})

acoes = ["cima","baixo","esquerda","direita"]

tiles = ['vazio', 'parede', 'fim', 'trap']

maze = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 1, 2, 0, 0, 1],
    [1, 0, 1, 0, 1, 1, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 1, 1, 0, 1],
    [1, 0, 1, 0, 1, 0, 0, 0, 1],
    [1, 3, 1, 3, 0, 0, 1, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1]
]



xStart = 3
yStart = 1
player = Actor("player", anchor=(0, 0), pos=(xStart * TILE_SIZE, yStart * TILE_SIZE))

def draw():
    screen.clear()
    for row in range(len(maze)):
        for column in range(len(maze[row])):
            x = column * TILE_SIZE
            y = row * TILE_SIZE
            tile = tiles[maze[row][column]]
            screen.blit(tile, (x, y))
    player.draw()

def on_key_down(key):
    # player movement
    row = int(player.y / TILE_SIZE)
    column = int(player.x / TILE_SIZE)
    if key == keys.UP:
        row = row - 1
    if key == keys.DOWN:
        row = row + 1
    if key == keys.LEFT:
        column = column - 1
    if key == keys.RIGHT:
        column = column + 1
    
    tile = tiles[maze[row][column]]

    if tile == 'vazio':
        x = column * TILE_SIZE
        y = row * TILE_SIZE
        animate(player, duration=0.1, pos=(x, y))
    if tile == 'fim':
        print("done")
        exit()
    if tile == 'trap':
        print("dead")
        exit()

def reward(x,y,acaoNumero):
    if acaoNumero == 0:
        y = y - 1
    if acaoNumero == 1:
        y = y + 1
    if acaoNumero == 2:
        x = x - 1
    if acaoNumero == 3:
        x = x + 1
    tile = tiles[maze[y][x]]
    if tile == "vazio":
        return -0.05
    if tile == "parede":
        return -0.5
    if tile == "fim":
        return 100
    if tile == "trap":
        return -10

def definirPosicao(x,y,acaoNumero):
    if acaoNumero == 0:
        y = y - 1
    if acaoNumero == 1:
        y = y + 1
    if acaoNumero == 2:
        x = x - 1
    if acaoNumero == 3:
        x = x + 1
    return x, y

def proximaAcao(x,y, explorationRate, qlearning):
    r = random.randint(0,10)
    if r < explorationRate: # nao ira explorar, ira exploitar
        return np.argmax(qlearning[y][x])
    return random.randint(0,3) # yay random explore

def treinar(qlearning, learningRate, discoutingFactor, explorationRate, maxEpisodes, xStart, yStart):
    for episodes in range(maxEpisodes):
        x = xStart
        y = yStart
        while(tiles[maze[y][x]] != "fim"):
            acaoNumero = proximaAcao(x,y,explorationRate, qlearning)
            rewardVar = reward(x,y,acaoNumero)
            
            xTemp, yTemp = definirPosicao(x,y,acaoNumero)
            qlearning[y,x,acaoNumero] = (1 - learningRate ) * qlearning[y,x,acaoNumero] + learningRate * (rewardVar + discoutingFactor * np.max(qlearning[yTemp][xTemp]))
            if(tiles[maze[yTemp][xTemp]] != "parede"):
                x, y = definirPosicao(x,y,acaoNumero)
            
    
    # desenhar grid
    print(qlearning)




learningRate = 0.5
discoutingFactor = 0.95
explorationRate = 8
maxEpisodes = 300
qlearning = np.zeros((HEIGHT_SIZE,WIDTH_SIZE,4)) # qlearning table
treinar(qlearning,learningRate,discoutingFactor,explorationRate,maxEpisodes,xStart,yStart)
pgzrun.go()
