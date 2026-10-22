def get_cr_details():
    return CommunityRaceDetails(
        flags="O2:quest_forge/3:quest_music/4:quest_lowerbabil/5:quest_cavebahamut/6:quest_toroiatreasury/7:boss_fabulgauntlet/8:quest_magma/req:6/win:crystal Kmain/moon/miab:standard/force:hook Pkey Cstandard/nofree/distinct:7/start:rosa,porom/no:tellah/restrict:cecil,yang,fusoya/abilities:j/nekkie/nodupes Tpro/no:j/maxtier:5 Spro Bstandard/alt:gauntlet/whichburn Etoggle Hrandom Glife/backrow Fweighted Aagnostic Zvanilla -kit:basic -kit3:random -noadamants -nocursed -smith:super -vanilla:miabs -wacky:omnidextrous",
        host="galeswift",
        name="OMG"
    )

class CommunityRaceDetails():
    def __init__(self, flags, host, name):
        self.flags = flags
        self.host = host
        self.name = name