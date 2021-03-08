from Scylla import *

enable_key = 0
show_smitable = False

enabled_autosmite = False

Scylla_Information = {
	"script": "AutoSmite",
	"author": "leryss",
	"description": "",
}

def Load_cfg(cfg):
	global enable_key, show_smitable
	enable_key = cfg.get_int("enable_key", 0)
	show_smitable = cfg.get_bool("show_smitable", True)
	
def Save_cfg(cfg):
	global enable_key, show_smitable
	cfg.set_int("enable_key", enable_key)
	cfg.set_bool("show_smitable", show_smitable)
	
def Draw_settings(game, ui):
	global enable_key, show_smitable
	show_smitable = ui.checkbox("Show when to smite", show_smitable)
	enable_key = ui.keyselect("Enable auto smite key", enable_key)
	
def Scylla_Update(game, ui):
	global enable_key, enabled_autosmite, show_smitable
	
	smite = game.player.get_summoner_spell(SummonerSpellType.Smite)
	if smite == None: 
		return

	if game.was_key_pressed(enable_key):
		enabled_autosmite = ~enabled_autosmite
	
	hovered = game.hovered_obj
	is_smitable = (hovered and (hovered.has_tags(UnitTag.Unit_Monster_Large) or hovered.has_tags(UnitTag.Unit_Monster_Epic)) and hovered.health - smite.value <= 0)
	if enabled_autosmite:
		p = game.world_to_screen(game.player.pos)
		p.y -= 50
		game.draw_button(p, "AutoSmiteOn", Color.BLACK, Color.YELLOW, 10);
		
		if is_smitable:
			smite.trigger()
	
	if show_smitable and is_smitable:
		game.draw_circle_world(hovered.pos, hovered.gameplay_radius, 30, 3, Color.YELLOW)