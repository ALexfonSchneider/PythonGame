import random
import tkinter
import arcade


class Player:
    def __init__(self, name, health=100, strenght=10):
        self.name = name
        self.health = health
        self.strenght = strenght
        self.type = 'player'

    def info(self):
        return f'{self.name}: {self.health}'

    def draw(self, x, y):
        arcade.draw_text(self.info(), x, y, color=arcade.color.BLACK)

    def hit(self, target):
        target.health -= self.strenght

class GameField:
    def __init__(self, size=(10, 10), objects=None):
        self.field = None
        self.size = size
        self.objects = {obj.name: obj for obj in objects} if objects != None else {}
        self.init_game_field()
        self.fill_objects()

    @property
    def objects_and_position(self):
        lst = []
        for i in range(0, self.size[0]):
            for j in range(0, self.size[1]):
                name = self.field[i][j]
                if name != 0:
                    lst.append(
                        ((i, j), self.objects[name])
                    )
        return lst

    def init_game_field(self):
        self.field = [0] * self.size[0]
        for n in range(self.size[0]):
            self.field[n] = [0] * self.size[1]

    def fill_objects(self):
        n, m = self.size
        for name in self.objects:
            while True:
                i, j = random.randint(0, n - 1), random.randint(0, m - 1)
                if self.field[i][j] == 0:
                    self.field[i][j] = name
                    break

    def find_object(self, name) -> tuple:
        n, m = self.size
        for i in range(0, n):
            for j in range(0, m):
                if self.field[i][j] == name:
                    return i, j
        return None

    def move(self, name, position):
        n1, m1 = self.find_object(name)
        n2, m2 = position

        target = self.field[n2][m2]

        if target == 0:
            self.field[n2][m2] = name
            self.field[n1][m1] = 0
            print(1)
            return

        source = self.objects[name]
        target = self.objects[target]

        if target.type == 'player' and source.type == 'player':
            source.hit(target)

    def __str__(self):
        info = ''
        for name in self.objects:
            info += f'{self.objects[name].info()}\n'
        return info

class MyGame(arcade.Window):
    def __init__(self, width=1280, height=720):
        super(MyGame, self).__init__(width, height)
        self.background_color = arcade.color.WHITE
        self.player_turn = None
        self.players = None
        self.game_field = None

    @property
    def cell_height(self):
        return self.height / self.size[0]

    @property
    def cell_width(self):
        return self.width / self.size[1]

    @property
    def size(self):
        return self.game_field.size

    def get_player_position(self, name):
        return self.game_field.find_object(name)

    def get_cell_number(self, x, y):
        n, m = self.size

        for i in range(0, n):
            if x < self.cell_width * (i + 1):
                for j in range(0, m):
                    if y < self.cell_height * (j + 1):
                        return i, j

    def setup(self, size, players):
        self.game_field = GameField(size, players)
        self.players = players

        self.player_turn = 0

    def on_draw(self):
        arcade.start_render()

        n, m = self.size

        for i in range(0, n):
            arcade.draw_line(i * self.cell_width, 0, i * self.cell_width, self.height, color=arcade.color.BLACK)

        for i in range(0, m):
            arcade.draw_line(0, i * self.cell_height, self.width, i * self.cell_height, color=arcade.color.BLACK)

        for (i, j), obj in self.game_field.objects_and_position:
            obj.draw(self.cell_width * i, self.cell_height * j + self.cell_height / 2)

        n, m = self.get_player_position(self.players[self.player_turn].name)

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        position = self.get_cell_number(x, y)
        if self.player_turn == 0:
            self.game_field.move(self.players[0].name, position)
            self.player_turn = 1
        else:
            self.game_field.move(self.players[1].name, position)
            self.player_turn = 0

    def on_update(self, delta_time: float):
        for player in self.players:
            if player.health <= 0:
                window = tkinter.Tk()
                lbl = tkinter.Label(window, text=f'{player.name} проиграл!')
                lbl.grid(column=0, row=0)
                window.mainloop()

                self.close()


game = MyGame()
game.setup((10, 10), [Player('alex'), Player('vladimir')])
game.run()
