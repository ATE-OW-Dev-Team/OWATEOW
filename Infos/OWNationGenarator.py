import json
import regex
import shrines

def dashandupper(txt):
    return(regex.sub('[^A-Za-z0-9]+', '_', txt.upper()))

def get_asset(nation, value):
    if value in nation["assets"]:
        if type(nation["assets"][value]) == str:
            return(dashandupper(nation["assets"][value]))
        else:
            return(nation["assets"][value])
    else:
        return(dashandupper(nation["assets"]["template"]))

def zvalues(values, prefix):
    result = ""
    for i in values:
        if prefix:
            result = result + f"			<zValue>{prefix}{dashandupper(i)}</zValue>\n"
        else:
            result = result + f"			<zValue>{i}</zValue>\n"
    return(result)

def get_portraits(nation):
    portraits = get_asset(nation, 'portraits')
    if type(portraits) == str:
        value, portraits = portraits, []
        for i in range(1, 16):
            portraits.append(f"{value}_LEADER_MALE_{'0' if i < 10 else ''}{i}")
            portraits.append(f"{value}_LEADER_FEMALE_{'0' if i < 10 else ''}{i}")
    return(zvalues(portraits, "CHARACTER_PORTRAIT_"))

def generate_nation(nation):
    return(f"""
    <Entry>
        <zType>NATION_{dashandupper(nation['name'])}</zType>
        <Name>TEXT_NATION_{dashandupper(nation['name'])}</Name>
        <TeamColor>TEAMCOLOR_NATION_{dashandupper(nation['name'])}</TeamColor>
        <Crest>CREST_NATION_{get_asset(nation, 'crest')}</Crest>
        <zAttackPortraitName>ATTACKPREVIEW_CITY</zAttackPortraitName>
        <zCharacterPortraitBackground>PORTRAIT_BACKGROUND_{get_asset(nation, 'background')}</zCharacterPortraitBackground>
        <CapitalAsset>ASSET_VARIATION_CITY_{get_asset(nation, 'capital')}_CAPITAL</CapitalAsset>
        <CityAsset>ASSET_VARIATION_CITY_{get_asset(nation, 'city')}_CAPITAL</CityAsset>
        <UrbanAsset>ASSET_VARIATION_{get_asset(nation, 'urban')}_URBAN</UrbanAsset>
        <Founder>CHARACTER_{dashandupper(nation['founder'])}</Founder>
        <FirstRuler>CHARACTER_{dashandupper(nation['first-ruler'])}</FirstRuler>
        <FirstBuild>{dashandupper(nation['start']['first-build']['type'])}</FirstBuild>
        <EffectPlayer>EFFECTPLAYER_NATION_{dashandupper(nation['name'])}</EffectPlayer>
        <MapElementNames>MAP_ELEMENT_NAMES_FOR_{dashandupper(nation['name'])}</MapElementNames>
        <iFirstBuildPercent>{dashandupper(nation['start']['first-build']['percent'])}</iFirstBuildPercent>
		<bShowSurname>{'1' if nation['show-surename'] == 'true' else '0'}</bShowSurname>
        <aiStartUnit>
            <Pair>
                <zIndex>UNIT_{dashandupper(nation['start']['unit']['type'])}</zIndex>
                <iValue>{dashandupper(nation['start']['unit']['value'])}</iValue>
            </Pair>
        </aiStartUnit>
        <aeStartingTech>
{zvalues(nation['start']['tech'], 'TECH_')}\t\t</aeStartingTech>
        <aeStartingLaw>
            <Pair>
                <zIndex>LAWCLASS_{dashandupper(nation['start']['law']['type'])}</zIndex>
                <zValue>LAW_{dashandupper(nation['start']['law']['value'])}</zValue>
            </Pair>
        </aeStartingLaw>
        <aeFirstNamesMale>
{zvalues(nation['names']['male'], 'NAME_')}\t\t</aeFirstNamesMale>
        <aeFirstNamesFemale>
{zvalues(nation['names']['female'], 'NAME_')}\t\t</aeFirstNamesFemale>
        <aeCityNames>
{zvalues(nation['names']['city'], 'CITYNAME_')}\t\t</aeCityNames>
        <aeCharacterPortraits>
{get_portraits(nation)}\t\t</aeCharacterPortraits>
        <zStory>{nation['story']}</zStory>
    </Entry>""")

def generate_nation_file(data):
    output = """<?xml version="1.0" encoding="UTF-8"?>
<Root>
    <Entry>
        <zType/>
        <Name/>
        <TeamColor/>
        <Crest/>
        <zAttackPortraitName/>
        <zCharacterPortraitBackground/>
        <CapitalAsset/>
        <CityAsset/>
        <UrbanAsset/>
        <Founder/>
        <FirstRuler/>
        <FirstBuild/>
        <EffectPlayer/>
        <MapElementNames/>
        <iFirstBuildPercent/>
        <bShowSurname/>
        <aiStartUnit/>
        <aiStartYield/>
        <aeStartingTech/>
        <aeStartingLaw/>
        <aeFirstNamesMale/>
        <aeFirstNamesFemale/>
        <aeCityNames/>
        <aeCharacterPortraits/>
        <zStory/>
    </Entry>"""
    for i in data['nations']:
        output = output + generate_nation(data['nations'][i])
    output = output + "\n</Root>\n"
    file = open(f"{data['file-preffix']}nation{data['file-suffix']}.xml", "w")
    file.write(output)
    file.close()

def generate_name(name):
    return(f"""
    <Entry>
        <zType>NAME_{dashandupper(name)}</zType>
        <zName>{name}</zName>
    </Entry>""")

def generate_name_file(data):
    output = """<?xml version="1.0"?>
<Root>
    <Entry>
        <zType/>
        <zName/>
    </Entry>"""
    for i in data['nations']:
        for o in data['nations'][i]['names']['male'] + data['nations'][i]['names']['female']:
            output += generate_name(o)
    output = output + "\n</Root>\n"
    file = open(f"{data['file-preffix']}name{data['file-suffix']}.xml", "w")
    file.write(output)
    file.close()

def generate_map_elements(nation):
    return(f"""
    <Entry>
        <zType>MAP_ELEMENT_NAMES_FOR_{dashandupper(nation['name'])}</zType>
        <azVolcanoNames>
{zvalues(nation['mapelements']['volcano'], '')}\t\t</azVolcanoNames>
        <azMountainRangeNames>
{zvalues(nation['mapelements']['mountainrange'], '')}\t\t</azMountainRangeNames>
        <azPeakNames>
{zvalues(nation['mapelements']['peak'], '')}\t\t</azPeakNames>
        <azRiverNames>
{zvalues(nation['mapelements']['river'], '')}\t\t</azRiverNames>
        <azForestNames>
{zvalues(nation['mapelements']['forest'], '')}\t\t</azForestNames>
        <azHeathNames>
{zvalues(nation['mapelements']['heath'], '')}\t\t</azHeathNames>
        <azPlainNames>
{zvalues(nation['mapelements']['plain'], '')}\t\t</azPlainNames>
        <azDesertNames>
{zvalues(nation['mapelements']['desert'], '')}\t\t</azDesertNames>
        <azPlateauNames>
{zvalues(nation['mapelements']['plateau'], '')}\t\t</azPlateauNames>
        <azValleyNames>
{zvalues(nation['mapelements']['valley'], '')}\t\t</azValleyNames>
        <azOceanNames>
{zvalues(nation['mapelements']['ocean'], '')}\t\t</azOceanNames>
        <azSeaNames>
{zvalues(nation['mapelements']['sea'], '')}\t\t</azSeaNames>
        <azBayNames>
{zvalues(nation['mapelements']['bay'], '')}\t\t</azBayNames>
        <azLakeNames>
{zvalues(nation['mapelements']['lake'], '')}\t\t</azLakeNames>
        <azIslandNames>
{zvalues(nation['mapelements']['island'], '')}\t\t</azIslandNames>
    </Entry>""")
    
def generate_map_elements_file(data):
    output = """<?xml version="1.0" encoding="UTF-8"?>
<Root>
    <Entry>
        <zType/>
        <azVolcanoNames/>
        <azMountainRangeNames/>
        <azPeakNames/>
        <azRiverNames/>
        <azForestNames/>
        <azHeathNames/>
        <azPlainNames/>
        <azDesertNames/>
        <azPlateauNames/>
        <azValleyNames/>
        <azOceanNames/>
        <azSeaNames/>
        <azBayNames/>
        <azLakeNames/>
        <azIslandNames/>
    </Entry>"""
    for i in data['nations']:
        output += generate_map_elements(data['nations'][i])
    output = output + "\n</Root>\n"
    file = open(f"{data['file-preffix']}mapElementNames{data['file-suffix']}.xml", "w")
    file.write(output)
    file.close()

def generate_family(family, index, nation):
    return(f"""
    <Entry>
        <zType>FAMILY_{dashandupper(family['name'])}</zType>
        <Name>TEXT_FAMILY_{dashandupper(family['name'])}</Name>
        <NameFemale>TEXT_FAMILY_{dashandupper(family['name'])}{'_FEMALE' if "name-female" in family else ''}</NameFemale>
        <iColorIndex>{index}</iColorIndex>
        <Nation>NATION_{dashandupper(nation)}</Nation>
        <FamilyClass>FAMILY_CLASS_{dashandupper(family['class'])}</FamilyClass>
    </Entry>""")

def generate_family_file(data):
    output = """<?xml version="1.0" encoding="UTF-8"?>
<Root>
    <Entry>
        <zType/>
        <Name/>
        <NameFemale/>
        <iColorIndex/>
        <Nation/>
        <FamilyClass/>
    </Entry>"""
    for i in data['nations']:
        for o, u in enumerate(data['nations'][i]['families']):
            output = output + generate_family(data['nations'][i]['families'][u], o, data['nations'][i]['name'])
    output = output + "\n</Root>\n"
    file = open(f"{data['file-preffix']}family{data['file-suffix']}.xml", "w")
    file.write(output)
    file.close()

def generate_text_nation(nation):
    return(f"""
    <Entry>
        <zType>TEXT_NATION_{dashandupper(nation['name'])}</zType>
        <English>{nation['name']}~{nation['adjective']}~{nation['plural']}</English>
    </Entry>""")

def generate_text_nation_file(data):
    output = """<?xml version="1.0" encoding="UTF-8"?>
<Root>
    <Entry>
        <zType/>
        <English/>
    </Entry>"""
    for i in data['nations']:
        output = output + generate_text_nation(data['nations'][i])
    output = output + "\n</Root>\n"
    file = open(f"{data['file-preffix']}text-nation{data['file-suffix']}.xml", "w")
    file.write(output)
    file.close()

def generate_text_family_female(family):
    if 'name-female' in family:
        return(f"""
    <Entry>
        <zType>TEXT_FAMILY_{dashandupper(family['name'])}_FEMALE</zType>
        <English>{family['name-female']}~{family['plural-female']}~{family['adjective-female']}</English>
    </Entry>""")
    else:
        return("")

def generate_text_family(family):
    return(f"""
    <Entry>
        <zType>TEXT_FAMILY_{dashandupper(family['name'])}</zType>
        <English>{family['name']}~{family['plural']}~{family['adjective']}</English>
    </Entry>{generate_text_family_female(family)}""")

def generate_text_family_file(data):
    output = """<?xml version="1.0" encoding="UTF-8"?>
<Root>
    <Entry>
        <zType/>
        <English/>
    </Entry>"""
    for i in data['nations']:
        for o in data['nations'][i]['families']:
            output = output + generate_text_family(data['nations'][i]['families'][o])
    output = output + "\n</Root>\n"
    file = open(f"{data['file-preffix']}text-family{data['file-suffix']}.xml", "w")
    file.write(output)
    file.close()

def get_families(nation):
    families = []
    for i in range(1, len(nation['families'])+1):
        families.append(("0" if i < 10 else "") + str(i))
    return(zvalues(families, f"PLAYERCOLOR_NATION_{dashandupper(nation['name'])}_FAMILY_"))

def generate_team_color(nation):
    return(f"""
	<Entry>
		<zType>TEAMCOLOR_NATION_{dashandupper(nation['name'])}</zType>
		<TeamPlayerColor>PLAYERCOLOR_NATION_{dashandupper(nation['name'])}</TeamPlayerColor>
		<aePlayerColors>
{get_families(nation)}\t\t</aePlayerColors>
		<aeBorderPatterns>
			<zValue>BORDER_PATTERN_TRIANGLE</zValue>
			<zValue>BORDER_PATTERN_DASH</zValue>
			<zValue>BORDER_PATTERN_PLUS</zValue>
			<zValue>BORDER_PATTERN_CIRCLE</zValue>
			<zValue>BORDER_PATTERN_DIAMOND</zValue>
			<zValue>BORDER_PATTERN_X</zValue>
		</aeBorderPatterns>
	</Entry>""")

def generate_team_color_file(data):
    output = """<?xml version="1.0" encoding="UTF-8"?>
<Root>
    <Entry>
		<zType/>
		<TeamPlayerColor/>
		<aePlayerColors/>
		<aeBorderPatterns/>
    </Entry>"""
    for i in data['nations']:
        output = output + generate_team_color(data['nations'][i])
    output = output + "\n</Root>\n"
    file = open(f"{data['file-preffix']}teamColor{data['file-suffix']}.xml", "w")
    file.write(output)
    file.close()

def generate_player_color(nationOrFamily):
    return(f"""
    <Entry>
		<zType>PLAYERCOLOR_NATION_{dashandupper(nationOrFamily)}</zType>
		<AssetColor>COLOR_NATION_{dashandupper(nationOrFamily)}</AssetColor>
		<TextColor>COLOR_NATION_{dashandupper(nationOrFamily)}_TEXT</TextColor>
		<BorderColor>COLOR_NATION_{dashandupper(nationOrFamily)}</BorderColor>
		<CrestColor>COLOR_NATION_{dashandupper(nationOrFamily)}</CrestColor>
	</Entry>""")

def generate_player_color_file(data):
    output = """<?xml version="1.0" encoding="UTF-8"?>
<Root>
    <Entry>
		<zType/>
		<AssetColor/>
		<TextColor/>
		<BorderColor/>
		<CrestColor/>
    </Entry>"""
    for i in data['nations']:
        output = output + generate_player_color(data['nations'][i]['name'])
        for o in range(1, len(data['nations'][i]['families'])+1):
            output = output + generate_player_color(data['nations'][i]['name']+" Family "+("0" if o < 10 else "") + str(o))
    output = output + "\n</Root>\n"
    file = open(f"{data['file-preffix']}playerColor{data['file-suffix']}.xml", "w")
    file.write(output)
    file.close()

def generate_color(nationOrFamily, color):
    return(f"""
	<Entry>
		<zType>COLOR_NATION_{dashandupper(nationOrFamily)}</zType>
		<zName>{nationOrFamily}</zName>
		<ColorClass>COLORCLASS_NATIONS</ColorClass>
		<zHexValue>{color}</zHexValue>
	</Entry>
	<Entry>
		<zType>COLOR_NATION_{dashandupper(nationOrFamily)}_TEXT</zType>
		<zName>{nationOrFamily} Text</zName>
		<ColorClass>COLORCLASS_NATIONS</ColorClass>
		<zHexValue>{color}</zHexValue>
	</Entry>""")

def generate_color_file(data):
    output = """<?xml version="1.0" encoding="UTF-8"?>
<Root>
    <Entry>
        <zType />
        <zName />
        <ColorClass />
        <zHexValue />
    </Entry>"""
    for i in data['nations']:
        output = output + generate_color(data['nations'][i]['name'], data['nations'][i]['color'])
        for u, y in enumerate(data['nations'][i]['families']):
            o = u+1
            output = output + generate_color(data['nations'][i]['name']+" Family "+("0" if o < 10 else "") + str(o), data['nations'][i]['families'][y]['color'])
    output = output + "\n</Root>\n"
    file = open(f"{data['file-preffix']}color{data['file-suffix']}.xml", "w")
    file.write(output)
    file.close()

def generate_city_name(name):
    return(f"""
    <Entry>
        <zType>CITYNAME_{dashandupper(name)}</zType>
        <zName>{name}</zName>
    </Entry>""")

def generate_city_name_file(data):
    output = """<?xml version="1.0"?>
<Root>
    <Entry>
        <zType/>
        <zName/>
		<azNationAdjectivesMale/>
		<azNationAdjectivesFemale/>
    </Entry>"""
    for i in data['nations']:
        for o in data['nations'][i]['names']['city']:
            output += generate_city_name(o)
    output = output + "\n</Root>\n"
    file = open(f"{data['file-preffix']}cityName{data['file-suffix']}.xml", "w")
    file.write(output)
    file.close()

def generate_improvement(nation, shrine):
    nation_name = dashandupper(nation)
    deity = dashandupper(shrine["deity"])
    if shrine["type"] == "war":
        return(shrines.war(deity,nation_name))
    elif shrine["type"] == "fire":
        return(shrines.fire(deity,nation_name))
    elif shrine["type"] == "sun":
        return(shrines.sun(deity,nation_name))
    elif shrine["type"] == "water":
        return(shrines.water(deity,nation_name))
    elif shrine["type"] == "love":
        return(shrines.love(deity,nation_name))
    elif shrine["type"] == "underworld":
        return(shrines.underworld(deity,nation_name))
    elif shrine["type"] == "healing":
        return(shrines.healing(deity,nation_name))
    elif shrine["type"] == "kingship":
        return(shrines.kingship(deity,nation_name))
    elif shrine["type"] == "hearth":
        return(shrines.hearth(deity,nation_name))
    elif shrine["type"] == "hunting":
        return(shrines.hunting(deity,nation_name))
    else:
        return("")

def generate_improvement_file(data):
    output = """<?xml version="1.0"?>
<Root>
	<Entry>
		<zType/>
		<Name/>
		<Class/>
		<Asset/>
		<AssetVariation/>
		<zIconName/>
		<fHillHeightOffset/>
		<iBuildTurns/>
		<iBuildCost/>
		<iUpgradeTurns/>
		<iUpgradeRand/>
		<iPillageTurns/>
		<iRevealChange/>
		<iDefenseModifier/>
		<iFreshWaterModifier/>
		<iRiverModifier/>
		<iVP/>
		<iMaxCityCount/>
		<iMaxFamilyCount/>
		<iMaxPlayerCount/>
		<iCitySiteUnits/>
		<iUpgradeUnits/>
		<iDefendUnits/>
		<iUnitTurns/>
		<iUnitReligionDie/>
		<iUnitHeal/>
		<iLegitimacy/>
		<bBuild/>
		<bHolyCity/>
		<bTerritoryOnly/>
		<bUrban/>
		<bRequiresUrban/>
		<bTradeNetwork/>
		<bSpreadsBorders/>
		<bNoAdjacentReligion/>
		<bNoVegetation/>
		<bFreshWaterSource/>
		<bFreshWaterValid/>
		<bRiverValid/>
		<bRotateTowardsLand/>
		<bCoastValid/>
		<bWaterCoastValid/>
		<bCityValid/>
		<bHolyCityValid/>
		<bPermanent/>
		<bWonder/>
		<bHeal/>
		<bBonus/>
		<bCitySite/>
		<bBarbarian/>
		<bBlockUpgrade/>
		<bRemoveBorder/>
		<bRemoveBonus/>
		<NationPrereq/>
		<ReligionPrereq/>
		<CulturePrereq/>
		<AdjacentImprovementClassPrereq/>
		<ImprovementPrereq/>
		<RaiseImprovement/>
		<UpgradeImprovement/>
		<BonusImprovement/>
		<EffectCity/>
		<EffectPlayer/>
		<UnitDefend/>
		<Bonus/>
		<BonusCities/>
		<aiYieldCost/>
		<aiYieldOutput/>
		<aiYieldPillage/>
		<aiYieldFreshWaterModifier/>
		<aiYieldRiverModifier/>
		<aiTerrainModifier/>
		<aiHeightModifier/>
		<aiAdjacentHeightModifier/>
		<aiAdjacentImprovementModifier/>
		<aiAdjacentImprovementClassModifier/>
		<aiUnitTraitHeal/>
		<aiUnitTraitXP/>
		<aiUnitDie/>
		<aiBonusDie/>
		<abTerrainValid/>
		<abTerrainInvalid/>
		<abHeightValid/>
		<abHeightAdjacentValid/>
		<abVegetationValid/>
		<abNoBaseOutput/>
		<aeResourceAsset/>
		<aeUnitDefend/>
		<aaiTerrainYieldModifier/>
		<aaiHeightYieldModifier/>
		<aaiAdjacentHeightYieldModifier/>
		<aaiAdjacentImprovementYieldModifier/>
		<aaiBarbarianUnitDie/>
		<zAudioLoopWhenBuilding/>
		<zAudioSwitchName/>
	</Entry>"""
    for i in data['nations']:
        for o in data['nations'][i]['shrines']:
            output += generate_improvement(i, data['nations'][i]['shrines'][o])
    output = output + "\n</Root>\n"
    file = open(f"{data['file-preffix']}improvement{data['file-suffix']}.xml", "w")
    file.write(output)
    file.close()

def generate_text_improvement(name):
    return(f"""
	<Entry>
		<zType>TEXT_IMPROVEMENT_SHRINE_{dashandupper(name)}</zType>
		<English>Shrine of {name}</English>
	</Entry>""")

def generate_text_improvement_file(data):
    output = """<?xml version="1.0"?>
<Root>
	<!--Assets/GameAssets/Resources/Infos/improvement.xml-->
	<!--NOTE: improvement names that are mass nouns or plural do not need multiple types in English-->
	<Entry>
		<zType/>
		<English/>
	</Entry>"""
    for i in data['nations']:
        for o in data['nations'][i]['shrines']:
            output += generate_text_improvement(data['nations'][i]['shrines'][o]["deity"])
    output = output + "\n</Root>\n"
    file = open(f"{data['file-preffix']}text-improvement{data['file-suffix']}.xml", "w")
    file.write(output)
    file.close()

def generate_text_unit(unit):
    return(f"""
	<Entry>
		<zType>TEXT_UNIT_{dashandupper(unit['name'])}</zType>
		<English>{unit['name']}~{unit['singular']}~{unit['plural']}</English>
	</Entry>""")

def generate_text_unit_file(data):
    output = """<?xml version="1.0"?>
<Root>
	<!--Assets/GameAssets/Resources/Infos/improvement.xml-->
	<!--NOTE: improvement names that are mass nouns or plural do not need multiple types in English-->
	<Entry>
		<zType/>
		<English/>
	</Entry>"""
    for i in data['nations']:
        for o in data['nations'][i]['units']:
            output += generate_text_unit(data['nations'][i]['units'][o])
    output = output + "\n</Root>\n"
    file = open(f"{data['file-preffix']}text-unit{data['file-suffix']}.xml", "w")
    file.write(output)
    file.close()

def generate_goal(unit, nation):
    return(f"""
	<Entry>
		<zType>GOAL_TWO_{dashandupper(unit['name'])}</zType>
		<zName>Control Two {unit['plural'].capitalize()}</zName>
		<iAmbitionClass>17</iAmbitionClass>
		<iMinTier>{'5' if int(unit['rank']) == 2 else '3'}</iMinTier>
		<iMaxTier>{'3' if int(unit['rank']) == 2 else '5'}</iMaxTier>
		<TechPrereq>TECH_{dashandupper(unit['tech1'])}</TechPrereq>
		<NationPrereq>NATION_{dashandupper(nation)}</NationPrereq>
		<aiFamilyClassWeight>
			<Pair>
				<zIndex>FAMILY_CLASS_{dashandupper(unit['family'])}</zIndex>
				<iValue>1000</iValue>
			</Pair>
		</aiFamilyClassWeight>
		<aiDesiredWeight>
			<Pair>
				<zIndex>TRAIT_TACTICIAN_ARCHETYPE</zIndex>
				<iValue>1000</iValue>
			</Pair>
			<Pair>
				<zIndex>TRAIT_COMMANDER_ARCHETYPE</zIndex>
				<iValue>1000</iValue>
			</Pair>
			<Pair>
				<zIndex>TRAIT_HERO_ARCHETYPE</zIndex>
				<iValue>1000</iValue>
			</Pair>
		</aiDesiredWeight>
		<aiUnitCount>
			<Pair>
				<zIndex>UNIT_{dashandupper(unit['name'])}</zIndex>
				<iValue>2</iValue>
			</Pair>
		</aiUnitCount>
	</Entry>""")

def generate_goal_file(data):
    output = """<?xml version="1.0"?>
<Root>
	<!--Assets/GameAssets/Resources/Infos/improvement.xml-->
	<!--NOTE: improvement names that are mass nouns or plural do not need multiple types in English-->
	<Entry>
		<zType/>
		<zName/>
		<iAmbitionClass/>
		<iMaxTurns/>
		<iMinTier/>
		<iMaxTier/>
		<TechPrereq/>
		<TechObsolete/>
		<NationPrereq/>
		<EstablishTheology/>
		<StartLaw/>
		<iLegitimacy/>
		<iCities/>
		<iConnectedCities/>
		<iCitizens/>
		<iSpecialists/>
		<iPopulation/>
		<iPopulationHighest/>
		<iMilitaryHighest/>
		<iUrbanImprovements/>
		<iWonders/>
		<iLaws/>
		<iRevealLand/>
		<iMilitaryUnits/>
		<iMaxLevelUnits/>
		<iImprovementClassThreshold/>
		<iUnitThreshold/>
		<iPlayerCapturedData/>
		<iBarbsClearedData/>
		<iPlayerKilledData/>
		<iBarbsKilledData/>
		<bVictoryEligible/>
		<bStateReligion/>
		<aiFamilyClassWeight/>
		<aiDesiredWeight/>
		<aiDiplomacyCount/>
		<aiBarbsKilledData/>
		<aiYieldProducedData/>
		<aiYieldRate/>
		<aiYieldCount/>
		<aiImprovementCount/>
		<aiImprovementClassCount/>
		<aiCultureCount/>
		<aiCultureWonders/>
		<aiSpecialistCount/>
		<aiProjectCount/>
		<aiEffectCityCount/>
		<aiUnitCount/>
		<aiUnitTraitCount/>
		<aiUnitTraitMaxLevelCount/>
		<aiStatCount/>
		<aiStatCountData/>
		<aeTechsAcquired/>
		<aeThresholdImprovementClasses/>
		<aeThresholdUnits/>
	</Entry>"""
    for i in data['nations']:
        for o in data['nations'][i]['units']:
            output += generate_goal(data['nations'][i]['units'][o], i)
    output = output + "\n</Root>\n"
    file = open(f"{data['file-preffix']}goal-unit{data['file-suffix']}.xml", "w")
    file.write(output)
    file.close()

def generate_bonus(unit):
    return(f"""
	<Entry>
		<zType>BONUS_TECH_{dashandupper(unit['name'])}</zType>
		<aiUnits>
			<Pair>
				<zIndex>UNIT_{dashandupper(unit['name'])}</zIndex>
				<iValue>1</iValue>
			</Pair>
		</aiUnits>
	</Entry>""")

def generate_bonus_file(data):
    output = """<?xml version="1.0"?>
<Root>
	<Entry>
		<zType/>
		<zName/>
		<MemoryPlayer/>
		<ForgetPlayer/>
		<MemoryBarb/>
		<ForgetBarb/>
		<MemoryReligion/>
		<ForgetReligion/>
		<MemoryFamily/>
		<ForgetFamily/>
		<MemoryAllFamilies/>
		<MemoryCharacter/>
		<ForgetCharacter/>
		<DiplomacyPlayer/>
		<DiplomacyBarb/>
		<MakeCourtier/>
		<StartLaw/>
		<FreeLaw/>
		<FoundReligion/>
		<AdoptReligion/>
		<FreeTheology/>
		<Quest/>
		<Ambition/>
		<DesiredAmbition/>
		<Mission/>
		<Council/>
		<SetArchetype/>
		<SetNickname/>
		<SetVegetation/>
		<SetResource/>
		<SetImprovement/>
		<iRevealRange/>
		<iCitizens/>
		<iBorderGrowth/>
		<iCultureLevels/>
		<iDiscontentLevels/>
		<iRebelUnits/>
		<iDestroyImprovements/>
		<iHPCity/>
		<iHPUnit/>
		<iXPUnit/>
		<iXPCharacter/>
		<iLegitimacy/>
		<iDiplomacyPlayer/>
		<iMarrySubject/>
		<iAdoptedBySubject/>
		<iGovernorOfSubject/>
		<iGeneralOfSubject/>
		<iSpreadToSubject/>
		<iTradeResourceSubject/>
		<iMissionSubject/>
		<bRevealTerritory/>
		<bCancelTrade/>
		<bPlayerAlliance/>
		<bPlayerAllianceEnd/>
		<bBarbAlliance/>
		<bBarbAllianceEnd/>
		<bBarbInvade/>
		<bStateReligion/>
		<bStateReligionEnd/>
		<bFoundReligion/>
		<bStartLaw/>
		<bFreeLaw/>
		<bFreeTheology/>
		<bFreeTech/>
		<bNoCourtier/>
		<bLeaveCouncil/>
		<bReleaseGeneral/>
		<bChangeSuccession/>
		<bDivorce/>
		<bAbdicate/>
		<bSeizeThrone/>
		<bChosenHeir/>
		<bDoomCharacter/>
		<bKillCharacter/>
		<bHaveBastard/>
		<bKillUnit/>
		<bRemoveVegetation/>
		<aiCityYields/>
		<aiGlobalYieldsBase/>
		<aiGlobalYieldsPer/>
		<aiYieldsSendBase/>
		<aiYieldsSendPerUs/>
		<aiYieldsSendPerThem/>
		<aiYieldsExchangeBase/>
		<aiYieldsExchangePerUs/>
		<aiYieldsExchangePerThem/>
		<aiYieldsTradeBase/>
		<aiYieldsTradePerUs/>
		<aiYieldsTradePerThem/>
		<aiYieldsTributeBase/>
		<aiYieldsTributePerUs/>
		<aiYieldsTributePerThem/>
		<aiUnits/>
		<aiBonusUnits/>
		<aiLawOpinion/>
		<aiRatings/>
		<aiTraitDie/>
		<aeAddProjects/>
		<aeRemoveProjects/>
		<aeAddSpecialistClasses/>
		<aePromotions/>
		<aeAddTraits/>
		<aeRemoveTraits/>
		<aeTechs/>
		<aeCultureProject/>
		<aaiCultureYield/>
		<aeBonuses/>
		<aeFamilyBonuses/>
		<aeAllCityBonuses/>
		<DiplomacySubjects/>
		<AddRelationshipSubjects/>
		<AddRelationshipReverse/>
		<RemoveRelationshipSubjects/>
		<RemoveRelationshipReverse/>
		<AddCourtierGender/>
	</Entry>"""
    for i in data['nations']:
        for o in data['nations'][i]['units']:
            output += generate_bonus(data['nations'][i]['units'][o])
    output = output + "\n</Root>\n"
    file = open(f"{data['file-preffix']}bonus-unit{data['file-suffix']}.xml", "w")
    file.write(output)
    file.close()

def generate_tech(unit, nation):
    return(f"""
	<Entry>
		<zType>TECH_{dashandupper(unit["name"])}_BONUS</zType>
		<zName>Free {unit["name"].capitalise()}</zName>
		<zIconName>UNIT_{dashandupper(unit["icon"])}</zIconName>
		<BonusDiscover>BONUS_TECH_{dashandupper(unit["name"])}_UNIT</BonusDiscover>
		<iCost>{'1600' if int(unit['rank']) == 2 else '200'}</iCost>
		<bHide>1</bHide>
		<bTrash>1</bTrash>
		<bNoBonus>1</bNoBonus>
		<bSkipLog>1</bSkipLog>
		<abNationValid>
			<Pair>
				<zIndex>NATION_{dashandupper(nation)}</zIndex>
				<bValue>1</bValue>
			</Pair>
		</abNationValid>
		<abTechPrereq>
			<Pair>
				<zIndex>TECH_{dashandupper(unit["tech2"])}</zIndex>
				<bValue>1</bValue>
			</Pair>
		</abTechPrereq>
	</Entry>""")

def generate_tech_file(data):
    output = """<?xml version="1.0"?>
<Root>
	<!--Assets/GameAssets/Resources/Infos/improvement.xml-->
	<!--NOTE: improvement names that are mass nouns or plural do not need multiple types in English-->
	<Entry>
		<zType/>
		<zName/>
		<zIconName/>
		<BonusDiscover/>
		<EffectPlayer/>
		<iCost/>
		<iColumn/>
		<iRow/>
		<bHide/>
		<bTrash/>
		<bNoBonus/>
		<bSkipLog/>
		<bReturn/>
		<bValidAll/>
		<abNationValid/>
		<abTechPrereq/>
	</Entry>"""
    for i in data['nations']:
        for o in data['nations'][i]['units']:
            output += generate_goal(data['nations'][i]['units'][o], i)
    output = output + "\n</Root>\n"
    file = open(f"{data['file-preffix']}tech-unit{data['file-suffix']}.xml", "w")
    file.write(output)
    file.close()

def generate_text_effect_player(nation):
    return(f"""
    <Entry>
        <zType>TEXT_EFFECTPLAYER_NATION_{dashandupper(nation)}</zType>
        <English>{nation}</English>
    </Entry>""")

def generate_text_effect_player_file(data):
    output = """<?xml version="1.0" encoding="UTF-8"?>
<Root>
    <Entry>
        <zType/>
        <English/>
    </Entry>"""
    for i in data['nations']:
        output = output + generate_text_effect_city(data['nations'][i]['name'])
    output = output + "\n</Root>\n"
    file = open(f"{data['file-preffix']}text-effectPlayer{data['file-suffix']}.xml", "w")
    file.write(output)
    file.close()

def generate_text_effect_city(nation):
    return(f"""
    <Entry>
        <zType>TEXT_EFFECTCITY_NATION_{dashandupper(nation)}</zType>
        <English>{nation}</English>
    </Entry>""")

def generate_text_effect_city_file(data):
    output = """<?xml version="1.0" encoding="UTF-8"?>
<Root>
    <Entry>
        <zType/>
        <English/>
    </Entry>"""
    for i in data['nations']:
        output = output + generate_text_effect_city(data['nations'][i]['name'])
    output = output + "\n</Root>\n"
    file = open(f"{data['file-preffix']}text-effectCity{data['file-suffix']}.xml", "w")
    file.write(output)
    file.close()

def main():
    data = json.load(open("data.json"))
    generate_nation_file(data)
    generate_name_file(data)
    generate_map_elements_file(data)
    generate_family_file(data)
    generate_text_nation_file(data)
    generate_text_family_file(data)
    generate_team_color_file(data)
    generate_player_color_file(data)
    generate_color_file(data)
    generate_city_name_file(data)
    generate_improvement_file(data)
    generate_text_improvement_file(data)
    generate_text_unit_file(data)
    generate_goal_file(data)
    generate_bonus_file(data)
    generate_text_effect_player_file(data)
    generate_text_effect_city_file(data)

if __name__ == "__main__":
    main()
