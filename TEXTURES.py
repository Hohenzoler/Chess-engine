import pyray as rl

def load_textures():

    textures = {}

    image = rl.load_image('assets/pieces/Black_king.png')
    textures["k"] = rl.load_texture_from_image(image)
    rl.unload_image(image)

    image = rl.load_image('assets/pieces/Black_bishop.png')
    textures["b"] = rl.load_texture_from_image(image)
    rl.unload_image(image)

    image = rl.load_image('assets/pieces/Black_knight.png')
    textures['n'] = rl.load_texture_from_image(image)
    rl.unload_image(image)

    image = rl.load_image('assets/pieces/Black_queen.png')
    textures['q'] = rl.load_texture_from_image(image)
    rl.unload_image(image)

    image = rl.load_image('assets/pieces/Black_pawn.png')
    textures['p'] = rl.load_texture_from_image(image)
    rl.unload_image(image)

    image = rl.load_image('assets/pieces/Black_rook.png')
    textures['r'] = rl.load_texture_from_image(image)
    rl.unload_image(image)

    image = rl.load_image('assets/pieces/White_king.png')
    textures['K'] = rl.load_texture_from_image(image)
    rl.unload_image(image)

    image = rl.load_image('assets/pieces/White_pawn.png')
    textures['P'] = rl.load_texture_from_image(image)
    rl.unload_image(image)

    image = rl.load_image('assets/pieces/White_rook.png')
    textures['R'] = rl.load_texture_from_image(image)
    rl.unload_image(image)

    image = rl.load_image('assets/pieces/White_queen.png')
    textures['Q'] = rl.load_texture_from_image(image)
    rl.unload_image(image)

    image = rl.load_image('assets/pieces/White_bishop.png')
    textures['B'] = rl.load_texture_from_image(image)
    rl.unload_image(image)

    image = rl.load_image('assets/pieces/White_knight.png')
    textures['N'] = rl.load_texture_from_image(image)
    rl.unload_image(image)

    return textures

