import typeManager
import pokemonCard
test = typeManager.TypesManager()
test.downloadTypeData()
pokemon = pokemonCard.Pokemon()
pokemon.type1 = "grass"
print(test.getAttackMultiplier("fire", pokemon))