def get_cr_details():
    return CommunityRaceDetails(
        flags="OA1:quest_forge/2:quest_tradepink OB1:quest_monsterqueen/2:quest_monsterking/3:quest_baronbasement OC1:collect_ki15/2:collect_boss20/do_all:adamantarmor OD1:quest_sealedcave/2:quest_crystalaltar/3:quest_masamunealtar/group_a:1/group_b:1/do_all:game OE1:boss_rubicant/2:quest_falcon/group_a:1/group_b:1/do_all:crystal Kmain/summon/miab:above/nofree Pkey Cstandard/nofree/distinct:8/start:not_cecil,not_kain,not_cid,not_fusoya/partner:edge/no:fusoya/j:abilities/nekkie/nodupes/party:4 Twildish Sstandard/no:sirens Bmaybe/no:waterhag,fabulgauntlet/whichburn/whichbez Etoggle Xnokeybonus/objbonus:8/kicheckbonus:8/maxmulti:300 Gwarp/life/sylph/backrow Qmsgspeedfix -kit:better -kit2:exit -kit3:random -noadamants -nocursed -spoon -smith:alt",
        host="alpha",
        name="The Prince's Gambit"
    )

class CommunityRaceDetails():
    def __init__(self, flags, host, name):
        self.flags = flags
        self.host = host
        self.name = name