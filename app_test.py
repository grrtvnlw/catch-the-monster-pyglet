import pyglet
from game import player, monster, goblin, resources
from random import randint

from config import WIDTH, HEIGHT

pyglet.font.load("Garamond")

# Set up a window
game_window = pyglet.window.Window(WIDTH, HEIGHT)

# Create the container for our graphics
main_batch = pyglet.graphics.Batch()

# Load the main music
theme_song = pyglet.media.load('./resources/music.wav')
music = pyglet.media.Player()
music.queue(theme_song)

# Set the music for when player wins
victory_song = pyglet.media.load('./resources/win.wav')
victory_music = pyglet.media.Player()
victory_music.queue(victory_song)

# Set the music for when player loses
losing_song = pyglet.media.load('./resources/lose.wav')
losing_music = pyglet.media.Player()
losing_music.queue(losing_song)

# Set up the two top labels, score label and lives label
score_label = pyglet.text.Label(text="Caught 0", font_name="Garamond", font_size=26, x=15, y=455, batch=main_batch)
lives_label = pyglet.text.Label(text="Lives 3", font_name="Garamond", font_size=26, x=400, y=455, batch=main_batch)

# Initialize the player sprite
hero = player.Player(x=400, y=300, batch=main_batch)
monster_inst = monster.Monster(x=randint(0, WIDTH), y=randint(0,HEIGHT), batch=main_batch)
goblin_inst = goblin.Goblin(x=randint(0, WIDTH), y=randint(0,HEIGHT), batch=main_batch)

# Store all objects that update each frame in a list
game_objects = [goblin_inst, hero, monster_inst]

# Tell the main window that the player object responds to events
game_window.push_handlers(hero.key_handler)

@game_window.event
def on_draw():
    game_window.clear()
    resources.background.blit(0, 0)
    main_batch.draw()

is_drawing = True  # Controls whether to show movement

# score = 0
# lives = 3

def game_won():
    global is_drawing

    is_drawing = False
    music.pause()
    # Play victory music!
    victory_music.play()
    # Set up victory label
    victory_label = pyglet.text.Label(text="YOU WON!!!", font_name="Garamond", font_size=40, x=110, y=230, batch=main_batch)

def game_lost():
    global is_drawing

    is_drawing = False
    music.pause()
    # Play losing music!
    losing_music.play()
    # Set up losing label
    losing_label = pyglet.text.Label(text="YOU Lost :(", font_name="Garamond", font_size=40, x=110, y=230, batch=main_batch)


def update(dt):

    # global score
    # global lives

    if is_drawing:

        for obj in game_objects:
            obj.update(dt)

        # To avoid handling collisions twice, we employ nested loops of ranges.
        # This method also avoids the problem of colliding an object with itself.
        for i in range(len(game_objects) - 1):
            for j in range(i + 1, len(game_objects) - 1):

                obj_1 = game_objects[0]
                obj_2 = game_objects[1]
                # add a 3rd object
                obj_3 = game_objects[2]

                # Make sure the objects haven't already been killed
                if not obj_2.dead and not obj_3.dead:
                    if obj_1.collides_with(obj_2):
                        print(f"{obj_1.name} collides with {obj_2.name}")
                        obj_1.handle_collision_with(obj_2)
                        obj_2.handle_collision_with(obj_1)
                    if obj_2.collides_with(obj_3):
                        print(f"{obj_2.name} collides with {obj_3.name}")
                        obj_2.handle_collision_with(obj_3)
                        obj_3.handle_collision_with(obj_2)
                    if obj_1.collides_with(obj_3):
                        print(f"{obj_1.name} collides with {obj_3.name}")
                        obj_1.handle_collision_with(obj_3)
                        obj_3.handle_collision_with(obj_1)

        # Get rid of dead objects
        for to_remove in [obj for obj in game_objects if obj.dead]:
            # Remove the object from any batches it is a member of
            to_remove.delete()

            # Remove the object from our list
            game_objects.remove(to_remove)

            # Set score and lives variables
            # score += 10

            if to_remove.name == "Joe":
                new_player = player.Player(x=randint(0, WIDTH), y=randint(0, HEIGHT), batch=main_batch)
                game_objects.insert(1, new_player)
                game_window.push_handlers(new_player.key_handler)
                hero.lives -= 1
            elif to_remove.name == "Monster":
                # Add a new monster
                new_monster = monster.Monster(x=randint(0, WIDTH), y=randint(0, HEIGHT), batch=main_batch)
                #new_goblin = goblin.Goblin(x=randint(0, WIDTH), y=randint(0, HEIGHT), batch=main_batch)
                game_objects.insert(2, new_monster)
                hero.score += 10
                #game_objects.append(new_goblin)

            score_label.text = f"Caught {hero.score}"
            lives_label.text = f"Lives {hero.lives}"

            gotcha_sound_effect = pyglet.media.load('./resources/bullet.wav', streaming=False)
            gotcha_sound_effect.play()

            if hero.score == 100:
                game_won()

            if hero.lives <= 0:
                game_lost()
            


if __name__ == "__main__":
    # Update the game 120 times per second
    pyglet.clock.schedule_interval(update, 1 / 120.0)

    music.play()
    # Tell pyglet to do its thing
    pyglet.app.run()
