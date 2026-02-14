from asyncio import sleep
from copy import deepcopy
import datetime
import re
import random
import string
import secrets
from .fe_seed_gen import FF4FESeedGen, InvalidFlagString, SeedGenerationError
from . import presets
from racetime_bot import RaceHandler, monitor_cmd, can_moderate, can_monitor, msg_actions
from .log_seed import FeInfoSeedLogger
from .log_race import RaceLogger
from .choices import *
from .monitors import *

ALPHABET = string.ascii_uppercase + string.digits

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

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    async def should_stop(self):
        return await super().should_stop()

    async def begin(self):
        """
        Send introduction messages.
        """
        if await self.should_stop():
            return
        if not self.state.get('intro_sent') and not self._race_in_progress():
            await self.send_message(
                random.choice(get_greetings()),
                actions=[
                    msg_actions.Action(
                        label='CC Sets',
                        help_text='Roll CC Flags',
                        message='!preset ${preset}',
                        submit='Roll Preset',
                        survey=msg_actions.Survey(
                            msg_actions.SelectInput(
                                name="preset",
                                label="choice",
                                default="50cc",
                                options=presets.get_cc_presets(),
                            )
                        )
                    ),
                    msg_actions.Action(
                        label='Preset',
                        help_text='Roll Preset Flags',
                        message='!preset ${preset}',
                        submit='Roll Preset',
                        survey=msg_actions.Survey(
                            msg_actions.SelectInput(
                                name="preset",
                                label="choice",
                                default="50cc",
                                options=presets.get_presets(),
                            )
                        )
                    ),
                    msg_actions.Action(
                        label='Flags',
                        help_text='Roll Flags',
                        message='!flags ${site} ${flags}',
                        submit='Roll Flags',
                        survey=msg_actions.Survey(
                            msg_actions.SelectInput(
                                name="site",
                                label="site",
                                default="main",
                                options={
                                    'main':'main',
                                    'galeswift':'galeswift',
                                    'alpha':'alpha'
                                    # , 'local':'local'
                                }
                            ),
                            msg_actions.TextInput(
                                name="flags",
                                placeholder="enter your flagstring here",
                                label="flags"
                            ),   
                        )
                    ),
                    msg_actions.ActionLink(
                        label='Help',
                        url='https://github.com/Antidale/racingway/blob/main/README.md',
                    ),
                ],
                pinned=True,
            )

            self.state['intro_sent'] = True
        if 'locked' not in self.state:
            self.state['locked'] = False

        # Restrict room creation to a single good call
        if (self.state.get('race_id') is None):
            opened_by = self.data['opened_by']
            info = self.data.get('info_user')
            goal = self.data.get('goal')
            slug = self.data.get('slug')
            try:
                response = await RaceLogger.log_race_created(slug, opened_by, info, goal.get('name'))
                self.logger.info('race logged')
                self.state['race_id'] = response
                self.state['slug'] = slug
            except Exception as e:
                self.logger.error('Race logging created exception.', exc_info=True)
                self.state['race_id'] = None

    async def end(self):
        if self.state.get('pinned_msg'):
            await self.unpin_message(self.state['pinned_msg'])
        if self.state.get('volunteer_msg'):
            await self.unpin_message(self.state['volunteer_msg'])

    async def chat_message(self, data):
        message = data.get('message', {})
        if (
            message.get('is_bot')
            and message.get('bot').lower() == 'racingway'
            and message.get('is_pinned')
        ):
            if(self.state.get('pinned_msg') is None):
                self.state['pinned_msg'] = message.get('id')
            else:
                self.state['volunteer_msg'] = message.get('id')

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

        if self.data.get('slug') is None:
            race = data.get('race')
            name = race.get('name')
            self.state['race_name'] = name
        
    ############################
    # COMMANDS
    ############################
    # Temporary comment out of lock/unlock commands. Have to check with people on if they want restrictions on rolling
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

    async def ex_preset(self, args, message):
        """
        Handle !preset commands.
        """
        if (self.state.get('locked')) and not can_monitor(message):
            return

        if self.state.get('seed_id') and not can_moderate(message):
            await self.send_message("A seed is being or has been rolled. Only a mod can re-generate a seed")
            return
        preset_choice = ' '.join(args)
        preset_data = presets.get_preset_details(preset_choice)

        await self.roll_seed(preset_data.flags, preset_data.host)

    async def ex_flags(self, args, message):
        """
        Handle !flags commands.
        """
        if (self.state.get('locked')) and not can_monitor(message):
            return

        if self.state.get('seed_id') and not can_moderate(message):
            await self.send_message("A seed is being or has been rolled. Only a mod can re-generate a seed")
            return

        host = args.pop(0)
        flags = ' '.join(args)
        await self.roll_seed(flags, host)

    async def ex_ff4flags(self, args, message):
        """
        Handle !ff4flags commands. Used as an easy replacement for people familiar with dr-race-bot
        """
        if (self.state.get('locked')) and not can_monitor(message):
            return

        if self.state.get('seed_id') and not can_moderate(message):
            await self.send_message("A seed is being or has been rolled. Only a mod can re-generate a seed")
            return

        args.insert(0, 'main')
        await self.ex_flags(args, message)

    async def ex_ff4galeswift(self, args, message):
        """
        Handle !ff4galeswift commands. Used as an easy replacement for people familiar with dr-race-bot
        """
        if (self.state.get('locked')) and not can_monitor(message):
            return

        if self.state.get('seed_id') and not can_moderate(message):
            await self.send_message("A seed is being or has been rolled. Only a mod can re-generate a seed")
            return

        args.insert(0, 'galeswift')
        await self.ex_flags(args, message)

    async def ex_ff4alpha(self, args, message):
        """
        Handle !ff4galeswift commands. Used as an easy replacement for people familiar with dr-race-bot
        """
        if (self.state.get('locked')) and not can_monitor(message):
            return

        if self.state.get('seed_id') and not can_moderate(message):
            await self.send_message("A seed is being or has been rolled. Only a mod can re-generate a seed")
            return

        args.insert(0, 'alpha')
        await self.ex_flags(args, message)

    async def ex_eatcookie(self, args, message):
        await self.send_message(random.choice(get_cookies()))

    async def ex_hook(self, args, message):
        await self.send_message(random.choice(get_hook()))

    async def ex_reminders(self, args, message):
        await self.send_message("For the restream, please turn off stream alerts, disable Ads Manager, and make sure to not enable flash effects in the game.")
        await self.send_message("Stream delay is not required for races, and should not be used on restream. You should be streaming at or below a resolution of 720p and a bitrate of 2000 kbps.")

    async def ex_monitor(self, args, message):
        user_name =  message.get('user', {}).get('full_name', 'no')
        user_id = message.get('user', {}).get('id')

        if(can_monitor(message)):
            await self.send_message("You're already a monitor", direct_to=user_id)
            return
        
        if(not self.can_volunteer(user_id)):
            await self.send_message("You must join the race first", direct_to=user_id)
            return

        if(check_promotability(userName=user_name)):
            await self.add_monitor(user_id)
        else:
            await self.send_message("You are not on the approved monitors list", direct_to=user_id)

    @monitor_cmd
    async def ex_ov(self, args, message):
        """
        Shorthand version of !openvolunteers
        """
        await self.ex_openvolunteers(args, message)

    @monitor_cmd
    async def ex_openvolunteers(self, args, message):
        """
        Handles !openvolunteers and !ov commands. Sets the user who used it as the restreamer, and sends a pinned message in chat saying that volunteering is open, and has a button to help racers volunteer easily.
        """
        if self.state.get('restreamer'):
            user = message.get('user').get('id')
            await self.send_message("someone already opened volunteering", direct_to=user)
            return

        await self.send_message("@here Want to be featured on restream? !volunteer or click the button.",
                                actions=[
                                    msg_actions.Action(
                                        label="Volunteer",
                                        help_text="Volunteer to be featured on restream",
                                        message="!volunteer"
                                    )
                                ],
                                pinned=True)
        await self.send_message("Want to be featured on restream? !volunteer or click the Volunteer button in the pinned message.")
        self.state['restreamer'] = message.get('user').get('id')

    @monitor_cmd
    async def ex_cv(self, args, message):
        """
        Shorthand version of !closevolunteers
        """
        await self.ex_closevolunteers(args, message)

    @monitor_cmd
    async def ex_closevolunteers(self, args, message):
        """
        Handles !closevolunteers and !cv. Unpins the volunteering message and sets the state of the race to prevent re-opening volunteering, or forwarding of !volunteer messages to the restreamer.
        """
        if(self.state.get('volunteer_msg') == 'closed'):
            return

        try:
            await self.unpin_message(self.state['volunteer_msg'])
            self.state['volunteer_msg'] = 'closed'
            await self.send_message("Restream volunteering has been closed")
        except:
            return

    async def ex_volunteer(self, args, message):
        """
        Hanlde !volunteer messages. If volunteering is not open, let the user know the current state of volunteering. otherwise send the 'restreamer' the info, and thank the user for volunteering.
        """
        if(self.state.get('volunteer_msg') == 'closed'):
            await self.send_message("The volunteering window has closed, sorry!", direct_to=message.get('user').get('id'))
            return

        volunteer = message.get('user', {}).get('name')
        volunteer_id = message.get('user', {}).get('id')
        # I don't think this should be possible, but handle the case
        if volunteer is None:
            return

        if not self.can_volunteer(volunteer_id):
            await self.send_message("You must join the race before you can volunteer.", direct_to=volunteer_id)
            return

        restreamer = self.state.get('restreamer')
        if restreamer is None:
            await self.send_message("Restream volunteering is not yet opened, please wait for the restreamer to open it", direct_to=volunteer_id)
            return

        message_text = volunteer + " volunteered for restream"
        await self.send_message(message_text, direct_to=restreamer)
        await self.send_message("Thanks for volunteering!", direct_to=volunteer_id)

    async def ex_r(self, args, message):
        await self.ex_reminders(args, message)

    async def ex_reminder(self, args, message):
        await self.ex_reminders(args, message)

    def can_volunteer(self, volunteer_id):
        try:
            entrants = self.data.get("entrants")
            if entrants is None:
                return False

            for racer in entrants:
                racer_id = racer.get("user", {}).get("id", "")
                racer_status = racer.get("status", {}).get("value", "")
                if racer is None:
                    return False
                if racer_id == volunteer_id and racer_status in ["not_ready", "ready"]:
                    return True
            return False
        except:
            self.logger.error('Processing volunteering raised exeption.', exc_info=True)
            return False

    ############################
    # Helper Methods
    ############################
    def _race_pending(self):
        return self.data.get('status').get('value') == 'pending'

    def _race_in_progress(self):
        return self.data.get('status').get('value') in ('pending', 'in_progress')

    def generate_seed_value(self):
        """
        Generates a 10 character alphanumeric string for the seed, sets it as state['seed_id'] and returns the value.
        """

        seed = ''.join(secrets.choice(ALPHABET) for i in range(10))
        self.state['seed_id'] = seed
        return seed
    
    async def send_seed_snark(self):
        """
        Sends a bit of text to the room to help further be all "bot is done!"
        """
        await self.send_message(random.choice(get_post_roll_snark()))

    async def send_preroll_snark(self):
        """
        Sends a bit of text to the room to indicate that a command is underway
        """
        await self.send_message(random.choice(get_pre_roll_snark()))

    async def check_remove_bot_pin(self):
        """
        If the bot has a pinned message that it is keeping track of, unpin it and remove the property from the state object
        """
        if self.state.get('pinned_msg'):
            await self.unpin_message(self.state['pinned_msg'])
            del self.state['pinned_msg']

    async def roll_seed(self, flags, host):
        """
        Handles actually rolling the seed, and catching exceptions during that process
        """
        if self._race_in_progress():
            return

        await self.send_preroll_snark()
        seedValue = self.generate_seed_value()

        try:
            seedData = await FF4FESeedGen.gen_fe_seed(flags, host, seedValue)
            await self.set_bot_raceinfo(seedData["url"] + "\n" + seedData["verification"])
            await self.send_seed_snark()
            await self.check_remove_bot_pin()
            race_name = self.state.get('slug')
            print(self.state)
            try:
                await FeInfoSeedLogger.log_rolled_seed(seedData, self.state.get('race_id'), race_name)
            except Exception:
                self.logger.error('Failed to log seed', exc_info=True)

        except NotImplementedError:
            await self.send_message("That feature isn't implemented yet")
            self.logger.error('Command raised exception.', exc_info=True)
            self.state['seed_id'] = None
        except InvalidFlagString:
            await self.send_message("Flag string was invalid")
            self.logger.error('Command raised exception.', exc_info=True)
            self.state['seed_id'] = None
        except SeedGenerationError:
            await self.send_message("Error generating seed")
            self.logger.error('Command raised exception.', exc_info=True)
            self.state['seed_id'] = None
        except TimeoutError:
            await self.send_message("Timed out on seed generation.")
            self.logger.error('Command raised exception.', exc_info=True)
            self.state['seed_id'] = None
        except Exception:
            await self.send_message("I got Meganuked!")
            self.logger.error('Command raised exception.', exc_info=True)
            self.state['seed_id'] = None
