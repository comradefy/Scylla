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

def crit_from_items(items):
	crit = 0.0
	for item in items:
		crit += item.crit
	return crit

def onhit_guinsoo(src, target):
	return crit_from_items(src.items) * 100.0 * 2.0
	
def onhit_rageknife(src, target):
	return crit_from_items(src.items) * 100.0 * 1.75

def onhit_noonquiver(src, target):
	return 0.0 if target.has_tags(UnitTag.Unit_Champion) else 20.0
	
def onhit_recurve_bow(src, target):
	return 15.0
	
def onhit_botrk(src, target):
	dmg = target.health * (0.06 if src.is_ranged else 0.1)
	if dmg > 60.0 and not target.has_tags(UnitTag.Unit_Champion):
		return 60.0
	return dmg
	
def onhit_doran_ring(src, target):
	return 5.0
	
def onhit_nashors(src, target):
	return 15.0 + 0.2 * src.ap
	
def onhit_wits_end(src, target):
	return 11.7 + 3.82 * src.lvl

OnHit_Physical = {
	3124: onhit_guinsoo,
	6677: onhit_rageknife,	
	6670: onhit_noonquiver,
	1043: onhit_recurve_bow,
	3153: onhit_botrk,
	1056: onhit_doran_ring
}

OnHit_Magical = {
	3115: onhit_nashors,
	3091: onhit_wits_end
}

def get_onhit_physical(source, target):
	global OnHit_Physical
	
	phys = source.base_atk + source.bonus_atk
	for item in source.items:
		if item.id in OnHit_Physical:
			phys += OnHit_Physical[item.id](source, target)
			
	return phys
	
def get_onhit_magical(source, target):
	global OnHit_Magical
	
	magical = 0.0
	for item in source.items:
		if item.id in OnHit_Magical:
			magical += OnHit_Magical[item.id](source, target)
			
	return magical
		