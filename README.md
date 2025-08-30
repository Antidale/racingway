Racingway is a [racetime.gg](https://racetime.gg) category bot for [Free Enterprise](https://ff4fe.com/make). If you'd like to help contribute, or have suggestions, hop in the [Tellah's Library](https://discord.gg/x95jN69Ggf) discord server.

# Commands
## !flags $host $your_flagstring
The flags command can roll seeds from either the main site, or from galeswift's fork. You can either use the `Roll...` button in the bot's pinned message in a race room to select the site and enter your flagstring, or use the `!flags` command directly in the chat. Below is an example of rolling a Fabul Gauntlet Swiss seed off of the main site

```
!flags main Orandom:5/win:crystal Kmain/summon/moon/nofree Pkey Cstandard/nofree/j:abilities Tstandard Sstandard Bstandard/alt:gauntlet Etoggle Glife/sylph/backrow -kit:basic -noadamants -vanilla:growup
```

## !ff4flags
In order to make a transition as easy as possible coming from people using DarkPaladin's dr-race-bot (now known as prof-race-bot and maintained by Wyelm), Racingway has an `!ff4flags` command that will always use the main site to generate your flagstring. Below is an example of a Pro-B-Otics seed being rolled

```
!ff4flags O1:quest_forge/2:quest_tradepink/3:quest_unlocksewer/random:2,tough_quest/req:4/win:crystal Kmain/summon/moon/unsafe Pkey Cstandard/nofree/distinct:7/no:tellah,fusoya/restrict:rydia,edward,yang,palom,porom/j:abilities/nekkie/nodupes/bye/hero Tpro Sstandard/no:j Bstandard/unsafe/alt:gauntlet/whyburn Etoggle/no:jdrops Glife/backrow -kit:freedom -kit2:notdeme -kit3:cid -noadamants -nocursed -spoon -pushbtojump
```

## !ff4galeswift
In order to make a transition as easy as possible coming from people using DarkPaladin's dr-race-bot (now known as prof-race-bot and maintained by Wyelm), Racingway has an `!ff4galeswift` command that will always use the Galeswift's site to generate your flagstring. Below is an example of rolling a Doorway To Tomorrow seed being rolled

```
!ff4galeswift 
Omode:ki11/req:all/win:crystal Kmain/summon/moon/miab:above,below Pshop Cstandard/nofree/start:not_tellah/thrift:4/j:abilities/hero Tstandard Swildish/no:sirens Bstandard/alt:gauntlet/whichburn/whichbez Etoggle Glife/sylph/backrow -kit:basic -kit2:freedom -kit3:exit -noadamants -spoon -exp:nokeybonus,kicheckbonus5,maxlevelbonus -doorsrando:all
```

## !ff4alpha
Continuing to make things as straightforward as possible for users of prof-race-bot, Racingway has teh `!ff4alpha` command that will always use the public alpha site to generate seeds. This command will be removed during periods where the alpha site is no longer public or active.  Below is an example of rolling a very long alpha seed with the command:

```
!ff4alpha Omode_dkmatter:quests OA1:boss_fabulgauntlet/2:boss_wyvern/3:boss_kainazzo/4:boss_valvalis/5:boss_golbez/do_1:dkmatter3/do_2:dkmatter3/do_3:abel/do_4:dkmatter4/do_all:dkmatter5 OB1:quest_cavebahamut/2:quest_murasamealtar/3:quest_crystalaltar/4:quest_whitealtar/5:quest_ribbonaltar/do_1:dkmatter5/do_2:dkmatter7/do_3:adamantarmor/do_4:dkmatter7/do_all:dkmatter10 OC1:quest_forge/2:quest_tradepink/3:quest_tradepan/4:char_edward/do_1:dkmatter3/do_2:dkmatter3/do_3:dkmatter4/do_all:dkmatter5 OD1:collect_dkmatter15/2:collect_dkmatter30/3:collect_dkmatter45/4:collect_dkmatter60/do_1:crystalring/do_2:powerrobe/do_3:spoon/do_all:crystal Kmain/miab:above/char/forge/latedark Pkey Cstandard/nofree/distinct:9/start:kain/restrict:cecil,edge,fusoya/j:abilities/nekkie Twildish/playable/mintier:3/miabs:pro Sstandard/playable/sell:quarter Bchaos/alt:gauntlet/chaosburn Etoggle Xobjbonus:5 Glife/sylph/backrow Qfastrom/msgspeedfix -kit:eblan -kit2:defense -kit3:cid -noadamants -nocursed -spoon
```

## !preset $preset_name
Presets have been implemented, and you can either use the `Preset...` button on the pinned message in a racetime room to select a preset, or you can use the `!preset` command directly in chat. Current preset options are: D2T, Sumomo, SMS, AC_Group, ZZ6, Pro_B_Otics, ACE, FBF, and ZZA. The preset names should be case insensitive to use in the chat command.

To see details on the presets, look at the [presets.py](./racingway/presets.py) file.

## !lock
Usable by a [race monitor](https://github.com/racetimeGG/racetime-app/wiki/Roles-and-permissions#race-monitor). When used, prevents anyone who is not a race monitor from rolling a seed

## !unlock
Usable by a [race monitor](https://github.com/racetimeGG/racetime-app/wiki/Roles-and-permissions#race-monitor). When used, removes lock on a race, allowing anyone to roll a seed. Re-rolling a seed is still restricted to a [category moderator](https://github.com/racetimeGG/racetime-app/wiki/Roles-and-permissions#category-moderator), even when a race is unlocked.

## !reminders
A command to help remind runners of stream expectations while their race is being restreamed. Can also be invoked by `!r` and `!reminder`.

## !openvolunteers
A command to open a volunteering window for racers to be featured on a restream. This pins a message with a `Volunteer` button, and allows users to use the `!volunteer` command to send a message to the restreamer (e.g. the person who invoked this command). This command is limited to use by race_monitors. Can also be invoked by `!ov`.

## !closevolunteers
A command to close the volunteering window. Unpins the message and racingway will no longer send a DM to the person who used `!openvolunteers`. Leaves the race state in a manner where `!openvolunteers` cannot be used again to re-open volunteering. This command is limited to use by race_monitors, and may later be restricted to _just_ the person who used `!openvolunteers`. Can also be invoked by `!cv`

## !volunteer
A command to volunteer to be featured on a restream. Currently _does not_ require the user to have joined the race, but restriction may be added in the future. Users will probably just use the `Volunteer` button that is in the pinned message that results from `!openvolunteers`, but can use this directly.

## !hook
Get Racingway's feelings about various Hook things.

## !eatcookie
Mmm, cookie.

# Credits and thanks
Racingway built with the [racetime-bot](https://github.com/racetimeGG/racetime-bot) and is initially patterned after [ootr-randobot](https://github.com/OoTRandomizer/rtgg-randobot). Seed generation code initially patterned after Yanguin8r's code for the same.