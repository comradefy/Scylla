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
import time

from ScyllaCommons.utils import buffIsAlive, ColorUtil

show_allies = False
show_enemies = False
summonerspells = ["summonerhaste", "summonerheal",
                  "summonerexhaust", "summonerbarrier",
                  "summonermana", "summonermark", "summonerflash",
                  "summonerteleport", "summonerboost", "summonerdot",
                  "summonersmite", "s5_summonersmiteplayerganker", "s5_summonersmiteduel"]

Scylla_Information = {
    "Script": "Spells Tracker",
    "Description": "",
}

def get_color_for_cooldown(cooldown, name):
    if cooldown > 0.0:
        return Color.DARK_RED
    elif name == "qiyanaq_water":
        return Color(0.129, 0.709, 0.909, 1)
    elif name == "qiyanaq_grass":
        return Color(0.141, 0.8, 0.149, 1)
    elif name == "qiyanaq_rock":
        return Color(0.760, 0.219, 0.0, 1)
    else:
        return Color(1, 1, 1, 1)


def draw_spell(ui, game, spell, pos, size, show_lvl = True, show_cd = True):
    #ui.text(spell.name)
    ColorYellow = Color.YELLOW
    ColorYellow.a = 5.0
    ColorWhite = Color.WHITE
    ColorWhite.a = 5.0


    cooldown = spell.get_current_cooldown(game.time)
    color = get_color_for_cooldown(cooldown, spell.name) if spell.level > 0 else Color.GRAY
    game.draw_image(spell.icon, pos, pos.add(Vec2(size, size)), color, 10.0)

    if show_cd and cooldown > 0.0:
        if spell.name not in summonerspells:
            game.draw_text(pos.add(Vec2(6, 5)), str(int(cooldown)), ColorWhite)
        else:
            game.draw_text(pos.add(Vec2(15, 5)), str(int(cooldown)), ColorWhite)
    if show_lvl:
        for i in range(spell.level):
            offset = i*4
            game.draw_rect_filled(Vec4(pos.x + offset, pos.y + 24, pos.x + offset + 3, pos.y + 26), ColorYellow)


def draw_overlay_on_champ(ui, game, champ):
    ColorRed = Color.RED
    ColorRed.a = 5.0
    ColorWhite = Color.WHITE
    ColorWhite.a = 5.0

    #clone avoiding
    if champ.D.name == champ.R.name:
        p = game.hp_bar_pos(champ)
        p.x -= 50
        p.y -= 70
        game.draw_text(p, "*** CLONE ***", ColorRed)
        p.x += 1
        p.y += 1
        game.draw_text(p, "*** CLONE ***", ColorWhite)
        return

    p = game.hp_bar_pos(champ)
    p.x -= 70
    if not game.is_point_on_screen(p):
        return

    if champ.W.name == 'yuumiwendwrapper':
        p.x -= 150
        p.y += 75

    p.y += 5
    p.x += 25
    draw_spell(ui, game, champ.Q, p, 24)
    p.x += 25
    draw_spell(ui, game, champ.W, p, 24)
    p.x += 25
    draw_spell(ui, game, champ.E, p, 24)
    p.x += 25
    draw_spell(ui, game, champ.R, p, 24)
    p.x -= 125
    p.y -= 45
    draw_xp(ui, game, champ.experience, champ.lvl, p, 45)

    if champ.name == 'aphelios':
        p.x += 215
        p.y -= -8
        draw_spell(ui, game, champ.D, p, 15, False, True)
        p.y += 17
        draw_spell(ui, game, champ.F, p, 15, False, True)
        return

    p.x += 160
    p.y -= -8
    draw_spell(ui, game, champ.D, p, 15, False, True)
    p.y += 17
    draw_spell(ui, game, champ.F, p, 15, False, True)


def draw_xp(ui, game, currentxp, lvl, pos, size):
    colorpurp =  Color(0.901, 0.298, 0.862, 1)
    colorpurp.a = 5.0
    ColorWhite = Color.WHITE
    ColorWhite.a = 5.0

    curr = 0.0

    #avoiding urf stuff
    if lvl >= 18 or lvl <= 0:
        return

    for i in range(1, lvl):
        curr += i * 100.0 + 180.0

    currentprc = (currentxp - curr) / (lvl * 100.0 + 180.0)
    output = str(int(currentxp - curr)) + '/' + str(int(lvl * 100.0 + 180.0))

    game.draw_rect_filled(Vec4(pos.x, pos.y, pos.x + size, pos.y + size/5), Color.BLACK)
    game.draw_rect_filled(Vec4(pos.x + 1, pos.y + 1, pos.x + 1 + (size - 1)*currentprc, pos.y + size/5 - 1), colorpurp)
    game.draw_text(pos.add(Vec2(-9, -15.0)), output, colorpurp)
    game.draw_text(pos.add(Vec2(-8, -16.0)), output, ColorWhite)


def Scylla_Update(game, ui):
    global show_allies, show_enemies

    ui.text(str(game.player.Q.icon))
    ui.text(str(game.player.W.icon))
    ui.text(str(game.player.E.icon))
    ui.text(str(game.player.R.icon))


    try:
        for champ in game.champs:
            if not champ.is_visible or not champ.is_alive:
                continue
            if champ.is_ally_to(game.player) and show_allies:
                draw_overlay_on_champ(ui, game, champ)
            elif champ.is_enemy_to(game.player) and show_enemies:
                draw_overlay_on_champ(ui, game, champ)
    except:
        pass

def Scylla_Load(cfg):
    global show_allies, show_enemies

    show_allies = cfg.get_bool("show_allies", False)
    show_enemies = cfg.get_bool("show_enemies", True)

def Scylla_Save(cfg):
    global show_allies, show_enemies

    cfg.set_bool("show_allies", show_allies)
    cfg.set_bool("show_enemies", show_enemies)

def Scylla_Draw(game, ui):
    global show_allies, show_enemies

    show_allies = ui.checkbox("Show overlay on allies", show_allies)
    show_enemies = ui.checkbox("Show overlay on enemies", show_enemies)