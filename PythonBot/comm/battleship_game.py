import discord
from discord.ext import commands
from secrets import prefix

CARRIER = 0
BATTLESHIP = 1
CRUISER = 2
SUBMARINE = 3
DESTROYER = 4

ships = {
    'carrier': CARRIER,
    'battleship': BATTLESHIP,
    'cruiser': CRUISER,
    'submarine': SUBMARINE,
    'destroyer': DESTROYER
}

ship_length = {
    CARRIER: 5,
    BATTLESHIP: 4,
    CRUISER: 3,
    SUBMARINE: 3,
    DESTROYER: 2
}

HIT = 5
MISS = 6
UNGUESSED = 7

HEIGHT = 9
WIDTH = 9


class BattleshipGame:
    def __init__(self, bot, p1: str, p2: str):
        self.bot = bot
        self.boards = {}
        self.ships = {}

        self.p1 = p1
        self.ships[p1] = []
        self.boards[p1] = self.new_board()

        self.p2 = p2
        self.ships[p2] = []
        self.boards[p2] = self.new_board()

    @staticmethod
    def new_board():
        return [[UNGUESSED for _ in range(WIDTH)] for _ in range(HEIGHT)]

    async def send_message(self, id: str, message: str):
        await self.bot.send_message(await self.bot.get_user_info(id), message)

    def to_str(self, player: str):
        return '\n'.join([' '.join([str(x) for x in self.boards.get(player)[y]]) for y in range(HEIGHT)])

    async def start(self):
        message = 'Place all your ships using `{}battleship place <coordinate> <N,E,S,W>`'.format(prefix)
        await self.send_message(self.p1, message)
        await self.send_message(self.p2, message)

    def guess(self, x: str, y: int):
        pass

    @staticmethod
    def coordinate_str_to_int(c: str):
        return int(c[1]) - 1, ord(c[0].lower()) - 97

    @staticmethod
    def get_tail(x, y, l, d):
        if d == 'n':
            return x, y - l, x, y
        if d == 'e':
            return x, y, x + l, y
        if d == 's':
            return x, y, x, y + l
        return x - l, y, x, y

    @staticmethod
    def check_space(board: [[int]], xh, yh, ship, d):
        xh, yh, xt, yt = BattleshipGame.get_tail(xh, yh, ship_length.get(ship), d)
        if not ((0 <= xh < WIDTH) and (0 <= xt < WIDTH) and (0 <= yh < HEIGHT) and (0 <= yt < HEIGHT)):
            return False
        ship_coord = set([(x, y) for x in range(xh, xt + 1) for y in range(yh, yt + 1)])
        ships_coords = set([(x, y) for x in range(WIDTH) for y in range(HEIGHT) if board[y][x] != UNGUESSED])
        if any(ship_coord.intersection(ships_coords)):
            return False

        for x, y in ship_coord:
            board[y][x] = ship
        return True

    async def set_ship(self, player: str, *args):
        if len(args) < 3:
            await self.send_message(player, 'Use `{}battleship place <shipname> <coordinate> <N,E,S,W>`'.format(prefix))
            return
        ship, coord, direc = args[:3]
        ship = ships.get(ship.lower(), ship)
        coord = coord.lower()
        direc = direc.lower()
        if ship not in ships.values():
            m = 'That is not a valid ship, choose from `{}`'.format('`, `'.join(ships.keys()))
            await self.send_message(player, m)
            return

        try:
            x, y = self.coordinate_str_to_int(coord)
        except (ValueError, TypeError):
            await self.send_message(player, 'That is not a valid coordinate...')
            return

        if ship in self.ships.get(player):
            await self.send_message(player, 'That ship is already on the board')
            return

        if not self.check_space(self.boards.get(player), x, y, ship, direc):
            await self.send_message(player, 'Make sure you aren\'t hitting other ships or the edge of the board')
            return
        self.ships.get(player).append(ship)

        await self.send_message(player, self.to_str(player))
