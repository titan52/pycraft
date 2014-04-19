import random
import copy

from console import CLEAR
from colors import colorStr, BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE


def move_map(map_, edges):

    # Create subset of slices from map_ between edges
    slices = {}
    for pos in range(*edges):
        slices[pos] = map_[str(pos)]
    return slices


def render_map(map_, player_x, player_y, blocks):

    # Sorts the dict as a list by pos
    map_ = list(map_.items())
    map_.sort(key=lambda item: int(item[0]))

    # Seperates the pos and data
    map_ = tuple(zip(*map_))[1]

    # Orientates the data
    map_ = tuple(zip(*map_))

    # Output the map
    out = ''
    for y, row in enumerate(map_):
        for x, pixel in enumerate(row):

            # Add the player
            if x == player_x and y in [player_y, player_y - 1]:
                pixel = '^*'[y - player_y]

            out += blocks[pixel][0]
        out += '\n'

    print(CLEAR + out, end='')


def slice_height(pos, meta):

    slice_height_ = meta['ground_height']

    # Check surrounding slices for a hill
    for x in range(pos - meta['max_hill'] * 2, pos + meta['max_hill'] * 2):
        # Set seed for random numbers based on position
        random.seed(str(meta['seed']) + str(x))

        # Generate a hill with a 15% chance
        if random.randint(0, 100) < 15:
            # Set height to height of hill minus distance from hill
            hill_height = (meta['ground_height'] +
                random.randint(0, meta['max_hill']) - abs(pos-x)/2)

            if hill_height > slice_height_:
                slice_height_ = hill_height

    return int(slice_height_)


def gen_slice(pos, meta):

    slice_height_ = slice_height(pos, meta)

    # Form slice of sky - ground - stone layers
    slice_ = ([' '] * (meta['height'] - slice_height_) +
        ['-'] + ['#'] * (slice_height_ - 1))

    return slice_


def detect_edges(map_, edges):

    slices = []
    for pos in range(*edges):
        try:
            # If it doesn't exist add the pos to the list
            map_[str(pos)]
        except KeyError:
            slices.append(pos)

    return slices


def is_solid(blocks, block):
    return blocks[block][1]


def gen_blocks():

    # Block dict entries - (str char, bool solid)
    return {
        ' ': (' ', False), # Air
        '-': (colorStr('-', GREEN), True), # Grass
        '|': (colorStr('|', MAGENTA), True), # Wood
        '@': (colorStr('@', GREEN), True), # Leaves
        '#': (colorStr('#', WHITE), True), # Stone
        'x': (colorStr('x', BLACK), True), # Coal
        '+': (colorStr('+', RED), True), # Iron
        ':': (colorStr(':', RED), True), # Redstone
        '"': (colorStr('"', YELLOW), True), # Gold
        'o': (colorStr('o', CYAN), True), # Diamond
        '*': (colorStr('*', WHITE), True), # Player head
        '^': (colorStr('^', WHITE), True) # Player legs
    }
