def _findflag(line):
    switchflag = line.find("|switch|")
    moveflag = line.find("|move|")
    cantflag = line.find("|cant|") #行動不能
    faintflag = line.find("|faint|")
    damageflag = line.find("|-damage|")
    supereffectiveflag = line.find("|-supereffective|")
    resistedflag = line.find("|-resisted|") #抵抗
    immuneflag = line.find("|-immune|") #免疫
    missflag = line.find("|-miss|")
    failflag = line.find("|-fail|")
    critflag = line.find("|-crit|")
    statusflag = line.find("|-status|")
    curestatusflag = line.find("|-curestatus|")
    healflag = line.find("|-heal|")
    formechange = line.find("|-formechange|") #形態変化
    replaceflag = line.find("|replace|") #ゾロアークがバレる
    detailschangeflag = line.find("|replace|") #コオリッポやミミッキュなどの形態変化
    itemflag = line.find("|-item|") #風船など
    enditemflag = line.find("|-enditem|") #食べ残しなど
    abilityflag = line.find("|-ability|")
    boostflag = line.find("|-boost|")
    unboostflag = line.find("|-unboost|")
    clearboost = line.find("|-clearboost|")
    fieldstartflag = line.find("|-fieldstart|") #フィールド効果発動
    fieldendflag = line.find("|-fieldend|") #フィールド効果消滅
    sidestartflag = line.find("|-sidestart|") #側フィールド効果発動
    sideendflag = line.find("|-sideend") #側フィールド効果消滅
    startflag = line.find("|-start|") #複数ターン効果発動
    endflag = line.find("|-end|") #複数ターン効果消滅
    dragflag = line.find("|drag|") #強制交換
    singleturnflag = line.find("|-singleturn|") #1ターン効果
    activateflag = line.find("|-activate|") #1ターン効果発動
    hitcountflag = line.find("|-hitcountflag|") #1ターンに複数回連続攻撃
    fieldactivateflag = line.find("|-fieldactivate|") #1ターンフィールド効果発動
    prepareflag = line.find("|-prepare|") #ため技
    animflag = line.find("|-anim|") #1ターンに2回行動
    sethpflag = line.find("|-sethp|") #痛み分け
    transformflag = line.find("|-transform|") #変身
    setboostflag = line.find("|-setboost|") #腹太鼓
    singlemoveflag = line.find("|-singlemove|") #怨念・道連れ
    swapboostflag = line.find("|-swapboost|") #パワースワップ
    clearnegativeboostflag = line.find("|-clearnegativeboost|") #しろいハーブ
    mustrechargeflag = line.find("|-mustrecharge|") #次のターン行動できない技
    endabilityflag = line.find("|-endability|") #特性が消失
    blockflag = line.find("|-block|") #アロマベールが発動
    weatherflag = line.find("|-weather|")








