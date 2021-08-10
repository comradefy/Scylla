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
from ScyllaCommons.utils import ColorUtil

Scylla_Information = {
	"Script": "Ward Assist",
	"Description": "",
}

wardlist = open('C:/Users/WIN-Conrado/source/repos/LViewLoL-master/GameplayScripts/ScyllaCommons/wardpos').read().split('\n')
key_show_wards = 0
key_assist_ward = 0
show = False

def Scylla_Load(cfg):
	global key_show_wards, key_assist_ward
	key_show_wards = cfg.get_int("key_show_wards", 0)	
	key_assist_ward     = cfg.get_int("key_assist_ward", 0)	
	
def Scylla_Save(cfg):
	global key_show_wards, key_assist_ward
	cfg.set_int("key_show_wards", key_show_wards)
	cfg.set_int("key_assist_ward", key_assist_ward)
	pass
def Scylla_Draw(game, ui):
	global key_show_wards, key_assist_ward
	key_show_wards = ui.keyselect("Show/Hide wards key", key_show_wards)
	key_assist_ward     = ui.keyselect("Ward Assist key", key_assist_ward)
def Scylla_Update(game, ui):
	global show
	if game.was_key_pressed(key_show_wards):
		show = not show
	if not show:
		return

	if game.map.type == MapType.SummonersRift:    
		for i in wardlist:
			wards = i.rsplit(':', 1)
			playerpos = wards[0].split(",")
			wardpos = wards[1].split(",")
			playerposvec = Vec3(float(playerpos[0]), float(playerpos[1]), float(playerpos[2]))
			wardposvec = Vec3(float(wardpos[0]), float(wardpos[1]), float(wardpos[2]))
			game.draw_circle_world(playerposvec, 45, 60, 3, ColorUtil(Color.ORANGE, 5.0))
			game.draw_circle_world(wardposvec, 5, 60, 3, ColorUtil(Color.CYAN, 5.0))
			if game.is_key_down(44) and playerposvec.distance(game.player.pos) < 300.0:
				if playerposvec.distance(game.player.pos) > 70.0:
					game.move_cursor(game.world_to_screen(playerposvec))
				else:
					game.move_cursor(game.world_to_screen(wardposvec))
				game.draw_circle_world(playerposvec, 300, 60, 3, ColorUtil(Color.RED, 5.0))