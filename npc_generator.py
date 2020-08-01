import math
import random


class Skills:

    def __init__(self):
        super().__init__()
        self.career_list = None
        self.skills = {}

        self._set_skills()
        self._set_skill_points()

    def _set_skills(self):

        if self.role == 'SOLO':
            self.career_list = ['Handgun', 'Melee', ('Weaponsmith', 2), 'Rifle', 'Athletics', 'Submachinegun',
                                ('Stealth', 2)]
            choice = random.choice(('Brawling', 'Martial Arts'))
            if choice == 'Martial Arts':
                martial_arts = (('Aikido', 3), ('Animal Kung Fu', 3), 'Boxing', ('Capoeria', 3), ('Choi Li Fut', 3),
                                'Judo', ('Karate', 2), ('Tae Kwon Do', 3), ('Thai Kick Boxing', 4), 'Wrestling')
                self.career_list.append('{}: {}'.format(choice, random.choice(martial_arts)))
            else:
                self.career_list.append(choice)
        elif self.role == 'CORPORATE':
            self.career_list = ['Human Perception', 'Education', 'Library Search', 'Social',
                                'Persuasion', 'Stock Market', 'Wardrobe & Style', 'Personal Grooming']
        elif self.role == 'MEDIA':
            self.career_list = ['Composition', 'Education', 'Persuasion', 'Human Perception',
                                'Social', 'Streetwise', 'Photo & Film', 'Interview']
        elif self.role == 'NOMAD':
            self.career_list = ['Endurance', 'Melee', 'Rifle', 'Drive', ('Basic Tech', 2),
                                'Wilderness Survival', 'Brawling', 'Athletics']
        elif self.role == 'TECHIE':
            self.career_list = [('Basic Tech', 2), ('CyberTech', 2), 'Teaching', 'Education', 'Electronics']
            tech_skills = (('Aero Tech', 2), ('AV Tech', 3), 'Cryotank Operation', ('Cyberdeck Design', 2),
                           ('Demolitions', 2), 'Disguise', ('Elect. Security', 2), 'First Aid', 'Forgery',
                           ('Gyro Tech', 3), 'Paint or Draw', 'Photo & Film', ('Pharmaceuticals', 2), 'Pick Lock',
                           'Pick Pocket', 'Play Instrument', ('Weaponsmith', 2))
            self.career_list.extend(random.sample(tech_skills, 3))
        elif self.role == 'COP':
            self.career_list = ['Handgun', 'Human Perception', 'Athletics', 'Education', 'Brawling', 'Melee',
                                'Interrogation', 'Streetwise']
        elif self.role == 'ROCKER':
            self.career_list = ['Perform', 'Wardrobe & Style', 'Composition', 'Brawling', 'Play Instrument',
                                'Streetwise', 'Persuasion', 'Seduction']
        elif self.role == 'MEDTECHIE':
            self.career_list = [('Basic Tech', 2), 'Diagnose', 'Education', 'Cryotank Operation', 'Library Search',
                                ('Pharmaceuticals', 2), 'Zoology', 'Human Perception']
        elif self.role == 'FIXER':
            self.career_list = ['Forgery', 'Handgun', 'Brawling', 'Melee', 'Pick Lock', 'Pick Pocket', 'Intimidate',
                                'Persuasion']
        else:  # self.role == 'NETRUNNER'
            self.career_list = [('Basic Tech', 2), 'Education', 'System Knowledge', ('CyberTech', 2),
                                ('Cyberdeck Design', 2), 'Composition', 'Electronics', 'Programming']

        self.career_list.append('Awareness/Notice')
        random.shuffle(self.career_list)

        return

    def _set_skill_points(self):

        def student_t():
            # nu = 1: See https://www.johndcook.com/python_student_t_rng.html for the original code.
            x = random.gauss(0.0, 1.0)
            y = 2.0 * random.gammavariate(0.5, 2.0)
            return x / (math.sqrt(y))

        def point_value():

            value = int(student_t() + 5.5)
            if value < 1:
                value = 1
            elif value > 10:
                value = 10
            return value, value

        def point_value_multiplier(ip, total_points):

            if total_points == 0:
                return 0, 0
            points = float('inf')
            while points > total_points:
                value = round(random.expovariate(0.3))
                if value > 9:
                    value = 9
                points = range(ip, 41, ip)[value]
            return value + 1, points

        key_skills = {'SOLO': 'Combat Sense', 'CORPORATE': 'Resources', 'MEDIA': 'Credibility', 'NOMAD': 'Family',
                      'TECHIE': 'Jury Rig', 'COP': 'Authority', 'ROCKER': 'Charismatic Leadership',
                      'MEDTECHIE': 'Medical Tech', 'FIXER': 'Streetdeal', 'NETRUNNER': 'Interface'}

        total_points = 40
        points = point_value()
        self.skills[key_skills[self.role]] = points[0]
        total_points -= points[1]

        for skill in self.career_list:
            if isinstance(skill, tuple):
                points = point_value_multiplier(skill[1], total_points)
            else:
                points = point_value()
            if points[1] <= total_points:
                self.skills[skill] = points[0]
                total_points -= points[1]
            else:
                self.skills[skill] = total_points
                total_points = 0
        if total_points > 0:
            self.skills[self.career_list[-1]] += total_points

        return


class Attributes:

    def __init__(self):
        super().__init__()
        self.roll_list = []
        self.attributes = {'INT': 0, 'REF': 0, 'TECH': 0, 'COOL': 0, 'ATTR': 0, 'MA': 0, 'LUCK': 0, 'BODY': 0, 'EMP': 0}

        self._create_attributes()
        self._set_attributes()
        self._set_reputation()

    def _create_attributes(self):

        for att in range(9):
            roll = 11
            while roll > 10:
                roll = random.randint(1, 6) + random.randint(1, 6)
            self.roll_list.append(roll)
        self.roll_list.sort()
        return

    def _set_attributes(self):

        if self.role == 'SOLO' or self.role == 'NOMAD':
            high = ['REF', 'COOL', 'BODY']
        elif self.role == 'ROCKER':
            high = ['REF', 'COOL', 'ATTR', 'BODY']
        elif self.role == 'NETRUNNER' or self.role == 'CORPORATE':
            high = ['INT']
        elif self.role == 'MEDIA':
            high = ['ATTR']
        elif self.role == 'FIXER':
            high = ['COOL']
        elif self.role == 'TECHI':
            high = ['TECH']
        else:  # self.role == 'MEDTECHIE' or self.role == 'COP'
            high = []

        attribute_list = ['INT', 'REF', 'TECH', 'COOL', 'ATTR', 'MA', 'LUCK', 'BODY', 'EMP']

        random.shuffle(high)
        for attribute in high:
            attribute_list.remove(attribute)
            self.attributes[attribute] = self.roll_list.pop()

        random.shuffle(attribute_list)
        for attribute in attribute_list:
            self.attributes[attribute] = self.roll_list.pop()

        run = self.attributes['MA'] * 9
        self.attributes['Run'] = f'{run}m'
        self.attributes['Leap'] = f'{int(run / 4)}m'
        kilos = self.attributes['BODY'] * 40
        self.attributes['Lift'] = f'{kilos} kg/{int(kilos * 2.205)} lbs'
        self.attributes['BTM'] = (0, 0, 0, 1, 1, 2, 2, 2, 3, 3, 4)[self.attributes['BODY']]

        return

    def _set_reputation(self):

        value = round(random.expovariate(0.5)) + 1
        if value > 10:
            value = 10
        if random.randint(1, 20) == 1:
            value = -value
        self.attributes['REP'] = value


class Character(Skills, Attributes):

    def __init__(self, role=None):
        self.roles = ('SOLO', 'ROCKER', 'NETRUNNER', 'MEDIA', 'NOMAD', 'FIXER', 'COP', 'CORPORATE', 'TECHIE',
                      'MEDTECHIE')
        if not role:
            role = random.choice(self.roles)
        self.role = role.upper()
        super().__init__()
        self.armor = None
        self.weapon = None
        self.cybernetics = set()
        self.damage = 0

        self._set_cyberware()
        self._set_armor_weapon()
        self.report()

    def facedown(self):

        d10 = random.randint(1, 10)
        return d10 + self.attributes['COOL'] + self.attributes['REP']

    def initiative(self):

        d10 = random.randint(1, 10)
        try:
            boost = int([item[-1] for item in self.cybernetics if item.startswith('Reflex')][0])
        except IndexError:
            boost = 0
        if self.role == 'SOLO':
            boost += self.skills['Combat Sense']
        return d10 + self.attributes['REF'] + boost

    def damage(self, value, location):
        pass

    def _set_cyberware(self):

        if self.role == 'SOLO':
            total = 6
        else:
            total = 3

        while len(self.cybernetics) < total:

            roll = random.randint(0, 9)

            if roll == 0:
                optic_roll = random.randint(0, 5)
                cyberoptics = ('Infrared', 'Lowlight', 'Camera', 'Dartgun',
                               'Antidazzle', 'Targeting Scope')
                self.cybernetics.add(cyberoptics[optic_roll])
            elif roll == 1:
                limit = float('inf')
                cyberarm = ((aw['Med Pistol'], 2), (aw['Light Pistol'], 0), (aw['Med Pistol'], 2),
                            (aw['Light SMG'], 2), (aw['V Hvy Pistol'], 4), (aw['Hvy Pistol'], 4))
                while limit > self.attributes['BTM']:
                    arm_roll = random.randint(0, 5)
                    limit = cyberarm[arm_roll][1]
                self.cybernetics.add(cyberarm[arm_roll][0])
            elif roll == 2:
                audio_roll = random.randint(0, 5)
                cyberaudio = ('Wearman', 'Radio Splice', 'Phone Link',
                              'Amplified Hearing', 'Sound Editing', 'Digital Recording Link')
                self.cybernetics.add(cyberaudio[audio_roll])
            else:
                cyberware = ('', '', '', aw['Big Knucks'], aw['Rippers'], aw['Vampires'], aw["Slice N' dice"],
                             f'Reflex Boost (Kerenzikov) +X', 'Reflex Boost (Sandevistan) +3',
                             'Nothing')
                if roll in (7, 8) and (cyberware[7] in self.cybernetics or cyberware[8] in self.cybernetics):
                    continue
                else:
                    self.cybernetics.add(cyberware[roll])

        self.cybernetics.discard('Nothing')
        self.cybernetics = list(self.cybernetics)
        self.cybernetics = [item.replace('X', str(random.randint(1, 2))) for item in self.cybernetics]
        return

    def _set_armor_weapon(self):

        roll = random.randint(0, 9)
        if self.role == 'NOMAD' or self.role == 'COP':
            roll += 2
        elif self.role == 'SOLO':
            roll += 3

        if roll > 9:
            roll = 9

        armor_weapon = (('Heavy Leather', aw['Knife']),
                        ('Armor Vest', aw['Light Pistol']),
                        ('Light Armor Jacket', aw['Med Pistol']),
                        ('Light Armor Jacket', aw['Hvy Pistol']),
                        ('Med Armor Jacket', aw['Hvy Pistol']),
                        ('Med Armor Jacket', aw['Light SMG']),
                        ('Med Armor Jacket', aw['Light Assault Rifle']),
                        ('Hvy Armor Jacket', aw['Med Assault Rifle']),
                        ('Hvy Armor Jacket', aw['Hvy Assault Rifle']),
                        ('MetalGear', aw['Hvy Assault Rifle']))

        armor_sp = (('Head: 0, Torso: 4, Arms: 4, Legs: 4', 0),
                    ('Head: 0, Torso: 10, Arms: 0, Legs: 0', 0),
                    ('Head: 0, Torso: 14, Arms: 14, Legs: 0', 0),
                    ('Head: 0, Torso: 14, Arms: 14, Legs: 0', 0),
                    ('Head: 0, Torso: 18, Arms: 18, Legs: 0', 1),
                    ('Head: 0, Torso: 18, Arms: 18, Legs: 0', 1),
                    ('Head: 0, Torso: 18, Arms: 18, Legs: 0', 1),
                    ('Head: 0, Torso: 20, Arms: 20, Legs: 0', 2),
                    ('Head: 0, Torso: 20, Arms: 20, Legs: 0', 2),
                    ('Head: 25, Torso: 25, Arms: 25, Legs: 25', 2))

        self.armor = f'{armor_weapon[roll][0]} SP: {armor_sp[roll][0]}'
        self.weapon = armor_weapon[roll][1]
        self.attributes['REF'] -= armor_sp[roll][1]

        return

    def report(self):

        print('Role\n\t{}'.format(self.role.title()))
        print('Weapon\n\t{}'.format(self.weapon))
        print('Armor\n\t{}\n\tBTM: -{}\n\tSave: {}'.format(self.armor, self.attributes['BTM'], self.attributes['BODY']))
        print('Cybernetics')
        for item in self.cybernetics:
            print('\t{}'.format(item))
        print('Attributes')
        print('\tINT: {}\tREF: {}\tTECH: {}\tCOOL: {}\n\tATTR: {}\tMA: {}\tLUCK: {}\tBODY: {}\n\tEMP: {}'
              '\t REP: {}\n\tRun: {}\tLeap: {}\tLift: {}'.format(self.attributes['INT'],
                                                                 self.attributes['REF'],
                                                                 self.attributes['TECH'],
                                                                 self.attributes['COOL'],
                                                                 self.attributes['ATTR'],
                                                                 self.attributes['MA'],
                                                                 self.attributes['LUCK'],
                                                                 self.attributes['BODY'],
                                                                 self.attributes['EMP'],
                                                                 self.attributes['REP'],
                                                                 self.attributes['Run'],
                                                                 self.attributes['Leap'],
                                                                 self.attributes['Lift']))
        print('Skills')
        for k, v in self.skills.items():
            k = k[0] if isinstance(k, tuple) else k
            print('\t{}: {}'.format(k, v))
        print('-----------------------------------------------------------')
        return


class Characters(object):

    def __init__(self, num=1, role=None):

        for x in range(num):
            if role:
                Character(role)
            else:
                Character()
        return


aw = {'Knife': 'Knife: Melee 0 P C 1d6 1m AP',
      'Big Knucks': 'Big Knucks: Melee 1d6+2 1m',
      "Slice N' dice": "Slice N' dice: Melee 2d6 Mono",
      'Rippers': 'Rippers: Melee 1d6+3 AP',
      'Vampires': 'Vampires: Melee 1d6/3',
      'Light Pistol': random.choice(('BudgetArms C-13: P -1 P E 1d6(5mm) 8 2 ST',
                                     'Dai Lung Cybermag 15: P -1 P C 1d6+1(6mm) 10 2 UR',
                                     'Federated Arms X-22: P 0 J E 1d6+1(6mm) 10 2 ST')),
      'Med Pistol': random.choice(('Militech Arms Avenger: P 0 J E 2d6+1(9mm) 10 2 VR',
                                   'Dai Lung Streetmaster: P 0 J E 2d6+3(10mm) 12 2 UR',
                                   'Federated Arms X-9mm: P 0 J E 2d6+1(9mm) 12 2 ST')),
      'Hvy Pistol': random.choice(('BudgetArms Auto 3: P -1 J E 3d6(11mm) 8 2 UR',
                                   'Sternmeyer Type 35: P 0 J C 3d6(11mm) 8 2 VR')),
      'Light SMG': random.choice(('Uzi Miniauto 9: SMG +1 J E 2d6+1(9mm) 30 35 VR',
                                  'H&K MP-2013: SMG +1 J C 2d6+3(10mm) 35 32 ST',
                                  'Federated Arms Tech Assault II: SMG +1 j c 1D6(6MM) 50 25 ST')),
      'V Hvy Pistol': random.choice(('Armalite 44: P 0 J E 4d6+1(12mm) 8 1 ST',
                                     'Colt AMT Model 2000: P 0 J C 4d6+1(12mm) 8 1 VR')),
      'Light Assault Rifle': 'Militech Ronin Light Assault: RIF +1 N C 5d6(5.56) 35 30 VR',
      'Med Assault Rifle': 'AKR-20 Medium Assault: RIF 0 N C 5d6(5.56) 30 30 ST',
      'Hvy Assault Rifle': random.choice(('FN-RAL Heavy Assault Rifle: RIF -1 N C 6d6+2(7.62) 30 30 VR',
                                          'Kalishnikov A-80 Hvy. Assault Rifle: '
                                          'RIF -1 N E 6d6+2(7.62) 35 25 ST'))}

if __name__ == '__main__':
    Characters(num=30, role='SOLO')
