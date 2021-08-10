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
import json

Scylla_Information = {
	"Script": "Vision Tracker",
	"Description": "",
}

show_clones, show_wards, show_traps = None, None, None

traps = {
	#Name -> (radius, show_radius_circle, show_radius_circle_minimap, icon)
	'caitlyntrap'          : [50,  True,  False, "caitlyn_yordlesnaptrap"],
	'jhintrap'             : [140, True,  False, "jhin_e"],
	'jinxmine'             : [50,  True,  False, "jinx_e"],
	'maokaisproutling'     : [50,  False, False, "maokai_e"],
	'nidaleespear'         : [50,  True,  False, "nidalee_w1"],
	'shacobox'             : [300, True,  False, "jester_deathward"],
	'teemomushroom'        : [75,  True,  True,  "teemo_r"]
}

wards = {
	'bluetrinket'          : [900, True, True, "bluetrinket"],
	'jammerdevice'         : [900, True, True, "pinkward"],
	'perkszombieward'      : [900, True, True, "bluetrinket"],
	'sightward'            : [900, True, True, "sightward"],
	'visionward'           : [900, True, True, "sightward"],
	'yellowtrinket'        : [900, True, True, "yellowtrinket"],
	'yellowtrinketupgrade' : [900, True, True, "yellowtrinket"],
	'ward'                 : [900, True, True, "sightward"],
}

clones = {
	'shaco'           : [0, False, False, ""],
	'leblanc'         : [0, False, False, ""],
	'monkeyking'      : [0, False, False, ""],
	'neeko'           : [0, False, False, ""],
	'fiddlesticks'    : [0, False, False, ""],
}


def Scylla_Load(cfg):
	global show_clones, show_wards, show_traps, traps, wards, clones

	show_clones = cfg.get_bool("show_clones", True)
	show_wards = cfg.get_bool("show_wards", True)
	show_traps = cfg.get_bool("show_traps", True)
	
	traps = json.loads(cfg.get_str("traps", json.dumps(traps)))
	wards = json.loads(cfg.get_str("wards", json.dumps(wards)))
	clones = json.loads(cfg.get_str("clones", json.dumps(clones)))
	
def Scylla_Save(cfg):
	global show_clones, show_wards, show_traps, traps, wards, clones
	
	cfg.set_bool("show_clones", show_clones)
	cfg.set_bool("show_wards", show_wards)
	cfg.set_bool("show_traps", show_traps)
	
	cfg.set_str("traps", json.dumps(traps))
	cfg.set_str("wards", json.dumps(wards))
	cfg.set_str("clones", json.dumps(clones))
	
def Scylla_Draw(game, ui):
	global traps, wards, clones
	global show_clones, show_wards, show_traps
	
	show_clones = ui.checkbox("Show clones", show_clones)
	show_wards = ui.checkbox("Show wards", show_wards)
	show_traps = ui.checkbox("Show traps", show_traps)
	
	ui.text("Traps")
	for x in traps.keys():
		if ui.treenode(x):
			traps[x][1] = ui.checkbox("Show range circles", traps[x][1])
			traps[x][2] = ui.checkbox("Show on minimap", traps[x][2])
			
			ui.treepop()
			
	ui.text("Wards")
	for x in wards.keys():
		if ui.treenode(x):
			wards[x][1] = ui.checkbox("Show range circles", wards[x][1])
			wards[x][2] = ui.checkbox("Show on minimap", wards[x][2])
			
			ui.treepop()

	ui.text("Clones")
	for x in clones.keys():
		if ui.treenode(x):
			clones[x][1] = ui.checkbox("Show range circles", clones[x][1])

			ui.treepop()

def draw(game, obj, radius, show_circle_world, show_circle_map, icon):
			
	sp = game.world_to_screen(obj.pos)
	
	if game.is_point_on_screen(sp):
		duration = obj.duration + obj.last_visible_at - game.time
		if duration > 0:
			game.draw_text(sp.add(Vec2(5, 30)), f'{duration:.0f}', ColorUtil(Color.WHITE, 1.0))
		game.draw_image(icon, sp, sp.add(Vec2(30, 30)), ColorUtil(Color.WHITE, 1.0), 10)
		
		if show_circle_world:
			game.draw_circle_world(obj.pos, radius, 30, 3, ColorUtil(Color.RED, 1.0))
	
	if show_circle_map:
		p = game.world_to_minimap(obj.pos)
		game.draw_circle(game.world_to_minimap(obj.pos), game.distance_to_minimap(radius), 15, 2, ColorUtil(Color.RED, 1.0))

def Scylla_Update(game, ui):
	
	global show_clones, show_wards, show_traps
	global traps, wards, clones
	
	for obj in game.others:
		if obj.is_ally_to(game.player) or not obj.is_alive:
			continue
		
		if show_wards and obj.has_tags(UnitTag.Unit_Ward) and obj.name in wards:
			draw(game, obj, *(wards[obj.name]))
		elif show_traps and obj.has_tags(UnitTag.Unit_Special_Trap) and obj.name in traps:
			draw(game, obj, *(traps[obj.name]))
	
	if show_clones:
		for champ in game.champs:
			if not champ.is_alive:
				continue
			if champ.name in clones and champ.R.name == champ.D.name:
				draw(game, champ, *(clones[champ.name]))
		