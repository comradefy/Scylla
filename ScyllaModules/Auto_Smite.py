#
#         ,gg,
#        i8""8i                        ,dPYb, ,dPYb,
#        `8,,8'                        IP'`Yb IP'`Yb
#         `88'                         I8  8I I8  8I
#         dP"8,                        I8  8' I8  8'
#        dP' `8a    ,gggg,  gg     gg  I8 dP  I8 dP    ,gggg,gg
#       dP'   `Yb  dP"  "Yb I8     8I  I8dP   I8dP    dP"  "Y8I
#    _,dP'     I8 i8'       I8,   ,8I  I8P    I8P    i8'    ,8I
#   "888,,____,dP,d8,_    _,d8b, ,d8I ,d8b,_ ,d8b,_ ,d8,   ,d8b,
#   a8P"Y88888P" P""Y8888PPP""Y88P"8888P'"Y888P'"Y88P"Y8888P"`Y8
#                                ,d8I'
#                              ,dP'8I
#                             ,8"  8I
#                             I8   8I
#                             `8, ,8I
#                              `Y8P"
#


from Scylla import *
from ScyllaCommons.utils import GetDistance

enable_key = 0
show_range = False
enabled_autosmite = False

Scylla_Information = {
    "Script": "Auto Smite",
    "Description": "Auto smite a monster when in range. (Only Large/Epic monsters)"
}

def Scylla_Load(cfg):
    global enable_key, show_range
    enable_key = cfg.get_int("enable_key", 0)
    show_range = cfg.get_bool("show_range", True)


def Scylla_Save(cfg):
    global enable_key, show_range
    cfg.set_int("enable_key", enable_key)
    cfg.set_bool("show_range", show_range)


def Scylla_Draw(game, ui):
    global enable_key, show_range
    enable_key = ui.keyselect("Enable auto smite key  ", enable_key); ui.sameline()
    show_range = ui.checkbox("Show Smite Range", show_range)
    ui.separator()

def Scylla_Update(game, ui):
    global enable_key, enabled_autosmite, show_range



    ColorWhite = Color.WHITE
    ColorWhite.a = 5.0
    ColorYellow = Color.YELLOW
    ColorYellow.a = 0.05
    ColorOrange = Color.ORANGE
    ColorOrange.a = 0.35

    smite = game.player.get_summoner_spell(SummonerSpellType.Smite)
    smite_range = game.player.gameplay_radius + 500

    # Zoe W Smite #
    if game.player.name == "zoe":
        if "smite" in game.player.W.name:
            smite = game.player.W

    if smite == None:
        return

    if game.was_key_pressed(enable_key):
        enabled_autosmite = ~enabled_autosmite

    if enabled_autosmite:
        if show_range:
            game.draw_circle_world_filled(game.player.pos, smite_range, 100, ColorYellow)
            game.draw_circle_world(game.player.pos, smite_range, 100, 3, ColorOrange)

        ReadySmite = 0.0
        SmiteCharge = smite.charges
        if SmiteCharge == 2 or SmiteCharge == 1:
            ReadySmite = smite.ready_at - game.time
        if SmiteCharge < 1:
            ReadySmite = smite.ready_at_smite - game.time

        p = game.world_to_screen(game.player.pos)
        p.y -= 65
        p.x += 25
        game.draw_button(p, "AutoSmite", ColorOrange, ColorWhite, 10)
        for monster in game.jungle:
            # Only in Smite Range #
            if GetDistance(monster.pos, game.player.pos) <= smite_range + 110:
                is_smitable = (ReadySmite <= 0 and not monster.health <= 0 and monster.health <= smite.value and monster.targetable and monster.is_visible
                           and (monster.has_tags(UnitTag.Unit_Monster_Large) or monster.has_tags(UnitTag.Unit_Monster_Epic)))
                cast_point = monster.pos
                if is_smitable:
                    cast_point = game.world_to_screen(cast_point)
                    old_cpos = game.get_cursor()
                    game.move_cursor(cast_point)
                    smite.trigger()
                    game.move_cursor(old_cpos)