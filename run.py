from title import Title

if __name__ == '__main__':
    while True:
        title = Title()
        game = title.run()
        if game is None:
            break
        message = game.operate()
        if message == 'end':
            break
