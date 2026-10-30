def get_cr_details():
    return CommunityRaceDetails(
        flags="O1:quest_monsterking/2:quest_ordeals/random:5,tough_quest/random2:2,quest,boss/req:7/hardreq:1,2/win:crystal Kmain/moon/nofree:dwarf/unreliabledark/start:legend Pkey Crelaxed/noearned/distinct:7/start:any/no:fusoya/abilities:j/nekkie/nodupes Twildish/playable/maxtier:7/mintier:3 Sstandard/playable/always:sirens,hrglass,bacchus,starveil,cure3,illusion,coffin Bstandard/alt:gauntlet/whichburn/newscriptstats Etoggle Hrandom Gwarp/life/backrow Fweighted Aagnostic Xzonkbonus:10 Zvanilla -kit:better -kit2:freedom -kit3:hero -noadamants -spoon -smith:super,good,spoilsuper -vanilla:miabs -tweak:yanghp",
        host="galeswift",
        name="Paladin Cup"
    )

class CommunityRaceDetails():
    def __init__(self, flags, host, name):
        self.flags = flags
        self.host = host
        self.name = name