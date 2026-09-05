def get_cr_details():
    return CommunityRaceDetails(
        flags="OA1:boss_mirrorcecil/2:boss_magus/3:boss_milonz/4:boss_plague/5:boss_dlunar/do_1:perseusarrow/do_2:item_t6_7/do_3:artemisbow/do_4:item_t7_8/do_5:crystalsword OB1:char_cecil/2:char_cid/3:char_kain/do_1:ribbon/do_2:crystalring/do_3:powerrobe OC1:quest_monsterqueen/2:quest_baronbasement/3:quest_zot/4:quest_curefever/5:quest_forge/do_1:heroine/do_2:crystalring/do_3:lifestaff/do_4:moonveil/do_5:cursedring OD1:quest_sealedcave/2:quest_giant/3:collect_ki13/do_1:auapple/do_2:cursedring/do_3:adamantarmor OEgroup_a:3/group_b:3/group_c:4/group_d:1/do_1:auapple/do_2:auapple/do_3:avenger/do_all:crystal Kmain/summon/miab:above/char/forge/latedark/force:magma/start:earthcrystal Pkey Cstandard/nofree/nogiant/risky/start:rosa/only:cecil,kain,rosa,cid/j:spells,abilities/nekkie/nodupes/party:4/bye/hero Twild/playable/maxtier:4/miabs:pro Scabins/free Bchaos/nofree/risky/alt:gauntlet/chaosburn Etoggle/noexp Xnokeybonus/objbonus:5/kicheckbonus:2/zonkbonus:2 Glife/backrow Qfastrom/msgspeedfix -kit:better -kit2:dwarf -kit3:notdeme -noadamants -nocursed -vanilla:miabs -pushbtojump",
        host="alpha",
        name="Push B for Baron"
    )

class CommunityRaceDetails():
    def __init__(self, flags, host, name):
        self.flags = flags
        self.host = host
        self.name = name