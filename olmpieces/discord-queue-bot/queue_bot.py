# Execution:
# DISCORD_TOKEN=<secret> python3 queue_bot.py

import os
import traceback

import discord

QUEUE_RULES_PREFIX = """
В этом чате установлены следующие правила:
""".strip()
QUEUE_RULES = """
  •   в очередь нужно записаться, указав задачи, которые вы хотите сдать;
:rage: нельзя писать несколько сообщений; можно редактировать или удалять старое;
:angry: записавшись, нужно подключиться к голосовому каналу очереди (с выключенным микрофоном);
:eyes: свободный преподаватель переключит вас в свой канал для разговора;
:woman_shrugging: поcле разговора сообщение отсюда нужно удалить.
""".strip()

QUEUE_ALGORITHM = """
Я буду отмечать сообщения учеников в текстовом чате очереди одной из реакций :rage:, :angry:, :eyes:, :woman_shrugging: (или ни одной из них). Наличие реакции означает, что сообщение нерелевантно по той или иной причине.

:rage: это не первое сообщение ученика в очереди;
:angry: ученик не подключен ни к какому голосовому каналу;
:eyes: ученик подключен (или его подключили) к некоторому голосовому каналу, кроме канала очереди;
:woman_shrugging: (после :eyes:) ученик подключен к голосовому каналу очереди либо не подключен ни к какому.

Можно видеть, что самостоятельно выйти из «прослушанного» состояния (:eyes:/:woman_shrugging:) ученик может, только удалив свое сообщение. Если преподаватель видит, что это состояние наступило некорректно (например, ученик случайно зашёл не в тот канал, или хотел сдавать определенному преподавателю), он можете _стереть все реакции_ у сообщения, вернув его к изначальному состоянию.

Сообщения от преподавателей игнорируются (кроме команд).

(Определения.
_Преподаватель_ — это участник сервера, у которого есть роль, название которой начинается с «препод» в любом регистре.
_Текстовый чат очереди_ — это любой текстовый чат, название которого начинается с «очередь» в любом регистре, либо находящийся в категории с подобным названием.
_Голосовой канал очереди_ — это любой голосовой канал, название которого начинается с «очередь» в любом регистре, либо находящийся в категории с подобным названием.)
""".strip()

QUEUE_PREFIX = "очередь"
TEXT_QUEUE_PREFIX = QUEUE_PREFIX
VOICE_QUEUE_PREFIX = QUEUE_PREFIX
TEACHER_ROLE_PREFIX = "препод"

FAIRY_NAME = "фея"
QUEUE_RULES_PREFIX_FAIRY = """
Я прилетела и установила в этом чате следующие правила:
""".strip()

EMOJI_ASTRAY = "\N{ANGRY FACE}"
EMOJI_TAKEN = "\N{EYES}"
EMOJI_DROPPED = "\N{SHRUG}\N{ZWJ}\N{FEMALE SIGN}\uFE0F"
EMOJI_DUPLICATE = "\N{POUTING FACE}"
EMOJI_SPECTRUM = frozenset({
    EMOJI_ASTRAY,
    EMOJI_TAKEN,
    EMOJI_DROPPED,
    EMOJI_DUPLICATE,
})
EMOJI_SPECTRUM_TAKEN = frozenset({
    EMOJI_TAKEN,
    EMOJI_DROPPED,
})

class QueueBot(discord.Client):

    def __init__(self, *args, **kwargs):
        kwargs["intents"] = discord.Intents(
            guilds=True, members=True,
            messages=True, voice_states=True )
        super().__init__(*args, **kwargs)

    def member_is_teacher(self, member):
        return any(
            role.name.lower().startswith(TEACHER_ROLE_PREFIX)
            for role in member.roles )

    def text_channel_is_queue(self, text_channel):
        if text_channel.name.lower().startswith(TEXT_QUEUE_PREFIX):
            return True
        category = text_channel.category
        if category is not None and \
                category.name.lower().startswith(QUEUE_PREFIX):
            return True
        return False

    def voice_channel_is_queue(self, voice_channel):
        if voice_channel.name.lower().startswith(VOICE_QUEUE_PREFIX):
            return True
        category = voice_channel.category
        if category is not None and \
                category.name.lower().startswith(QUEUE_PREFIX):
            return True
        return False

    def get_queue_channels(self, guild):
        for text_channel in guild.text_channels:
            if self.text_channel_is_queue(text_channel):
                yield text_channel

    async def on_ready(self):
        print(f"{self.user} has connected to Discord")
        for guild in self.guilds:
            try:
                await self.on_ready_guild(guild)
            except Exception:
                print(f"{guild.name} (id={guild.id}): error occured")
                traceback.print_exc()

    async def on_ready_guild(self, guild):
        print( f"{guild.name} (id={guild.id}): "
            f"{guild.me.name}" )
        queued_members = set()
        queued_count = 0
        me = self.user
        for queue_channel in self.get_queue_channels(guild):
            async for message in queue_channel.history(oldest_first=True):
                author = message.author
                if not isinstance(author, discord.Member):
                    print( f"Warning: ignoring {author.name}'s message")
                    continue
                if self.member_is_teacher(author) or author == me:
                    continue
                queued_members.add(message.author)
                queued_count += 1
        print( f"{guild.name} (id={guild.id}): "
            f"{queued_count} messages in queues found" )
        for member in queued_members:
            await self.update_queue_reactions(member)

    async def on_message(self, message):
        if message.author == self.user:
            return
        if self.user in message.mentions:
            if await self.on_command(message):
                return
        if self.member_is_teacher(message.author):
            return
        channel = message.channel
        if not isinstance(channel, discord.TextChannel):
            return
        if not self.text_channel_is_queue(channel):
            return
        await self.update_queue_reactions(
            message.author,
            queue_channels=[channel] )

    async def on_command(self, message):
        if not self.member_is_teacher(message.author):
            return False
        channel = message.channel
        if not isinstance(channel, discord.TextChannel):
            return False
        mention_prefix = f"<@!{self.user.id}> "
        if message.content.startswith(mention_prefix):
            command = message.content[len(mention_prefix):]
        else:
            await self.send_help( channel,
                reply_to=message.author, error="Команда не распознана." )
            return True
        if command.lower() == "команды":
            await self.send_help(channel)
        elif command.lower() == "правила":
            if not self.text_channel_is_queue(channel):
                await channel.send( f"<@!{message.author.id}> "
                    "Команду «правила» можно запустить "
                    "только в чате очереди." )
                return True
            await self.on_command_rules(channel)
        elif command.lower() == "алгоритм":
            await self.on_command_algorithm(channel)
        else:
            await self.send_help( channel,
                reply_to=message.author,
                error=f"Команда «{command}» не распознана" )
        return True

    async def on_command_rules(self, channel):
        nick = channel.guild.me.nick
        is_fairy = nick is not None and nick.lower() == FAIRY_NAME
        prefix = QUEUE_RULES_PREFIX_FAIRY if is_fairy else QUEUE_RULES_PREFIX
        await channel.send(prefix + "\n" + QUEUE_RULES)

    async def on_command_algorithm(self, channel):
        await channel.send(QUEUE_ALGORITHM)

    async def send_help(self, channel, *, reply_to=None, error=None):
        sentences = []
        if reply_to is not None:
            sentences.append(f"<@!{reply_to.id}>")
        if error is not None:
            sentences.append(error)
        sentences.append(
            f"Формат команд: `@{channel.guild.me.name} <команда>`." )
        sentences.append("Команды: «команды», «правила», «алгоритм».")
        await channel.send(" ".join(sentences))

    async def on_message_delete(self, message):
        if self.member_is_teacher(message.author) or \
                message.author == self.user:
            return
        channel = message.channel
        if not isinstance(channel, discord.TextChannel):
            return
        if not self.text_channel_is_queue(channel):
            return
        await self.update_queue_reactions(
            message.author,
            queue_channels=[channel] )

    async def on_voice_state_update(self, member, before, after):
        if self.member_is_teacher(member):
            return
        if before.channel == after.channel:
            return
        await self.update_queue_reactions(member, voice=after)

    async def update_queue_reactions( self, member, *,
        voice=None, queue_channels=None
    ):
        if voice is None:
            voice = member.voice
        if queue_channels is None:
            queue_channels = self.get_queue_channels(member.guild)
        if voice is None or voice.channel is None:
            status = "astray"
        elif self.voice_channel_is_queue(voice.channel):
            status = "queue"
        else:
            status = "taken"
        for queue_channel in queue_channels:
            first = True
            async for message in queue_channel.history(oldest_first=True):
                if message.author != member:
                    continue
                if not first:
                    await self.add_single_reaction(message, EMOJI_DUPLICATE)
                    continue
                first = False
                had_been_taken = any( reaction.emoji in EMOJI_SPECTRUM_TAKEN
                    for reaction in message.reactions )
                if had_been_taken and status in {"queue", "astray"}:
                    await self.add_single_reaction(message, EMOJI_DROPPED)
                elif status == "queue":
                    await self.add_single_reaction(message, None)
                elif status == "astray":
                    await self.add_single_reaction(message, EMOJI_ASTRAY)
                elif status == "taken":
                    await self.add_single_reaction(message, EMOJI_TAKEN)
                else:
                    raise RuntimeError("should not get here")

    async def add_single_reaction(self, message, emoji):
        if emoji is not None and emoji not in EMOJI_SPECTRUM:
            raise RuntimeError(
                f"Unrecognised emoji {emoji} "
                f"(code {''.join(hex(ord(e)) for e in emoji)})" )
        me = self.user
        already_added = False
        cleared_reactions = list()
        for reaction in message.reactions:
            if reaction.emoji not in EMOJI_SPECTRUM:
                continue
            if emoji is not None and reaction.emoji == emoji:
                async for user in reaction.users():
                    if user == me:
                        already_added = True
                        break
            else:
                cleared_reactions.append(reaction)
        if emoji is not None and not already_added:
            await message.add_reaction(emoji)
        for reaction in cleared_reactions:
            await reaction.clear()

if __name__ == '__main__':
    client = QueueBot()
    client.run(os.getenv('DISCORD_TOKEN'))

# vim: set wrap lbr :
