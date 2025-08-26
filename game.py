#python -m pip install -U pgzero
import pgzrun
import numpy as np

TILE_SIZE = 64
WIDTH_SIZE = 9
HEIGHT_SIZE = 9
WIDTH = TILE_SIZE * WIDTH_SIZE
HEIGHT = TILE_SIZE * HEIGHT_SIZE

qlearning = np.zeros((WIDTH_SIZE,HEIGHT_SIZE,4)) # qlearning table

tiles = ['empty', 'wall', 'goal', 'trap']

maze = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 1, 2, 0, 0, 1],
    [1, 0, 1, 0, 1, 1, 0, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 0, 0, 1],
    [1, 3, 1, 3, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1]
]

player = Actor("player", anchor=(0, 0), pos=(1 * TILE_SIZE, 1 * TILE_SIZE))

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

    if tile == 'empty':
        x = column * TILE_SIZE
        y = row * TILE_SIZE
        animate(player, duration=0.1, pos=(x, y))
    if tile == 'goal':
        print("Well done")
        exit()
    if tile == 'trap':
        print("dead")
        exit()


pgzrun.go()