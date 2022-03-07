import AquariumEngine

if __name__ == '__main__':
    # Initialise the aquarium game engine
    # Modify the parameters to adjust the game setup
    app = AquariumEngine.Aquarium(
        width=800,
        height=520
    )
    app.game_loop()