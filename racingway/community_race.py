def get_cr_details():
    return CommunityRaceDetails(
        flags="OA1:quest_forge/random:7,tough_quest/do_6:crystal Kmain/summon/moon/nofree Pkey Cstandard/nofree/start:cecil,kain,rydia,edward,rosa,yang,palom,porom,cid,edge/no:tellah,fusoya/j:abilities/nekkie/nodupes/hero Tpro/no:j/mintier:3/maxtier:7 Spro Bstandard/alt:gauntlet/whichburn Etoggle/no:jdrops Glife/backrow -kit:freedom -noadamants -nocursed -spoon",
        host="alpha",
        name="ZZ6"
    )

class CommunityRaceDetails():
    def __init__(self, flags, host, name):
        self.flags = flags
        self.host = host
        self.name = name