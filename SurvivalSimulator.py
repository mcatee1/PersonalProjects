import random
from enum import Enum

tributeCount = 14
tributes = [{'name': "Alex", 'stats': [0, 3, 10, 1, 3, 3], 'items': [], 'effects': [], 'district': 1},
    {'name': "Bart", 'stats': [10, 7, 0, 3, 0, 0], 'items': [], 'effects': [], 'district': 1},
    {'name': "Caroline", 'stats': [0, 0, 5, 5, 5, 5], 'items': [], 'effects': [], 'district': 2},
    {'name': "Daryl", 'stats': [4, 4, 4, 4, 4, 0], 'items': [], 'effects': [], 'district': 2},
    {'name': "Evelynn", 'stats': [0, 5, 5, 0, 10, 0], 'items': [], 'effects': [], 'district': 3},
    {'name': "Fiona", 'stats': [7, 4, 3, 5, 1, 0], 'items': [], 'effects': [], 'district': 4},
    {'name': "Geraldo", 'stats': [2, 2, 2, 5, 4, 5], 'items': [], 'effects': [], 'district': 5},
    {'name': "Harry", 'stats': [0, 10, 5, 3, 2, 0], 'items': [], 'effects': [], 'district': 6},
    {'name': "Indiana", 'stats': [0, 0, 0, 0, 0, 20], 'items': [], 'effects': [], 'district': 7},
    {'name': "Jocelynn", 'stats': [0, 0, 0, 20, 0, 0], 'items': [], 'effects': [], 'district': 8},
    {'name': "Kristina", 'stats': [0, 0, 0, 0, 20, 0], 'items': [], 'effects': [], 'district': 9},
    {'name': "Liam", 'stats': [0, 20, 0, 0, 0, 0], 'items': [], 'effects': [], 'district': 10},
    {'name': "Miguel", 'stats': [20, 0, 0, 0, 0, 0], 'items': [], 'effects': [], 'district': 11},
    {'name': "Neil", 'stats': [0, 0, 20, 0, 0, 0], 'items': [], 'effects': [], 'district': 12}
    ]
displayTributes = tributes.copy()

for tribute in tributes:
    newStats = []
    for statValue in tribute['stats']:
        statValue = (statValue + 1) / 20
        newStats.append(statValue)
    tribute['stats'] = newStats

statsNames = ["Strength", "Agility", "Intelligence", "Survival", "Charisma", "Luck"]
statsAbr = ["STR", "AGI", "INT", "SRV", "CHR", "LCK"]
item_categories = {
    'melee_weapons': ['dagger', 'sword']
}
arenaStatus = {'mines': 0}

class Stats(Enum):
    STR = 0
    AGI = 1
    INT = 2
    SRV = 3
    CHR = 4
    LCK = 5
    
inc = 0
    
"""for tribute in tributes:
    print("-", tribute['name'].upper(), "-")
    for k, stat_abr in enumerate(statsAbr):
        stat_value = tribute['stats'][k]
        if stat_value == 0:
            print(stat_abr + ":")
        elif stat_value < 10:
            print(stat_abr + ": ", stat_value)
        else:
            print(stat_abr + ":", stat_value)"""
            
print("\nLet the games begin!\n")

#-- SINGLE EVENTS --#

def event_dance(current_idx, order, tributes):
    print("dances")

def event_hums(current_idx, order, tributes):
    print("hums")
    
def event_findDagger(current_idx, order, tributes):
    actingTribute = tributes[order[current_idx]]
    print("finds a dagger")
    giveItem(actingTribute, 'dagger')
    
def event_findMed(current_idx, order, tributes):
    actingTribute = tributes[order[current_idx]]
    if 'injured' in actingTribute['effects']:
        print("finds medical supplies and treats their wounds")
        removeEffect(actingTribute, 'injured')
    else:
        print("finds medical supplies")
        giveItem(actingTribute, 'medical')
        
def event_findItem(current_idx, order, tributes):
    actingTribute = tributes[order[current_idx]]
    prob_dagger = 1.0
    prob_med = 1.0
    prob_fishing = 1.0
    prob_explosive = 1.0
    outcome = pick(['dagger','medical','fishingGear', 'explosive'], [prob_dagger, prob_med, prob_fishing, prob_explosive])
    if outcome == 'dagger':
        print("finds a dagger")
        giveItem(actingTribute, 'dagger')
    if outcome == 'medical':
        print("finds medical supplies")
        giveItem(actingTribute, 'medical')
    if outcome == 'fishingGear':
        print("finds fishing gear")
        giveItem(actingTribute, 'fishingGear')
    if outcome == 'explosive':
        print("finds an explosive device")
        giveItem(actingTribute, 'explosive')
    
def event_findFood(current_idx, order, tributes):
    actingTribute = tributes[order[current_idx]]
    if 'fishingGear' in actingTribute['items']:
        prob_win = 1.0 +\
            (20.0 * actingTribute['stats'][Stats.SRV.value])
        prob_lose = 1.0
        outcome = pick([0,1], [prob_win, prob_lose])
        if outcome == 0:
            print("catches fish to eat")
        if outcome == 1:
            print("is unable to catch fish")
    else:
        prob_win = 1.0 +\
            (20.0 * actingTribute['stats'][Stats.SRV.value])
        prob_lose = 4.0
        outcome = pick([0,1], [prob_win, prob_lose])
        if outcome == 0:
            print("finds berries to eat")
            if 'starving' in actingTribute['effects']:
                removeEffect(actingTribute, 'starving')
            elif 'energized' not in actingTribute['effects']:
                giveEffect(actingTribute, 'energized')
        elif outcome ==1:
            if 'starving' in actingTribute['effects']:
                print("fails to find food, and dies of starvation")
                killTribute(order[current_idx], order, tributes)
            elif 'energized' in actingTribute['effects']:
                print("fails to find food, beginning to feel hungry")
                removeEffect(actingTribute,'energized')
            else:
                print("fails to find food, and begins to starve.")
                giveEffect(actingTribute,'starving')
                
def event_plantMine(current_idx, order, tributes):
    actingTribute = tributes[order[current_idx]]
    arenaStatus['mines'] += 1
    removeItem(actingTribute, 'explosive')
    print(actingTribute['name'], "plants a landmine trap using their explosive")

def event_findMine(current_idx, order, tributes):
    actingTribute = tributes[order[current_idx]]
    prob_win = 1.0

#-- DOUBLE EVENTS --#

def event_romantic(current_idx, order, tributes):
    receivingTribute = tributes[order[current_idx + 1]]
    print("hugs", receivingTribute['name'])

def event_beg(current_idx, order, tributes):
    receivingTribute = tributes[order[current_idx + 1]]
    print("begs", receivingTribute['name'], "for their life")

def event_fistfight(current_idx, order, tributes):
    actingTribute = tributes[order[current_idx]]
    receivingTribute = tributes[order[current_idx + 1]]
    print("attacks", receivingTribute['name'], end = "")
    prob_win = 1.0 * \
        (20.0 * actingTribute['stats'][Stats.STR.value]) * \
        (5.0 if 'dagger' in actingTribute['items'] else 1.0) * \
        (2.0 if 'energized' in actingTribute['effects'] else 1.0) * \
        (0.25 if 'injured' in actingTribute['effects'] else 1.0)
    prob_lose = 1.0 + \
        (20.0 * receivingTribute['stats'][Stats.STR.value]) * \
        (5.0 if 'dagger' in receivingTribute['items'] else 1.0) * \
        (2.0 if 'energized' in receivingTribute['effects'] else 1.0) * \
        (0.25 if 'injured' in receivingTribute['effects'] else 1.0)
    prob_escape = 1.0 + \
        (20.0 * receivingTribute['stats'][Stats.AGI.value]) * \
        (2.0 if 'energized' in receivingTribute['effects'] else 1.0) * \
        (0.1 if 'injured' in receivingTribute['effects'] else 1.0)
    outcome = pick([0,1,2], [prob_win, prob_lose, prob_escape])
    if outcome == 0:
        print(", eliminating them")
        killTribute(order[current_idx + 1], order, tributes)
    elif outcome == 1:
        print(", but is slain")
        killTribute(order[current_idx], order, tributes)
    else:
        prob_healthy = 1.0 + \
            (4.0 * receivingTribute['stats'][Stats.STR.value]) * \
            (4.0 * receivingTribute['stats'][Stats.AGI.value])
        prob_injured = 1.0
        outcome = pick([0,1], [prob_healthy, prob_injured])
        if outcome == 0:
            print(", but they run away")
        if outcome == 1:
            if 'medical' in receivingTribute['items']:
                print(", but they escape, recovering using their medical supplies")
            else:
                print(", but they escape, wounded")
                giveEffect(receivingTribute,'injured')
            

#-- TRIPLE EVENTS --#

def event_forceKill(current_idx, order, tributes):
    receivingTributeOne = tributes[order[current_idx + 1]]
    receivingTributeTwo = tributes[order[current_idx + 2]]
    print("forces", receivingTributeOne['name'], "to kill", receivingTributeTwo['name'])
    killTribute(order[current_idx + 2], order, tributes)

def event_talk(current_idx, order, tributes):
    receivingTributeOne = tributes[order[current_idx + 1]]
    receivingTributeTwo = tributes[order[current_idx + 2]]
    print("talks with", receivingTributeOne['name'], "and", receivingTributeTwo['name'])

#-- QUADRUPLE EVENTS --#

def event_triHuntSuccess(current_idx, order, tributes):
    actingTributes = [tributes[order[current_idx]], tributes[order[current_idx + 1]],
        tributes[order[current_idx + 2]], tributes[order[current_idx + 3]]]
    statList = [actingTributes[0]['stats'][Stats.SRV.value],
        actingTributes[1]['stats'][Stats.SRV.value],
        actingTributes[2]['stats'][Stats.SRV.value]]
    maxValue = sum(statList)
    nameOne = actingTributes[statList.index(max(statList))]['name']
    prob_win = 1.0 +\
        (20.0 * maxValue)
    prob_lose = 1.0 +\
        (20.0 * actingTributes[3]['stats'][Stats.SRV.value])
    outcome = pick([0,1], [prob_win, prob_lose])
    if outcome == 0:
        statList = [actingTributes[0]['stats'][Stats.AGI.value],
        actingTributes[1]['stats'][Stats.AGI.value],
        actingTributes[2]['stats'][Stats.AGI.value]]
        maxValue = max(statList)
        nameTwo = actingTributes[statList.index(max(statList))]['name']
        prob_win = 1.0 +\
            (20.0 * maxValue)
        prob_lose = 1.0 +\
            (20.0 * actingTributes[3]['stats'][Stats.AGI.value])
        outcome = pick([0,1], [prob_win, prob_lose])
        if outcome == 0:
            statList = [actingTributes[0]['stats'][Stats.STR.value],
            actingTributes[1]['stats'][Stats.STR.value],
            actingTributes[2]['stats'][Stats.STR.value]]
            sumValue = sum(statList) * 0.583
            prob_win = 1.0 +\
                (20.0 * sumValue) *\
                (2.0 if 'dagger' in actingTributes[0]['items'] else 1.0) *\
                (2.0 if 'dagger' in actingTributes[1]['items'] else 1.0) *\
                (2.0 if 'dagger' in actingTributes[2]['items'] else 1.0)
            prob_lose = 1.0 +\
                (20.0 * actingTributes[3]['stats'][Stats.STR.value]) *\
                (2.0 if 'dagger' in actingTributes[3]['items'] else 1.0)
            outcome = pick([0,1], [prob_win, prob_lose])
            if outcome == 0:
                print(actingTributes[1]['name'], "and",
                    actingTributes[2]['name'], "spot", actingTributes[3]['name'] + ".", nameOne,
                    "is able to track", ("them and chase them down," if nameOne == nameTwo else "them, " + nameTwo + " chases them down,"), 
                    "and the group eliminates them")
                killTribute(order[current_idx + 3], order, tributes)
            elif outcome == 1:
                print(actingTributes[1]['name'], "and",
                    actingTributes[2]['name'], "spot", actingTributes[3]['name'] + ".", nameOne,
                    "is able to track them,", nameTwo, "chases them down,", 
                    "and a brawl breaks out. ", end = "")
                deadTributeOne = actingTributes[statList.index(min(statList))]
                killTribute(order[current_idx + statList.index(min(statList))], order, tributes)
                statList = [actingTributes[0]['stats'][Stats.STR.value],
                    actingTributes[1]['stats'][Stats.STR.value],
                    actingTributes[2]['stats'][Stats.STR.value]]
                sumValue = (sum(statList) - deadTributeOne['stats'][Stats.STR.value]) * 0.75
                prob_win = 1.0 +\
                    (20.0 * sumValue) *\
                    (2.0 if 'dagger' in actingTributes[0]['items'] else 1.0) *\
                    (2.0 if 'dagger' in actingTributes[1]['items'] else 1.0) *\
                    (2.0 if 'dagger' in actingTributes[2]['items'] else 1.0) /\
                    (2.0 if 'dagger' in deadTributeOne['items'] else 1.0)
                prob_lose = 1.0 +\
                    (20.0 * actingTributes[3]['stats'][Stats.STR.value]) *\
                    (2.0 if 'dagger' in actingTributes[3]['items'] else 1.0)
                outcome = pick([0,1], [prob_win, prob_lose])
                if outcome == 0:
                    print(deadTributeOne['name'], "and", actingTributes[3]['name'], "are eliminated in the fight")
                elif outcome == 1:
                    deadTributeTwo = actingTributes[statList.index(min(statList))]
                    killTribute(order[current_idx + statList.index(min(statList))], order, tributes)
                    prob_win = 1.0 +\
                        (20.0 * actingTributes[0]['stats'][Stats.STR.value]) *\
                        (2.0 if 'dagger' in actingTributes[0]['items'] else 1.0) *\
                        (2.0 if 'dagger' in actingTributes[1]['items'] else 1.0) *\
                        (2.0 if 'dagger' in actingTributes[2]['items'] else 1.0) /\
                        (2.0 if 'dagger' in deadTributeOne['items'] else 1.0) /\
                        (2.0 if 'dagger' in deadTributeTwo['items'] else 1.0)
                    prob_lose = 1.0 +\
                        (20.0 * actingTributes[3]['stats'][Stats.STR.value]) *\
                        (2.0 if 'dagger' in actingTributes[3]['items'] else 1.0)
                    outcome = pick([0,1], [prob_win, prob_lose])
                    if outcome == 0:
                        print(deadTributeOne['name'], deadTributeTwo['name'], "and", actingTribute[1],
                            "are eliminated in the fight")
                        killTribute(order[current_idx + 3], order, tributes)
                    elif outcome == 1:
                        print(deadTributeOne['name'], deadTributeTwo['name'], "and", actingTribute[0]['name'],
                            "are eliminated in the fight")
                        killTribute(order[current_idx + statList.index(max(statList))], order, tributes)
        elif outcome == 1:
            print(actingTributes[1]['name'], "and",
                actingTributes[2]['name'], "spot", actingTributes[3]['name'] + ".", nameOne,
                "is able to track them, but the group is unable to chase them down")
    elif outcome == 1:
        print(actingTributes[1]['name'], "and",
            actingTributes[2]['name'], "spot", actingTributes[3]['name'] + ", but are unable" +\
            " to track them down")

def event_triHuntFail(current_idx, order, tributes):
    receivingTributeOne = tributes[order[current_idx + 1]]
    receivingTributeTwo = tributes[order[current_idx + 2]]
    receivingTributeThree = tributes[order[current_idx + 3]]
    print("fails to hunt with", receivingTributeOne['name'],
        receivingTributeTwo['name'], "and", receivingTributeThree['name'])

#### ITEMS AND EFFECTS ####

def giveItem(tribute, item):
    tribute['items'].append(item)

def giveEffect(tribute, effect):
    tribute['effects'].append(effect)

def removeItem(tribute, item):
    tribute['items'].remove(item)
    
def removeEffect(tribute, effect):
    tribute['effects'].remove(effect)
    
def killTribute(idx_to_remove, order, tributes):
    global tributeCount
    global inc
    tributeCount -= 1
    inc -= 1
    tributes.pop(idx_to_remove)
    order.remove(idx_to_remove)
    for i in range(len(order)):
        if order[i] > idx_to_remove:
            order[i] -= 1

def pick(outcomes, probabilities):
    return random.choices(outcomes, weights=probabilities)[0]
    

# Name, Base, Stat, StatWeightAdditive, DayOneMultiplier

multiEventsList = [
    #one
    [
        ["event_dance", 5.0, Stats.LCK.value, 0, 0.0],
        ["event_hums", 5.0, Stats.LCK.value, 0, 0.0],
        ["event_findItem", 1.0, Stats.INT.value, 3.0, 2.0],
        ["event_findFood", 5.0, Stats.LCK.value, 0.0, 1.0],
        ["event_plantMine", 5.0, Stats.LCK.value, 0.0, 0.0]
    ],
    #two
    [
        ["event_romantic", 3.0, Stats.CHR.value, 3.0, 0.0],
        ["event_beg", 3.0, Stats.INT.value, -3.3, 0.5],
        ["event_fistfight", 3.0, Stats.STR.value, 3.0, 2.0]
    ],
    #three
    [
        ["event_forceKill", 0.0, Stats.STR.value, 5.0, 1.0],
        ["event_talk", 5.0, Stats.CHR.value, 5.0, 0.0]
    ],
    #four
    [
        ["event_triHuntSuccess", 5.0, Stats.INT.value, 5.0, 1.0],
        ["event_triHuntFail", 5.0, Stats.INT.value, -5.0, 1.0]],
    ]
    
def getItemEffect(tribute, event):
    multiplier = 1.0
    eventName = event[0]
    for item in tribute['items']:
        if item in item_categories['melee_weapons']:
            if eventName == 'event_forceKill':
                multiplier += 2.0
            elif eventName == 'event_fistfight':
                multiplier = 2.0
            elif eventName == 'event_findDagger':
                multiplier = 0.0
    for effect in tribute['effects']:
        if effect == 'injured':
            if eventName == 'event_fistfight':
                multiplier = 0.0
        if effect == 'starving':
            if eventName == 'event_findFood':
                multiplier = 3.0
    if eventName == 'event_plantMine':
        if 'explosive' not in tribute['items']:
            multiplier = 0.0
    return multiplier
    
#### ORDER BEGINS ####
    
day = 1
dayCount = 1
while(tributeCount > 1):
    print(" *** DAY", dayCount, "***")
    order = list(range(tributeCount))
    random.shuffle(order)
    
    inc = 0
    while inc < tributeCount:
        currentTribute = tributes[order[inc]]
        
        tributeProbabilities = [
            [ 
                (event[4] ** day) * (event[1] + (currentTribute['stats'][event[2]] * event[3])) * \
                getItemEffect(currentTribute, event) for event in events
            ]
            for events in multiEventsList
        ]
        """for each in range(len(tributeProbabilities)):
            for length in range(len(tributeProbabilities[each])):
                print(tributeProbabilities[each][length])
                print(multiEventsList[each][length][0])"""
        
        turnsRemaining = tributeCount - inc
        print(f"{currentTribute['name']} ", end="")
                
        combinedEvents = []
        for indexNum, events in enumerate(multiEventsList):
            if indexNum < turnsRemaining:
                for event, weight in zip(events, tributeProbabilities[indexNum]):
                    combinedEvents.append((event, weight, indexNum + 1))
                    
        selectedEvent, weight, participants = random.choices(combinedEvents,
            weights=[w for _, w, _ in combinedEvents])[0]
        
        eventFunctionName = selectedEvent[0]
        eventFunction = globals()[eventFunctionName]
        eventFunction(inc, order, tributes)
        
        print()
        inc += participants
    print("---Continue?---")
    #input()
    
    tInc = 0
    for dInc in range(len(displayTributes)):
        print("DISTRICT", displayTributes[dInc]['district'],":", displayTributes[dInc]['name'], "")
        if tInc >= len(tributes) or displayTributes[dInc]['name'] != tributes[tInc]['name']:
            print("xxx ELIMINATED xxx", end = "")
        else:
            print("Items: ", end = "")
            for item in tributes[tInc]['items']:
                print(item.capitalize(), end = " ")
            print("\nStatus: ", end = "")
            for effect in tributes[tInc]['effects']:
                print(effect.capitalize(), end = " ")
            tInc += 1
        print("")
        print("")
    if day == 1:
        day = 0
    dayCount += 1
    print("---Continue?---")
    #input()
print("Ladies and gentlemen, I present to you the winner of this year's Hunger Games,", 
    tributes[0]['name'].upper() + "!")
