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
	"Script": "Crowd Control Cleaner (Auto-QSS/Cleanse)",
	"Description": "",
}

avoiding = {}

time = 0.0;
qss_key  = 	  0;
Stun 		= False;
Silence	    = False;
Taunt 	    = False;
Polymorph   = False;
Slow 		= False;
Snare 	    = False;
Sleep 	 	= False;
NearSigh    = False;
Fear 		= False;
Charm 		= False;
Suppression = False;
Blind 		= False;
Knockup 	= False;
Knockback 	= False;

def Scylla_Load(cfg):
	global Stun, Silence, Taunt, Polymorph, Slow, Snare, Sleep, NearSigh, Fear, Charm, Suppression, Blind, Knockup, Knockback, qss_key

	qss_key  = cfg.get_int("qss_key", 	  0)
	Stun 		= cfg.get_bool("Stun", 	 	  False)
	Silence 	= cfg.get_bool("Silence", 	  False)
	Taunt 		= cfg.get_bool("Taunt", 	  False)
	Polymorph 	= cfg.get_bool("Polymorph",   False)
	Slow 		= cfg.get_bool("Slow",		  False)
	Snare 		= cfg.get_bool("Snare", 	  False)
	Sleep 		= cfg.get_bool("Sleep", 	  False)
	NearSigh    = cfg.get_bool("NearSigh", 	  False)
	Fear 		= cfg.get_bool("Fear", 		  False)
	Charm 		= cfg.get_bool("Charm", 	  False)
	Suppression = cfg.get_bool("Suppression", False)
	Blind 		= cfg.get_bool("Blind",		  False)
	Knockup 	= cfg.get_bool("Knockup", 	  False)
	Knockback 	= cfg.get_bool("Knockback",   False)

def Scylla_Save(cfg):
	global Stun, Silence, Taunt, Polymorph, Slow, Snare, Sleep, NearSigh, Fear, Charm, Suppression, Blind, Knockup, Knockback, qss_key

	cfg.set_int("qss_key",      qss_key)
	cfg.set_bool("Stun", 		Stun)
	cfg.set_bool("Silence", 	Silence)
	cfg.set_bool("Taunt", 		Taunt)
	cfg.set_bool("Polymorph",   Polymorph)
	cfg.set_bool("Slow", 		Slow)
	cfg.set_bool("Snare", 		Snare)
	cfg.set_bool("Sleep", 		Sleep)
	cfg.set_bool("NearSigh",    NearSigh)
	cfg.set_bool("Fear",	    Fear)
	cfg.set_bool("Charm", 		Charm)
	cfg.set_bool("Suppression", Suppression)
	cfg.set_bool("Blind", 		Blind)
	cfg.set_bool("Knockup", 	Knockup)
	cfg.set_bool("Knockback",   Knockback)

def Scylla_Draw(game, ui):
	global Stun, Silence, Taunt, Polymorph, Slow, Snare, Sleep, NearSigh, Fear, Charm, Suppression, Blind, Knockup, Knockback, qss_key

	qss_key  = ui.keyselect("QSS Slot", 				     qss_key)
	ui.text("CC Types:");
	Stun 		= ui.checkbox("Stun       ", 		Stun); ui.sameline()
	Silence 	= ui.checkbox("Silence", 		 Silence); ui.sameline()
	Taunt 		= ui.checkbox("Taunt   ", 		   Taunt); ui.sameline()
	Polymorph   = ui.checkbox("Polymorph", 	   Polymorph); ui.sameline()
	Slow 		= ui.checkbox("Slow",			    Slow)
	Snare 		= ui.checkbox("Snare      ", 	   Snare); ui.sameline()
	Sleep 		= ui.checkbox("Sleep  ", 		   Sleep); ui.sameline()
	NearSigh    = ui.checkbox("NearSigh", 		NearSigh); ui.sameline()
	Fear 	    = ui.checkbox("Fear     ", 			Fear); ui.sameline()
	Charm 		= ui.checkbox("Charm", 			   Charm)
	Suppression = ui.checkbox("Suppression", Suppression); ui.sameline()
	Blind 		= ui.checkbox("Blind  ", 			   Blind); ui.sameline()
	Knockup 	= ui.checkbox("Knockup ", 		 Knockup); ui.sameline()
	Knockback   = ui.checkbox("Knockback",	   Knockback)

def Scylla_Update(game, ui):
	global Stun, Silence, Taunt, Polymorph, Slow, Snare, Sleep, NearSigh, Fear, Charm, Suppression, Blind, Knockup, Knockback, qss_key, time

	if Stun:
		avoiding["Stun"] = [5]
	else:
		if "Stun" in avoiding:
			avoiding.pop("Stun")

	if Silence:
		avoiding["Silence"] = [7]
	else:
		if "Silence" in avoiding:
			avoiding.pop("Silence")

	if Taunt:
		avoiding["Taunt"] = [8]
	else:
		if "Taunt" in avoiding:
			avoiding.pop("Taunt")

	if Polymorph:
		avoiding["Polymorph"] = [9]
	else:
		if "Polymorph" in avoiding:
			avoiding.pop("Polymorph")

	if Slow:
		avoiding["Slow"] = [10]
	else:
		if "Slow" in avoiding:
			avoiding.pop("Slow")

	if Snare:
		avoiding["Snare"] = [11]
	else:
		if "Snare" in avoiding:
			avoiding.pop("Snare")

	if Sleep:
		avoiding["Sleep"] = [18]
	else:
		if "Sleep" in avoiding:
			avoiding.pop("Sleep")

	if NearSigh:
		avoiding["NearSigh"] = [19]
	else:
		if "NearSigh" in avoiding:
			avoiding.pop("NearSigh")

	if Fear:
		avoiding["Fear"] = [21]
	else:
		if "Fear" in avoiding:
			avoiding.pop("Fear")

	if Charm:
		avoiding["Charm"] = [22]
	else:
		if "Charm" in avoiding:
			avoiding.pop("Charm")

	if Suppression:
		avoiding["Suppression"] = [24]
	else:
		if "Suppression" in avoiding:
			avoiding.pop("Suppression")

	if Blind:
		avoiding["Blind"] = [25]
	else:
		if "Blind" in avoiding:
			avoiding.pop("Blind")

	if Knockup:
		avoiding["Knockup"] = [29]
	else:
		if "Knockup" in avoiding:
			avoiding.pop("Knockup")

	if Knockback:
		avoiding["Knockback"] = [30]
	else:
		if "Knockback" in avoiding:
			avoiding.pop("Knockback")

	for buff in game.player.buffs:
		# avoid ended buffs #
		if game.time < buff.end_time:
			# try to read buffptr and pass if can't [0x100]
			try:
                # avoid blastcone #
				if not buff.name == "plantsatchelknockback":
					for av in avoiding:
						if buff.type == avoiding[av][0]:
							cleanse = game.player.get_summoner_spell(SummonerSpellType.Cleanse)
							if not cleanse == None:
								if cleanse.get_current_cooldown(game.time) == 0:
									cleanse.trigger()
							if not qss_key == None:
								game.press_key(qss_key)
			except:
				pass