unequippable_cost = 0.01

skill_point_tags = {
    "rawStrength": 0,
    "rawDexterity": 0,
    "rawIntelligence": 0,
    "rawDefence": 0,
    "rawAgility": 0
}

skill_tags = {
    "strength": 0,
    "dexterity": 0,
    "intelligence": 0,
    "defence": 0,
    "agility": 0
}

skill_point_tags_conversion = {
    "rawStrength": "strength",
    "rawDexterity": "dexterity",
    "rawIntelligence": "intelligence",
    "rawDefence": "defence",
    "rawAgility": "agility"
}

inverse_skill_point_tags_conversion = {
    "strength": "rawStrength",
    "dexterity": "rawDexterity",
    "intelligence": "rawIntelligence",
    "defence": "rawDefence",
    "agility": "rawAgility"
}


percentage_conversion = {
    "healthRegen" : "healthRegenRaw",
    'mainAttackDamage' : 'rawMainAttackDamage',
    'elementalMainAttackDamage' : 'rawElementalMainAttackDamage',
    'elementalDamage' : 'rawElementalDamage',
    'spellDamage' : 'rawSpellDamage',
    'fireDamage': 'rawFireDamage',
    'earthDamage': 'rawEarthDamage',
    'waterDamage': 'rawWaterDamage',
    'airDamage': 'rawAirDamage',
    'thunderDamage': 'rawThunderDamage'
}

inverse_percentage_conversion = {
    "healthRegenRaw" : "healthRegen",
    'rawMainAttackDamage' : 'rawMainAttackDamage',
    'rawElementalMainAttackDamage' : 'elementalMainAttackDamage',
    'rawElementalDamage' : 'elementalDamage',
    'rawSpellDamage' : 'spellDamage',
    'rawFireDamage': 'fireDamage',
    'rawEarthDamage': 'earthDamage',
    'rawWaterDamage': 'waterDamage',
    'rawAirDamage': 'airDamage',
    'rawThunderDamage': 'thunderDamage'
}

build_items = [
    "helmet",
    "chestplate",
    "leggings",
    "boots",
    "ring1",
    "ring2",
    "bracelet",
    "necklace",
    "weapon"
]

conversion = {
    "helmet":"helmets",
    "chestplate":"chestplates",
    "leggings":"leggings",
    "boots":"boots",
    "ring1":"rings",
    "ring2":"rings",
    "bracelet":"bracelets",
    "necklace":"necklaces",
    "weapon":"reliks"
}