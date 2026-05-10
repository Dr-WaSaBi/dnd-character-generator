"""
D&D 5e SRD feature data for auto-populating the Features & Traits editor.

CLASS_FEATURES:  class name -> list of (min_level, feature_name, description)
RACE_TRAITS:     race name  -> list of (trait_name, description)
BACKGROUND_FEATURES: background -> (feature_name, description)
"""

# ---------------------------------------------------------------------------
# CLASS FEATURES
# ---------------------------------------------------------------------------

CLASS_FEATURES: dict[str, list[tuple[int, str, str]]] = {

    "Barbarian": [
        (1,  "Rage",
             "You can enter a rage as a bonus action, gaining advantage on STR checks and saves, "
             "a damage bonus on melee attacks, and resistance to bludgeoning, piercing, and slashing damage."),
        (1,  "Unarmored Defense",
             "While not wearing armor your AC equals 10 + your DEX modifier + your CON modifier."),
        (2,  "Reckless Attack",
             "When you make your first attack on your turn you can choose to attack recklessly, "
             "gaining advantage on all melee weapon attacks this turn but granting enemies advantage on attack rolls against you."),
        (2,  "Danger Sense",
             "You have advantage on DEX saving throws against effects you can see, "
             "provided you are not blinded, deafened, or incapacitated."),
        (3,  "Primal Path",
             "You choose a subclass (Berserker, Totem Warrior, etc.) that shapes the nature of your rage "
             "and grants bonus features at 3rd, 6th, 10th, and 14th levels."),
        (4,  "Ability Score Improvement",
             "Increase one ability score by 2, or two ability scores by 1 each (to a maximum of 20)."),
        (5,  "Extra Attack",
             "You can attack twice instead of once whenever you take the Attack action on your turn."),
        (5,  "Fast Movement",
             "Your speed increases by 10 feet while you are not wearing heavy armor."),
        (6,  "Path Feature",
             "You gain a feature granted by your Primal Path subclass."),
        (7,  "Feral Instinct",
             "Your instincts are so honed that you have advantage on initiative rolls. "
             "If you are surprised, you can still act on your first turn if you enter your rage before doing anything else."),
        (8,  "Ability Score Improvement",
             "Increase one ability score by 2, or two ability scores by 1 each (to a maximum of 20)."),
        (9,  "Brutal Critical (1 die)",
             "You can roll one additional weapon damage die when determining the extra damage for a critical hit."),
        (10, "Path Feature",
             "You gain a feature granted by your Primal Path subclass."),
        (11, "Relentless Rage",
             "When you drop to 0 HP while raging and don't die, you can make a DC 10 CON save to drop to 1 HP instead; "
             "the DC increases by 5 each time until you finish a short or long rest."),
        (12, "Ability Score Improvement",
             "Increase one ability score by 2, or two ability scores by 1 each (to a maximum of 20)."),
        (13, "Brutal Critical (2 dice)",
             "You can roll two additional weapon damage dice when determining the extra damage for a critical hit."),
        (14, "Path Feature",
             "You gain a feature granted by your Primal Path subclass."),
        (15, "Persistent Rage",
             "Your rage is so fierce that it ends only if you fall unconscious or choose to end it."),
        (16, "Ability Score Improvement",
             "Increase one ability score by 2, or two ability scores by 1 each (to a maximum of 20)."),
        (17, "Brutal Critical (3 dice)",
             "You can roll three additional weapon damage dice when determining the extra damage for a critical hit."),
        (18, "Indomitable Might",
             "If your total for a STR check is less than your STR score, you can use that score in place of the total."),
        (19, "Ability Score Improvement",
             "Increase one ability score by 2, or two ability scores by 1 each (to a maximum of 20)."),
        (20, "Primal Champion",
             "Your STR and CON scores each increase by 4, and their maximums each increase to 24."),
    ],

    "Bard": [
        (1,  "Spellcasting",
             "You cast bard spells using CHA as your spellcasting ability, using your spellbook of known spells "
             "and a number of spell slots determined by your level."),
        (1,  "Bardic Inspiration (d6)",
             "As a bonus action you grant one creature within 60 feet a Bardic Inspiration die (d6) they can add to "
             "one ability check, attack roll, or saving throw within 10 minutes."),
        (2,  "Jack of All Trades",
             "You can add half your proficiency bonus (rounded down) to any ability check you make "
             "that doesn't already include your proficiency bonus."),
        (2,  "Song of Rest (d6)",
             "If you or friendly creatures who can hear you spend Hit Dice during a short rest, "
             "each regains 1d6 extra hit points."),
        (3,  "Expertise",
             "Choose two of your skill proficiencies; your proficiency bonus is doubled for any ability check "
             "you make that uses either of those proficiencies."),
        (3,  "Bard College",
             "You delve into one of the advanced techniques of a bard college, gaining subclass features "
             "at 3rd, 6th, and 14th levels."),
        (4,  "Ability Score Improvement",
             "Increase one ability score by 2, or two ability scores by 1 each (to a maximum of 20)."),
        (5,  "Bardic Inspiration (d8)",
             "Your Bardic Inspiration die improves to a d8."),
        (5,  "Font of Inspiration",
             "You regain all expended uses of Bardic Inspiration when you finish a short or long rest."),
        (6,  "Countercharm",
             "As an action you can start a performance that lasts until the end of your next turn, "
             "granting friendly creatures within 30 feet advantage on saving throws against being frightened or charmed."),
        (6,  "Bard College Feature",
             "You gain a feature from your Bard College subclass."),
        (8,  "Ability Score Improvement",
             "Increase one ability score by 2, or two ability scores by 1 each (to a maximum of 20)."),
        (9,  "Song of Rest (d8)",
             "The extra hit points regained during a short rest from Song of Rest increase to 1d8."),
        (10, "Bardic Inspiration (d10)",
             "Your Bardic Inspiration die improves to a d10."),
        (10, "Expertise",
             "Choose two more of your skill proficiencies to double your proficiency bonus for."),
        (10, "Magical Secrets",
             "Choose two spells from any class spell list; these spells count as bard spells for you."),
        (12, "Ability Score Improvement",
             "Increase one ability score by 2, or two ability scores by 1 each (to a maximum of 20)."),
        (13, "Song of Rest (d10)",
             "The extra hit points regained during a short rest from Song of Rest increase to 1d10."),
        (14, "Magical Secrets",
             "Choose two more spells from any class spell list."),
        (14, "Bard College Feature",
             "You gain a feature from your Bard College subclass."),
        (15, "Bardic Inspiration (d12)",
             "Your Bardic Inspiration die improves to a d12."),
        (16, "Ability Score Improvement",
             "Increase one ability score by 2, or two ability scores by 1 each (to a maximum of 20)."),
        (17, "Song of Rest (d12)",
             "The extra hit points regained during a short rest from Song of Rest increase to 1d12."),
        (18, "Magical Secrets",
             "Choose two more spells from any class spell list."),
        (19, "Ability Score Improvement",
             "Increase one ability score by 2, or two ability scores by 1 each (to a maximum of 20)."),
        (20, "Superior Inspiration",
             "When you roll initiative and have no uses of Bardic Inspiration left, you regain one use."),
    ],

    "Cleric": [
        (1,  "Spellcasting",
             "You cast cleric spells using WIS as your spellcasting ability, preparing a number of spells "
             "equal to your WIS modifier + cleric level from the cleric spell list after each long rest."),
        (1,  "Divine Domain",
             "Choose a Divine Domain (Life, Light, War, etc.) that shapes your connection to your deity "
             "and grants domain spells and features at 1st, 2nd, 6th, 8th, and 17th levels."),
        (2,  "Channel Divinity (1/rest)",
             "You gain the ability to channel divine energy, usable once per short or long rest, "
             "to power special magical effects defined by your domain and the Turn Undead option."),
        (2,  "Channel Divinity: Turn Undead",
             "As an action, you present your holy symbol; each undead within 30 feet must make a WIS save "
             "or be turned for 1 minute."),
        (2,  "Divine Domain Feature",
             "You gain a feature from your Divine Domain subclass."),
        (4,  "Ability Score Improvement",
             "Increase one ability score by 2, or two ability scores by 1 each (to a maximum of 20)."),
        (5,  "Destroy Undead (CR 1/2)",
             "When an undead of CR 1/2 or lower fails its saving throw against your Turn Undead, "
             "it is instantly destroyed."),
        (6,  "Channel Divinity (2/rest)",
             "You can use Channel Divinity twice between rests."),
        (6,  "Divine Domain Feature",
             "You gain a feature from your Divine Domain subclass."),
        (8,  "Ability Score Improvement",
             "Increase one ability score by 2, or two ability scores by 1 each (to a maximum of 20)."),
        (8,  "Destroy Undead (CR 1)",
             "Your Turn Undead now destroys undead of CR 1 or lower."),
        (8,  "Divine Domain Feature",
             "You gain a feature from your Divine Domain subclass."),
        (10, "Divine Intervention",
             "You can implore your deity to intervene, rolling percentile dice; if you roll equal to or lower "
             "than your cleric level, your deity intervenes (effect chosen by DM). Usable once per 7 days on success."),
        (11, "Destroy Undead (CR 2)",
             "Your Turn Undead now destroys undead of CR 2 or lower."),
        (12, "Ability Score Improvement",
             "Increase one ability score by 2, or two ability scores by 1 each (to a maximum of 20)."),
        (14, "Destroy Undead (CR 3)",
             "Your Turn Undead now destroys undead of CR 3 or lower."),
        (16, "Ability Score Improvement",
             "Increase one ability score by 2, or two ability scores by 1 each (to a maximum of 20)."),
        (17, "Destroy Undead (CR 4)",
             "Your Turn Undead now destroys undead of CR 4 or lower."),
        (17, "Divine Domain Feature",
             "You gain a feature from your Divine Domain subclass."),
        (18, "Channel Divinity (3/rest)",
             "You can use Channel Divinity three times between rests."),
        (19, "Ability Score Improvement",
             "Increase one ability score by 2, or two ability scores by 1 each (to a maximum of 20)."),
        (20, "Divine Intervention (Improved)",
             "Your deity's intervention is so powerful that your call for intervention succeeds automatically, "
             "no roll needed."),
    ],

    "Druid": [
        (1,  "Druidic",
             "You know Druidic, a secret language understood only by druids; you can leave messages in it "
             "and notice such messages automatically."),
        (1,  "Spellcasting",
             "You cast druid spells using WIS as your spellcasting ability, preparing spells from the druid list "
             "after each long rest equal to your WIS modifier + half your druid level (rounded down)."),
        (2,  "Wild Shape",
             "As an action you can magically assume the shape of a beast you have seen before, "
             "limited by CR and features based on your level, usable twice per short rest."),
        (2,  "Druid Circle",
             "You choose a Druid Circle (Moon, Land, etc.) that grants subclass features "
             "at 2nd, 6th, 10th, and 14th levels."),
        (4,  "Wild Shape Improvement",
             "You can transform into a beast with a swim speed (CR 1/4 cap lifts to 1/2)."),
        (4,  "Ability Score Improvement",
             "Increase one ability score by 2, or two ability scores by 1 each (to a maximum of 20)."),
        (6,  "Druid Circle Feature",
             "You gain a feature from your Druid Circle subclass."),
        (8,  "Wild Shape Improvement",
             "You can transform into a beast with a fly speed (CR 1 cap lifts to 1)."),
        (8,  "Ability Score Improvement",
             "Increase one ability score by 2, or two ability scores by 1 each (to a maximum of 20)."),
        (10, "Druid Circle Feature",
             "You gain a feature from your Druid Circle subclass."),
        (12, "Ability Score Improvement",
             "Increase one ability score by 2, or two ability scores by 1 each (to a maximum of 20)."),
        (14, "Druid Circle Feature",
             "You gain a feature from your Druid Circle subclass."),
        (16, "Ability Score Improvement",
             "Increase one ability score by 2, or two ability scores by 1 each (to a maximum of 20)."),
        (18, "Timeless Body",
             "The primal magic you wield causes you to age more slowly; for every 10 years that pass "
             "your body ages only 1 year."),
        (18, "Beast Spells",
             "You can cast many of your druid spells in any shape you assume using Wild Shape, "
             "as long as the spell lacks a material component."),
        (19, "Ability Score Improvement",
             "Increase one ability score by 2, or two ability scores by 1 each (to a maximum of 20)."),
        (20, "Archdruid",
             "You can use Wild Shape an unlimited number of times, and ignore the verbal and somatic components "
             "of your druid spells, as well as any material components that lack a cost."),
    ],

    "Fighter": [
        (1,  "Fighting Style",
             "You adopt a particular style of fighting as your specialty, choosing from options such as Archery, "
             "Defense, Dueling, Great Weapon Fighting, Protection, or Two-Weapon Fighting."),
        (1,  "Second Wind",
             "As a bonus action you can regain hit points equal to 1d10 + your fighter level once per short or long rest."),
        (2,  "Action Surge (1/rest)",
             "On your turn you can push yourself beyond your normal limits, taking one additional action; "
             "usable once per short or long rest."),
        (3,  "Martial Archetype",
             "You choose a Martial Archetype (Champion, Battle Master, Eldritch Knight, etc.) that grants "
             "subclass features at 3rd, 7th, 10th, 15th, and 18th levels."),
        (4,  "Ability Score Improvement",
             "Increase one ability score by 2, or two ability scores by 1 each (to a maximum of 20)."),
        (5,  "Extra Attack (2 attacks)",
             "You can attack twice instead of once whenever you take the Attack action on your turn."),
        (6,  "Ability Score Improvement",
             "Increase one ability score by 2, or two ability scores by 1 each (to a maximum of 20)."),
        (7,  "Martial Archetype Feature",
             "You gain a feature from your Martial Archetype subclass."),
        (8,  "Ability Score Improvement",
             "Increase one ability score by 2, or two ability scores by 1 each (to a maximum of 20)."),
        (9,  "Indomitable (1/long rest)",
             "You can reroll a saving throw that you fail; you must use the new roll."),
        (10, "Martial Archetype Feature",
             "You gain a feature from your Martial Archetype subclass."),
        (11, "Extra Attack (3 attacks)",
             "You can attack three times whenever you take the Attack action on your turn."),
        (12, "Ability Score Improvement",
             "Increase one ability score by 2, or two ability scores by 1 each (to a maximum of 20)."),
        (13, "Indomitable (2/long rest)",
             "You can use Indomitable twice between long rests."),
        (14, "Ability Score Improvement",
             "Increase one ability score by 2, or two ability scores by 1 each (to a maximum of 20)."),
        (15, "Martial Archetype Feature",
             "You gain a feature from your Martial Archetype subclass."),
        (16, "Ability Score Improvement",
             "Increase one ability score by 2, or two ability scores by 1 each (to a maximum of 20)."),
        (17, "Action Surge (2/rest)",
             "You can use Action Surge twice between rests."),
        (17, "Indomitable (3/long rest)",
             "You can use Indomitable three times between long rests."),
        (18, "Martial Archetype Feature",
             "You gain a feature from your Martial Archetype subclass."),
        (19, "Ability Score Improvement",
             "Increase one ability score by 2, or two ability scores by 1 each (to a maximum of 20)."),
        (20, "Extra Attack (4 attacks)",
             "You can attack four times whenever you take the Attack action on your turn."),
    ],

    "Monk": [
        (1,  "Unarmored Defense",
             "While you are wearing no armor and not wielding a shield your AC equals 10 + your DEX modifier "
             "+ your WIS modifier."),
        (1,  "Martial Arts",
             "You can use DEX instead of STR for attack and damage rolls with unarmed strikes and monk weapons; "
             "your unarmed strikes deal a die (1d4 at 1st, scaling up) instead of 1, and you can make an unarmed "
             "strike as a bonus action after attacking with a monk weapon or unarmed strike."),
        (2,  "Ki",
             "You have a pool of ki points equal to your monk level that fuel special abilities (Flurry of Blows, "
             "Patient Defense, Step of the Wind), recovering on a short or long rest."),
        (2,  "Unarmored Movement",
             "Your speed increases by 10 feet while not wearing armor or wielding a shield."),
        (3,  "Monastic Tradition",
             "You commit to a Monastic Tradition (Way of the Open Hand, Shadow, Four Elements, etc.) "
             "granting features at 3rd, 6th, 11th, and 17th levels."),
        (3,  "Deflect Missiles",
             "When hit by a ranged weapon attack you can use your reaction to reduce the damage by 1d10 + "
             "your DEX modifier + your monk level; if reduced to 0 you can catch and redirect it as a ranged attack."),
        (4,  "Ability Score Improvement",
             "Increase one ability score by 2, or two ability scores by 1 each (to a maximum of 20)."),
        (4,  "Slow Fall",
             "As a reaction you can reduce falling damage you take by an amount equal to five times your monk level."),
        (5,  "Extra Attack",
             "You can attack twice instead of once whenever you take the Attack action on your turn."),
        (5,  "Stunning Strike",
             "When you hit another creature with a melee weapon attack, you can spend 1 ki point to attempt a stunning "
             "strike; the target must succeed on a CON save or be stunned until the end of your next turn."),
        (6,  "Ki-Empowered Strikes",
             "Your unarmed strikes count as magical for the purpose of overcoming resistance and immunity "
             "to nonmagical attacks and damage."),
        (6,  "Monastic Tradition Feature",
             "You gain a feature from your Monastic Tradition subclass."),
        (7,  "Evasion",
             "When subjected to an effect that allows a DEX save for half damage, you instead take no damage "
             "on a success and only half on a failure."),
        (7,  "Stillness of Mind",
             "As an action you can end one effect on yourself that is causing you to be charmed or frightened."),
        (8,  "Ability Score Improvement",
             "Increase one ability score by 2, or two ability scores by 1 each (to a maximum of 20)."),
        (9,  "Unarmored Movement (improved)",
             "You gain the ability to move along vertical surfaces and across liquids without falling "
             "during your move (your speed bonus is now +15 ft)."),
        (10, "Purity of Body",
             "Your mastery of ki has made you immune to disease and poison."),
        (11, "Monastic Tradition Feature",
             "You gain a feature from your Monastic Tradition subclass."),
        (13, "Tongue of the Sun and Moon",
             "You learn to touch the ki of other minds so that you understand all spoken languages "
             "and all creatures that understand a language can understand what you say."),
        (14, "Diamond Soul",
             "You gain proficiency in all saving throws; additionally, whenever you make a saving throw "
             "and fail, you can spend 1 ki point to reroll and must use the new roll."),
        (15, "Timeless Body",
             "Your ki sustains you so you no longer need food or water, and you can't be aged magically."),
        (16, "Ability Score Improvement",
             "Increase one ability score by 2, or two ability scores by 1 each (to a maximum of 20)."),
        (17, "Monastic Tradition Feature",
             "You gain a feature from your Monastic Tradition subclass."),
        (18, "Empty Body",
             "As an action you can spend 4 ki points to become invisible for 1 minute; during that time "
             "you also have resistance to all damage but force."),
        (19, "Ability Score Improvement",
             "Increase one ability score by 2, or two ability scores by 1 each (to a maximum of 20)."),
        (20, "Perfect Self",
             "When you roll for initiative and have no ki points remaining, you regain 4 ki points."),
    ],

    "Paladin": [
        (1,  "Divine Sense",
             "As an action you can open your awareness to detect celestials, fiends, and undead within 60 feet "
             "until the end of your next turn; usable a number of times equal to 1 + your CHA modifier per long rest."),
        (1,  "Lay on Hands",
             "You have a pool of healing power (5 × paladin level HP) that you can expend as an action "
             "to restore hit points to a creature or cure a disease or poison (5 HP from pool)."),
        (2,  "Fighting Style",
             "You adopt a fighting style specialty: Defense, Dueling, Great Weapon Fighting, or Protection."),
        (2,  "Spellcasting",
             "You cast paladin spells using CHA as your spellcasting ability, preparing a number of spells "
             "equal to your CHA modifier + half your paladin level (rounded down) after each long rest."),
        (2,  "Divine Smite",
             "When you hit a creature with a melee weapon attack, you can expend one paladin spell slot "
             "to deal radiant damage (2d8 per slot level, +1d8 vs. undead or fiends)."),
        (3,  "Divine Health",
             "The divine magic flowing through you makes you immune to disease."),
        (3,  "Sacred Oath",
             "You swear the sacred oath (Devotion, Ancients, Vengeance, etc.) that grants Channel Divinity options, "
             "oath spells, and features at 3rd, 7th, 15th, and 20th levels."),
        (4,  "Ability Score Improvement",
             "Increase one ability score by 2, or two ability scores by 1 each (to a maximum of 20)."),
        (5,  "Extra Attack",
             "You can attack twice instead of once whenever you take the Attack action on your turn."),
        (6,  "Aura of Protection",
             "Whenever you or a friendly creature within 10 feet of you must make a saving throw, "
             "the creature gains a bonus equal to your CHA modifier (minimum +1); you must be conscious."),
        (7,  "Sacred Oath Feature",
             "You gain a feature from your Sacred Oath subclass."),
        (8,  "Ability Score Improvement",
             "Increase one ability score by 2, or two ability scores by 1 each (to a maximum of 20)."),
        (10, "Aura of Courage",
             "You and friendly creatures within 10 feet of you can't be frightened while you are conscious."),
        (11, "Improved Divine Smite",
             "You are so suffused with righteous might that all your melee weapon strikes carry divine power; "
             "whenever you hit with a melee weapon, you deal an extra 1d8 radiant damage."),
        (12, "Ability Score Improvement",
             "Increase one ability score by 2, or two ability scores by 1 each (to a maximum of 20)."),
        (14, "Cleansing Touch",
             "As an action you can end one spell on yourself or one willing creature you touch; "
             "usable a number of times equal to your CHA modifier per long rest."),
        (15, "Sacred Oath Feature",
             "You gain a feature from your Sacred Oath subclass."),
        (16, "Ability Score Improvement",
             "Increase one ability score by 2, or two ability scores by 1 each (to a maximum of 20)."),
        (18, "Aura Improvements",
             "The range of your Aura of Protection and Aura of Courage expands to 30 feet."),
        (19, "Ability Score Improvement",
             "Increase one ability score by 2, or two ability scores by 1 each (to a maximum of 20)."),
        (20, "Sacred Oath Feature",
             "You gain the capstone feature of your Sacred Oath subclass."),
    ],

    "Ranger": [
        (1,  "Favored Enemy",
             "Choose one type of favored enemy (beast, humanoid, undead, etc.); you have advantage on Survival "
             "checks to track them and on INT checks to recall information about them."),
        (1,  "Natural Explorer",
             "Choose a favored terrain type; while traveling in it you gain several benefits including doubled "
             "foraging, better tracking, and no navigation disadvantage."),
        (2,  "Fighting Style",
             "You adopt a fighting style specialty: Archery, Defense, Dueling, or Two-Weapon Fighting."),
        (2,  "Spellcasting",
             "You cast ranger spells using WIS as your spellcasting ability; you know a number of spells "
             "determined by your ranger level."),
        (3,  "Ranger Archetype",
             "You choose an archetype (Hunter, Beast Master, Gloom Stalker, etc.) that grants subclass features "
             "at 3rd, 7th, 11th, and 15th levels."),
        (3,  "Primeval Awareness",
             "As an action you can spend a spell slot to focus your awareness, sensing the presence of "
             "your favored enemy types within 1 mile (6 miles in your favored terrain) for 1 minute per slot level."),
        (4,  "Ability Score Improvement",
             "Increase one ability score by 2, or two ability scores by 1 each (to a maximum of 20)."),
        (5,  "Extra Attack",
             "You can attack twice instead of once whenever you take the Attack action on your turn."),
        (6,  "Favored Enemy Improvement",
             "You gain one additional favored enemy and one additional language associated with it."),
        (6,  "Natural Explorer Improvement",
             "You gain an additional favored terrain."),
        (7,  "Ranger Archetype Feature",
             "You gain a feature from your Ranger Archetype subclass."),
        (8,  "Ability Score Improvement",
             "Increase one ability score by 2, or two ability scores by 1 each (to a maximum of 20)."),
        (8,  "Land's Stride",
             "Moving through nonmagical difficult terrain costs you no extra movement; you can also pass through "
             "nonmagical plants without being slowed or taking damage and have advantage on saves against plants."),
        (10, "Hide in Plain Sight",
             "You can spend 1 minute creating camouflage, gaining a +10 bonus to Stealth checks as long as "
             "you remain still and don't take actions."),
        (11, "Ranger Archetype Feature",
             "You gain a feature from your Ranger Archetype subclass."),
        (12, "Ability Score Improvement",
             "Increase one ability score by 2, or two ability scores by 1 each (to a maximum of 20)."),
        (14, "Vanish",
             "You can use the Hide action as a bonus action on your turn, and you can't be tracked by nonmagical means."),
        (15, "Ranger Archetype Feature",
             "You gain a feature from your Ranger Archetype subclass."),
        (16, "Ability Score Improvement",
             "Increase one ability score by 2, or two ability scores by 1 each (to a maximum of 20)."),
        (18, "Feral Senses",
             "You gain preternatural senses that help you fight creatures you can't see; you don't have "
             "disadvantage on attack rolls against invisible creatures and are aware of invisible creatures "
             "within 30 feet."),
        (19, "Ability Score Improvement",
             "Increase one ability score by 2, or two ability scores by 1 each (to a maximum of 20)."),
        (20, "Foe Slayer",
             "Once on each of your turns you can add your WIS modifier to the attack roll or the damage roll "
             "of an attack against one of your favored enemies."),
    ],

    "Rogue": [
        (1,  "Expertise",
             "Choose two of your skill proficiencies or one skill and your thieves' tools proficiency; "
             "your proficiency bonus is doubled for those checks."),
        (1,  "Sneak Attack (1d6)",
             "Once per turn, you can deal an extra 1d6 damage to one creature you hit with an attack if you "
             "have advantage on the attack roll or if an ally is within 5 feet of the target."),
        (1,  "Thieves' Cant",
             "During your rogue training you learned thieves' cant, a secret mix of dialect, jargon, and code "
             "that allows you to hide messages in seemingly normal conversation."),
        (2,  "Cunning Action",
             "Your quick thinking and agility lets you move and act quickly; on each turn you can take a bonus "
             "action to Dash, Disengage, or Hide."),
        (3,  "Roguish Archetype",
             "You choose an archetype (Thief, Assassin, Arcane Trickster, etc.) that grants subclass features "
             "at 3rd, 9th, 13th, and 17th levels."),
        (3,  "Sneak Attack (2d6)",
             "Your Sneak Attack damage increases to 2d6."),
        (4,  "Ability Score Improvement",
             "Increase one ability score by 2, or two ability scores by 1 each (to a maximum of 20)."),
        (5,  "Uncanny Dodge",
             "When an attacker that you can see hits you with an attack, you can use your reaction to halve "
             "the attack's damage against you."),
        (5,  "Sneak Attack (3d6)",
             "Your Sneak Attack damage increases to 3d6."),
        (6,  "Expertise",
             "Choose two more of your skill proficiencies to double your proficiency bonus for."),
        (6,  "Sneak Attack (4d6)",
             "Your Sneak Attack damage increases to 4d6."),
        (7,  "Evasion",
             "When subjected to an effect that allows a DEX save for half damage, you take no damage "
             "on a success and only half on a failure."),
        (7,  "Sneak Attack (4d6, continued)",
             "Sneak Attack remains 4d6 at 7th level."),
        (8,  "Ability Score Improvement",
             "Increase one ability score by 2, or two ability scores by 1 each (to a maximum of 20)."),
        (9,  "Roguish Archetype Feature",
             "You gain a feature from your Roguish Archetype subclass."),
        (9,  "Sneak Attack (5d6)",
             "Your Sneak Attack damage increases to 5d6."),
        (10, "Ability Score Improvement",
             "Increase one ability score by 2, or two ability scores by 1 each (to a maximum of 20)."),
        (10, "Sneak Attack (6d6)",
             "Your Sneak Attack damage increases to 6d6."),
        (11, "Reliable Talent",
             "Whenever you make an ability check that lets you add your proficiency bonus, "
             "you can treat a d20 roll of 9 or lower as a 10."),
        (12, "Ability Score Improvement",
             "Increase one ability score by 2, or two ability scores by 1 each (to a maximum of 20)."),
        (13, "Roguish Archetype Feature",
             "You gain a feature from your Roguish Archetype subclass."),
        (13, "Sneak Attack (7d6)",
             "Your Sneak Attack damage increases to 7d6."),
        (14, "Blindsense",
             "If you are able to hear, you are aware of the location of any hidden or invisible creature "
             "within 10 feet of you."),
        (14, "Sneak Attack (8d6)",
             "Your Sneak Attack damage increases to 8d6."),
        (15, "Slippery Mind",
             "You have acquired greater mental strength; you gain proficiency in WIS saving throws."),
        (16, "Ability Score Improvement",
             "Increase one ability score by 2, or two ability scores by 1 each (to a maximum of 20)."),
        (17, "Roguish Archetype Feature",
             "You gain a feature from your Roguish Archetype subclass."),
        (17, "Sneak Attack (9d6)",
             "Your Sneak Attack damage increases to 9d6."),
        (18, "Elusive",
             "No attack roll has advantage against you while you aren't incapacitated."),
        (18, "Sneak Attack (10d6)",
             "Your Sneak Attack damage increases to 10d6."),
        (19, "Ability Score Improvement",
             "Increase one ability score by 2, or two ability scores by 1 each (to a maximum of 20)."),
        (20, "Stroke of Luck",
             "You have an uncanny knack for succeeding when you need to: if your attack misses a target "
             "you can turn the miss into a hit, or if you fail an ability check you can treat the d20 roll "
             "as a 20. Usable once per short or long rest."),
    ],

    "Sorcerer": [
        (1,  "Spellcasting",
             "You cast sorcerer spells using CHA as your spellcasting ability; you know a fixed number "
             "of spells and cantrips that scale with your sorcerer level."),
        (1,  "Sorcerous Origin",
             "Choose an origin (Draconic Bloodline, Wild Magic, Divine Soul, etc.) that grants subclass features "
             "at 1st, 6th, 14th, and 18th levels."),
        (2,  "Font of Magic",
             "You have sorcery points equal to your sorcerer level that you can use to create spell slots "
             "or fuel Metamagic; they restore on a long rest."),
        (3,  "Metamagic",
             "Choose two Metamagic options (Careful, Distant, Empowered, Extended, Heightened, Quickened, "
             "Subtle, Twinned) that let you modify your spells by spending sorcery points."),
        (4,  "Ability Score Improvement",
             "Increase one ability score by 2, or two ability scores by 1 each (to a maximum of 20)."),
        (6,  "Sorcerous Origin Feature",
             "You gain a feature from your Sorcerous Origin subclass."),
        (8,  "Ability Score Improvement",
             "Increase one ability score by 2, or two ability scores by 1 each (to a maximum of 20)."),
        (10, "Metamagic",
             "You learn one additional Metamagic option."),
        (12, "Ability Score Improvement",
             "Increase one ability score by 2, or two ability scores by 1 each (to a maximum of 20)."),
        (14, "Sorcerous Origin Feature",
             "You gain a feature from your Sorcerous Origin subclass."),
        (16, "Ability Score Improvement",
             "Increase one ability score by 2, or two ability scores by 1 each (to a maximum of 20)."),
        (17, "Metamagic",
             "You learn one additional Metamagic option."),
        (18, "Sorcerous Origin Feature",
             "You gain a feature from your Sorcerous Origin subclass."),
        (19, "Ability Score Improvement",
             "Increase one ability score by 2, or two ability scores by 1 each (to a maximum of 20)."),
        (20, "Sorcerous Restoration",
             "You regain 4 expended sorcery points whenever you finish a short rest."),
    ],

    "Warlock": [
        (1,  "Otherworldly Patron",
             "You have struck a bargain with a powerful otherworldly being (Archfey, Fiend, Great Old One, etc.) "
             "that grants you patron-specific spells and features at 1st, 6th, 10th, and 14th levels."),
        (1,  "Pact Magic",
             "You cast warlock spells using CHA as your spellcasting ability; you have a small number of "
             "spell slots that are all the same level and recover on a short or long rest."),
        (2,  "Eldritch Invocations",
             "You learn two Eldritch Invocations, supernatural boons from your patron, gaining additional "
             "invocations as you level up."),
        (3,  "Pact Boon",
             "Your patron bestows a gift: Pact of the Chain (familiar), Pact of the Blade (bound weapon), "
             "or Pact of the Tome (Book of Shadows with cantrips)."),
        (4,  "Ability Score Improvement",
             "Increase one ability score by 2, or two ability scores by 1 each (to a maximum of 20)."),
        (5,  "Eldritch Invocation",
             "You learn one additional Eldritch Invocation."),
        (6,  "Otherworldly Patron Feature",
             "You gain a feature from your Otherworldly Patron subclass."),
        (7,  "Eldritch Invocation",
             "You learn one additional Eldritch Invocation."),
        (8,  "Ability Score Improvement",
             "Increase one ability score by 2, or two ability scores by 1 each (to a maximum of 20)."),
        (9,  "Eldritch Invocation",
             "You learn one additional Eldritch Invocation."),
        (10, "Otherworldly Patron Feature",
             "You gain a feature from your Otherworldly Patron subclass."),
        (11, "Mystic Arcanum (6th level)",
             "Your patron bestows a 6th-level spell upon you, usable once per long rest without expending a spell slot."),
        (12, "Ability Score Improvement",
             "Increase one ability score by 2, or two ability scores by 1 each (to a maximum of 20)."),
        (13, "Mystic Arcanum (7th level)",
             "Your patron gives you a 7th-level spell, usable once per long rest without a spell slot."),
        (14, "Otherworldly Patron Feature",
             "You gain a feature from your Otherworldly Patron subclass."),
        (15, "Mystic Arcanum (8th level)",
             "Your patron gives you an 8th-level spell, usable once per long rest without a spell slot."),
        (16, "Ability Score Improvement",
             "Increase one ability score by 2, or two ability scores by 1 each (to a maximum of 20)."),
        (17, "Mystic Arcanum (9th level)",
             "Your patron gives you a 9th-level spell, usable once per long rest without a spell slot."),
        (18, "Eldritch Invocation",
             "You learn one additional Eldritch Invocation."),
        (19, "Ability Score Improvement",
             "Increase one ability score by 2, or two ability scores by 1 each (to a maximum of 20)."),
        (20, "Eldritch Master",
             "As an action you can beseech your patron for aid, regaining all expended spell slots; "
             "you must spend 1 minute in prayer and meditation before using this feature again."),
    ],

    "Wizard": [
        (1,  "Spellcasting",
             "You cast wizard spells using INT as your spellcasting ability; you have a spellbook containing "
             "6 first-level spells at start and can copy additional spells into it."),
        (1,  "Arcane Recovery",
             "Once per day when you finish a short rest, you can recover expended spell slots totaling "
             "a combined level equal to half your wizard level (rounded up), with no slot above 5th level."),
        (2,  "Arcane Tradition",
             "You choose a school of magic or tradition (Evocation, Abjuration, Divination, etc.) "
             "that grants subclass features at 2nd, 6th, 10th, and 14th levels."),
        (4,  "Ability Score Improvement",
             "Increase one ability score by 2, or two ability scores by 1 each (to a maximum of 20)."),
        (6,  "Arcane Tradition Feature",
             "You gain a feature from your Arcane Tradition subclass."),
        (8,  "Ability Score Improvement",
             "Increase one ability score by 2, or two ability scores by 1 each (to a maximum of 20)."),
        (10, "Arcane Tradition Feature",
             "You gain a feature from your Arcane Tradition subclass."),
        (12, "Ability Score Improvement",
             "Increase one ability score by 2, or two ability scores by 1 each (to a maximum of 20)."),
        (14, "Arcane Tradition Feature",
             "You gain a feature from your Arcane Tradition subclass."),
        (16, "Ability Score Improvement",
             "Increase one ability score by 2, or two ability scores by 1 each (to a maximum of 20)."),
        (18, "Spell Mastery",
             "You have achieved mastery over two spells (one 1st-level, one 2nd-level); you can cast each "
             "at their lowest level at will without expending a spell slot."),
        (19, "Ability Score Improvement",
             "Increase one ability score by 2, or two ability scores by 1 each (to a maximum of 20)."),
        (20, "Signature Spells",
             "You gain mastery over two powerful spells (both 3rd-level or lower); you always have them "
             "prepared and can cast each once per short rest without expending a spell slot."),
    ],

    "Artificer": [
        (1,  "Magical Tinkering",
             "You learn to invest a spark of magic in mundane objects; as an action you can imbue a Tiny "
             "object with one of several minor magical properties (light, recorded message, odor, etc.)."),
        (1,  "Spellcasting",
             "You cast artificer spells using INT as your spellcasting ability; you prepare spells from "
             "the artificer list equal to your INT modifier + half your artificer level (rounded up)."),
        (2,  "Infuse Item",
             "You learn a set of artificer infusions—magical enhancements to objects—and can infuse a "
             "number of objects per long rest; infused items function as magic items."),
        (3,  "Artificer Specialist",
             "You choose a specialist subclass (Alchemist, Artillerist, Battle Smith, Armorer) "
             "that grants features at 3rd, 5th, 9th, and 15th levels."),
        (3,  "The Right Tool for the Job",
             "In 1 hour of work using thieves' tools or artisan's tools, you can magically create "
             "any tool you need (the tool vanishes after you use The Right Tool for the Job again)."),
        (4,  "Ability Score Improvement",
             "Increase one ability score by 2, or two ability scores by 1 each (to a maximum of 20)."),
        (5,  "Artificer Specialist Feature",
             "You gain a feature from your Artificer Specialist subclass."),
        (6,  "Tool Expertise",
             "Your proficiency bonus is doubled for any ability check you make that uses your proficiency "
             "with a tool."),
        (7,  "Flash of Genius",
             "When you or another creature you can see within 30 feet makes an ability check or saving throw, "
             "you can use your reaction to add your INT modifier to the roll (usable INT modifier times per long rest)."),
        (8,  "Ability Score Improvement",
             "Increase one ability score by 2, or two ability scores by 1 each (to a maximum of 20)."),
        (9,  "Artificer Specialist Feature",
             "You gain a feature from your Artificer Specialist subclass."),
        (10, "Magic Item Adept",
             "You achieve a profound understanding of how to craft and use magic items; "
             "you can attune to up to four magic items at once and craft common and uncommon items faster."),
        (11, "Spell-Storing Item",
             "You can store a 1st- or 2nd-level artificer spell in a non-magical item; "
             "a creature holding the item can expend charges to cast it using your spell save DC."),
        (12, "Ability Score Improvement",
             "Increase one ability score by 2, or two ability scores by 1 each (to a maximum of 20)."),
        (14, "Magic Item Savant",
             "You can attune to up to five magic items at once and can ignore class, race, spell, and level "
             "requirements on attuning to magic items."),
        (15, "Artificer Specialist Feature",
             "You gain a feature from your Artificer Specialist subclass."),
        (16, "Ability Score Improvement",
             "Increase one ability score by 2, or two ability scores by 1 each (to a maximum of 20)."),
        (18, "Magic Item Master",
             "You can attune to up to six magic items at once."),
        (19, "Ability Score Improvement",
             "Increase one ability score by 2, or two ability scores by 1 each (to a maximum of 20)."),
        (20, "Soul of Artifice",
             "You develop a mystical connection to your magic items; you gain +1 to all saving throws "
             "per magic item you are attuned to, and when reduced to 0 HP you can use a reaction to end "
             "one of your artificer infusions to drop to 1 HP instead."),
    ],
}


# ---------------------------------------------------------------------------
# RACE TRAITS
# ---------------------------------------------------------------------------

RACE_TRAITS: dict[str, list[tuple[str, str]]] = {

    "Dragonborn": [
        ("Ability Score Increase",
         "Your STR score increases by 2 and your CHA score increases by 1."),
        ("Draconic Ancestry",
         "You have draconic ancestry of a particular dragon type that determines your breath weapon "
         "and damage resistance (choose from: Black/Acid, Blue/Lightning, Brass/Fire, Bronze/Lightning, "
         "Copper/Acid, Gold/Fire, Green/Poison, Red/Fire, Silver/Cold, White/Cold)."),
        ("Breath Weapon",
         "As an action you can exhale destructive energy in a 15-ft cone (or 30×5-ft line); "
         "each creature in the area makes a DEX (line) or DEX (cone) save (DC 8 + CON mod + prof bonus) "
         "taking 2d6 damage, increasing at higher levels. Usable once per short or long rest."),
        ("Damage Resistance",
         "You have resistance to the damage type associated with your draconic ancestry."),
        ("Languages",
         "You can speak, read, and write Common and Draconic."),
    ],

    "Dwarf": [
        ("Ability Score Increase",
         "Your CON score increases by 2."),
        ("Age",
         "Dwarves mature at the same rate as humans but are considered young until age 50; "
         "they can live to over 350 years."),
        ("Size",
         "Dwarves stand between 4 and 5 feet tall and average about 150 pounds (Medium size)."),
        ("Speed",
         "Your base walking speed is 25 feet; your speed is not reduced by wearing heavy armor."),
        ("Darkvision",
         "Accustomed to underground life you can see in dim light within 60 feet as if it were bright light "
         "and in darkness as if it were dim light (only shades of gray in darkness)."),
        ("Dwarven Resilience",
         "You have advantage on saving throws against poison and resistance against poison damage."),
        ("Dwarven Combat Training",
         "You have proficiency with the battleaxe, handaxe, light hammer, and warhammer."),
        ("Tool Proficiency",
         "You gain proficiency with one type of artisan's tools of your choice: smith's tools, "
         "brewer's supplies, or mason's tools."),
        ("Stonecunning",
         "Whenever you make an INT (History) check related to the origin of stonework, "
         "you are considered proficient in the History skill and add double your proficiency bonus."),
        ("Languages",
         "You can speak, read, and write Common and Dwarvish."),
        ("Subrace",
         "Choose Hill Dwarf (+1 WIS, Dwarven Toughness: +1 HP per level) or Mountain Dwarf "
         "(+2 STR, proficiency with light and medium armor)."),
    ],

    "Elf": [
        ("Ability Score Increase",
         "Your DEX score increases by 2."),
        ("Age",
         "Elves reach physical maturity at about the same age as humans but consider themselves adults "
         "around 100 and can live to be 750 years old."),
        ("Size",
         "Elves range from under 5 to over 6 feet tall and are slender (Medium size)."),
        ("Speed",
         "Your base walking speed is 30 feet."),
        ("Darkvision",
         "You can see in dim light within 60 feet as if it were bright light and in darkness as if "
         "it were dim light (only shades of gray in darkness)."),
        ("Keen Senses",
         "You have proficiency in the Perception skill."),
        ("Fey Ancestry",
         "You have advantage on saving throws against being charmed and magic can't put you to sleep."),
        ("Trance",
         "Elves don't need to sleep; instead they meditate deeply for 4 hours a day (long rest equivalent) "
         "remaining semiconscious and aware of their surroundings."),
        ("Languages",
         "You can speak, read, and write Common and Elvish."),
        ("Subrace",
         "Choose High Elf (+1 INT, one wizard cantrip, one extra language, longsword/shortsword/shortbow/"
         "longbow proficiency), Wood Elf (+1 WIS, fleet of foot 35 ft, mask of the wild, weapon proficiencies), "
         "or Dark Elf/Drow (+1 CHA, superior darkvision 120 ft, sunlight sensitivity, drow magic)."),
    ],

    "Gnome": [
        ("Ability Score Increase",
         "Your INT score increases by 2."),
        ("Age",
         "Gnomes mature at the same rate as humans and are expected to settle down around age 40; "
         "they can live to 350–500 years."),
        ("Size",
         "Gnomes are between 3 and 4 feet tall and average about 40 pounds (Small size)."),
        ("Speed",
         "Your base walking speed is 25 feet."),
        ("Darkvision",
         "You can see in dim light within 60 feet as if it were bright light and in darkness as "
         "if it were dim light."),
        ("Gnome Cunning",
         "You have advantage on all INT, WIS, and CHA saving throws against magic."),
        ("Languages",
         "You can speak, read, and write Common and Gnomish."),
        ("Subrace",
         "Choose Forest Gnome (+1 DEX, Minor Illusion cantrip, speak with small animals) or "
         "Rock Gnome (+1 CON, Artificer's Lore for history on magic/alchemical objects, tinker to craft "
         "clockwork toys)."),
    ],

    "Half-Elf": [
        ("Ability Score Increase",
         "Your CHA score increases by 2 and two other ability scores of your choice each increase by 1."),
        ("Age",
         "Half-elves mature at the same rate as humans and live to around 180 years."),
        ("Size",
         "Half-elves range from 5 to 6 feet tall (Medium size)."),
        ("Speed",
         "Your base walking speed is 30 feet."),
        ("Darkvision",
         "You can see in dim light within 60 feet as if it were bright light and in darkness as "
         "if it were dim light."),
        ("Fey Ancestry",
         "You have advantage on saving throws against being charmed and magic can't put you to sleep."),
        ("Skill Versatility",
         "You gain proficiency in two skills of your choice."),
        ("Languages",
         "You can speak, read, and write Common, Elvish, and one extra language of your choice."),
    ],

    "Half-Orc": [
        ("Ability Score Increase",
         "Your STR score increases by 2 and your CON score increases by 1."),
        ("Age",
         "Half-orcs mature a little faster than humans and rarely live longer than 75 years."),
        ("Size",
         "Half-orcs range from 5 to 6 feet tall and generally weigh between 180 and 250 pounds (Medium size)."),
        ("Speed",
         "Your base walking speed is 30 feet."),
        ("Darkvision",
         "You can see in dim light within 60 feet as if it were bright light and in darkness as "
         "if it were dim light."),
        ("Menacing",
         "You gain proficiency in the Intimidation skill."),
        ("Relentless Endurance",
         "When you are reduced to 0 hit points but not killed outright, you can drop to 1 hit point instead; "
         "usable once per long rest."),
        ("Savage Attacks",
         "When you score a critical hit with a melee weapon attack, you can roll one of the weapon's "
         "damage dice one additional time and add it to the extra damage of the critical hit."),
        ("Languages",
         "You can speak, read, and write Common and Orc."),
    ],

    "Halfling": [
        ("Ability Score Increase",
         "Your DEX score increases by 2."),
        ("Age",
         "Halflings reach adulthood at age 20 and generally live into the middle of their second century."),
        ("Size",
         "Halflings average about 3 feet tall and weigh about 40 pounds (Small size)."),
        ("Speed",
         "Your base walking speed is 25 feet."),
        ("Lucky",
         "When you roll a 1 on the d20 for an attack roll, ability check, or saving throw, "
         "you can reroll the die and must use the new roll."),
        ("Brave",
         "You have advantage on saving throws against being frightened."),
        ("Halfling Nimbleness",
         "You can move through the space of any creature that is of a size larger than yours."),
        ("Languages",
         "You can speak, read, and write Common and Halfling."),
        ("Subrace",
         "Choose Lightfoot Halfling (+1 CHA, Naturally Stealthy: can hide behind creatures one size larger) "
         "or Stout Halfling (+1 CON, Stout Resilience: advantage on saves vs. poison, resistance to poison damage)."),
    ],

    "Human": [
        ("Ability Score Increase",
         "Each of your ability scores increases by 1."),
        ("Age",
         "Humans reach adulthood in their late teens and live to around 80 years."),
        ("Size",
         "Humans vary widely in height and build, from barely 5 feet to well over 6 feet tall (Medium size)."),
        ("Speed",
         "Your base walking speed is 30 feet."),
        ("Languages",
         "You can speak, read, and write Common and one extra language of your choice."),
    ],

    "Tiefling": [
        ("Ability Score Increase",
         "Your INT score increases by 1 and your CHA score increases by 2."),
        ("Age",
         "Tieflings mature at the same rate as humans but live a few years longer."),
        ("Size",
         "Tieflings are about the same size and build as humans (Medium size)."),
        ("Speed",
         "Your base walking speed is 30 feet."),
        ("Darkvision",
         "You can see in dim light within 60 feet as if it were bright light and in darkness as "
         "if it were dim light."),
        ("Hellish Resistance",
         "You have resistance to fire damage."),
        ("Infernal Legacy",
         "You know the Thaumaturgy cantrip. At 3rd level you can cast Hellish Rebuke as a 2nd-level spell "
         "once per long rest. At 5th level you can cast Darkness once per long rest. CHA is your spellcasting ability."),
        ("Languages",
         "You can speak, read, and write Common and Infernal."),
    ],
}


# ---------------------------------------------------------------------------
# BACKGROUND FEATURES
# ---------------------------------------------------------------------------

BACKGROUND_FEATURES: dict[str, tuple[str, str]] = {
    "Acolyte": (
        "Shelter of the Faithful",
        "You and your companions can receive free healing and care at temples or shrines of your faith; "
        "those who share your religion will support you (though only you, not companions) at a modest lifestyle.",
    ),
    "Charlatan": (
        "False Identity",
        "You have a second identity including documentation, established acquaintances, and disguises "
        "that let you assume that persona; you can also create forgeries of mundane documents.",
    ),
    "Criminal": (
        "Criminal Contact",
        "You have a reliable and trustworthy contact who acts as your liaison to a network of criminals; "
        "you can send and receive messages via this contact even over great distances.",
    ),
    "Entertainer": (
        "By Popular Demand",
        "You can always find a place to perform in an inn, tavern, circus, or similar venue, "
        "receiving free lodging and food of a modest standard in exchange for your performances.",
    ),
    "Folk Hero": (
        "Rustic Hospitality",
        "Since you come from the common folk, you fit in among them with ease; "
        "common people will shelter you from those searching for you and never report you to the authorities.",
    ),
    "Guild Artisan": (
        "Guild Membership",
        "Your guild provides support including access to its facilities, lodging, and help with legal trouble; "
        "in return you pay dues of 5 gp per month.",
    ),
    "Hermit": (
        "Discovery",
        "The quiet seclusion of your extended hermitage gave you access to a unique and powerful discovery — "
        "a great truth about the cosmos, the gods, or the forces of nature (work with your DM to determine).",
    ),
    "Noble": (
        "Position of Privilege",
        "Thanks to your noble birth, people are inclined to think the best of you; "
        "you are welcome in high society and commoners defer to you, giving you access to places and "
        "conversations that others might not enjoy.",
    ),
    "Outlander": (
        "Wanderer",
        "You have an excellent memory for maps and geography, and can always recall the general layout of "
        "terrain, settlements, and other features; you can also find food and water for yourself and up to "
        "five others each day in the wilderness.",
    ),
    "Sage": (
        "Researcher",
        "When you attempt to learn or recall a piece of lore, if you don't know it you often know where "
        "and from whom you can obtain it; usually from a library, university, or another sage.",
    ),
    "Sailor": (
        "Ship's Passage",
        "When you need to, you can secure free passage on a sailing ship for yourself and your companions; "
        "you might have to work during the voyage, and the passage doesn't include dangerous waters.",
    ),
    "Soldier": (
        "Military Rank",
        "You have a military rank from your career as a soldier; soldiers loyal to your former military "
        "organization still recognize your authority and obey your orders where possible.",
    ),
    "Urchin": (
        "City Secrets",
        "You know the secret patterns and flows of cities and can find passages through urban sprawl that "
        "others would miss; when not in combat you can travel between any two locations in the city "
        "twice as fast as your speed would normally allow.",
    ),
}
