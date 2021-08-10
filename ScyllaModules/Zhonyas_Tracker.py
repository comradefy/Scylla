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

Scylla_Information = {
    "Script": "Zhonyas Tracker",
    "Description": "",
}

tracker = {}


def Scylla_Load(cfg):
    pass


def Scylla_Save(cfg):
    pass


def Scylla_Draw(game, ui):
    global tracker

    if ui.treenode("Champions that purchased Zhonya's are checked."):
        for t in tracker:
            tracker[t][1] = ui.checkbox(str(t), tracker[t][1])
            ui.sameline()
        ui.treepop()


def trackertime(game, champ, start_time):
    elapsed_time = game.time - start_time
    tracker[champ.name][0] = round(elapsed_time, 1)


def Scylla_Update(game, ui):
    global tracker

    for ch in game.champs:
        if ch.is_enemy_to(game.player):
            if ch.name not in tracker:
                tracker[ch.name] = [0.0, False, 0.0]
            for item in ch.items:
                if item.id == 3157 or item.id == 2420:
                    tracker[ch.name][1] = True

    for t in tracker:
        if tracker[t][1]:

            ch = getChamp_by_name(game.champs, t)
            p = game.hp_bar_pos(ch)
            p.y -= 100
            p.x -= 20

            if not game.is_point_on_screen(p):
                return

            if ch.is_alive and ch.is_visible:
                for cBuff in ch.buffs:
                    if cBuff and cBuff.name == 'zhonyasringshield' and buffIsAlive(game.time, cBuff):
                        tracker[t][2] = round(cBuff.start_time, 1)
                        game.draw_text(p.add(Vec2(10, -20)), str(round(2.50 - tracker[t][0], 1)),
                                       ColorUtil(Color.WHITE, 1))

            trackertime(game, ch, tracker[t][2])
            cd = round(tracker[t][0] - 110.0, 1)
            if cd < 0.0:
                game.draw_image('hourglass', p, p.add(Vec2(35, 35)), ColorUtil(Color.GRAY, 0.6), 50)
                p.y += 12.5
                game.draw_text(p, str(round(tracker[t][0] - 110.0, 1)), ColorUtil(Color.WHITE, 1))
                return
            game.draw_image('hourglass', p, p.add(Vec2(35, 35)), ColorUtil(Color.WHITE, 0.9), 50)
