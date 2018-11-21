import discord
from discord.ext import commands
from secrets import prefix
import string

CARRIER = 0
BATTLESHIP = 1
CRUISER = 2
SUBMARINE = 3
DESTROYER = 4

ships = {'carrier': CARRIER, 'battleship': BATTLESHIP, 'cruiser': CRUISER, 'submarine': SUBMARINE,
         'destroyer': DESTROYER}

nums = {1: 'one', 2: 'two', 3: 'three', 4: 'four', 5: 'five', 6: 'six', 7: 'seven', 8: 'eight', 9: 'nine'}
inv_ships = {v: k for k, v in ships.items()}

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

        self.other = {p1: p2, p2: p1}

        self.running = False
        self.turn = p1

    @staticmethod
    def new_board():
        return [[UNGUESSED for _ in range(WIDTH)] for _ in range(HEIGHT)]

    async def send_message(self, id: str, message: str):
        await self.bot.send_message(await self.bot.get_user_info(id), message)

    @staticmethod
    def encode(c, secret=False):
        if c == HIT:
            return '🚢'
        if c == MISS:
            return '🌊'
        if secret:
            return '❓'
        if c in ships.values():
            return '🚢'
        return '❌'

    def to_str(self, board: [[int]], secret=False):
        m = '⚓ ' + ' '.join([':regional_indicator_{}:'.format(c) for c in string.ascii_lowercase][:WIDTH]) + '\n'
        return m + '\n'.join([':' + nums.get(y+1, 'zero') + ':' + ' ' + ' '.join(
            [self.encode(x, secret) for x in board[y]]) for y in range(HEIGHT)])

    async def start(self):
        message = 'Place all your ships using `{}battleship place <coordinate> <N,E,S,W>`'.format(prefix)
        await self.send_message(self.p1, message)
        await self.send_message(self.p2, message)

    @staticmethod
    def resolve_guess(board: [[int]], x, y):
        if board[y][x] == UNGUESSED:
            board[y][x] = MISS
            return 'You missed...'
        elif board[y][x] in [HIT, MISS]:
            return 'You have already guessed there... Try another spot'
        else:
            s = board[y][x]
            board[y][x] = HIT
            if s not in [board[y][x] for x in range(WIDTH) for y in range(HEIGHT)]:
                s = inv_ships.get(s)
                return 'You just sunk your opponents {}!'.format(s[0].upper() + s[1:])
            else:
                return 'Hit!'

    async def guess(self, player: str, coord: str):
        if not self.running:
            m = 'The game has not started yet, wait for both players to place all their ships'
            await self.send_message(player, m)
            return
        if not player == self.turn:
            await self.send_message(player, 'Wait for your turn to start...')
            return
        try:
            x, y = self.coordinate_str_to_int(coord)
        except (ValueError, TypeError):
            m = 'Those aren\'t valid coordinates, an example of a valid coordinate is `b4`'
            await self.send_message(player, m)
            return

        b = self.boards.get(self.other.get(player))
        await self.send_message(player, self.resolve_guess(b, x, y) + '\n' + self.to_str(b, True))
        if not any([b[y][x] for x in range(WIDTH) for y in range(HEIGHT) if b[y][x] not in [HIT, MISS, UNGUESSED]]):
            await self.send_message(player, 'You sunk all your opponents battleships, congratulations with this win!')
            await self.send_message(self.other.get(player),
                                    'Your opponent sunk all your battleships, you lost this game...')
            self.quit()
            return
        await self.send_message(self.other.get(player), 'Your turn!')

    @staticmethod
    def coordinate_str_to_int(c: str):
        return ord(c[0].lower()) - 97, int(c[1]) - 1

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
        except (ValueError, TypeError, IndexError):
            await self.send_message(player, 'That is not a valid coordinate...')
            return

        if ship in self.ships.get(player):
            await self.send_message(player, 'That ship is already on the board')
            return

        if not self.check_space(self.boards.get(player), x, y, ship, direc):
            await self.send_message(player, 'Make sure you aren\'t hitting other ships or the edge of the board')
            return
        self.ships.get(player).append(ship)

        await self.send_message(player, self.to_str(self.boards.get(player), False))

        if len(self.ships.get(player)) >= len(ships.values()):
            await self.send_message(player, 'All your ships have been placed')

            if len(self.ships.get(self.other.get(player))) >= len(ships.values()):
                self.running = True
                m = 'All ships have been placed, start the guessing with `{}battleship guess <coordinate>`'
                await self.send_message(self.turn, m)

    def quit(self):
        del self.bot.battleships.games[self.p1]
        del self.bot.battleships.games[self.p2]
