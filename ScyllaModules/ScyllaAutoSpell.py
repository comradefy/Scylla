from Scylla import *
from ScyllaCommons.Scylla_targeting import TargetingConfig
from ScyllaCommons.Scylla_skills import *
import json, time
from pprint import pprint

Scylla_Information = {
	"script": "AutoSpell",
	"author": "leryss",
	"description": "",
}

targeting = TargetingConfig()
cast_keys = {
	'Q': 0,
	'W': 0,
	'E': 0,
	'R': 0
}

def Load_cfg(cfg):
	global targeting, cast_keys
	targeting.load_from_cfg(cfg)
	cast_keys = json.loads(cfg.get_str('cast_keys', json.dumps(cast_keys)))
	
def Save_cfg(cfg):
	global targeting, cast_keys
	targeting.save_to_cfg(cfg)
	cfg.set_str('cast_keys', json.dumps(cast_keys))

def Draw_settings(game, ui):
	global targeting, cast_keys
	targeting.draw(ui)
	for slot, key in cast_keys.items():
		cast_keys[slot] = ui.keyselect(f'Key to cast {slot}', key)
	draw_prediction_info(game, ui)
	
def Scylla_Update(game, ui):
	global targeting, cast_keys

	for slot, key in cast_keys.items():
		if game.was_key_pressed(key):
			skill = getattr(game.player, slot)
			b_is_skillshot = is_skillshot(skill.name)
			skill_range = get_skillshot_range(game, skill.name) if b_is_skillshot else 1500.0
			target = targeting.get_target(game, skill_range)
			
			if target:
				if b_is_skillshot:
					cast_point = castpoint_for_collision(game, skill, game.player, target)
				else:
					cast_point = target.pos
					
				if cast_point:
					cast_point = game.world_to_screen(cast_point)
					
					old_cpos = game.get_cursor()
					game.move_cursor(cast_point)
					
					skill.trigger()
					
					time.sleep(0.01)
					game.move_cursor(old_cpos)