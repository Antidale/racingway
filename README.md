Racingway is a [racetime.gg](https://racetime.gg) category bot for [Free Enterprise](https://ff4fe.com/make). If you'd like to help contribute, or have suggestions, hop in the [Tellah's Library](https://discord.gg/x95jN69Ggf) discord server.

# Commands
## !flags $host $your_flagstring
The flags command can roll seeds from either the main site, or from galeswift's fork. You can either use the `Roll...` button in the bot's pinned message in a race room to select the site and enter your flagstring, or use the `!flags` command directly in the chat. Below is an example of rolling a Fabul Gauntlet Swiss seed off of the main site

```
!flags main Orandom:5/win:crystal Kmain/summon/moon/nofree Pkey Cstandard/nofree/j:abilities Tstandard Sstandard Bstandard/alt:gauntlet Etoggle Glife/sylph/backrow -kit:basic -noadamants -vanilla:growup
```

## !ff4flags
In order to make a transition as easy as possible coming from people using DarkPaladin's dr-race-bot, Racingway has an `!ff4flags` command that will always use the main site to generate your flagstring. Below is an example of a Pro-B-Otics seed being rolled

```
!ff4flags O1:quest_forge/2:quest_tradepink/3:quest_unlocksewer/random:2,tough_quest/req:4/win:crystal Kmain/summon/moon/unsafe Pkey Cstandard/nofree/distinct:7/no:tellah,fusoya/restrict:rydia,edward,yang,palom,porom/j:abilities/nekkie/nodupes/bye/hero Tpro Sstandard/no:j Bstandard/unsafe/alt:gauntlet/whyburn Etoggle/no:jdrops Glife/backrow -kit:freedom -kit2:notdeme -kit3:cid -noadamants -nocursed -spoon -pushbtojump
```

## !ff4galeswift
In order to make a transition as easy as possible coming from people using DarkPaladin's dr-race-bot, Racingway has an `!ff4galeswift` command that will always use the main site to generate your flagstring. Below is an example of rolling a Doorway To Tomorrow seed being rolled

```
!ff4galeswift 
Omode:ki11/req:all/win:crystal Kmain/summon/moon/miab:above,below Pshop Cstandard/nofree/start:not_tellah/thrift:4/j:abilities/hero Tstandard Swildish/no:sirens Bstandard/alt:gauntlet/whichburn/whichbez Etoggle Glife/sylph/backrow -kit:basic -kit2:freedom -kit3:exit -noadamants -spoon -exp:nokeybonus,kicheckbonus5,maxlevelbonus -doorsrando:all
```

## !preset $preset_name
Presets have been implemented, and you can either use the `Preset...` button on the pinned message in a racetime room to select a preset, or you can use the `!preset` command directly in chat. Current preset options are: D2T, Sumomo, SMS, AC_Group, ZZ6, and Pro_B_Otics. The preset names should be case insensitive to use in the chat command.

## !lock
Usable by a [race monitor](https://github.com/racetimeGG/racetime-app/wiki/Roles-and-permissions#race-monitor). When used, prevents anyone who is not a race monitor from rolling a seed

## !unlock
Usable by a [race monitor](https://github.com/racetimeGG/racetime-app/wiki/Roles-and-permissions#race-monitor). When used, removes lock on a race, allowing anyone to roll a seed. Re-rolling a seed is still restricted to a [category moderator](https://github.com/racetimeGG/racetime-app/wiki/Roles-and-permissions#category-moderator), even when a race is unlocked.

# Credits and thanks
Racingway built with the [racetime-bot](https://github.com/racetimeGG/racetime-bot) and is initially patterned after [ootr-randobot](https://github.com/OoTRandomizer/rtgg-randobot). Seed generation code initially patterned after Yanguin8r's code for the same.