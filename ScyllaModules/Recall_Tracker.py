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
from ScyllaCommons.utils import *

recalling = {}
show_allies = False
show_enemies = False

Scylla_Information = {
    "Script": "Enemy Recall Tracker *Out-vision",
    "Description": "",
}

types = {
    # channeling -> (hudcolor, strsize, time)
    'Odin_Recall' : [Color(0.280, 0.815, 0.845, 1),  "6", 8.0],
    'Super_Recall': [Color(0.885, 0.535, 0.865, 1), "11", 4.0],
    'Teleporting' : [Color(0.650, 0.310, 0.790, 1), "16", 4.0],
    'Stand_United': [Color(0.380, 0.310, 0.790, 1), "19", 3.0],
    'Yuumi_W_Ally': [Color(0.735, 0.685, 0.285, 1), "10", 0.0]
}


def recalltrackertime(game, champ, t, time_stamp):
    elapsed_time = t - (game.time - time_stamp)
    if elapsed_time > 0:
        recalling[champ.name][1] = round(elapsed_time, 3)


def recalltracker(ui, game):
    for champ in game.champs:
        if not champ.is_recalling and champ.name in recalling:
            recalling.pop(champ.name)

        for x in types.keys():
            if str(champ.is_recalling) == types[x][1]:
                if champ.name not in recalling:
                    recalling[champ.name] = [game.time, types[x][2], types[x][0], x, types[x][2], champ]
                recalltrackertime(game, champ, types[x][2], recalling[champ.name][0])


def draw_tracker(game, champ, posx, color, state, channelingtime):
    #collors to avoid ui 'a' bugs
    ColorWhite = ColorUtil(Color.WHITE, 1)
    ColorBlack = ColorUtil(Color.BLACK, 1)
    color = ColorUtil(color, 1)

    pos = Vec2(posx, 650)
    size = 50
    s = size / 2
    if channelingtime == 0.0: trackerprc = 1
    if channelingtime != 0.0: trackerprc = channelingtime / recalling[champ][4]
    game.draw_image(champ.lower() + "_square", pos, pos.add(Vec2(size + 14, size + 12.5)), ColorWhite, 100.0)
    pos.x -= 95
    pos.y -= 57.5
    game.draw_image(f'{state.lower()}_hud', pos, pos.add(Vec2(size + 200, size + 210)), ColorWhite, 100.0)
    # pos.y += size
    pos.x += 72.5
    pos.y += 112.5
    game.draw_rect_filled(Vec4(pos.x, pos.y, pos.x + size + 60, pos.y + s), ColorBlack)
    game.draw_rect_filled(Vec4(pos.x + 1, pos.y + 1, pos.x + 1 + (size + 60) * trackerprc, pos.y + s - 1), color)
    game.draw_rect_filled(Vec4(pos.x + 1, pos.y + 1, pos.x + 1 + (size + 60) * trackerprc, pos.y + s - 1), color)
    pos.x += s
    pos.y += s
    pos.x -= 45
    pos.y -= 115
    game.draw_image(f'{state.lower()}_bar', pos, pos.add(Vec2(size + 100, size + 110)), ColorWhite, 100.0)
    pos.x += 20
    pos.y += 122.5
    game.draw_button(pos, state + " " + str(round(recalling[champ][1], 1)), ColorBlack, color, 10);


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

    show_allies = ui.checkbox("Show allies recall", show_allies)
    show_enemies = ui.checkbox("Show enemies recall", show_enemies)


def Scylla_Update(game, ui):
    global show_allies, show_enemies
    recalltracker(ui, game)

    posx = 500
    for ch in recalling:
        if recalling[ch][5].is_ally_to(game.player) and show_allies:
            posx += 135
            draw_tracker(game, ch, posx, recalling[ch][2], recalling[ch][3], recalling[ch][1])
        if recalling[ch][5].is_enemy_to(game.player) and show_enemies:
            posx += 135
            draw_tracker(game, ch, posx, recalling[ch][2], recalling[ch][3], recalling[ch][1])

