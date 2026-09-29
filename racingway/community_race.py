def get_cr_details():
    return CommunityRaceDetails(
        flags="O1:quest_murasamealtar/2:quest_forge/3:quest_tradepink/random:2,tough_quest/req:all/win:game Kmain/force:magma Pnone Crelaxed/noearned/distinct:7/start:not_fusoya/no:fusoya/abilities:j/nekkie Twildish/maxtier:7 Scabins/free Bstandard/alt:gauntlet/whichburn Etoggle/noexp Hrandom Glife/sylph/backrow Fweighted Aagnostic Zvanilla -kit:better -kit2:freedom -noadamants -spoon -smith:super,playable -vanilla:miabs",
        host="galeswift",
        name="Kokkol Express"
    )

class CommunityRaceDetails():
    def __init__(self, flags, host, name):
        self.flags = flags
        self.host = host
        self.name = name