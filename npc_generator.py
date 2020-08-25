import math
import random
import re


class Skills:

    def __init__(self):
        super().__init__()
        self.career_list = None
        self.skills = {}

        self._set_skills()
        self._set_skill_points()

    def _set_skills(self):
        # 44, Career Skills
        if self.role == 'SOLO':
            self.career_list = ['Handgun', 'Melee', ('Weaponsmith', 2), 'Rifle', 'Athletics', 'Submachinegun',
                                ('Stealth', 2)]
            choice = random.choice(('Brawling', 'Martial Arts'))
            if choice == 'Martial Arts':
                martial_arts = (('Aikido', 3), ('Animal Kung Fu', 3), 'Boxing', ('Capoeria', 3), ('Choi Li Fut', 3),
                                'Judo', ('Karate', 2), ('Tae Kwon Do', 3), ('Thai Kick Boxing', 4), 'Wrestling')
                self.career_list.append(random.choice(martial_arts))
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

    def _set_skill_points(self):

        def student_t():
            # nu = 1: See https://www.johndcook.com/python_student_t_rng.html for the original code.
            x = random.gauss(0.0, 1.0)
            y = 2.0 * random.gammavariate(0.5, 2.0)
            return x / (math.sqrt(y))

        def point_value():
            # Add the random value (+ or -) to an average d10 roll
            value = int(student_t() + 5.5)
            if value < 1:
                value = 1
            elif value > 10:
                value = 10
            # Without an IP multiplier, skill value = skill points spent
            return value, value

        def point_value_multiplier(ip, total_points):
            # 53, IP Multipliers
            if total_points < ip:
                return 0, 0
            elif total_points == ip:
                return 1, ip
            else:
                points = float('inf')
                while points > total_points:
                    value = round(random.expovariate(0.3))
                    if value > 9:
                        value = 9
                    points = range(ip, 41, ip)[value]
                # Track both skill value and the skill points spent to attain that value
                return value + 1, points

        key_skills = {'SOLO': 'Combat Sense', 'CORPORATE': 'Resources', 'MEDIA': 'Credibility', 'NOMAD': 'Family',
                      'TECHIE': 'Jury Rig', 'COP': 'Authority', 'ROCKER': 'Charismatic Leadership',
                      'MEDTECHIE': 'Medical Tech', 'FIXER': 'Streetdeal', 'NETRUNNER': 'Interface'}

        total_points = 40
        # Key skill
        points = point_value()
        self.skills[key_skills[self.role]] = points[0]
        total_points -= points[1]
        # All other skills
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
        # Add remaining skill points to skills with no IP
        while total_points > 0:
            skill = random.choice(list(self.skills.keys()))
            if not isinstance(skill, tuple) and self.skills[skill] < 10:
                self.skills[skill] += 1
                total_points -= 1

        weapon_skills = ['Brawling', 'Melee', 'Handgun', 'Rifle', 'Submachinegun', ('Aikido', 3), ('Animal Kung Fu', 3),
                         'Boxing', ('Capoeria', 3), ('Choi Li Fut', 3), 'Judo', ('Karate', 2), ('Tae Kwon Do', 3),
                         ('Thai Kick Boxing', 4), 'Wrestling']

        if self.sp:
            print(self.skills)
            for weapon in weapon_skills:
                sp = self._random_sp()
                if weapon in self.skills and self.skills[weapon] < sp:
                    self.skills[weapon] = sp

    def _random_sp(self):
        sp = None
        if self.sp == 'E':
            sp = random.randint(1, 2)
        elif self.sp == 'D':
            sp = random.randint(3, 4)
        elif self.sp == 'C':
            sp = random.randint(5, 6)
        elif self.sp == 'B':
            sp = random.randint(7, 8)
        elif self.sp == 'A':
            sp = random.randint(9, 10)
        return sp


class Attributes:

    def __init__(self):
        super().__init__()
        self.roll_list = []
        self.attributes = {'INT': 0, 'REF': 0, 'TECH': 0, 'COOL': 0, 'ATTR': 0, 'MA': 0, 'LUCK': 0, 'BODY': 0, 'EMP': 0}

        self._create_attributes()
        self._set_attributes()
        self._set_reputation()

    def _create_attributes(self):
        # 30, Fast and Dirty Expendables
        for attribute in range(9):
            roll = 11
            while roll > 10:
                roll = random.randint(1, 6) + random.randint(1, 6)
            self.roll_list.append(roll)

        if self.ap:
            while sum(self.roll_list) > self.ap:
                index = random.choice(range(9))
                if self.roll_list[index] > 2:
                    self.roll_list[index] -= 1
            while sum(self.roll_list) < self.ap:
                index = random.choice(range(9))
                if self.roll_list[index] < 10:
                    self.roll_list[index] += 1

        self.roll_list.sort()

    def _set_attributes(self):
        # 26, Statistics
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
        elif self.role == 'TECHIE':
            high = ['TECH']
        else:  # self.role == 'MEDTECHIE' or self.role == 'COP'
            high = []

        attribute_list = ['INT', 'REF', 'TECH', 'COOL', 'ATTR', 'MA', 'LUCK', 'BODY', 'EMP']
        # Apply the highest roll values to role-specific attributes
        random.shuffle(high)
        for attribute in high:
            attribute_list.remove(attribute)
            self.attributes[attribute] = self.roll_list.pop()
        # Apply the remaining roll values to the remaining attributes
        random.shuffle(attribute_list)
        for attribute in attribute_list:
            self.attributes[attribute] = self.roll_list.pop()
        # 26, Movement Allowance
        run = self.attributes['MA'] * 9
        self.attributes['Run'] = f'{run}m'
        self.attributes['Leap'] = f'{int(run / 4)}m'
        # 29, Body Type
        kilos = self.attributes['BODY'] * 10
        self.attributes['Carry'] = f'{kilos} kg/{int(kilos * 2.205)} lbs'
        self.attributes['Lift'] = f'{kilos * 4} kg/{int(kilos * 4 * 2.205)} lbs'
        # 29, Body Type Modifier
        self.attributes['BTM'] = (0, 0, 0, 1, 1, 2, 2, 2, 3, 3, 4)[self.attributes['BODY']]

        self.attributes.update({'REFO': self.attributes['REF'], 'INTO': self.attributes['INT'],
                                'COOLO': self.attributes['COOL']})

    def _set_reputation(self):
        # 54-55, Another Kind of Experience: Reputation
        value = round(random.expovariate(0.5)) + 1
        if value > 10:
            value = 10
        if random.randint(1, 20) == 1:
            value = -value
        self.attributes['REP'] = value


class Character(Skills, Attributes):

    def __init__(self, role=None, ap=None, code=None):
        roles = ('SOLO', 'ROCKER', 'NETRUNNER', 'MEDIA', 'NOMAD', 'FIXER', 'COP', 'CORPORATE', 'TECHIE', 'MEDTECHIE')
        if not role:
            role = random.choice(roles)
        self.role = role.upper()
        self.ap = ap
        self.sp = None
        self.wa = None
        self.aa = None
        if code:
            self._parse_code(code)
        super().__init__()
        self.armor = {}
        self.weapon = None
        self.cybernetics = set()
        self.wounds = 0
        self.wound_type = None
        self.stunned = False
        self.fastdraw = False

        self._set_cyberware()
        self._set_armor_weapon()

        self.report()
        print(self.ap, self.sp, self.wa, self.aa)

    def facedown(self):
        # 55, Another Kind of Experience: Reputation
        d10 = random.randint(1, 10)
        return d10 + self.attributes['COOL'] + self.attributes['REP']

    def initiative(self):
        # 97, Rounds & Turn Order
        self.fastdraw = False
        d10 = random.randint(1, 10)
        # 81, Reflex Boosters
        # Regarding Sandevistan boosters, this implementation assumes the NPC always subvocalizes
        # exactly one turn before combat
        try:
            boost = int([item[-1] for item in self.cybernetics if item.startswith('Reflex')][0])
        except IndexError:
            boost = 0
        # 46, Combat Sense
        if self.role == 'SOLO':
            boost += self.skills['Combat Sense']
        total = d10 + self.attributes['REF'] + boost
        # 97, The Fast Draw or Snapshot
        # Apply if initiative is less than average and NPC is intelligent enough to consider using it
        if total < 11 and (random.random() * 10 <= self.attributes['INT']):
            self.fastdraw = True
            total += 3
        return total

    def attack(self):
        pass

    def damage(self, value, roll, ap=False):
        location = ('', 'Head', 'Torso', 'Torso', 'Torso', 'R. Arm', 'L. Arm', 'R. Leg', 'R. Leg', 'L. Leg', 'L. Leg')[
            roll]
        # 102, Armor Piercing Rounds
        if ap:
            value -= int(self.armor[location] / 2)
            value = int(value / 2)
        # 100-101, Armor
        else:
            value -= self.armor[location]
        if value > 0:
            # 102, Staged Penetration
            self.armor[location] -= 1
            value -= self.attributes['BTM']
            # 103, The Body Type Modifier
            if value < 1:
                value = 1
            # 103, Special Wound Cases
            if location == 'Head':
                value *= 2
            self._take_wound(value, roll)

    def _parse_code(self, code):
        pattern = '([A-E])?([1-5])?([A-E])?'
        m = re.match(pattern, code.upper())
        self.sp = m.group(1)
        self.wa = m.group(2)
        self.aa = m.group(3)

    def _take_wound(self, value, roll):
        # 103, Special Wound Cases
        if value > 8:
            if roll == 1:
                self._death()
            elif roll > 4:
                self._death_save(0)
        self.wounds += value
        if self.wounds < 5:
            self.wound_type = 'Light'
            self._stun_save(0)
        # 103, Wound Effects
        elif 4 < self.wounds < 9:
            if self.wound_type != 'Serious':
                self.wound_type = 'Serious'
                self.attributes['REF'] -= 2
            self._stun_save(1)
        elif 8 < self.wounds < 13:
            # Remove previous effect before applying new one
            if self.wound_type == 'Serious':
                self.attributes['REF'] += 2
            if self.wound_type != 'Critical':
                self.wound_type = 'Critical'
                for attribute in ('REF', 'INT', 'COOL'):
                    self.attributes[attribute] = round(self.attributes[attribute] / 2)
            self._stun_save(2)
        elif 12 < self.wounds:
            # Remove previous effect before applying new one
            if self.wound_type == 'Serious':
                self.attributes['REF'] += 2
            elif self.wound_type == 'Critical':
                for attribute in ('REF', 'INT', 'COOL'):
                    self.attributes[attribute] = self.attributes[f'{attribute}O']
            if self.wound_type != 'Mortal':
                self.wound_type = 'Mortal'
                for attribute in ('REF', 'INT', 'COOL'):
                    self.attributes[attribute] = round(self.attributes[attribute] / 3)
            if 12 < self.wounds < 17:
                stun, mortal = 3, 0
            elif 16 < self.wounds < 21:
                stun, mortal = 4, 1
            elif 20 < self.wounds < 25:
                stun, mortal = 5, 2
            elif 24 < self.wounds < 29:
                stun, mortal = 6, 3
            elif 28 < self.wounds < 33:
                stun, mortal = 7, 4
            elif 32 < self.wounds < 37:
                stun, mortal = 8, 5
            elif 36 < self.wounds < 41:
                stun, mortal = 9, 6
            else:
                self._death()
                return
            self._stun_save(stun)
            self._death_save(mortal)

    def _stun_save(self, stun):
        # 29, Save Number; 104, Stun/Shock Saves
        if random.randint(1, 10) > (self.attributes['BODY'] - stun):
            self.stunned = True
            overacting = random.choice(('screams, windmills arms and falls',
                                        'crumples like a rag doll',
                                        'spins around in place and falls',
                                        'clutches their wound, staggers and falls',
                                        'stares stupidly at their wound then falls',
                                        'slumps to the ground, moaning'))
            print(f'The {self.role.lower()} {overacting}.')
            return
        if self.stunned:
            self.stunned = False
            print(f'The {self.role.lower()} is back in the fight!')

    def _death_save(self, mortal):
        # 29, Save Number; 104, Very Important: Death Saves
        if random.randint(1, 10) > (self.attributes['BODY'] - mortal):
            self._death()

    def _death(self):
        if self.wounds < 41:
            self.wounds = 41
        print(f'The {self.role.lower()} is dead.')

    def _set_cyberware(self):

        if self.role == 'SOLO':
            total = 6
        else:
            total = 3

        while len(self.cybernetics) < total:
            roll = random.randint(0, 9)
            if roll == 0:
                optic_roll = random.randint(0, 5)
                cyberoptics = ('Infrared', 'Lowlight', 'Camera', 'Dartgun', 'Antidazzle', 'Targeting Scope')
                self.cybernetics.add(cyberoptics[optic_roll])
            elif roll == 1:
                limit = float('inf')
                cyberarm = ((weapons['Med Pistol'], 2), (weapons['Light Pistol'], 0), (weapons['Med Pistol'], 2),
                            (weapons['Light SMG'], 2), (weapons['V Hvy Pistol'], 4), (weapons['Hvy Pistol'], 4))
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
                cyberware = ('', '', '', weapons['Big Knucks'], weapons['Rippers'], weapons['Vampires'],
                             weapons["Slice N' dice"], 'Reflex Boost (Kerenzikov) +X', 'Reflex Boost (Sandevistan) +3',
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

        weapon = (weapons['Knife'],
                  weapons['Light Pistol'],
                  weapons['Med Pistol'],
                  weapons['Hvy Pistol'],
                  weapons['Hvy Pistol'],
                  weapons['Light SMG'],
                  weapons['Light Assault Rifle'],
                  weapons['Med Assault Rifle'],
                  weapons['Hvy Assault Rifle'],
                  weapons['Hvy Assault Rifle'])

        armor = (
            {'Name': 'Heavy Leather', 'Head': 0, 'Torso': 4, 'R. Arm': 4, 'L. Arm': 4, 'R. Leg': 4, 'L. Leg': 4,
             'EV': 0},
            {'Name': 'Armor Vest', 'Head': 0, 'Torso': 10, 'R. Arm': 0, 'L. Arm': 0, 'R. Leg': 0, 'L. Leg': 0, 'EV': 0},
            {'Name': 'Light Armor Jacket', 'Head': 0, 'Torso': 14, 'R. Arm': 14, 'L. Arm': 14, 'R. Leg': 0, 'L. Leg': 0,
             'EV': 0},
            {'Name': 'Light Armor Jacket', 'Head': 0, 'Torso': 14, 'R. Arm': 14, 'L. Arm': 14, 'R. Leg': 0, 'L. Leg': 0,
             'EV': 0},
            {'Name': 'Med Armor Jacket', 'Head': 0, 'Torso': 18, 'R. Arm': 18, 'L. Arm': 18, 'R. Leg': 0, 'L. Leg': 0,
             'EV': 1},
            {'Name': 'Med Armor Jacket', 'Head': 0, 'Torso': 18, 'R. Arm': 18, 'L. Arm': 18, 'R. Leg': 0, 'L. Leg': 0,
             'EV': 1},
            {'Name': 'Med Armor Jacket', 'Head': 0, 'Torso': 18, 'R. Arm': 18, 'L. Arm': 18, 'R. Leg': 0, 'L. Leg': 0,
             'EV': 1},
            {'Name': 'Hvy Armor Jacket', 'Head': 0, 'Torso': 20, 'R. Arm': 20, 'L. Arm': 20, 'R. Leg': 0, 'L. Leg': 0,
             'EV': 2},
            {'Name': 'Hvy Armor Jacket', 'Head': 0, 'Torso': 20, 'R. Arm': 20, 'L. Arm': 20, 'R. Leg': 0, 'L. Leg': 0,
             'EV': 2},
            {'Name': 'MetalGear', 'Head': 25, 'Torso': 25, 'R. Arm': 25, 'L. Arm': 25, 'R. Leg': 25, 'L. Leg': 25,
             'EV': 2})

        self.weapon = weapon[roll]
        self.armor = armor[roll]
        # 67, Body Armor
        self.attributes['REF'] -= self.armor['EV']

    def report(self):

        print(f'Role\n\t{self.role.title()}\n\tREP: {self.attributes["REP"]}')
        print(f'Weapon\n\t{self.weapon}')
        print(f'Armor\n\t{self.armor["Name"]}\n\t\tHead: {self.armor["Head"]}\t\tTorso: {self.armor["Torso"]}'
              f'\n\t\tArm: {self.armor["L. Arm"]}\t\tLeg: {self.armor["L. Leg"]}'
              f'\n\tBTM: -{self.attributes["BTM"]}\n\tSave: {self.attributes["BODY"]}')
        print('Cybernetics')
        for item in self.cybernetics:
            print('\t{}'.format(item))
        print('Attributes')
        attributes = ''
        for index, key in enumerate(self.attributes):
            attributes += f'\t{key}: {self.attributes[key]}'
            if key in ('COOL', 'EMP'):
                attributes += '\n'
            if key == 'Lift':
                break
        print(attributes)
        print('Skills')
        for k, v in self.skills.items():
            k = k[0] if isinstance(k, tuple) else k
            print('\t{}: {}'.format(k, v))
        print('-----------------------------------------------------------')
        return


class FNFF:

    def __init__(self, num=1, role=None, ap=None, code=None):

        for x in range(num):
            Character(role, ap, code)


weapons = {'Knife': 'Knife: Melee 0 P C 1d6 1m AP',
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

    FNFF(num=200, role='solo', ap=None, code='a1a')
