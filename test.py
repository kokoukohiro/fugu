import re

def _findflag(line):
    flags = {
        "switch" : r'\|switch\|(?P<p>p1|p2)a: (?P<nickname>[^\|]+)\|(?P<key>[^\|]+)\|(?P<currenthp>\d+)/\d+(?: (?P<status>\w+))?(?:\|\[from\]move: (?P<switchmove>[^\|]+))?',
        "move" : r'\|move\|(?P<p>p1|p2)a: (?P<nickname>[^\|]+)\|(?P<move>[^\|]+)\|(?:(?P<opp>p1|p2)a: (?P<opnickname>[^\|]+))?(?:\|\[(?P<result1>\w+)\](?:(?:(?P<flag>\w+): )?(?P<flagname>[^\|]+)(?:\|\[(?P<result2>\w+)\])?)?)?',
        "cant" : r'\|cant\|(?P<p>p1|p2)a: (?P<nickname>[^\|]+)\|(?:(?P<flag>\w+): )?(?P<flagname>[^\|]+)(?:\|(?P<move>[^\|]+))?',#行動不能
        "faint" : r'\|faint\|(?P<p>p1|p2)a: (?P<nickname>[^\|]+)',
        "drag" : r'\|drag\|(?P<p>p1|p2)a: (?P<nickname>[^\|]+)\|(?P<key>[^\|]+)\|(?P<currenthp>\d+)/\d+(?: (?P<status>\w+))?', #強制交換
        "damage" : r'\|-damage\|(?P<p>p1|p2)a: (?P<nickname>[^\|]+)\|(?P<currenthp>\d+)/\d+(?: (?P<status>\w+))?(?:\|\[from\] (?:(?P<flag>\w+): )?(?P<flagname>[^\|]+))?(?:\|\[of\] (?P<opp>p1|p2)a: (?P<opnickname>[^\|]+))?',
        "supereffective" : r'\|-supereffective\|(?P<p>p1|p2)a: (?P<nickname>[^\|]+)',
        "resisted" : r'\|-resisted\|(?P<p>p1|p2)a: (?P<nickname>[^\|]+)', #抵抗
        "immune" : r'\|-immune\|(?P<p>p1|p2)a: (?P<nickname>[^\|]+)(?:\|\[from\] ability: (?P<ability>[^\|]+))?', #免疫
        "miss" : r'\|-miss\|(?P<p>p1|p2)a?: (?P<nickname>[^\|]+)\|(?P<opp>p1|p2)a?: (?P<opnickname>[^\|]+)',
        "crit" : r'\|-crit\|(?P<p>p1|p2)a: (?P<nickname>[^\|]+)',
        "status" : r'\|-status\|(?P<p>p1|p2)a: (?P<nickname>[^\|]+)\|(?P<status>\w+)(?:\|\[from\] (?P<flag>\w+): (?P<flagname>[^\|]+))?(?:\|\[of\] (?P<opp>p1|p2)a: (?P<opnickname>[^\|]+))?',
        "curestatus" : r'\|-curestatus\|(?P<p>p1|p2)a?: (?P<nickname>[^\|]+)\|(?P<status>\w+)\|(?:\[from\] (?P<flag>\w+): (?P<flagname>[^\|]+))?',
        "heal" : r'\|-heal\|(?P<p>p1|p2)a: (?P<nickname>[^\|]+)\|(?P<currenthp>\d+)/\d+(?: (?P<status>\w+))?(?:\|\[from\] (?:(?P<flag>\w+): )?(?P<flagname>[^\|]+))?(?:\|\[of\] (?P<opp>p1|p2)a: (?P<opnickname>[^\|]+))?(?:\|\[wisher\] (?P<wisher>[^\|]+))?',
        "formechange" : r'\|-formechange\|(?P<p>p1|p2)a: (?P<nickname>[^\|]+)\|(?P<frome>[^\|]+)\|(?:\|\[from\] ability: (?P<ability>[^\|]+))?', #形態変化
        "replace" : r'\|replace\|(?P<p>p1|p2)a: (?P<nickname>[^\|]+)\|(?P<key>[^\|]+)', #ゾロアークがバレる
        "detailschange" : r'\|detailschange\|(?P<p>p1|p2)a: (?P<nickname>[^\|]+)\|(?P<key>[^\|]+)', #コオリッポやミミッキュなどの形態変化
        "item" : r'\|-item\|(?P<p>p1|p2)a: (?P<nickname>[^\|]+)\|(?P<item>[^\|]+)(?:\|\[from\] (?P<flag>\w+): (?P<flagname>[^\|]+))?(?:\|\[of\] (?P<opp>p1|p2)a: (?P<opnickname>[^\|]+))?(?:\|\[identify\])?', #風船など
        "enditem" : r'\|-enditem\|(?P<p>p1|p2)a: (?P<nickname>[^\|]+)\|(?P<item>[^\|]+)(?:\|\[silent\])?(?:\|\[from\] (?:(?P<flag>\w+): )?(?P<flagname>[^\|]+))?(?:\|\[of\] (?P<opp>p1|p2)a: (?P<opnickname>[^\|]+))?(?:\|(?P<afterflag>[^\|]+))?', #食べ残しなど
        "ability" : r'\|-ability\|(?P<p>p1|p2)a: (?P<nickname>[^\|]+)\|(?P<ability>[^\|]+)(?:\|(?:\[from\] (?P<flag>\w+): )?(?P<flagname>[^\|]+))?(?:\|\[of\] (?P<opp>p1|p2)a: (?P<opnickname>[^\|]+))?',
        "boost" : r'\|-boost\|(?P<p>p1|p2)a: (?P<nickname>[^\|]+)\|(?P<stats>[^\|]+)\|(?P<level>\d)(?:\|\[from\] item: (?P<item>[^\|]+))?',
        "unboost" : r'\|-unboost\|(?P<p>p1|p2)a: (?P<nickname>[^\|]+)\|(?P<stats>[^\|]+)\|(?P<level>\d)',
        "clearboost" : r'\|-clearboost\|(?P<p>p1|p2)a: (?P<nickname>[^\|]+)',
        "fieldstart" : r'\|-fieldstart\|move: (?P<move>[^\|]+)(?:\|\[from\] ability: (?P<ability>[^\|]+))?(?:\|\[of\] (?P<opp>p1|p2)a: (?P<opnickname>[^\|]+))?', #フィールド効果発動
        "fieldend" : r'\|-fieldend\|move: (?P<move>[^\|]+)(?:\|\[of\] (?P<opp>p1|p2)a?: (?P<opnickname>[^\|]+))?', #フィールド効果消滅
        "sidestart" : r'\|-sidestart\|(?P<p>p1|p2): (?P<user>[^\|]+)\|(?:move: )?(?P<move>[^\|]+)', #側フィールド効果発動 ここだけP1/P2:の後ろはユーザー名
        "sideend" : r'\|-sideend\|(?P<p>p1|p2): (?P<user>[^\|]+)\|(?:move: )?(?P<field>[^\|]+)(?:\|\[from\] move: (?P<move>[^\|]+))?(?:\|\[of\] (?P<opp>p1|p2)a: (?P<opnickname>[^\|]+))?', #側フィールド効果消滅
        "start" : r'\|-start\|(?P<p>p1|p2)a: (?P<nickname>[^\|]+)\|(?:(?:typechange\|(?P<typechange>[^\|]+))|(?:Disable\|(?P<disabledmove>[^\|]+))|(?:(?:move: )?(?P<effect>[^\|]+)))(?:\|\[from\] (?P<flag>\w+): (?P<flagname>[^\|]+))?(?:\|\[of\] (?P<opp>p1|p2)a: (?P<opnickname>[^\|]+))?', #複数ターン効果発動
        "end" : r'\|-end\|(?P<p>p1|p2)a: (?P<nickname>[^\|]+)\|(?:(?P<flag>\w+): )?(?P<flagname>[^\|]+)(?:\|\[from\] move: (?P<move>[^\|]+))?(?:\|\[of\] (?P<opp>p1|p2)a: (?P<opnickname>[^\|]+))?', #複数ターン効果消滅
        "singleturn" : r'\|-singleturn\|(?P<p>p1|p2)a: (?P<nickname>[^\|]+)\|(?:move: )?(?P<move>[^\|]+)', #1ターン効果
        "activate" : r'\|-activate\|(?P<p>p1|p2)a: (?P<nickname>[^\|]+)\|(?:(?P<flag>\w+): )?(?P<flagname>[^\|]+)(?:\|(?P<effect>[^\|\[\]]+)(?:\|(?P<pluseffect>[^\|]+))?)?(?:\|\[of\] (?P<opp>p1|p2)a: (?P<opnickname>[^\|]+))?(?:\|(?P<afterflag>[^\|]+))?', #1ターン効果発動
        "fail" : r'\|-fail\|(?P<p>p1|p2)a: (?P<nickname>[^\|]+)(?:\|(?:(?P<flag1>\w+): )?(?P<flag1name>[^\|]+)(?:\|(?P<effect>[^\|\[\]]+))?)?(?:\|\[from\] ability: (?P<ability>[^\|]+))?(?:\|\[of\] (?P<opp>p1|p2)a: (?P<opnickname>[^\|]+))?(?:\|(?P<afterflag>[^\|]+))?',
        "hitcount" : r'\|-hitcount\|(?P<p>p1|p2)a?: (?P<nickname>[^\|]+)\|(?P<hitcount>\d+)', #1ターンに複数回連続攻撃
        "fieldactivate" : r'\|-fieldactivate\|move: (?P<move>[^\|]+)', #1ターンフィールド効果発動
        "prepare" : r'\|-prepare\|(?P<p>p1|p2)a: (?P<nickname>[^\|]+)\|(?P<move>[^\|]+)', #ため技
        "anim" : r'\|-anim\|(?P<p>p1|p2)a?: (?P<nickname>[^\|]+)\|(?P<move>[^\|]+)\|(?P<opp>p1|p2)a?: (?P<opnickname>[^\|]+)(?:\|(?P<afterflag>[^\|]+))?', #1ターンに2回行動
        "sethp" : r'\|-sethp\|(?P<p>p1|p2)a: (?P<nickname>[^\|]+)\|(?P<currenthp>\d+)/\d+(?: (?P<status>\w+))?\|\[from\] move: (?P<move>[^\|]+)(?:\|(?P<afterflag>\[silent\]+))?', #痛み分け
        "transform" : r'\|-transform\|(?P<p>p1|p2)a: (?P<nickname>[^\|]+)\|(?P<opp>p1|p2)a: (?P<opnickname>[^\|]+)(?:\|\[from\] ability: (?P<ability>Imposter))?', #変身
        "setboost" : r'\|-setboost\|(?P<p>p1|p2)a: (?P<nickname>[^\|]+)\|(?P<stats>\w+)\|(?P<level>\d)\|\[from\] move: (?P<move>[^\|]+)', #腹太鼓
        "singlemove" : r'\|-singlemove\|(?P<p>p1|p2)a: (?P<nickname>[^\|]+)\|(?P<move>[^\|]+)', #怨念・道連れ
        "swapboost" : r'\|-swapboost\|(?P<p>p1|p2)a: (?P<nickname>[^\|]+)\|(?P<opp>p1|p2)a: (?P<opnickname>[^\|]+)(?:\|(?P<stats>[^\|]+))?\|\[from\] move: (?P<move>[^\|]+)', #パワースワップ
        "clearnegativeboost" : r'\|-clearnegativeboost\|(?P<p>p1|p2)a: (?P<nickname>[^\|]+)', #しろいハーブ
        "mustrecharge" : r'\|-mustrecharge\|(?P<p>p1|p2)a: (?P<nickname>[^\|]+)', #次のターン行動できない技
        "endability" : r'\|-endability\|(?P<p>p1|p2)a: (?P<nickname>[^\|]+)(?:\|(?P<ability>[^\|]+)\|\[from\] move: (?P<move>[^\|]+))?', #特性が消失
        "block" : r'\|-block\|(?P<p>p1|p2)a: (?P<nickname>[^\|]+)\|ability: (?P<ability>[^\|]+)\|\[of\] (?P<opp>p1|p2)a: (?P<opnickname>[^\|]+)', #アロマベールが発動
        "weather" : r'\|-weather\|(?P<weather>[^\|]+)(?:\|\[from\] ability: (?P<ability>[^\|]+)\|\[of\] (?P<opp>p1|p2)a: (?P<opnickname>[^\|]+))?'
    }

    flaglines = line.split('\n')
    for flagline in flaglines:
        for flag in flags:
            if re.match(flag,flagline):
                pass

    

line = """11
|inactive|KM has 270 seconds left.
|
|t:|1667450498
|move|p2a: Celesteela|Protect|p2a: Celesteela
|-singleturn|p2a: Celesteela|Protect
|move|p1a: choice cowboy|Sunny Day|p1a: choice cowboy
|-weather|SunnyDay
|
|-weather|SunnyDay|[upkeep]
|-heal|p2a: Celesteela|99/100|[from] item: Leftovers
|upkeep
"""

_findflag(line)










