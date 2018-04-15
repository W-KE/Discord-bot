import discord
from discord.ext import commands
import random

from board import Board
from player import Player

description = '''An example bot to showcase the discord.ext.commands extension
module.

There are a number of utility commands being showcased here.'''
bot = commands.Bot(command_prefix='$', description=description)
owner = None
preparing = False
playing = False
players = []
board = None


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


@bot.command(pass_context=True)
async def start(ctx):
    if not preparing and not playing:
        global owner, preparing, players
        owner = ctx.message.author
        preparing = True
        players = [owner]
        await bot.say(
            "{} 想要开始游戏，输入 $join 加入，玩家加入后 {} 输入 $go 开始".format(ctx.message.author.mention, ctx.message.author.mention))
    else:
        await bot.say("游戏已经开始，等待下一局")


@bot.command(pass_context=True)
async def join(ctx):
    if playing:
        await bot.say("游戏已经开始，等待下一局")
        return
    if ctx.message.author in players:
        await bot.say("你已经在游戏中了，不要重复加入")
    else:
        if preparing:
            global players
            players.append(ctx.message.author)
            await bot.say("{} 加入了游戏".format(ctx.message.author.mention))
            return
        if not preparing:
            await bot.say("没有进行中的游戏,输入 $start 开始新游戏")


@bot.command(pass_context=True)
async def go(ctx):
    if playing:
        await bot.say("游戏已经开始，等待下一局")
        return
    if ctx.message.author != owner:
        await bot.say("只有主持人可以开始游戏")
        return
    if len(players) < 2:
        await bot.say("人数不足")
    else:
        global board, preparing, playing
        preparing = False
        playing = True
        board = Board([Player(str(i), i) for i in players])
        board.deal_all()
        await bot.say("本局游戏共有{}人参加\n庄家为{}\n单注最低{}点\n轮到庄家行动".format(len(players), board.dealer.user.mention, board.min))
        await bot.say("1. 放弃")
        await bot.say("2. 看牌")
        await bot.say("3. 加注")
        await bot.say("4. 跟注")
        await bot.say("输入 $move 1-4 选择")


@bot.command(pass_context=True)
async def move(ctx, option, addition=0):
    if preparing:
        await bot.say("游戏还没有开始")
        return
    if ctx.message.author not in players:
        await bot.say("你不在游戏中")
        return
    if ctx.message.author != board.players[board.current].user:
        await bot.say("还没有轮到你")
    else:
        if option == "2":
            await bot.send_message(ctx.message.author, " ".join(board.players[board.current].see()))
            await bot.say("1. 放弃")
            await bot.say("3. 加注")
            await bot.say("4. 跟注")
            await bot.say("输入 $move 1-4 选择")
        else:
            if option == "1":
                board.players[board.current].pack()
            elif option == "3":
                if addition < board.current_chips:
                    addition = board.current_chips
                board.players[board.current].chips -= addition
                board.chips += addition
                board.current_chips = addition
            elif option == "4":
                board.players[board.current].chips -= board.current_chips
                board.chips += board.current_chips
            board.current += 1
            board.current %= len(board.players)
            while board.players[board.current].state == 2:
                board.current += 1
                board.current %= len(board.players)
            count = 0
            for player in board.players:
                if player.state != 2:
                    count += 1
            if board.chips >= board.max or count < 2:
                for i in board.players:
                    await bot.say("".format(i.user.mention, i.get_score(), i.hand))
                winner = board.check()
                global playing
                playing = False
                await bot.say("{} 获胜".format(winner.user.mention))
            else:
                await bot.say("轮到 {} 输入 $move 行动".format(board.players[board.current].user.mention))
                await bot.say("1. 放弃")
                await bot.say("2. 看牌")
                await bot.say("3. 加注")
                await bot.say("4. 跟注")
                await bot.say("输入 $move 1-4 选择")


@bot.group(pass_context=True)
async def cool(ctx):
    """Says if a user is cool.

    In reality this just checks if a subcommand is being invoked.
    """
    if ctx.invoked_subcommand is None:
        await bot.say('No, {0.subcommand_passed} is not cool'.format(ctx))


@cool.command(name='Poker')
async def _bot():
    """Is the bot cool?"""
    await bot.say('Yes, the Poker is cool.')


bot.run('NDM0MjA2ODc0MDI4NjA1NDQw.DbMOVw.4Hu__7h6bYHQtJYbkggAwBFtG7E')
