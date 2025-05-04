from asyncio import sleep
from copy import deepcopy
import datetime
import re
import random
import string
import secrets
from .fe_seed_gen import FF4FESeedGen
from racetime_bot import RaceHandler, monitor_cmd, can_moderate, can_monitor, msg_actions

GREETING = "I'm a racebot! "

def natjoin(sequence, default):
    if len(sequence) == 0:
        return str(default)
    elif len(sequence) == 1:
        return str(sequence[0])
    elif len(sequence) == 2:
        return f'{sequence[0]} and {sequence[1]}'
    else:
        return ', '.join(sequence[:-1]) + f', and {sequence[-1]}'


def format_duration(duration):
    parts = []
    hours, duration = divmod(duration, datetime.timedelta(hours=1))
    if hours > 0:
        parts.append(f'{hours} hour{"" if hours == 1 else "s"}')
    minutes, duration = divmod(duration, datetime.timedelta(minutes=1))
    if minutes > 0:
        parts.append(f'{minutes} minute{"" if minutes == 1 else "s"}')
    if duration > datetime.timedelta():
        seconds = duration.total_seconds()
        parts.append(f'{seconds} second{"" if seconds == 1 else "s"}')
    return natjoin(parts, '0 seconds')

def parse_duration(args, default):
    if len(args) == 0:
        raise ValueError('Empty duration args')
    duration = datetime.timedelta()
    for arg in args:
        arg = arg.lower()
        while len(arg) > 0:
            match = re.match('([0-9]+)([smh:]?)', arg)
            if not match:
                raise ValueError('Unknown duration format')
            unit = {
                '': default,
                's': 'seconds',
                'm': 'minutes',
                'h': 'hours',
                ':': default
            }[match.group(2)]
            default = {
                'hours': 'minutes',
                'minutes': 'seconds',
                'seconds': 'seconds'
            }[unit]
            duration += datetime.timedelta(**{unit: float(match.group(1))})
            arg = arg[len(match.group(0)):]
    return duration

class RandoHandler(RaceHandler):
    """
    Racingway race handler. Generates seeds, presets, and frustration.
    """
    stop_at = ['cancelled', 'finished']
    max_status_checks = 50
    greetings = (
        'Tip: Baron Inn is the best place for up to date news and extras',
        'Can I interest you in a hook route?',
        'Why do the seeds keep increasing?',
        'Only the best players fade Antlion',
        'I\'m here to repair the refund machine',
        'Would you like a good plate of brisky?',
        'Eblan, come for the treasure, say for the monsters!',
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    async def should_stop(self):
        if self.data.get('opened_by') is None:
            # This is okay because Racingway does not open any rooms.
            return True
        return await super().should_stop()

    async def begin(self):
        """
        Send introduction messages.
        """
        if await self.should_stop():
            return
        if not self.state.get('intro_sent') and not self._race_in_progress():
            await self.send_message(
                GREETING + random.choice(self.greetings),
                actions=[
                    msg_actions.Action(
                        label='Roll Flags',
                        help_text='Rolls flags for galeswift\'s fork',
                        message='!flags ${flags}',
                        submit='Roll race seed',
                        survey=msg_actions.Survey(
                            msg_actions.TextInput(
                                name="flags",
                                placeholder="enter your flagstring here",
                                label="flags"
                            )
                        )
                    ),
                    msg_actions.ActionLink(
                        label='Help',
                        url='https://github.com/Antidale/racingway/blob/develop/README.md',
                    ),
                ],
                pinned=True,
            )
            self.state.setdefault('draft_data', {})
            self.state['intro_sent'] = True
        if 'locked' not in self.state:
            self.state['locked'] = False

    async def end(self):
        if self.state.get('pinned_msg'):
            await self.unpin_message(self.state['pinned_msg'])

    async def chat_message(self, data):
        message = data.get('message', {})
        if (
            message.get('is_bot')
            and message.get('bot') == 'Racingway'
            and message.get('is_pinned')
            and message.get('message_plain', '').startswith(GREETING)
        ):
            self.state['pinned_msg'] = message.get('id')

        # pulled from racetime_bot/handler.py to avoid the automatic .lower() call on message data that'd be passed into commands
        if message.get('is_bot') or message.get('is_system'):
            self.logger.info('Ignoring bot/system message.')
            return

        words = message.get('message', '').split(' ')
        if words and words[0].lower().startswith(self.command_prefix.lower()):
            method = 'ex_' + words[0][len(self.command_prefix):]
            args = words[1:]
            if hasattr(self, method):
                self.logger.info('[%(race)s] Calling handler for %(word)s' % {
                    'race': self.data.get('name'),
                    'word': words[0],
                })
                try:
                    await getattr(self, method)(args, message)
                except Exception as e:
                    self.logger.error('Command raised exception.', exc_info=True)

    async def race_data(self, data):
        await super().race_data(data)

        if self._race_in_progress() and self.state.get('pinned_msg'):
            await self.unpin_message(self.state['pinned_msg'])
            del self.state['pinned_msg']

    @monitor_cmd
    async def ex_lock(self, args, message):
        """
        Handle !lock commands.

        Prevent seed rolling unless user is a race monitor.
        """
        if self._race_in_progress():
            return
        self.state['locked'] = True
        await self.send_message(
            'Lock initiated. I will now only roll seeds for race monitors.'
        )

    @monitor_cmd
    async def ex_unlock(self, args, message):
        """
        Handle !unlock commands.

        Remove lock preventing seed rolling unless user is a race monitor.
        """
        if self._race_in_progress():
            return
        self.state['locked'] = False
        await self.send_message(
            'Lock released. Anyone may now roll a seed.'
        )

    # async def ex_preset(self, args, message):
    #     """
    #     Handle !preset commands.
    #     """
    #     if self._race_in_progress() or not can_monitor(message):
    #         return
        
    #     if self.state.get('seed_id') and not can_moderate(message):
    #         await self.send_message("A seed is being or has been rolled. Only a mod can re-generate a seed")
    #         return

    #     await self.send_message("hold on, let me get that for you")
    #     seedValue = self.generate_seed_value()
    #     self.state['seed_id'] = seedValue
    #     seedData = await FF4FESeedGen.gen_fe_seed("Omode:ki12/random:2,quest/random2:1,tough_quest/req:all/win:crystal Kmain/summon/moon/nofree:dwarf/unweighted Pkey Cstandard/nofree/restrict:cecil,fusoya/j:abilities/paladin/nekkie/party:4/treasure:free Twildish Sprice:200/pricey:items/standard Bstandard/alt:gauntlet/whichbez Etoggle Glife/sylph/backrow -kit:better -smith:alt -fusoya:sequential_r -exp:objectivebonus25 -tweak:edwardheal", seedValue)
    #     await self.set_bot_raceinfo(seedData["url"] + " Hash: " + seedData["verification"])
    #     await self.send_message("Here's your seed: " + seedData["url"])
    #     await self.send_message("Verification code: " + seedData["verification"])

    async def ex_flags(self, args, message):
        """
        Handle !flags commands.
        """

        if self._race_in_progress() or not can_monitor(message):
            return
        
        if self.state.get('seed_id') and not can_moderate(message):
            await self.send_message("A seed is being or has been rolled. Only a mod can re-generate a seed")
            return

        await self.send_preroll_snark()
        seedValue = self.generate_seed_value()
        self.state['seed_id'] = seedValue
        flags = ' '.join(args)
        seedData = await FF4FESeedGen.gen_fe_seed(flags, seedValue)
        await self.set_bot_raceinfo(seedData["url"] + "\nHash: " + seedData["verification"])
        await self.send_seed_snark()
        if self.state.get('pinned_msg'):
            await self.unpin_message(self.state['pinned_msg'])

    def _race_pending(self):
        return self.data.get('status').get('value') == 'pending'

    def _race_in_progress(self):
        return self.data.get('status').get('value') in ('pending', 'in_progress')
    
    def generate_seed_value(self):
        alphabet = string.ascii_uppercase + string.digits
        seed = ''.join(secrets.choice(alphabet) for i in range(10))
        return seed
    
    async def send_seed_snark(self):
        snark = (
            'I recalled a seed I had forgotten.  Hopefully there wasn\'t a reason to forget it.',
            'Please remember to keep your arms, legs, and spoon inside the seed at all times.',
            'Well that seed\'s gone',
            'Was it Random? I will show you how!',
            'Seed has 34.3 percent chance of betrayal by dragoon.'
        )

        await self.send_message(random.choice(snark))

    async def send_preroll_snark(self):
        snark = (
            'Workin\' on it boss.',
            'As you wish!',
            'Would you like cheese with that?',
            'Guac is extra.',
            'It\'s a tiny town after all.'
        )

        await self.send_message(random.choice(snark))
