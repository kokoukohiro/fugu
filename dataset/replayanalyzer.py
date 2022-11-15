import re,urllib,datetime,os,orjson,json
import urllib.request as ur

from decimal import Decimal
from urllib.error import HTTPError
from poke_env.data import GEN_TO_POKEDEX,NATURES

UNKNOW_FORME = {"Arceus","Genesect","Pumpkaboo","Gourgeist","Silvally","Zacian","Zamazenta","Urshifu"}

def analyze(replay,statsdict,format='gen8ou'):
    directory = os.path.join(os.path.dirname(os.path.realpath(__file__)), "replays", format)
    path = os.path.join(directory, replay[1:]+".txt")

    fromp1 = {}
    fromp2 = {}

    """fromp1["start"] = {
        "x":{
            "team":{},
            "opponent_team":{}
        },
        "t":None
    }
    fromp2["start"] = {
        "x":{
            "team":{},
            "opponent_team":{}
        },
        "t":None
    }"""

    if not os.path.exists(path):
        replayurl = 'https://replay.pokemonshowdown.com{replay}.log'
        replayline = _getinfo(replayurl.format(replay=replay))

        if not os.path.exists(directory):
            os.makedirs(directory)
        with open(path,"w",encoding='UTF-8') as f:
            f.write(replayline)
    else:
        with open(path,encoding='UTF-8') as f:
            replayline = f.read()

    replaylines = replayline.split('\n|poke|')
    if replaylines[0].find("|rated|Tournament battle") >= 0 or replaylines[0].find("|rule|Dynamax Clause: You cannot dynamax") < 0 or replaylines[-1].find("|Metronome|") >= 0:
        return
    replaylines[-1] = replaylines[-1].split('\n')[0]
    pokes = replaylines[1:]

    #p1teamfromp2 = _analyzedel(pokes[:6],statsdict)
    #p2teamfromp1 = _analyzedel(pokes[6:],statsdict)

    replaylines = replayline.split('\n|turn|')
    if len(replaylines) <= 1:
        return
    start = replaylines[0].split('\n|start\n')[1]
    replaylines[-1] = replaylines[-1].split('\n|win|')[0]
    turns = replaylines[1:]

    #fromp2["start"]["x"]["opponent_team"] = p1teamfromp2
    #fromp1["start"]["x"]["opponent_team"] = p2teamfromp1

    flags = {}
    for line in [start]+turns:
        flag = re.findall(r'\n(\|-?\w+\|)',line)
        for f in flag:
            if f not in flags:
                flags[f] = set()
            flags[f].add(replay)
    
    return flags


def _analyzedel(pokes,statsdict):
    team = {}
    for poke in pokes:
        pokelines = poke.split(', ')
        if len(pokelines) > 1:
            name = pokelines[0][3:]
            team[name] = {
                "gender":pokelines[1][:1]
            }
        else:
            name = pokelines[0][3:-1]
            team[name] = {
                "gender":None
            }
        temp = "".join(filter(str.isalnum, name))
        if temp in UNKNOW_FORME:
            formes = GEN_TO_POKEDEX[8][temp.lower()]["formeOrder"]
            formesreal = formes.copy()
            formecount = 0
            for forme in formes:
                team[forme] = {
                    "gender":team[name]["gender"]
                }
                try:
                    team[forme] |= statsdict[forme]
                    formecount += team[forme]["Raw count"]
                except:
                    del team[forme]
                    formesreal.remove(forme)
            del team[name]
            if len(formesreal) > 1:
                for forme in formesreal:
                    team[forme]["Forme weight"] = team[forme]["Raw count"]/formecount
                    del team[forme]["Raw count"]
            else:
                del team[formesreal[0]]["Raw count"]
        else:
            team[name] |= statsdict[name]
            del team[name]["Raw count"]
        
    return team

def getreplays(format='gen8ou',refresh=False):
    directory = os.path.join(os.path.dirname(os.path.realpath(__file__)), "replays")
    path = os.path.join(directory, format+".txt")

    if refresh or not os.path.exists(path):
        playerlist = []
        replaylist = set()

        ladderurl = 'https://pokemonshowdown.com/ladder/{format}'
        replayurl1 = 'https://replay.pokemonshowdown.com/search?user={user}'
        replayurl2 = 'https://replay.pokemonshowdown.com/search?format={format}&rating'

        print("Searching for replays of " + format + " ...")

        ladderline = _getinfo(ladderurl.format(format=format))
        playerlist = re.findall(r'<td align="right">\d+</td><td><a data-target="push" class="subtle" href="/users/[\w\d]+">(.+)</a></td><td style="text-align:center"><strong>\d+</strong></td>',ladderline)

        for player in playerlist:
            user = urllib.parse.quote(player)
            replayline = _getinfo(replayurl1.format(user=user))
            replayresultspread = re.findall(r'<li><a href="(.+)" data-target="push"><small>\['+format+']<br /></small> <strong>.+</strong> vs. <strong>.+</strong></a></li>',replayline)
            replaylist |= set(replayresultspread)
        
        replayline = _getinfo(replayurl2.format(format=format))
        replayresultspread = re.findall(r'<li><a href="(.+)" data-target="push"><small>\['+format+'] rating: \d+<br /></small> <strong>.+</strong> vs. <strong>.+</strong></a></li>',replayline)
        replaylist |= set(replayresultspread)

        print("Found "+str(len(replaylist))+" replays.")

        if not os.path.exists(directory):
            os.makedirs(directory)
        with open(path,"w") as f:
            f.write("\n".join(replaylist))
        return list(replaylist)

    else:
        with open(path) as f:
            replaylist = f.read().splitlines()
        return replaylist


def getstats(format='gen8ou',forbattle=True):
    _POKEUSAGE_DICT = {}

    today = datetime.date.today()
    _url = 'https://www.smogon.com/stats/{month}/moveset/{format}-0.txt'
    try:
        month = str(today)[:7]
        url = _url.format(month=month,format=format)
        f = ur.urlopen(url)
    except HTTPError:
        thismonth = datetime.datetime(today.year, today.month, 1)
        lastmonth = thismonth + datetime.timedelta(days=-1)
        month = str(lastmonth)[:7]
        url = _url.format(month=month,format=format)
        f = ur.urlopen(url)
    
    directory = os.path.join(os.path.dirname(os.path.realpath(__file__)), "stats", month)
    path = os.path.join(directory, format+".json")

    if os.path.exists(path):
        f.close()
        print('Importing usagedata from : '+path)
        with open(path) as usagepath:
            _POKEUSAGE_DICT = orjson.loads(usagepath.read())
    else:
        print('Importing usagedata from : '+url)
        lines = f.readlines()
        f.close()
        if not os.path.exists(directory):
            os.makedirs(directory)

        _NAME = None
        _RAW_COUNT = None
        _AVG_WEIGHT = None
        _VIABILITY_CEILING = None
        _ABULITIES = {}
        _ITEMS = {}
        _SpreadPREADS = {}
        _MOVES = {}
        _TEAMMATES = {}
        _CHECKS_AND_COUNTERS = {}

        index = 0
        readabilities = False
        readitems = False
        readspreads = False
        readmoves = False
        readteammates = False
        readchecksandcounters = False
        checksandcounterdata1 = None
        checksandcounterdata2 = None

        for line in lines:
            dealline = line.decode().strip()
            isbar = re.match(r'\+(\-+)\+',dealline)
            iswords = re.match(r'\|\s(\S.*\S)(\s+)\|',dealline)
            isabilities = re.match(r'\|\sAbilities(\s+)\|',dealline)
            isitems = re.match(r'\|\sItems(\s+)\|',dealline)
            isspreads = re.match(r'\|\sSpreads(\s+)\|',dealline)
            ismoves = re.match(r'\|\sMoves(\s+)\|',dealline)
            isteammates = re.match(r'\|\sTeammates(\s+)\|',dealline)
            ischecksandcounters = re.match(r'\|\sChecks\sand\sCounters(\s+)\|',dealline)
            israwcount = re.match(r'\|\sRaw count:\s(\d+)(\s+)\|',dealline)
            isavgweight = re.match(r'\|\sAvg. weight:\s([\d\.\-]+)(\s+)\|',dealline)
            isviabilityceiling = re.match(r'\|\sViability Ceiling:\s(\d+)(\s+)\|',dealline)
            isusagedata = re.match(r'\|\s(\S.*\S)\s(\s?)([\d\.]+)%(\s+)\|',dealline)
            isother = re.match(r'\|\sOther\s(\s?)([\d\.]+)%(\s+)\|',dealline)
            isspreaddata = re.match(r'\|\s((\w+):(\d[\d/]+\d))\s(\s?)([\d\.]+)%(\s+)\|',dealline)
            ischecksandcounterdata1 = re.match(r'\|\s(\S.*\S)\s([\d\.]+)\s\([\d\.±]+\)(\s+)\|',dealline)
            ischecksandcounterdata2 = re.match(r'\|(\s+)\(([\d\.]+)%\sKOed\s/\s(\s?)([\d\.]+)%\sswitched\sout\)(\s*)\|',dealline)

            if index == 1 and iswords:
                _NAME = iswords.group(1)
            if index == 3 and israwcount:
                _RAW_COUNT = int(israwcount.group(1))
            if index == 4 and isavgweight:
                try:
                    _AVG_WEIGHT = float(isavgweight.group(1))
                except:
                    _AVG_WEIGHT = isavgweight.group(1)
            if index == 5 and isviabilityceiling:
                _VIABILITY_CEILING = int(isviabilityceiling.group(1))
            if index == 7 and isabilities:
                readabilities = True
            if index > 7:
                if readabilities:
                    if isusagedata:
                        _ABULITIES[isusagedata.group(1)] = float(Decimal(isusagedata.group(3))/100)
                    if isbar:
                        readabilities = False
                if isitems:
                    readitems = True
                if readitems:
                    if isother:
                        continue
                    if isusagedata:
                        _ITEMS[isusagedata.group(1)] = float(Decimal(isusagedata.group(3))/100)
                    if isbar:
                        readitems = False
                if isspreads:
                    readspreads = True
                if readspreads:
                    if isother:
                        continue
                    if isspreaddata: 
                        _SpreadPREADS[isspreaddata.group(1)] = float(Decimal(isspreaddata.group(5))/100)   
                    if isbar:
                        readspreads = False
                if ismoves:
                    readmoves = True
                if readmoves:
                    if isother:
                        continue
                    if isusagedata:
                        _MOVES[isusagedata.group(1)] = float(Decimal(isusagedata.group(3))/100)
                    if isbar:
                        readmoves = False
                if isteammates:
                    readteammates = True
                if readteammates:
                    if isusagedata:
                        _TEAMMATES[isusagedata.group(1)] = float(Decimal(isusagedata.group(3))/100)
                    if isbar:
                        readteammates = False
                if ischecksandcounters:
                    readchecksandcounters = True
                if readchecksandcounters:
                    if ischecksandcounterdata1:
                        checksandcounterdata1 = ischecksandcounterdata1.group(1)
                        checksandcounterdata2 = float(ischecksandcounterdata1.group(2))
                    if ischecksandcounterdata2:
                        _CHECKS_AND_COUNTERS[checksandcounterdata1] = {
                            'Weight':checksandcounterdata2,
                            'KOed':float(Decimal(ischecksandcounterdata2.group(2))/100),
                            'Switched out':float(Decimal(ischecksandcounterdata2.group(4))/100)
                        }
                    if isbar:
                        readchecksandcounters = False
                        checksandcounterdata1 = None
                        checksandcounterdata2 = None
                        index = -1
                        _POKEUSAGE_DICT[_NAME] = {
                            'Raw count':_RAW_COUNT,
                            'Avg. weight':_AVG_WEIGHT,
                            'Viability Ceiling':_VIABILITY_CEILING,
                            'Abilities':_ABULITIES,
                            'Items':_ITEMS,
                            'Spreads':_SpreadPREADS,
                            'Moves':_MOVES,
                            'Teammates':_TEAMMATES,
                            'Checks and Counters':_CHECKS_AND_COUNTERS
                        }
                        _NAME = None
                        _RAW_COUNT = None
                        _AVG_WEIGHT = None
                        _VIABILITY_CEILING = None
                        _ABULITIES = {}
                        _ITEMS = {}
                        _SpreadPREADS = {}
                        _MOVES = {}
                        _TEAMMATES = {}
                        _CHECKS_AND_COUNTERS = {}
            index += 1

        with open(path,"w") as f:
            json.dump(_POKEUSAGE_DICT,f,indent=1)
    
    if forbattle:
        for pokeusage in _POKEUSAGE_DICT:
            del _POKEUSAGE_DICT[pokeusage]["Avg. weight"]
            del _POKEUSAGE_DICT[pokeusage]["Viability Ceiling"]
            del _POKEUSAGE_DICT[pokeusage]["Teammates"]
            del _POKEUSAGE_DICT[pokeusage]["Checks and Counters"]
            spreads = list(_POKEUSAGE_DICT[pokeusage]["Spreads"].keys())
            spreadscalculations = []
            for spread in spreads:
                spreadlines = spread.split(':')
                spreadscalculations.append(spreadscalculation(pokeusage,spreadlines[0],spreadlines[1]))

            resultspread = {"hp": 0, "atk": 0, "def": 0, "spa": 0, "spd": 0, "spe": 0}

            for _spread in spreadscalculations:
                if resultspread["hp"] < _spread["hp"]:
                    resultspread["hp"] = _spread["hp"]
                if resultspread["atk"] < _spread["atk"]:
                    resultspread["atk"] = _spread["atk"]
                if resultspread["def"] < _spread["def"]:
                    resultspread["def"] = _spread["def"]
                if resultspread["spa"] < _spread["spa"]:
                    resultspread["spa"] = _spread["spa"]
                if resultspread["spd"] < _spread["spd"]:
                    resultspread["spd"] = _spread["spd"]
                if resultspread["spe"] < _spread["spe"]:
                    resultspread["spe"] = _spread["spe"]
            
            _POKEUSAGE_DICT[pokeusage]["Spreads"] = resultspread

    return _POKEUSAGE_DICT

def spreadscalculation(name,nature,evs,lv=100):
    _POKEDEX_DICT = GEN_TO_POKEDEX[8]
    name = "".join(filter(str.isalnum, name)).lower()
    nature = NATURES[nature.lower()]
    evs = list(map(int, evs.split('/')))
    resultspread = {"hp": 0, "atk": 0, "def": 0, "spa": 0, "spd": 0, "spe": 0}
    bases = _POKEDEX_DICT[name]["baseStats"]
    if name != "shedinja":
        resultspread["hp"] = int((bases["hp"]*2+31+evs[0]/4)*lv/100+10+lv)
    else:resultspread["hp"] = 1
    _bases = ["atk", "def", "spa", "spd", "spe"]
    for i in range(len(_bases)):
        base = _bases[i]
        resultspread[base] = int(((bases[base]*2+31+evs[i+1]/4)*lv/100+5)*nature[base])
    return resultspread    
    
def _getinfo(url):
    req = ur.Request(url,headers={'User-Agent': 'Mozilla/5.0'})
    with ur.urlopen(req) as f:
        lines = f.read().decode('utf-8')
    return lines

def main():
    """statsdict = getstats()
    analyze("/gen8ou-1646107486",statsdict)"""

    flags = {}
    path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "flags.json")
    
    if os.path.exists(path):
        with open(path) as f:
            flags = orjson.loads(f.read())
        
        for f in flags:
            flags[f] = set(flags[f])


    replays = getreplays("gen8ru")
    for replay in replays:
        result = analyze(replay,None,"gen8ru")
        if result is not None:
            if len(flags) >= 1:
                for flag in result:
                    if flag in flags:
                        if len(flags[flag]) <=3:
                            flags[flag] |= result[flag]
                    else:
                        flags[flag] = result[flag]
            else:
                flags = result
    
    for f in flags:
        flags[f] = list(flags[f])
    
    with open(path,"w") as f:
        json.dump(flags,f,indent=1)    
    






if __name__ == '__main__':
    main()