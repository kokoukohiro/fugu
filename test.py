from poke_env.data import GEN_TO_POKEDEX
formes = GEN_TO_POKEDEX[8]["silvally"]["formeOrder"]
a = list(formes)
a.remove("Silvally")
print(a)