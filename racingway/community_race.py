def get_cr_details():
    return CommunityRaceDetails(
        flags="OArandom:7,tough_quest OB1:quest_cavebahamut/2:quest_traderat/group_a:5/do_all:game OC1:boss_milonz/2:boss_kainazzo/3:boss_valvalis/4:boss_rubicant/5:boss_wyvern/do_1:siren/do_2:siren/do_3:siren/do_4:siren/do_all:siren OD1:collect_gp250/do_all:superweapon OE1:quest_forge/do_all:adamantarmor Kmain/summon/miab:above/char/force:magma/unweighted/start:earthcrystal Pkey Crelaxed/nofree/nogiant/distinct:4/start:any/partner:char/no:yang,fusoya/j:abilities/nekkie/nodupes/party:1/bye Twildish/mintier:3/maxtier:6 Spro/sell:quarter/no:sirens,life/maxitemtier:5 Bstandard/nofree/risky/alt:gauntlet/whichburn/whichbez/whybez Enoencounters/keep:behemoths/no:sirens Xobjbonus:10/kicheckbonus:2/zonkbonus:2/bonuses:mul Gwarp/backrow Qfastrom/msgspeedfix -kit:basic -kit2:random -kit3:random -noadamants -smith:none -wacky:omnidextrous",
        host="alpha",
        name="Crystal Warrior"
    )

class CommunityRaceDetails():
    def __init__(self, flags, host, name):
        self.flags = flags
        self.host = host
        self.name = name