import asyncio
import time
import enka
from enka.enums import ItemType, FightPropType, EquipmentType
# from enkanetwork import EnkaNetworkAPI
# from enkanetwork import EquipmentsType, DigitType
from enka_config import *
from pydantic import ValidationError

# UNCOMMENT THE DESIRED STATS IN THE CSV
desired_stats = {
    # 1: "Base HP",
    # 4: "Base ATK",
    # 7: "Base DEF",
    FightPropType.FIGHT_PROP_MAX_HP: "Max HP",
    FightPropType.FIGHT_PROP_CUR_ATTACK: "ATK",
    FightPropType.FIGHT_PROP_CUR_DEFENSE: "DEF",
    FightPropType.FIGHT_PROP_CRITICAL: "CRIT Rate",
    FightPropType.FIGHT_PROP_CRITICAL_HURT: "CRIT DMG",
    FightPropType.FIGHT_PROP_CHARGE_EFFICIENCY: "Energy Recharge",
    FightPropType.FIGHT_PROP_HEAL_ADD: "Healing Bonus",
    # 27: "Incoming Healing Bonus",
    FightPropType.FIGHT_PROP_ELEMENT_MASTERY: "Elemental Mastery",
    # 29: "Physical RES",
    FightPropType.FIGHT_PROP_PHYSICAL_ADD_HURT: "Physical DMG Bonus",
    FightPropType.FIGHT_PROP_FIRE_ADD_HURT: "Pyro DMG Bonus",
    FightPropType.FIGHT_PROP_ELEC_ADD_HURT: "Electro DMG Bonus",
    FightPropType.FIGHT_PROP_WATER_ADD_HURT: "Hydro DMG Bonus",
    FightPropType.FIGHT_PROP_GRASS_ADD_HURT: "Dendro DMG Bonus",
    FightPropType.FIGHT_PROP_WIND_ADD_HURT: "Anemo DMG Bonus",
    FightPropType.FIGHT_PROP_ROCK_ADD_HURT: "Geo DMG Bonus",
    FightPropType.FIGHT_PROP_ICE_ADD_HURT: "Cryo DMG Bonus",
    # 50: "Pyro RES",
    # 51: "Electro RES",
    # 52: "Hydro RES",
    # 53: "Dendro RES",
    # 54: "Anemo RES",
    # 55: "Geo RES",
    # 56: "Cryo RES",
    # 70: "Pyro Energy Cost",
    # 71: "Electro Energy Cost",
    # 72: "Hydro Energy Cost",
    # 73: "Dendro Energy Cost",
    # 74: "Anemo Energy Cost",
    # 75: "Cryo Energy Cost",
    # 76: "Geo Energy Cost",
}

async def main():
    async with enka.EnkaAPI() as client:
        cpt = 1
        error_uids = []
        header = ['uid', 'nickname', 'character', 'attack_lvl', 'skill_lvl', 'burst_lvl']
        for stat in desired_stats.values():
            header.append(stat)
        header.append('level')
        header.append('element')
        header.append('weapon')
        header.append('artifacts')
        writer = csv.writer(open(filename + '.csv', 'w', encoding='UTF8', newline=''))
        writer.writerow(header)

        for uid in uids:
            print('{} / {} : {}'.format(cpt, len(uids), uid), end="\r")
            cpt += 1

            for i in range(20):
                try:
                    data = await client.fetch_showcase(uid)
                    for character in data.characters:
                        line = []
                        line.append(uid)
                        line.append(data.player.nickname)

                        if character.id in traveler_ids:
                            line.append("Traveler")
                        else:
                            line.append(characters[str(character.id)]["name"])
                        j = 1
                        for skill in character.talents:
                            if j > 3:
                                print("There are more than 3 talents for " + characters[str(character.id)]["name"])
                            if (skill.name != "Illusory Torrent" and skill.name != "Kamisato Art: Senho"):
                                # line.append(skill.name)
                                line.append(skill.level)
                            else:
                                j += 1

                        for statId in desired_stats:
                            for stat_type, stat_object in character.stats.items():
                                if stat_type == statId:
                                    line.append(round(stat_object.value, 3))

                        line.append(character.level)
                        line.append(character.element.name.title())
                        line.append(character.weapon.name)
                        line.append(character.weapon.level)
                        mainstats = {
                            EquipmentType.FLOWER: "",
                            EquipmentType.FEATHER: "",
                            EquipmentType.SANDS: "",
                            EquipmentType.GOBLET: "",
                            EquipmentType.CIRCLET: ""
                        }
                        substats = {
                            "Flat HP": 0.00,
                            "Flat ATK": 0.00,
                            "Flat DEF": 0.00,
                            "HP": 0.00,
                            "ATK": 0.00,
                            "DEF": 0.00,
                            "CRIT Rate": 0.00,
                            "CRIT DMG": 0.00,
                            "Energy Recharge": 0.00,
                            "Flat Elemental Mastery": 0.00
                        }

                        artis = {}
                        for artifact in character.artifacts:
                            mainstats[artifact.equip_type] = artifact.main_stat.name
                            for substate in artifact.sub_stats:
                                if substate.is_percentage:
                                    substats[substate.name] += substate.value
                                else:
                                    substats["Flat " + substate.name] += substate.value
                            if artifact.set_name not in artis:
                                artis[artifact.set_name] = 1
                            else:
                                artis[artifact.set_name] += 1

                        for i in list(substats.keys())[3:]:
                            line.append(round(substats[i], 3))

                        for i in list(mainstats.keys())[2:]:
                            line.append(mainstats[i])

                        char_set = None
                        for set in artis:
                            if artis[set] >= 2:
                                if char_set != None:
                                    if set < char_set:
                                        char_set = set + ", " + char_set
                                    else:
                                        char_set += ", " + set
                                else:
                                    char_set = set
                        if len(artis) > 3:
                            if char_set != None:
                                char_set += ", Flex"
                            else:
                                char_set = "Flex"
                        elif len(artis) == 3 and "," not in char_set:
                            char_set += ", Flex"
                        line.append(char_set)
                        writer.writerow(line)
                    writer = csv.writer(open(filename + '.csv', 'a', encoding='UTF8', newline=''))
                    break
                # except TypeError as e:
                #     try:
                #         line = []
                #         line.append(uid)
                #         line.append(data.player.nickname)
                #         for j in range(20):
                #             line.append("")
                #         line.append(data.player.level)
                #         writer.writerow(line)
                #         writer = csv.writer(open(filename + '.csv', 'a', encoding='UTF8', newline=''))
                #         break
                #     except Exception as e:
                #         error_uids.append('{}: {}'.format(uid, e))
                #         break
                except asyncio.exceptions.TimeoutError as e:
                    time.sleep(1)
                    pass
                except ValidationError as e:
                    print('{}: {}'.format(uid, e))
                    exit()
                except Exception as e:
                    error_uids.append('{}: {}'.format(uid, e))
                    break

        print('\nFinished')

        if len(error_uids):
            print('Error with UIDs:')
            for i in error_uids:
                print(i)

asyncio.run(main())
