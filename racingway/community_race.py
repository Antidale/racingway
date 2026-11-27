def get_cr_details():
    return CommunityRaceDetails(
        flags="O1:quest_traderat/2:quest_falcon/3:quest_ribbonaltar/random:3,tough_quest,boss/req:5/win:crystal Kmain/summon/moon/nofree Pkey Crelaxed/nofree/distinct:7/start:not_cecil,not_tellah,not_fusoya/j:abilities/nekkie/nodupes/bye/permajoin/hero Twildish/mintier:3 Sstandard Bstandard/alt:gauntlet/whichburn Etoggle Gwarp/life/sylph/backrow -kit:freedom -spoon",
        flagsLink="https://ff4fe.com/make?flags=bBAYAEOUZAQAAADBmXsgcAEhAAAAAAHDMAgEBpAF4BQAC",
        host="main",
        name="Sumomo"
    )

class CommunityRaceDetails():
    def __init__(self, flags, flagsLink, host, name):
        self.flags = flags
        self.flagsLink = flagsLink
        self.host = host
        self.name = name