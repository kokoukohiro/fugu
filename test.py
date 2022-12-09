import re

def _findflag(line):
    switchflag = re.match(r'\|switch\|(?P<p>p1|p2)a: (?P<nickname>[^\|]+)\|(?P<key>[^\|]+)\|(?P<currenthp>\d+)/\d+(?: (?P<status>\w+))?(?:\|\[from\]move: (?P<switchmove>[^\|]+))?',line)
    moveflag = re.match(r'\|move\|(?P<p>p1|p2)a: (?P<nickname>[^\|]+)\|(?P<move>[^\|]+)\|(?:(?P<opp>p1|p2)a: (?P<opnickname>[^\|]+))?(?:\|\[(?P<result1>\w+)\](?:(?:(?P<flag>\w+): )?(?P<flagname>[^\|]+)(?:\|\[(?P<result2>\w+)\])?)?)?',line)
    cantflag = re.findall(r'\|cant\|(?P<p>p1|p2)a: (?P<nickname>[^\|]+)\|(?:(?P<flag>\w+): )?(?P<flagname>[^\|]+)(?:\|(?P<move>[^\|]+))?',line) #行動不能
    faintflag = re.findall(r'\|faint\|(?P<p>p1|p2)a: (?P<nickname>[^\|]+)',line)
    dragflag = re.findall(r'\|drag\|(?P<p>p1|p2)a: (?P<nickname>[^\|]+)\|(?P<key>[^\|]+)\|(?P<currenthp>\d+)/\d+(?: (?P<status>\w+))?',line) #強制交換
    damageflag = re.findall(r'\|-damage\|(?P<p>p1|p2)a: (?P<nickname>[^\|]+)\|(?P<currenthp>\d+)/\d+(?: (?P<status>\w+))?(?:\|\[from\] (?:(?P<flag>\w+): )?(?P<flagname>[^\|]+))?(?:\|\[of\] (?P<opp>p1|p2)a: (?P<opnickname>[^\|]+))?',line)
    supereffectiveflag = re.findall(r'\|-supereffective\|(?P<p>p1|p2)a: (?P<nickname>[^\|]+)',line)
    resistedflag = re.findall(r'\|-resisted\|(?P<p>p1|p2)a: (?P<nickname>[^\|]+)',line) #抵抗
    immuneflag = re.findall(r'\|-immune\|(?P<p>p1|p2)a: (?P<nickname>[^\|]+)(?:\|\[from\] ability: (?P<ability>[^\|]+))?',line) #免疫
    missflag = re.findall(r'\|-miss\|(?P<p>p1|p2)a?: (?P<nickname>[^\|]+)\|(?P<opp>p1|p2)a?: (?P<opnickname>[^\|]+)',line)
    critflag = re.findall(r'\|-crit\|(?P<p>p1|p2)a: (?P<nickname>[^\|]+)',line)
    statusflag = re.findall(r'\|-status\|(?P<p>p1|p2)a: (?P<nickname>[^\|]+)\|(?P<status>\w+)(?:\|\[from\] (?P<flag>\w+): (?P<flagname>[^\|]+))?(?:\|\[of\] (?P<opp>p1|p2)a: (?P<opnickname>[^\|]+))?',line)
    curestatusflag = re.findall(r'\|-curestatus\|(?P<p>p1|p2)a?: (?P<nickname>[^\|]+)\|(?P<status>\w+)\|(?:\[from\] (?P<flag>\w+): (?P<flagname>[^\|]+))?',line)
    healflag = re.findall(r'\|-heal\|(?P<p>p1|p2)a: (?P<nickname>[^\|]+)\|(?P<currenthp>\d+)/\d+(?: (?P<status>\w+))?(?:\|\[from\] (?:(?P<flag>\w+): )?(?P<flagname>[^\|]+))?(?:\|\[of\] (?P<opp>p1|p2)a: (?P<opnickname>[^\|]+))?(?:\|\[wisher\] (?P<wisher>[^\|]+))?',line)
    formechangeflag = re.findall(r'\|-formechange\|(?P<p>p1|p2)a: (?P<nickname>[^\|]+)\|(?P<frome>[^\|]+)\|(?:\|\[from\] ability: (?P<ability>[^\|]+))?',line) #形態変化
    replaceflag = re.findall(r'\|replace\|(?P<p>p1|p2)a: (?P<nickname>[^\|]+)\|(?P<key>[^\|]+)',line) #ゾロアークがバレる
    detailschangeflag = re.findall(r'\|detailschange\|(?P<p>p1|p2)a: (?P<nickname>[^\|]+)\|(?P<key>[^\|]+)',line) #コオリッポやミミッキュなどの形態変化
    itemflag = re.findall(r'\|-item\|(?P<p>p1|p2)a: (?P<nickname>[^\|]+)\|(?P<item>[^\|]+)(?:\|\[from\] (?P<flag>\w+): (?P<flagname>[^\|]+))?(?:\|\[of\] (?P<opp>p1|p2)a: (?P<opnickname>[^\|]+))?(?:\|\[identify\])?',line) #風船など
    enditemflag = re.findall(r'\|-enditem\|(?P<p>p1|p2)a: (?P<nickname>[^\|]+)\|(?P<item>[^\|]+)(?:\|\[silent\])?(?:\|\[from\] (?:(?P<flag>\w+): )?(?P<flagname>[^\|]+))?(?:\|\[of\] (?P<opp>p1|p2)a: (?P<opnickname>[^\|]+))?(?:\|(?P<afterflag>[^\|]+))?',line) #食べ残しなど
    abilityflag = re.findall(r'\|-ability\|(?P<p>p1|p2)a: (?P<nickname>[^\|]+)\|(?P<ability>[^\|]+)(?:\|(?:\[from\] (?P<flag>\w+): )?(?P<flagname>[^\|]+))?(?:\|\[of\] (?P<opp>p1|p2)a: (?P<opnickname>[^\|]+))?',line)
    boostflag = re.findall(r'\|-boost\|(?P<p>p1|p2)a: (?P<nickname>[^\|]+)\|(?P<stats>[^\|]+)\|(?P<level>\d)(?:\|\[from\] item: (?P<item>[^\|]+))?',line)
    unboostflag = re.findall(r'\|-unboost\|(?P<p>p1|p2)a: (?P<nickname>[^\|]+)\|(?P<stats>[^\|]+)\|(?P<level>\d)',line)
    clearboostflag = re.findall(r'\|-clearboost\|(?P<p>p1|p2)a: (?P<nickname>[^\|]+)',line)
    fieldstartflag = re.findall(r'\|-fieldstart\|move: (?P<move>[^\|]+)(?:\|\[from\] ability: (?P<ability>[^\|]+))?(?:\|\[of\] (?P<opp>p1|p2)a: (?P<opnickname>[^\|]+))?',line) #フィールド効果発動
    fieldendflag = re.findall(r'\|-fieldend\|move: (?P<move>[^\|]+)(?:\|\[of\] (?P<opp>p1|p2)a?: (?P<opnickname>[^\|]+))?',line) #フィールド効果消滅
    sidestartflag = re.findall(r'\|-sidestart\|(?P<p>p1|p2): (?P<user>[^\|]+)\|(?:move: )?(?P<move>[^\|]+)',line) #側フィールド効果発動 ここだけP1/P2:の後ろはユーザー名
    sideendflag = re.findall(r'\|-sideend\|(?P<p>p1|p2): (?P<user>[^\|]+)\|(?:move: )?(?P<field>[^\|]+)(?:\|\[from\] move: (?P<move>[^\|]+))?(?:\|\[of\] (?P<opp>p1|p2)a: (?P<opnickname>[^\|]+))?',line) #側フィールド効果消滅
    startflag = re.findall(r'\|-start\|(?P<p>p1|p2)a: (?P<nickname>[^\|]+)\|(?:(?:typechange\|(?P<typechange>[^\|]+))|(?:Disable\|(?P<disabledmove>[^\|]+))|(?:(?:move: )?(?P<effect>[^\|]+)))(?:\|\[from\] (?P<flag>\w+): (?P<flagname>[^\|]+))?(?:\|\[of\] (?P<opp>p1|p2)a: (?P<opnickname>[^\|]+))?',line) #複数ターン効果発動
    endflag = re.findall(r'\|-end\|(?P<p>p1|p2)a: (?P<nickname>[^\|]+)\|(?:(?P<flag>\w+): )?(?P<flagname>[^\|]+)(?:\|\[from\] move: (?P<move>[^\|]+))?(?:\|\[of\] (?P<opp>p1|p2)a: (?P<opnickname>[^\|]+))?',line) #複数ターン効果消滅
    singleturnflag = re.findall(r'\|-singleturn\|(?P<p>p1|p2)a: (?P<nickname>[^\|]+)\|(?:move: )?(?P<move>[^\|]+)',line) #1ターン効果
    activateflag = re.findall(r'\|-activate\|(?P<p>p1|p2)a: (?P<nickname>[^\|]+)\|(?:(?P<flag>\w+): )?(?P<flagname>[^\|]+)(?:\|(?P<effect>[^\|\[\]]+)(?:\|(?P<pluseffect>[^\|]+))?)?(?:\|\[of\] (?P<opp>p1|p2)a: (?P<opnickname>[^\|]+))?(?:\|(?P<afterflag>[^\|]+))?',line) #1ターン効果発動
    failflag = re.findall(r'\|-fail\|(?P<p>p1|p2)a: (?P<nickname>[^\|]+)(?:\|(?:(?P<flag1>\w+): )?(?P<flag1name>[^\|]+)(?:\|(?P<effect>[^\|\[\]]+))?)?(?:\|\[from\] ability: (?P<ability>[^\|]+))?(?:\|\[of\] (?P<opp>p1|p2)a: (?P<opnickname>[^\|]+))?(?:\|(?P<afterflag>[^\|]+))?',line)
    hitcountflag = re.findall(r'\|-hitcount\|(?P<p>p1|p2)a?: (?P<nickname>[^\|]+)\|(?P<hitcount>\d+)',line) #1ターンに複数回連続攻撃
    fieldactivateflag = re.findall(r'\|-fieldactivate\|move: (?P<move>[^\|]+)',line) #1ターンフィールド効果発動
    prepareflag = re.findall(r'\|-prepare\|(?P<p>p1|p2)a: (?P<nickname>[^\|]+)\|(?P<move>[^\|]+)',line) #ため技
    animflag = re.findall(r'\|-anim\|(?P<p>p1|p2)a?: (?P<nickname>[^\|]+)\|(?P<move>[^\|]+)\|(?P<opp>p1|p2)a?: (?P<opnickname>[^\|]+)(?:\|(?P<afterflag>[^\|]+))?',line) #1ターンに2回行動
    sethpflag = re.findall(r'\|-sethp\|(?P<p>p1|p2)a: (?P<nickname>[^\|]+)\|(?P<currenthp>\d+)/\d+(?: (?P<status>\w+))?\|\[from\] move: (?P<move>[^\|]+)(?:\|(?P<afterflag>\[silent\]+))?',line) #痛み分け
    transformflag = re.findall(r'\|-transform\|(?P<p>p1|p2)a: (?P<nickname>[^\|]+)\|(?P<opp>p1|p2)a: (?P<opnickname>[^\|]+)(?:\|\[from\] ability: (?P<ability>Imposter))?',line) #変身
    setboostflag = re.findall(r'\|-setboost\|(?P<p>p1|p2)a: (?P<nickname>[^\|]+)\|(?P<stats>\w+)\|(?P<level>\d)\|\[from\] move: (?P<move>[^\|]+)',line) #腹太鼓
    singlemoveflag = re.findall(r'\|-singlemove\|(?P<p>p1|p2)a: (?P<nickname>[^\|]+)\|(?P<move>[^\|]+)',line) #怨念・道連れ
    swapboostflag = re.findall(r'\|-swapboost\|(?P<p>p1|p2)a: (?P<nickname>[^\|]+)\|(?P<opp>p1|p2)a: (?P<opnickname>[^\|]+)(?:\|(?P<stats>[^\|]+))?\|\[from\] move: (?P<move>[^\|]+)',line) #パワースワップ
    clearnegativeboostflag = re.findall(r'\|-clearnegativeboost\|(?P<p>p1|p2)a: (?P<nickname>[^\|]+)',line) #しろいハーブ
    mustrechargeflag = re.findall(r'\|-mustrecharge\|(?P<p>p1|p2)a: (?P<nickname>[^\|]+)',line) #次のターン行動できない技
    endabilityflag = re.findall(r'\|-endability\|(?P<p>p1|p2)a: (?P<nickname>[^\|]+)(?:\|(?P<ability>[^\|]+)\|\[from\] move: (?P<move>[^\|]+))?',line) #特性が消失
    blockflag = re.findall(r'\|-block\|(?P<p>p1|p2)a: (?P<nickname>[^\|]+)\|ability: (?P<ability>[^\|]+)\|\[of\] (?P<opp>p1|p2)a: (?P<opnickname>[^\|]+)',line) #アロマベールが発動
    weatherflag = re.findall(r'\|-weather\|(?P<weather>[^\|]+)(?:\|\[from\] ability: (?P<ability>[^\|]+)\|\[of\] (?P<opp>p1|p2)a: (?P<opnickname>[^\|]+))?',line)

    for flag in weatherflag:
        print(flag)

line = """|-weather|SunnyDay
"""

_findflag(line)










