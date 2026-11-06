def get_cr_details():
    return CommunityRaceDetails(
        flags="OArandom:7,tough_quest/do_7:crystal Kmain/summon/moon Pkey Cstandard/nofree/restrict:cecil,fusoya/j:abilities/nekkie/party:4 Twildish/maxtier:7 Sstandard Bstandard/alt:gauntlet Etoggle Glife/sylph/backrow -kit:better -spoon",
        host="alpha",
        name="Adamant Cup (group)"
    )

class CommunityRaceDetails():
    def __init__(self, flags, host, name):
        self.flags = flags
        self.host = host
        self.name = name