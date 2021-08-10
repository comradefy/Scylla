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

Scylla_Information = {
    "Script": "Map Awareness",
    "Description": "Cheat that improves your map awareness."
}

bound_max = 0
show_alert_enemy_close = False
show_last_enemy_pos = False
show_last_enemy_pos_minimap = False


def Scylla_Load(cfg):
    global bound_max, show_alert_enemy_close, show_last_enemy_pos, show_last_enemy_pos_minimap
    show_alert_enemy_close = cfg.get_bool("show_alert_enemy_close", True)
    show_last_enemy_pos = cfg.get_bool("show_last_enemy_pos", True)
    show_last_enemy_pos_minimap = cfg.get_bool("show_last_enemy_pos_minimap", True)
    bound_max = cfg.get_float("bound_max", 4000)


def Scylla_Save(cfg):
    global bound_max, show_alert_enemy_close, show_last_enemy_pos, show_last_enemy_pos_minimap
    cfg.set_float("bound_max", bound_max)
    cfg.set_bool("show_alert_enemy_close", show_alert_enemy_close)
    cfg.set_bool("show_last_enemy_pos", show_last_enemy_pos)
    cfg.set_bool("show_last_enemy_pos_minimap", show_last_enemy_pos_minimap)


def Scylla_Draw(game, ui):
    global bound_max, show_alert_enemy_close, show_last_enemy_pos, show_last_enemy_pos_minimap

    show_last_enemy_pos = ui.checkbox("Show last position of champions", show_last_enemy_pos)
    show_last_enemy_pos_minimap = ui.checkbox("Show last position of champions on minimap", show_last_enemy_pos_minimap)

    ui.separator()
    show_alert_enemy_close = ui.checkbox("Show champions that are getting close", show_alert_enemy_close)
    bound_max = ui.dragfloat("Alert when distance less than", bound_max, 100.0, 500.0, 10000.0)


def draw_champ_world_icon(game, champ, pos, size, draw_distance=False, draw_hp_bar=False,
                          draw_invisible_duration=False):
    size_hp_bar = size / 10.0
    percent_hp = champ.health / champ.max_health

    ColorGray = Color(0.600, 0.700, 0.700, 1)
    ColorGray.a = 5.0
    ColorGreen = Color.GREEN
    ColorGreen.a = 5.0
    ColorWhite = Color.WHITE
    ColorWhite.a = 5.0

    # Draw champ icon
    pos.x -= size / 2.0
    pos.y -= size / 2.0
    game.draw_image(champ.name.lower() + "_square", pos, pos.add(Vec2(size, size)),
                    ColorWhite if champ.is_visible else ColorGray, 100.0)

    # Draw hp bar
    if draw_hp_bar:
        pos.y += size
        game.draw_rect_filled(Vec4(pos.x, pos.y, pos.x + size, pos.y + size_hp_bar), Color.BLACK)
        game.draw_rect_filled(Vec4(pos.x + 1, pos.y + 1, pos.x + 1 + (size - 1) * percent_hp, pos.y + size_hp_bar - 1),
                              ColorGreen)

    # Draw distance
    if draw_distance:
        pos.x += size_hp_bar
        pos.y += size_hp_bar
        game.draw_text(pos, '{:.0f}m'.format(game.distance(champ, game.player)), ColorWhite)

    if not champ.is_visible and draw_invisible_duration:
        pos.x += 2 * size_hp_bar
        pos.y += size_hp_bar
        game.draw_text(pos, '{:.0f}'.format(game.time - champ.last_visible_at), ColorWhite)


def show_alert(game, champ):
    if game.is_point_on_screen(champ.pos) or not champ.is_alive or not champ.is_visible or champ.is_ally_to(
            game.player):
        return

    dist = champ.pos.distance(game.player.pos)
    if dist > bound_max:
        return

    pos = game.world_to_screen(champ.pos.sub(game.player.pos).normalize().scale(500).add(game.player.pos))
    draw_champ_world_icon(game, champ, pos, 48.0, True, True, False)


def show_last_pos_world(game, champ):
    if champ.is_visible or not champ.is_alive or not game.is_point_on_screen(champ.pos):
        return

    draw_champ_world_icon(game, champ, game.world_to_screen(champ.pos), 48.0, False, True, True)


def show_last_pos_minimap(game, champ):
    if champ.is_visible or not champ.is_alive:
        return

    draw_champ_world_icon(game, champ, game.world_to_minimap(champ.pos), 24.0, False, False, False)


def Scylla_Update(game, ui):
    global bound_max, show_alert_enemy_close, show_last_enemy_pos, show_last_enemy_pos_minimap
    for champ in game.champs:
        if show_alert_enemy_close:
            show_alert(game, champ)

        if show_last_enemy_pos:
            show_last_pos_world(game, champ)

        if show_last_enemy_pos_minimap:
            show_last_pos_minimap(game, champ)