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
from time import time
from ScyllaCommons.skills import *
from ScyllaCommons.items import *
from ScyllaCommons.utils import *
import itertools, math
from copy import copy
import array

Scylla_Information = {
    "Script": "Drawings",
    "Description": "Draws indicators for different things"
}

turret_ranges = False
enemy_ranges = False
attack_range = False
minion_last_hit = False
draw_spell_range = False

skillshots_predict    = False
skillshots_min_range  = 0
skillshots_max_speed  = 0
skillshots_show_ally  = False
skillshots_show_enemy = False

circle_filled1 = False
circle_filled2 = False
circle_filled3 = False

cast_keys = {
    'Q': 0,
    'W': 0,
    'E': 0,
    'R': 0
}

def Scylla_Load(cfg):
    global turret_ranges, enemy_ranges, attack_range, draw_spell_range
    global skillshots_predict, skillshots_min_range, minion_last_hit, skillshots_max_speed, skillshots_show_ally, skillshots_show_enemy
    global circle_filled1, circle_filled2, circle_filled3
    turret_ranges = cfg.get_bool("turret_ranges", True)
    enemy_ranges = cfg.get_bool("enemy_ranges", True)
    minion_last_hit = cfg.get_bool("minion_last_hit", True)
    draw_spell_range = cfg.get_bool("draw_spell_range", True)
    attack_range = cfg.get_bool("attack_range", True)

    skillshots_show_ally = cfg.get_bool("skillshots_show_ally", True)
    skillshots_show_enemy = cfg.get_bool("skillshots_show_enemy", True)
    skillshots_predict = cfg.get_bool("skillshots_predict", True)
    skillshots_min_range = cfg.get_float("skillshots_min_range", 500)
    skillshots_max_speed = cfg.get_float("skillshots_max_speed", 2500)
    circle_filled1 = cfg.get_bool("circle_filled1", False)
    circle_filled2 = cfg.get_bool("circle_filled2", False)
    circle_filled3 = cfg.get_bool("circle_filled3", False)


def Scylla_Save(cfg):
    global turret_ranges, enemy_ranges, attack_range, draw_spell_range
    global skillshots_predict, skillshots_min_range, minion_last_hit, skillshots_max_speed, skillshots_show_ally, skillshots_show_enemy
    global circle_filled1, circle_filled2, circle_filled3
    cfg.set_bool("turret_ranges", turret_ranges)
    cfg.set_bool("enemy_ranges", enemy_ranges)
    cfg.set_bool("minion_last_hit", minion_last_hit)
    cfg.set_bool("draw_spell_range", draw_spell_range)
    cfg.set_bool("attack_range", attack_range)

    cfg.set_bool("skillshots_show_ally", skillshots_show_ally)
    cfg.set_bool("skillshots_show_enemy", skillshots_show_enemy)
    cfg.set_bool("skillshots_predict", skillshots_predict)
    cfg.set_float("skillshots_min_range", skillshots_min_range)
    cfg.set_float("skillshots_max_speed", skillshots_max_speed)

    cfg.set_bool("circle_filled1", circle_filled1)
    cfg.set_bool("circle_filled2", circle_filled2)
    cfg.set_bool("circle_filled3", circle_filled3)


def Scylla_Draw(game, ui):
    global turret_ranges, enemy_ranges, attack_range, minion_last_hit, draw_spell_range
    global skillshots_predict, skillshots_min_range, skillshots_max_speed, skillshots_show_ally, skillshots_show_enemy
    global circle_filled1, circle_filled2, circle_filled3
    turret_ranges = ui.checkbox("Turret ranges", turret_ranges); ui.sameline()
    circle_filled1 = ui.checkbox("FilledCircle1", circle_filled1)
    enemy_ranges = ui.checkbox("Draw enemy ranges", enemy_ranges); ui.sameline()
    circle_filled2 = ui.checkbox("FilledCircle2", circle_filled2)
    minion_last_hit = ui.checkbox("Minion last hit", minion_last_hit)
    draw_spell_range = ui.checkbox("Champion spell range", draw_spell_range)
    attack_range = ui.checkbox("Champion attack range", attack_range); ui.sameline()
    circle_filled3 = ui.checkbox("FilledCircle3", circle_filled3)

    ui.text("* Skillshots (Experimental) *")
    skillshots_show_ally = ui.checkbox("Show for allies", skillshots_show_ally); ui.sameline()
    skillshots_show_enemy = ui.checkbox("Show for enemies", skillshots_show_enemy)

def draw_rect(game, start_pos, end_pos, radius, color):
    dir = Vec3(end_pos.x - start_pos.x, 0, end_pos.z - start_pos.z).normalize()

    left_dir = Vec3(dir.x, dir.y, dir.z).rotate_y(90).scale(radius)
    right_dir = Vec3(dir.x, dir.y, dir.z).rotate_y(-90).scale(radius)

    p1 = Vec3(start_pos.x + left_dir.x, start_pos.y + left_dir.y, start_pos.z + left_dir.z)
    p2 = Vec3(end_pos.x + left_dir.x, end_pos.y + left_dir.y, end_pos.z + left_dir.z)
    p3 = Vec3(end_pos.x + right_dir.x, end_pos.y + right_dir.y, end_pos.z + right_dir.z)
    p4 = Vec3(start_pos.x + right_dir.x, start_pos.y + right_dir.y, start_pos.z + right_dir.z)

    color.a = 0.2
    # game.draw_triangle_world_filled(p1, p2, p3, color)
    # game.draw_triangle_world_filled(p1, p3, p4, color)
    game.draw_rect_world(p1, p2, p3, p4, 1, color)


def draw_atk_range(game, player):
    if player.is_alive and player.is_visible and game.is_point_on_screen(player.pos):
        if circle_filled3:
            game.draw_circle_world_filled(player.pos, player.atk_range + player.gameplay_radius, 50, ColorUtil(Color.CYAN, 0.1))
        game.draw_circle_world(player.pos, player.atk_range + player.gameplay_radius, 100, 2, ColorUtil(Color.PURPLE, 5.0))


def draw_spell_ranges(game, player):
    global cast_keys
    if player.is_alive and player.is_visible and game.is_point_on_screen(player.pos):
        for slot, key in cast_keys.items():
            skill = getattr(game.player, slot)
            for champ in game.champs:
                range = champ.atk_range + champ.gameplay_radius
                dist = champ.pos.distance(player.pos) - range
                if dist <= player.gameplay_radius:
                    if skill.cast_range > 0 and not skill.cast_range > 2500:
                        game.draw_circle_world(player.pos, skill.cast_range, 100, 5, ColorUtil(Color.PURPLE, 0.1))
                else:
                    if skill.cast_range > 0 and not skill.cast_range > 2500:
                        game.draw_circle_world(player.pos, skill.cast_range, 100, 5, ColorUtil(Color.WHITE, 0.1))

def draw_turret_ranges(game, player):
    for turret in game.turrets:
        if turret.is_alive and turret.is_enemy_to(player) and game.is_point_on_screen(turret.pos):
            range = turret.atk_range + 30
            dist = turret.pos.distance(player.pos) - range
            if dist <= player.gameplay_radius:
                if circle_filled1:
                    game.draw_circle_world_filled(turret.pos, range, 100, ColorUtil(Color.ORANGE, 0.08))
                game.draw_circle_world(turret.pos, range, 100, 5, ColorUtil(Color.ORANGE, 0.2))
            else:
                if circle_filled1:
                    game.draw_circle_world_filled(turret.pos, range, 100, ColorUtil(Color.ORANGE, 0.08))
                game.draw_circle_world(turret.pos, range, 100, 5, ColorUtil(Color.ORANGE, 0.2))


def draw_minion_last_hit(game, player):
    for minion in game.minions:
        if minion.is_visible and minion.is_alive and minion.is_enemy_to(player) and game.is_point_on_screen(minion.pos):
            if is_last_hitable(game, player, minion):
                p = game.hp_bar_pos(minion)
                game.draw_rect(Vec4(p.x - 34, p.y - 9, p.x + 32, p.y + 1), ColorUtil(Color.WHITE, 5.0), 0, 2)


def draw_champ_ranges(game, player):
    for champ in game.champs:
        if champ.is_alive and champ.is_visible and champ.is_enemy_to(player) and game.is_point_on_screen(
                champ.pos) and champ.movement_speed > 0:
            range = champ.atk_range + champ.gameplay_radius
            dist = champ.pos.distance(player.pos) - range
            if dist <= player.gameplay_radius:
                if circle_filled2:
                    game.draw_circle_world_filled(champ.pos, champ.atk_range + champ.gameplay_radius, 100, ColorUtil(Color.RED, 0.05))
                game.draw_circle_world(champ.pos, champ.atk_range + champ.gameplay_radius, 100, 3, ColorUtil(Color.GREEN, 0.05))
            else:
                if circle_filled2:
                    game.draw_circle_world_filled(champ.pos, champ.atk_range + champ.gameplay_radius, 100, ColorUtil(Color.GREEN, 0.05))
                game.draw_circle_world(champ.pos, champ.atk_range + champ.gameplay_radius, 100, 3, ColorUtil(Color.RED, 0.15))


def draw_skillshots(game, player):
    global skillshots_predict, skillshots_min_range, skillshots_max_speed, skillshots_show_ally, skillshots_show_enemy

    for missile in game.missiles:
        if not skillshots_show_ally and missile.is_ally_to(game.player):
            continue
        if not skillshots_show_enemy and missile.is_enemy_to(game.player):
            continue

        if not is_skillshot(missile.name) or missile.speed > skillshots_max_speed or missile.start_pos.distance(
                missile.end_pos) < skillshots_min_range:
            continue

        spell = get_missile_parent_spell(missile.name)
        if not spell:
            continue

        end_pos = missile.end_pos.clone()
        start_pos = missile.start_pos.clone()
        curr_pos = missile.pos.clone()
        impact_pos = None

        start_pos.y = game.map.height_at(start_pos.x, start_pos.z) + missile.height
        end_pos.y = start_pos.y
        curr_pos.y = start_pos.y

        if spell.flags & SFlag.Line:
            draw_rect(game, curr_pos, end_pos, missile.width, ColorUtil(Color.WHITE, 5.0))
            game.draw_circle_world_filled(curr_pos, missile.width, 20, ColorUtil(Color.RED, 0.1))

        if spell.flags & SFlag.SkillshotLine:
            draw_rect(game, curr_pos, end_pos, missile.width, ColorUtil(Color.WHITE, 5.0))
            game.draw_circle_world_filled(curr_pos, missile.width, 20, ColorUtil(Color.RED, 0.1))

        elif spell.flags & SFlag.Area:
            r = game.get_spell_info(spell.name)
            end_pos.y = game.map.height_at(end_pos.x, end_pos.z)
            percent_done = missile.start_pos.distance(curr_pos) / missile.start_pos.distance(end_pos)
            color = Color(1, 1.0 - percent_done, 0, 0.25)

            game.draw_circle_world(end_pos, r.cast_radius, 40, 3, color)
            game.draw_circle_world_filled(end_pos, r.cast_radius * percent_done, 40, color)
        else:
            percent_done = missile.start_pos.distance(curr_pos) / missile.start_pos.distance(end_pos)
            color = Color(1, 1.0 - percent_done, 0, 0.25)
            draw_rect(game, curr_pos, end_pos, missile.width, color)

def Scylla_Update(game, ui):
    global turret_ranges, attack_range, minion_last_hit, draw_spell_range

    player = game.player
    draw_skillshots(game, player)

    if attack_range:
        draw_atk_range(game, player)

    if draw_spell_range:
        draw_spell_ranges(game, player)

    if turret_ranges:
        draw_turret_ranges(game, player)

    if enemy_ranges:
        draw_champ_ranges(game, player)

    if minion_last_hit:
        draw_minion_last_hit(game, player)