
def get_presets():
    return {
        'D2T': 'Doorway To Tomorrow',
        'Sumomo': 'Sumomo',
        'SMS': 'Supermarket Sweep',
        'AC_Group': 'Adamant Cup: Groups',
        'ZZ6': 'ZZ6',
        'Pro_B_Otics': 'Pro B Otics',
    }

def get_preset_details(preset):
    match preset.lower().replace('-','').replace('_','').replace(' ',''):
        case 'd2t': 
            return PresetDetails(
                flags='Omode:ki11/req:all/win:crystal Kmain/summon/moon/miab:above,below Pshop Cstandard/nofree/start:not_tellah/thrift:4/j:abilities/hero Tstandard Swildish/no:sirens Bstandard/alt:gauntlet/whichburn/whichbez Etoggle Glife/sylph/backrow -kit:basic -kit2:freedom -kit3:exit -noadamants -spoon -exp:nokeybonus,kicheckbonus5,maxlevelbonus -doorsrando:all',
                host='galeswift'
            )
        case 'sumomo':
            return PresetDetails(
                flags='O1:quest_traderat/2:quest_falcon/3:quest_ribbonaltar/random:3,tough_quest,boss/req:5/win:crystal Kmain/summon/moon/nofree Pkey Crelaxed/nofree/distinct:7/start:not_cecil,not_tellah,not_fusoya/j:abilities/nekkie/nodupes/bye/permajoin/hero Twildish/mintier:3 Sstandard Bstandard/alt:gauntlet/whichburn Etoggle Gwarp/life/sylph/backrow -kit:freedom -spoon',
                host='main'
            )
        case 'sms':
            return PresetDetails(
                flags='Orandom:4,tough_quest,boss/req:3/win:crystal Kmain Pshop Crelaxed/j:abilities Twild Swild/free/no:apples Bstandard/whyburn Etoggle Glife/sylph -spoon',
                host='main'
            )
        case 'acgroup' |'acgroups' :
            return PresetDetails(
                flags='Orandom:7,tough_quest/req:7/win:crystal Kmain/summon/moon Pkey Cstandard/nofree/restrict:cecil,fusoya/j:abilities/nekkie/party:4 Twildish/maxtier:7 Sstandard Bstandard/alt:gauntlet Etoggle Glife/sylph/backrow -kit:better -spoon',
                host='main'
            )
        case 'zz6':
            return PresetDetails(
                flags='O1:quest_magnes/2:quest_forge/3:boss_fabulgauntlet/4:boss_golbez/random:3,tough_quest/req:6/win:crystal Kmain/summon/moon/nofree Pkey Cstandard/nofree/restrict:cecil,fusoya/j:abilities/nekkie/hero Twildish/maxtier:5 Sstandard Bstandard/alt:gauntlet/whichburn Etoggle/cantrun Gwarp/life/sylph/backrow -kit:better -kit2:dwarf -spoon',
                host='main'
            )
        case 'probotics':
            return PresetDetails(
                flags='O1:quest_forge/2:quest_tradepink/3:quest_unlocksewer/random:2,tough_quest/req:4/win:crystal Kmain/summon/moon/unsafe Pkey Cstandard/nofree/distinct:7/no:tellah,fusoya/restrict:rydia,edward,yang,palom,porom/j:abilities/nekkie/nodupes/bye/hero Tpro Sstandard/no:j Bstandard/unsafe/alt:gauntlet/whyburn Etoggle/no:jdrops Glife/backrow -kit:freedom -kit2:notdeme -kit3:cid -noadamants -nocursed -spoon -pushbtojump',
                host='main'
            )
        case _:
            raise NotImplementedError("Preset option not implemented")
        
class PresetDetails():
    def __init__(self, flags, host):
        self.flags = flags
        self.host = host
    