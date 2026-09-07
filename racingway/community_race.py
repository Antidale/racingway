def get_cr_details():
    return CommunityRaceDetails(
        flags="OArandom:5,tough_quest OB1:quest_forge/group_a:4/do_all:crystal Kmain/summon/moon/char/nofree/latedark Pkey Cstandard/nofree/nogiant/distinct:9/start:any/partner:char/no:fusoya/j:abilities/nekkie Twildish/maxtier:7/miabs:pro Sstandard Bmaybe/alt:gauntlet/chaosburn/whichbez Etoggle Xnokeybonus/objbonus:20/kicheckbonus:3/maxmulti:400/bonuses:mul Gwarp/life/sylph/backrow Qfastrom/msgspeedfix -kit:basic -kit2:better -noadamants -spoon -smith:super,playable",
        host="alpha",
        name="Sample Standard"
    )

class CommunityRaceDetails():
    def __init__(self, flags, host, name):
        self.flags = flags
        self.host = host
        self.name = name