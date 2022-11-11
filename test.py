def _findflag(line):
    p1switchflag = line.find("|switch|p1a: ")
    p2switchflag = line.find("|switch|p2a: ")
    p1moveflag = line.find("|move|p1a: ")
    p2moveflag = line.find("|move|p2a: ")
    p1damageflag = line.find("|-damage|p1a: ")
    p2damageflag = line.find("|-damage|p2a: ")
    p1supereffectiveflag = line.find("|-supereffective|p1a: ")
    p2supereffectiveflag = line.find("|-supereffective|p2a: ")
    p1resistedflag = line.find("|-resisted|p1a: ")
    p2resistedflag = line.find("|-resisted|p2a: ")
    p1healfalg = line.find("|-heal|p1a: ")
    p2healfalg = line.find("|-heal|p2a: ")
    p1enditemfalg = line.find("|-enditem|p1a: ")
    p2enditemfalg = line.find("|-enditem|p2a: ")
    p1unboostfalg = line.find("|-unboost|p1a: ")
    p2unboostfalg = line.find("|-unboost|p2a: ")
    p1sidestartflag = line.find("|-sidestart|p1: ") #フィールド効果発動
    p2sidestartflag = line.find("|-sidestart|p2: ")
    p1sideendflag = line.find("|-sideend|p1: ") #フィールド効果消滅
    p2sideendflag = line.find("|-sideend|p2: ")
    p1startflag = line.find("|-start|p1a: ") #複数ターン効果発動
    p2startflag = line.find("|-start|p2a: ")
    p1endflag = line.find("|-end|p1a: ") #複数ターン効果消滅
    p2endflag = line.find("|-end|p1a: ")
    p1statusflag = line.find("|-status|p1a: ")
    p2statusflag = line.find("|-status|p2a: ")
    p1curestatusflag = line.find("|-curestatus|p1: ")
    p2curestatusflag = line.find("|-curestatus|p2: ")
    p1dragflag = line.find("|drag|p1a: ") #強制交換
    p2dragflag = line.find("|drag|p2a: ")
    p1singleturnflag = line.find("|-singleturn|p1a: ") #1ターン効果
    p2singleturnflag = line.find("|-singleturn|p2a: ")
    p1activateflag = line.find("|-activate|p1a: ") #1ターン効果発動
    p2activateflag = line.find("|-activate|p2a: ")

flags = {'|-start|p2a: ', '|-sidestart|p2: ', '|-sethp|p1a: ', '|-damage|p1a: ', '|-item|p2a: ', '|replace|p1a: ', '|-hitcount|p1: ', '|-hitcount|p2: ', '|-end|p1a: ', '|error|Error: ', '|-prepare|p1a: ', '|-start|p1a: ', '|-unboost|p2a: ', '|cant|p2a: ', '|-singlemove|p1a: ', '|-clearboost|p1a: ', '|-resisted|p1a: ', '|-swapboost|p2a: ', '|-zpower|p1a: ', '|-copyboost|p1a: ', '|-hitcount|p1a: ', '|-fail|p2a: ', '|-end|p2a: ', '|-mega|p2a: ', '|-activate|p1a: ', '|-damage|p2a: ', '|-immune|p2a: ', '|-resisted|p2a: ', '|-curestatus|p1: ', '|detailschange|p1a: ', '|move|p2a: ', '|-crit|p2a: ', '|-singleturn|p2a: ', '|detailschange|p2a: ', '|-curestatus|p1a: ', '|-zbroken|p1a: ', '|-prepare|p2a: ', '|-miss|p1: ', '|-crit|p1a: ', '|-curestatus|p2: ', '|-status|p2a: ', '|-ability|p2a: ', '|-swapboost|p1a: ', '|-setboost|p1a: ', '|-endability|p1a: ', '|-sideend|p2: ', '|faint|p2a: ', '|-sethp|p2a: ', '|move|p1a: ', '|replace|p2a: ', '|-singleturn|p1a: ', '|-clearnegativeboost|p2a: ', '|-transform|p2a: ', '|drag|p1a: ', '|-fieldactivate|move: ', '|-sidestart|p1: ', '|-miss|p1a: ', '|-transform|p1a: ', '|-setboost|p2a: ', '|-mustrecharge|p1a: ', '|-enditem|p2a: ', '|-singlemove|p2a: ', '|-block|p1a: ', '|-enditem|p1a: ', '|-zbroken|p2a: ', '|-unboost|p1a: ', '|drag|p2a: ', '|cant|p1a: ', '|-hitcount|p2a: ', '|-anim|p2a: ', '|-formechange|p2a: ', '|-curestatus|p2a: ', '|-supereffective|p1a: ', '|switch|p2a: ', '|faint|p1a: ', '|-fail|p1a: ', '|-mega|p1a: ', '|-boost|p2a: ', '|-clearboost|p2a: ', '|-supereffective|p2a: ', '|-mustrecharge|p2a: ', '|-status|p1a: ', '|-heal|p2a: ', '|-boost|p1a: ', '|-heal|p1a: ', '|-anim|p1a: ', '|-endability|p2a: ', '|-activate|p2a: ', '|-fieldstart|move: ', '|-fieldend|move: ', '|switch|p1a: ', '|-formechange|p1a: ', '|-sideend|p1: ', '|-clearnegativeboost|p1a: ', '|-ability|p1a: ', '|-item|p1a: ', '|-immune|p1a: ', '|-miss|p2a: '}






