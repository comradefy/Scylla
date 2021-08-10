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


import math

def GetDistanceSqr(p1, p2):
    p2 = p2
    d = p1.sub(p2)
    d.z = (p1.z or p1.y) - (p2.z or p2.y)
    return d.x * d.x + d.z * d.z

def GetDistance(p1, p2):
    squaredDistance = GetDistanceSqr(p1, p2)
    return math.sqrt(squaredDistance)

def isValidTarget(game, target, range):
    return target and target.is_visible and target.is_alive and (not range or GetDistance(target.pos, game.player.pos) <= range)
	
def ValidTarget(obj):
    return (obj and obj.is_alive and obj.is_visible and obj.isTargetable)

def getSkill(game, slot):
    skill = getattr(game.player, slot)
    if skill:
        return skill
    return None

def buffIsAlive(time, buff) -> bool:
    if not buff or not buff.start_time or not buff.end_time:
        return False
    return buff.end_time > time

def getChamp_by_name(champs, name):
    for champ in champs:
        if champ.name == name:
            return champ

def IsReady(game, skill):
    return skill and skill.get_current_cooldown(game.time) == 0.0 and skill.level > 0

def ColorUtil(color, opacity):
    colorutil = color
    colorutil.a = opacity
    return colorutil