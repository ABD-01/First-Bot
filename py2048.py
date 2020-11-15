from random import randrange,choice
from discord import Embed
import asyncio

# Highest power of two less than or equal to a number
def Powerof2(n):
    power = 1
    for i in range(n, 0, -1):
        if not i & (i - 1):
            power = i
            break
    return power


# Inserting 2 in random in board
def insert_two(board):
    i = randrange(len(board))
    j = randrange(len(board))
    while board[i][j] != 0:
        i = randrange(len(board))
        j = randrange(len(board))
    board[i][j] = 2
    return board


# Function to Transpose a 2D List
def transpose(board):
    return [list(row) for row in zip(*board)]


# Function to Flip the 2D List
def invert(board):
    return [row[::-1] for row in board]


# Validating the Move
def isValid(move, gboard):
    # Orienting as the convinience
    if move in ['w', 's']:
        board = transpose(gboard)
    else:
        board = gboard

    # Checking for any consecutive equal values
    for row in board:
        if any(row[i] == row[i + 1] and row[i] != 0 for i in range(len(row) - 1)):
            #print("Found consecutive equal value")
            return True

    if move in ['a', 'w']:
        board = invert(board)

    for row in board:
        nrow = sorted(row, key=bool)
        # Else checking is the previous state and state after the move is same or different
        if row != nrow:
            #print("Check here", row)
            return True

    # If none of the above case happens then move in Invalid
    #print("Cannot move in given Direction", move)
    return False


# Pretty Printing the Game Board
def printboard(gboard):
    board = []
    for row in gboard:
        board.append([i if i != 0 else "  " for i in row])
    boardstr = '-' + '-------' * len(board) + '\n'
    for row in board:
        # s = ' | '.join(['`%4s`' %str(cell) for cell in row])
        s = ' | '.join(['%4s' % str(cell) for cell in row])
        boardstr = boardstr + f"| {s} |\n"
        boardstr = boardstr + '-' + '-------' * len(board) + '\n'
    print(boardstr)
    return '`' + boardstr + '`'


# Checking if users lost or not
def didLose(board):
    # Check for any zero present
    if any(0 in row for row in board):
        #print("There is still zero present,You didn't lose")
        return False

    # Checking for any eual consecutive Values in rows
    for row in board:
        if any(row[i] == row[i + 1] for i in range(len(row) - 1)):
            #print("consecutive equal values exists, Didn'i lose")
            return False


def start_game(win_cond=2048, board_size=5):
    win_cond = Powerof2(win_cond)
    # Initializing the board with all zeros and one 2 at random position
    game_board = [[0]*board_size for _ in range(board_size)]
    game_board = insert_two(game_board)
    game_board = insert_two(game_board)
    return win_cond, game_board


# Most Important part of the program
def game_move(ch, gboard):

    # Orienting the board so as all the actions are simply Left to Right
    if ch == 'd':
        board = gboard
    elif ch == 'a':
        board = invert(gboard)
    elif ch == 's':
        board = transpose(gboard)
    elif ch == 'w':
        board = transpose(gboard)
        board = invert(board)

    # Moving all Non-Zero elements to Rigth
    for row in board:
        row.sort(key=bool)

        #  merging two consecutive equal values
        i = len(row)-1
        while i >= 0:
            if row[i] == row[i-1]:
                row[i] = 2*row[i]
                row[i-1] = 0
                i -= 2
            else:
                i -= 1

    # Again moving all Non-zero elements to right
    for row in board:
        row.sort(key=bool)

    # Re-orienting the board back to the form it was
    if ch == 'w':
        board = invert(board)
        board = transpose(board)
    elif ch == 'a':
        board = invert(board)
    elif ch == 's':
        board = transpose(board)

    return board


def didWin(win_cond, game_board):
    return any(win_cond in row for row in game_board)

# Similar to main function
# while True:
#
#     ch = getKey()
#     system('clear')
#     game_board = game_move(ch, game_board)
#     game_board = insert_two(game_board)
#     printboard(game_board)
#
#     # Checking the game progress
#     if didLose(game_board) == True:
#         print('Game Over, You Lose')
#         exit(0)
#
#     # checking for winning Criteria
#     if any(win_cond in row for row in game_board) == True:
#         print('You Win')
#         exit(0)


async def play_2048_game(client,message,win_cond):
    channel = message.channel
    author = message.author

    emojis = ['⬅️', '⬆️', '⬇️', '➡️', '❌']

    win_cond, game_board = start_game(win_cond=win_cond, board_size=4)
    # desc = f"Use the letters `w`,`a`,`s`,`d` to Play.\n Use `q` or `Quit` to stop the game\nYour `win_conditon` is `{win_cond}`"
    desc = (f"Use {emojis[0]},{emojis[1]},{emojis[2]},{emojis[3]} to Play.\n" +
            f"Use {emojis[4]} to stop the game\nYour `win_conditon` is `{win_cond}`")

    color = ''.join([choice('0123456789ABCDEF') for x in range(6)])
    color = int(color, 16)
    embed = Embed(title='2048', description=desc, color=color)
    embed.set_footer(text=f'{author.name}', icon_url=author.avatar_url)
    # embed.add_field(name='Usage', value='`$2048 -w <win_cond>`', inline=False)

    strboard = printboard(game_board)
    embed.add_field(name='Board', value=strboard)
    bemsg = await channel.send(embed=embed)

    def check(reaction, user):
        # return m.author == message.author and m.channel == channel
        emojis = ['⬅️', '⬆️', '⬇️', '➡️', '❌']
        return user == author and str(reaction.emoji) in emojis

    async def addallemoj(bemsg,emojis):
        for emoji in emojis:
            await bemsg.add_reaction(emoji)

    def emojitochar(reaction):
        emoj = str(reaction.emoji)
        if emoj == emojis[0]:
            return 'a'
        elif emoj == emojis[1]:
            return 'w'
        elif emoj == emojis[2]:
            return 's'
        elif emoj == emojis[3]:
            return 'd'
        else:
            return 'q'

    await addallemoj(bemsg, emojis)

    while True:
        try:
            # msg = await self.wait_for('message',timeout=60, check=check)
            reaction, user = await client.wait_for('reaction_add', timeout=60, check=check)
            await bemsg.remove_reaction(reaction, user)
            print('Received reaction', reaction, 'from', user)
        except asyncio.TimeoutError:
            # await channel.send(f'<@{author.id}> did not respond in time, what a noob!')
            embed.add_field(name='Result', value=f'<@{author.id}>, did not respond in time, SED', inline=False)
            await bemsg.edit(embed=embed)
            await bemsg.clear_reactions()
            break
        else:
            ch = emojitochar(reaction)
            # ch = msg.content
            # checking if entered key is correct
            if ch.lower() in ['a', 's', 'd', 'w']:
                if isValid(ch, game_board) == False:
                    print("Invalid move = ", ch)
                    # await channel.send(f'<@{author.id}> That\'s an invalid move', delete_after=2)
                    embed.add_field(name='Invalid Move', value=f'{reaction.emoji} is Invalid Move', inline=False)
                    await bemsg.edit(embed=embed)
                    embed.remove_field(1)
                    continue
                else:
                    ##print("You pressed", ch)
                    game_board = game_move(ch, game_board)
                    game_board = insert_two(game_board)
                    strboard = printboard(game_board)
                    # embed.clear_fields()
                    # embed.add_field(name='Board', value=strboard)
                    embed.set_field_at(index=0, name='Board', value=strboard)
                    await bemsg.edit(embed=embed)
                    # await msg.delete(delay=0.5)

                    # Checking the game progress
                    if didLose(game_board) == True:
                        print('Game Over, You Lose')
                        # await channel.send(f'<@{author.id}> You Lose')
                        embed.add_field(name='Result', value=f'{author.name}, You Lost ☹️', inline=False)
                        await bemsg.edit(embed=embed)
                        await bemsg.clear_reactions()
                        break

                    # checking for winning Criteria
                    if didWin(win_cond,game_board) == True:
                        print('You Win')
                        # await channel.send(f'<@{author.id}> You Won')
                        embed.add_field(name='Result', value=f'{author.name}, You Won 🏆', inline=False)
                        await bemsg.edit(embed=embed)
                        await bemsg.clear_reactions()
                        break

            # If user wants to quit b/w gthe game
            elif ch.lower() in ['q', 'quit']:
                # await channel.send(f'<@{author.id}> , Oh no! You Gave Up, SED!')
                embed.add_field(name='Result', value=f'{author.name}, You Gave Up 😞', inline=False)
                await bemsg.edit(embed=embed)
                await bemsg.clear_reactions()
                break