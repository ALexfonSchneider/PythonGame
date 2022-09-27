import random
import arcade

class GameObject:
    def __init__(self, type=0, gamefield=None, position=None):
        self.type = type
        self.gamefield = gamefield
        self.position = position

    def draw(self):
        pass

class Teleport(GameObject):
    def __init__(self):
        super(Teleport, self).__init__(type='teleport')
        self.used = False

    def draw(self, x, y):
        arcade.draw_text('teleport', x, y, color=arcade.color.BLACK)

    @property
    def point_at(self):
        n, m = self.gamefield.size
        while True:
            i, j = random.randint(0, n - 1), random.randint(0, m - 1)
            if self.gamefield.field[i][j] == 0:
                return i, j

class Player(GameObject):
    def __init__(self, name, health=100, strenght=10):
        super(Player, self).__init__(type='player')
        self.name = name
        self.health = health
        self.strenght = strenght

        self.hit_zone = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if not(i == 0 and j == 0):
                    self.hit_zone.append((i, j))

    def __str__(self):
        return f'{self.name}: {self.health}'

    def draw(self, x, y):
        arcade.draw_text(self.__str__(), x, y, color=arcade.color.BLACK)

    def move(self, position):
        i, j = position

        target = self.gamefield.field[i][j]

        def move_to(obj: Player, position):
            i1, j1 = obj.position
            obj.gamefield.field[i1][j1] = 0

            i2, j2 = position
            obj.gamefield.field[i2][j2] = obj
            obj.position = position

        if target == 0:
            move_to(self, position)
        elif target.type == 'player':
            target.health -= self.strenght
        elif target.type == 'teleport':
            move_to(self, target.point_at)
            target.used = True

    def is_in_hit_zone(self, target_position):
        i1, j1 = self.position
        i2, j2 = target_position

        for h in self.hit_zone:
            n, m = h
            if i2 - i1 == n and j2 - j1 == m:
                return True
        return False

class GameField:
    def __init__(self, objects=None, size=(10, 10)):
        self.field = None
        self.size = size
        self.init_game_field()

        self.objects = objects
        self.fill_objects()

    def init_game_field(self):
        n, m = self.size

        self.field = [0] * n
        for n in range(n):
            self.field[n] = [0] * m

    def fill_objects(self, objects=None):
        n, m = self.size

        if objects == None: objects = self.objects

        for obj in objects:
            while True:
                i, j = random.randint(0, n - 1), random.randint(0, m - 1)
                if self.field[i][j] == 0:

                    if obj.position != None:
                        i1,j1 = obj.position
                        obj.gamefield.field[i1][j1] = 0

                    self.field[i][j] = obj
                    obj.position = i, j
                    obj.gamefield = self
                    break

class MyGame(arcade.Window):
    @property
    def cell_height(self):
        return self.height / self.size[0]

    @property
    def cell_width(self):
        return self.width / self.size[1]

    @property
    def size(self):
        return self.game_field.size

    @property
    def objects(self):
        return self.game_field.objects

    def get_cell_indexes(self, x, y):
        n, m = self.size

        for i in range(0, n):
            if x < self.cell_width * (i + 1):
                for j in range(0, m):
                    if y < self.cell_height * (j + 1):
                        return i, j

    def __init__(self, width=1280, height=720):
        super(MyGame, self).__init__(width, height)
        arcade.set_background_color(arcade.color.WHITE)

        self.game_field = None
        self.players = None
        self.player_turn = 0

    def setup(self, players, size=(5, 5)):
        self.players = players
        self.teleports = [Teleport(), Teleport(), Teleport()]

        self.gameobjects = []
        self.gameobjects.extend(self.players)
        self.gameobjects.extend(self.teleports)

        self.game_field = GameField(self.gameobjects, size)

    def on_draw(self):
        arcade.start_render()

        n, m = self.size

        for cell in self.players[self.player_turn].hit_zone:
            i, j = self.players[self.player_turn].position
            i1, j1 = i + cell[0], j + cell[1]
            arcade.draw_rectangle_filled(i1 * self.cell_width, j1 * self.cell_height, self.cell_width, self.cell_height, arcade.color.RED)

        for i in range(0, n):
            arcade.draw_line(i * self.cell_width, 0, i * self.cell_width, self.height, color=arcade.color.BLACK)

        for i in range(0, m):
            arcade.draw_line(0, i * self.cell_height, self.width, i * self.cell_height, color=arcade.color.BLACK)

        for obj in self.objects:
            i, j = obj.position
            obj.draw(i * self.cell_width, j * self.cell_height)




    def on_update(self, delta_time: float):
        for teleport in self.teleports:
            if teleport.used:
                teleport.used = False
                self.game_field.fill_objects(self.teleports)

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        position = self.get_cell_indexes(x, y)

        player = self.players[self.player_turn]

        if player.is_in_hit_zone(position):
            if self.player_turn == 0:
                self.players[0].move(position)
                self.player_turn += 1
            else:
                self.players[1].move(position)
                self.player_turn = 0

game = MyGame()
game.setup([Player('A'), Player('B')], (10, 10))
game.run()
