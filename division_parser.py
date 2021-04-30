import re

class DivisionParser:

    division_descriptor_name_map = {
        'CAN_3CID_Dv2': '3rd Canadian Infantry',

        'FIN_Gr_Raappana_multi': 'Ryhmä Raappana',
        'FIN_Panssaridivisioona_multi': 'Panssaridivisioona',

        'FR_2e_DB_multi': '2e Blindée',

        'GR_116_Panzer_multi': '116 Panzer',
        'GR_11SS_Panzergrenadier_multi': '11. SS-Fr.-Panzergrenadier "Nordland"',
        'GR_122_Infanterie_multi': '122. Infanterie',
        'GR_12SS_Panzer_multi': '12. SS-Panzer "Hitlerjugend"',
        'GR_14_Inf_multi': '14. Infanterie',
        'GR_16_Panzer_multi': '16. Panzer',
        'GR_17SS_Panzergrenadier_multi': '17. SS-Panzergrenadier "Götz von B."',
        'GR_1_Fallschirmjager_multi': '1. Fallschirmjäger',
        'GR_1_Skijager_multi': '1. Skijäger',
        'GR_20_Panzer_multi': '20. Panzer',
        'GR_20_PzGren_multi': '20. Panzergrenadier',
        'GR_21_Panzer_multi': '21. Panzer',
        'GR_25_PzGren_multi': '25. Panzergrenadier',
        'GR_28_Jager_multi': '28. Jäger',
        'GR_352_Infanterie_multi': '352. Infanterie',
        'GR_3_Fallschirmjager_multi': '3. Fallschirmjäger',
        'GR_52_Sicherungs_multi': '52. Sicherungs z.b.V.',
        'GR_5SS_Panzer_multi': '5. SS-Panzer "Wiking"',
        'GR_5_Panzer_Dv2': '5. Panzer',
        'GR_78_Sturm_multi': '78. Sturm',
        'GR_Gr_Harteneck_multi': 'Gruppe Harteneck',
        'GR_Grossdeutschland_multi': 'Panzergrenadier "Großdeutschland"',
        'GR_Koruck_559_multi': 'Korück 559',
        'GR_Panzer_HG_multi': 'Fallschirm-Panzer "Hermann Göring"',
        'GR_Panzer_Lehr_multi': 'Panzer Lehr',
        'GR_Pzverbande_Strachwitz_multi': 'Panzerverband Strachwitz',

        'HO_1_Hussard_multi': '1. Lovas',
        'HO_5_Reserve_multi': '12. Tartalék',

        'NZ_2nd_NZ_multi': '2nd New-Zealand',

        'POL_1DI_AWP_multi': '1 Piechoty "Tadeusza Kościuszki"',
        'POL_1_Pancera_multi': '1 Pancerna',
        'POL_ArmiaKrajowa_multi': 'Armia Krajowa',

        'ROU_1_Blindata_multi': '1 Blindată "Romania Mare"',
        'ROU_4_Munte_multi': '4 Munte',
        'ROU_5_CavMot_multi': '5 Cavalerie Motorizată',

        'SOV_10CCharGd_multi': '10-y Gv. Tankovy Korpus',
        'SOV_126CFusMont_multi': '126-y L. Gronostrelkovy Korpus',
        'SOV_184DFusGd_multi': '184-ya Strelkovy',
        'SOV_19CChar_multi': '19-y Tankovy Korpus',
        'SOV_26DFusGd_multi': '26-ya Gvard. Strelkovy',
        'SOV_29CChar_multi': '29-y Tankovy Korpus',
        'SOV_2CCharGd_multi': '2-y Gv. Tankovy Korpus',
        'SOV_358DFusGd_multi': '358-ya Strelkovy',
        'SOV_3CCharGd_multi': '3-y Gv. Tankovy Korpus',
        'SOV_3CMechGd_multi': '3-y Gv. Mechanizi. Korpus',
        'SOV_3VDV_multi': '3-ya VDV',
        'SOV_43A_Reserve_multi': 'Rezerv 43-y Armii',
        'SOV_44DFusGd_multi': '44-ya Gvard. Strelkovy',
        'SOV_7CMech_multi': '7-y Mechanizi. Korpus',
        'SOV_7DFus_Esto_multi' : '7. Eesti Laskurdiviis',
        'SOV_84DFusGd_multi': '84-ya Gvard. Strelkovy',
        'SOV_97DFusGd_multi': '97-ya Gvard. Strelkovy',
        'SOV_9GCavGd_multi': '9-ya Gvard. Kavalerii',
        'SOV_GM_39A_multi': 'Podv. Gruppa Bezuglogo',
        'SOV_GM_Fedyunkin_multi': 'Podv. Gruppa Fedyunkina',
        'SOV_GM_Tyurin_multi': 'Podv. Gruppa Tyurina',
        'SOV_NavalGroup_Bakthin_multi': 'Morskaya Gruppa Bakhtina',
        'SOV_VyborgReserve_multi': 'Podv. Gruppa Vyborg',

        'UK_15Scot_multi': '15th Infantry',
        'UK_6_Airborne_multi': '6th Airborne',

        'US_2nd_Infantry_multi': '2nd Infantry "Indianhead"',
        'US_3rd_Armored_Dv2': '3rd Armored "Spearhead"',
    }

    non_std_division_descriptors = [
        ('Descriptor_Deck_Division_SOV_NavalGroup_Bakthin', 'SOV_NavalGroup_Bakthin_multi'),
        ('Descriptor_Deck_Division_GR_5_Panzer_Dv2', 'GR_5_Panzer_Dv2'),
        ('Descriptor_Deck_Division_US_3rd_Armored_Dv2', 'US_3rd_Armored_Dv2'),
        ('Descriptor_Deck_Division_CAN_3CID_Dv2', 'CAN_3CID_Dv2')
    ]

    divisions = {}
    last_div = None
    last_div_descriptor = None

    def parse(self, line: str):
        self.parse_division_names(line)
        self.parse_descriptor_id(line)
        self.parse_unit_packs(line)
        self.parse_alliance(line)
        self.parse_country_id(line)

    def parse_division_names(self, line):
        if line.startswith('export'):
            pattern = r'(^export Descriptor_Deck_Division_)(\w+_multi)(.*$)'
            matches = re.match(pattern, line)
            if matches:
                div_name = matches.group(2)
                self.add_division(div_name)
            else:
                for descriptor, div_name in self.non_std_division_descriptors:
                    if descriptor in line:
                        self.add_division(div_name)
                        break

    def add_division(self, div_name):
        if not div_name:
            return

        real_name = self.division_descriptor_name_map[div_name]

        self.divisions[real_name] = {
            'name': real_name,
            'GUID': None,
            'unit_packs': []
        }

        self.last_div = real_name
        self.last_div_descriptor = div_name

    def parse_descriptor_id(self, line):
        if line.startswith('DescriptorId = GUID:') and self.divisions[self.last_div]['GUID'] is None:
            self.divisions[self.last_div]['GUID'] = line.split('=')[1].strip().split(':')[1].strip('{}')

    def parse_unit_packs(self, line):

        if line.startswith('(~/Descriptor_Deck_Pack_TOE_'):
            parts = line.split(self.last_div_descriptor)
            if len(parts) > 1:
                pattern = r'^\_(\w+)_(\w{2,3})\, (\d)\)\,?$'
                matches = re.match(pattern, parts[1])

                if matches is not None:
                    unit_name = matches.group(1).replace('_', ' ')
                    amount = matches.group(3)

                    self.divisions[self.last_div]['unit_packs'].append({
                        'name': unit_name,
                        'amount': int(amount)
                    })

    def parse_alliance(self, line):
        if line.startswith('DivisionNationalite'):
            alliance = line.split('=')[1].strip().split('/')[1]
            if self.last_div is not None:
                self.divisions[self.last_div]['alliance'] = alliance

    def parse_country_id(self, line):

        if line.startswith('CountryId'):
            country = line.split('=')[1].strip(' "')

            if self.last_div is not None:
                self.divisions[self.last_div]['country'] = country
