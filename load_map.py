def load_map(path):
    """load a map template from txt file"""
    file = open(path + '.txt', 'r')
    data = file.read().split('\n')
    game_map = []
    file.close()
    for row in data:
        game_map.append(list(row))
    return game_map