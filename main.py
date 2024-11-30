#basketgame
#0.0.0

'''
You start the game with the possession ->

OFFENSIVE LOOP

you get the option to drive, pass, or shoot from 3 ->
drive uses stats from your defender's int-defense stats and your layup % to determine outcome (math tbd) - >
pass prompts you with who to pass to. Pass outcome determined with your TOV% and the player you're passing too's defender's interception stats ->
    pass receiver semi-randomly decides whether to pass, shoot, or defend (light influence by IRL stats)
shooting outcome determined via your 3pt stats and defender's perimeter defense stats



'''

#PLACEHOLDER STATS: 0.20 PASSING FOR SG, 0.4 FOR PG, 0.1 FOR ALL ELSE. FG% used for drivinglay

#amir coffey turnover stat derived from 7 possessions a game average, with 0.5 turnovers a game = 1/14 possesions turned over

# PASSING STAT UNUSED

import random
import time
from KermLib import *
from ascii import *

version = '2024.11.29.1500.alpha'

class BasketballPlayer():
    def __init__(self, name, position, positionnumber, team, threept, passing, drivinglay, tov, perd, intd, interception, passpref, possession, defender, player, points_made, passes_made, interceptions_made):
        self.name = name
        self.position = position
        self.positionnumber = positionnumber
        self.team = team
        self.threept = threept
        self.passing = passing
        self.tov = tov
        self.drivinglay = drivinglay
        self.perd = perd
        self.intd = intd
        self.interception = interception
        self.passpref = passpref
        self.haspossession = possession
        self.defender = defender
        self.isplayer = player
        self.pointsMade = points_made
        self.passesMade = passes_made
        self.interceptionsMade = interceptions_made



    def commentator_randomizer(self, event, secondary_player):
        if event == '3ptshot':
            last_name = self.name.split(" ")[1]
            announcer_call = random.randint(1, 7)
            if announcer_call == 1:
                print(self.name, 'fires it from deep!')
            elif announcer_call == 2:
                print(self.name, 'lets it fly!')
            elif announcer_call == 3:
                print(self.name, 'from downtown!')
            elif announcer_call == 4:
                print(self.name, 'steps back and pulls from three!')
            elif announcer_call == 5:
                print('Corner three from', last_name + '!')
            elif announcer_call == 6:
                print(last_name, 'fires a three!')
            else:
                print(self.name, 'pulls up from beyond the arc!')

        elif event == '3ptmake':
            announcer_call = random.randint(1, 5)
            if announcer_call == 1:
                print('Count it!')
            elif announcer_call == 2:
                print('Bang!')
            elif announcer_call == 3:
                print('BANG! BANG! WHAT A SHOT FROM', self.name.upper() + '!')
            elif announcer_call == 4:
                print('And he sinks the three!')
            else:
                print('NOTHING BUT NET!')

        elif event == '3ptmiss':
            announcer_call = random.randint(1, 6)
            if announcer_call == 1:
                print('And airballs!', self.defender.name, 'gathers it up.')
            elif announcer_call == 2:
                print('And the shot is off the mark.')
            elif announcer_call == 3:
                print('And he bricks it!', self.defender.name, 'brings it back up for the', self.defender.team + '.')
            elif announcer_call == 4:
                print('And he misfires.', self.defender.name, 'with the rebound.')
            elif announcer_call == 5:
                print('SMOTHERED BY', self.defender.name.upper() + '!')
            else:
                print('And the ball clanks off the rim.')

        elif event == 'drive':
            defender_last_name = self.defender.name.split(" ")[1]
            last_name = self.name.split(" ")[1]
            announcer_call = random.randint(1, 6)
            if announcer_call == 1:
                print(self.name, 'drives into the paint!')
            elif announcer_call == 2:
                print('Here comes ' + self.name + '!')
            elif announcer_call == 3:
                print(self.name, 'drives the lane!')
            elif announcer_call == 4:
                print(self.name, 'cuts to the hoop!')
            elif announcer_call == 5:
                print(last_name, 'spins past', defender_last_name + '!' )
            else:
                print(self.name, 'slashes to the basket!')
        
        elif event == 'drivemake':
            announcer_call = random.randint(1, 5)
            if announcer_call == 1:
                print('And he rattles it in!')
            elif announcer_call == 2:
                print('AND HE SLAMS IT DOWN!')
            elif announcer_call == 3:
                print('And he lays it up and in!')
            elif announcer_call == 4:
                print('And he brings the house down!')
            else:
                print('And he kisses it off the glass!')

        elif event == 'miss':
            defender_last_name = self.defender.name.split(" ")[1]
            last_name = self.name.split(" ")[1]
            announcer_call = random.randint(1, 5)
            if announcer_call == 1:
                print('And the ball rims out!', defender_last_name, 'recovers it.')
            elif announcer_call == 2:
                print('A BACKBOARD BLOCK BY', self.defender.name.upper() + '!')
            elif announcer_call == 3:
                print('And he bricks it!', self.defender.name, 'brings it back up for the', self.defender.team + '.')
            elif announcer_call == 4:
                print('And that layup by', last_name, 'is no good.')
            else:
                print('And the ball clanks off the rim.')
        
        elif event == 'pass':
            last_name = self.name.split(" ")[1]
            pass_receiver_last_name = secondary_player.name.split(" ")[1]
            announcer_call = random.randint(1, 8)
            if announcer_call == 1:
                print('And he kicks it out to ' + pass_receiver_last_name + '!')
            elif announcer_call == 2:
                print('He swings it out to ' + secondary_player.name + '!')
            elif announcer_call == 3:
                print('Out to ' + pass_receiver_last_name + '!')
            elif announcer_call == 4:
                print('And he feeds it to ' + secondary_player.name + '!')
            elif announcer_call == 5:
                print(last_name + ', bounce pass to', pass_receiver_last_name + '!')
            elif announcer_call == 6:
                print(last_name + ' finds', pass_receiver_last_name + '!')
            elif announcer_call == 7:
                print('Bullet pass to ' + pass_receiver_last_name + '!')
            else:
                print('Bullet pass to ' + secondary_player.name + '!')
        
        elif event == 'stolen':
            announcer_call = random.randint(1, 5)
            if announcer_call == 1:
                print('Stolen by ' + secondary_player.defender.name + '!')
            elif announcer_call == 2:
                print('Stripped away by ' + secondary_player.defender.name + '!')
            elif announcer_call == 3:
                print('Swiped away by ' + secondary_player.defender.name + '!')
            elif announcer_call == 4:
                print('And ' + secondary_player.defender.name + ' intercepts it!')
            else:
                print(self.name, 'turns it over!', secondary_player.defender.name, 'brings it back up the court!')






    def decision(self):
        generated_probability = random.randint(1, 100)
        modified_probability  = generated_probability * (1 + self.passpref)
        if 81 > modified_probability >= 33.3:
            return 'pass'
        elif 150 >= modified_probability >= 81:
            return '3pt'
        else:
            return 'drive'
    
    def action_success(self, decision, defender_perd, defender_intd, pass_receiver_preset, active_team):
        if decision == '3pt':
            self.commentator_randomizer('3ptshot', None)
            make_chance = 10 - ( random.uniform(1, 4) * (1 + self.threept) ) - ( 1.5 + defender_perd ) * 1.5
            if make_chance > 4.8:
                self.commentator_randomizer('3ptmake', None)
                print(harden_shooting)
                self.pointsMade += 3
                self.haspossession = False
                self.defender.haspossession = True
                return 'shot', 3
            else:
                self.commentator_randomizer('3ptmiss', None)
                self.haspossession = False
                self.defender.haspossession = True
                return 'miss', 0

        if decision == 'drive':
            self.commentator_randomizer('drive', None)
                
            make_chance = 10 - ( random.uniform(1, 4) * (1 + self.drivinglay) ) - ( 1 + defender_intd ) * 1.5
            if make_chance > 3.8:
                self.commentator_randomizer('drivemake', None)
                print(lebron_dwyane)
                self.pointsMade += 2
                self.haspossession = False
                self.defender.haspossession = True
                return 'shot', 2
            else:
                self.commentator_randomizer('miss', None)
                self.haspossession = False
                self.defender.haspossession = True
                return 'miss', 0
            
        if decision == 'pass':


            if pass_receiver_preset:
                if calculate_turnover_chance(self, pass_receiver_preset.defender) is False: 
                    self.commentator_randomizer('pass', pass_receiver_preset)

                    self.passesMade += 1
                    pass_receiver_preset.haspossession = True
                    self.haspossession = False
                    return 'miss', 0
                else:
                    self.commentator_randomizer('pass', pass_receiver_preset)
                    self.commentator_randomizer('stolen', pass_receiver_preset)

                    pass_receiver_preset.defender.interceptionsMade += 1
                    pass_receiver_preset.defender.haspossession = True
                    self.haspossession = False
                    return 'miss', 0
            else:
                while True:
                    pass_receiver_position_number = random.randint(1, 5)
                    if self.positionnumber != pass_receiver_position_number:
                        break
                if active_team == user_team:
                    for pass_receiver in user_team_list:
                        if pass_receiver.positionnumber == pass_receiver_position_number:
                            break
                    if calculate_turnover_chance(self, pass_receiver.defender) is False: 
                        self.commentator_randomizer('pass', pass_receiver)
                        print(haliburton)

                        self.passesMade += 1
                        pass_receiver.haspossession = True
                        self.haspossession = False
                        return 'miss', 0
                    else:
                        self.commentator_randomizer('pass', pass_receiver)
                        self.commentator_randomizer('stolen', pass_receiver)

                        pass_receiver.defender.interceptionsMade += 1
                        pass_receiver.defender.haspossession = True
                        self.haspossession = False
                        return 'miss', 0

                else:
                    for pass_receiver in opposing_team_list:
                        if pass_receiver.positionnumber == pass_receiver_position_number:
                            break
                    if calculate_turnover_chance(self, pass_receiver.defender) is False: # PLACEHOLDER, NEEDS TO INCORPORATE STATS
                        self.commentator_randomizer('pass', pass_receiver)
                        print(haliburton)

                        self.passesMade += 1
                        pass_receiver.haspossession = True
                        self.haspossession = False
                        return 'miss', 0
                    else:
                        self.commentator_randomizer('pass', pass_receiver)
                        self.commentator_randomizer('stolen', pass_receiver)

                        pass_receiver.defender.interceptionsMade += 1
                        pass_receiver.defender.haspossession = True
                        self.haspossession = False
                        return 'miss', 0

                            


                                



                



#placeholder stats for James Harden, Austin Reaves, Ivica Zubac, Anthony Davis, Rui Hachimura, Kawhi Leonard, Norman Powell and Lebron James

d_knecht = BasketballPlayer("Dalton Knecht", "Shooting Guard", 2, "Los Angeles Lakers", .481, 0.25, 0.521, 0.143, 0.25, 0.1, 0.04, 0.2, False, None, False, 0, 0, 0)
a_coffey = BasketballPlayer("Amir Coffey", "Shooting Guard", 2, "LA Clippers", .381, 0.25, 0.554, 0.071, 0, 0, 0.086, 0.25, False, None, False, 0, 0, 0)
j_brown = BasketballPlayer("Jaylen Brown", "Shooting Guard", 2, "Boston Celtics", .480, .335, .765, .120, .180, .050, .060, .200, False, None, False, 0, 0, 0)
m_bridges = BasketballPlayer("Mikal Bridges", "Shooting Guard", 2, "New York Knicks", 0.410, 0.65, 0.68, 0.11, 0.22, 0.18, 0.10, 0.30, False, None, False, 0, 0, 0)


j_harden = BasketballPlayer("James Harden", "Point Guard", 1, "LA Clippers", .400, 0.85, 0.65, 0.15, 0.30, 0.25, 0.12, 0.6, False, None, False, 0, 0, 0)
a_reaves = BasketballPlayer("Austin Reaves", "Point Guard", 1, "Los Angeles Lakers", .390, 0.75, 0.60, 0.09, 0.20, 0.18, 0.09, 0.4, False, None, False, 0, 0, 0)
j_holiday = BasketballPlayer("Jrue Holiday", "Point Guard", 1, "Boston Celtics", .480, .429, .833, .120, .180, .080, .090, .160, False, None, False, 0, 0, 0)
j_brunson = BasketballPlayer("Jalen Brunson", "Point Guard", 1, "New York Knicks", 0.470, 0.75, 0.70, 0.09, 0.28, 0.22, 0.12, 0.40, False, None, False, 0, 0, 0)


a_davis = BasketballPlayer("Anthony Davis", "Center", 5, "Los Angeles Lakers", .350, 0.30, 0.72, 0.12, 0.25, 0.28, 0.15, 0.3, False, None, False, 0, 0, 0)
i_zubac = BasketballPlayer("Ivica Zubac", "Center", 5, "LA Clippers", .310, 0.20, 0.60, 0.10, 0.18, 0.22, 0.14, 0.25, False, None, False, 0, 0, 0)
k_porzingis = BasketballPlayer("Kristaps Porzingis", "Center", 5, "Boston Celtics", .498, .385, .850, .120, .180, .190, .070, .220, False, None, False, 0, 0, 0)
k_towns = BasketballPlayer("Karl-Anthony Towns", "Center", 5, "New York Knicks", 0.370, 0.15, 0.75, 0.08, 0.18, 0.28, 0.20, 0.30, False, None, False, 0, 0, 0)


r_hachimura = BasketballPlayer("Rui Hachimura", "Power Forward", 4, "Los Angeles Lakers", .370, 0.35, 0.60, 0.10, 0.22, 0.20, 0.10, 0.3, False, None, False, 0, 0, 0)
k_leonard = BasketballPlayer("Kawhi Leonard", "Power Forward", 4, "LA Clippers", .420, 0.45, 0.64, 0.08, 0.35, 0.45, 0.18, 0.35, False, None, False, 0, 0, 0)
a_horford = BasketballPlayer("Al Horford", "Power Forward", 4, "Boston Celtics", .470, .380, .820, .130, .180, .100, .060, .140, False, None, False, 0, 0, 0)
p_achiuwa = BasketballPlayer("Precious Achiuwa", "Power Forward", 4, "New York Knicks", 0.460, 0.45, 0.70, 0.10, 0.30, 0.32, 0.15, 0.40, False, None, False, 0, 0, 0)


n_powell = BasketballPlayer("Norman Powell", "Small Forward", 3, "LA Clippers", .380, 0.40, 0.66, 0.10, 0.20, 0.18, 0.12, 0.3, False, None, False, 0, 0, 0)
l_james = BasketballPlayer("LeBron James", "Small Forward", 3, "Los Angeles Lakers", .450, 0.80, 0.70, 0.12, 0.50, 0.50, 0.20, 0.5, False, None, False, 0, 0, 0)
j_tatum = BasketballPlayer("Jayson Tatum", "Small Forward", 3, "Boston Celtics", .473, .354, .854, .091, .200, .100, .060, .250, False, None, False, 0, 0, 0)
o_anunoby = BasketballPlayer("OG Anunoby", "Small Forward", 3, "New York Knicks", 0.450, 0.60, 0.65, 0.12, 0.24, 0.20, 0.14, 0.35, False, None, False, 0, 0, 0)

#initializing defenders


#adding to lists

clippers_list = [j_harden, a_coffey, n_powell, k_leonard, i_zubac]
lakers_list = [a_reaves, d_knecht, l_james, r_hachimura, a_davis]
celtics_list = [j_holiday, j_brown, j_tatum, a_horford, k_porzingis]
knicks_list = [j_brunson, m_bridges, o_anunoby, p_achiuwa, k_towns]

# ------------------------------------------------------------------------------------------------------------------

def calculate_turnover_chance(passer, receiver_defender):
    """
    Calculate the chance of a turnover during a pass.
    Factors include passer's turnover tendency, passing skill, and receiver defender's interception skill.
    """
    # Adjusted base chance and scaling factors for better dynamics
    base_chance = 0.05  # Lower base chance for turnover (5%)
    
    # More fine-tuned weights for player attributes
    turnover_factor = passer.tov * 15  # Passer's turnover tendency (scaled down)
    passing_factor = passer.passing * -12  # Higher impact for good passing skills
    interception_factor = receiver_defender.interception * 20  # Defender's interception skill (scaled to balance)
    
    # Adding a dynamic component for randomness within a range based on the passer's passing skill
    dynamic_factor = random.uniform(-0.02, 0.02) * (1 - passer.passing)
    
    # Calculate turnover chance
    turnover_chance = base_chance + turnover_factor + passing_factor + interception_factor + dynamic_factor
    
    # Ensure the value stays within a meaningful range (0% to 40%)
    turnover_chance = max(0.0, min(0.4, turnover_chance))
    
    # Determine if the pass is turned over
    random_roll = random.random()  # Random number between 0 and 1
    if random_roll < turnover_chance:
        return True  # Pass is turned over
    else:
        return False  # Pass is successful


def turn_over_chance(passer, receiver_defender):
    base_chance = 0.10  # Base chance for turnover (10%)
    
    turnover_factor = passer.tov * 25
    passing_factor = passer.passing * -7.8
    interception_factor = receiver_defender.interception * 25
    
    turnover_chance = base_chance + turnover_factor + passing_factor + interception_factor
    # Clamp the value between 0 and 1
    turnover_chance = max(0.1, min(0.25, turnover_chance))
    return turnover_chance * 100




KermLib.ascii_run()
print('Blacktop ' + version + '\n')

print('Select your team! 1 for the LA Clippers, 2 for the Los Angeles Lakers, 3 for the Boston Celtics, 4 for the New York Knicks')
user_team_input = KermLib.get_user_input(['1', '2', '3', '4'])

print('\n')
if user_team_input == '1':
    user_team = 'LA Clippers'
    user_team_list = clippers_list
elif user_team_input == '2':
    user_team = 'Los Angeles Lakers'
    user_team_list = lakers_list
elif user_team_input == '3':
    user_team = 'Boston Celtics'
    user_team_list = celtics_list
elif user_team_input == '4':
    user_team = 'New York Knicks'
    user_team_list = knicks_list


if user_team == 'LA Clippers':
    print('Select your opposing team! 2 for the Los Angeles Lakers, 3 for the Boston Celtics, 4 for the New York Knicks')
    user_decision = KermLib.get_user_input(['2', '3', '4'])
    if user_decision == '2':
        opposing_team_list = lakers_list
        opposing_team = 'Los Angeles Lakers'
    elif user_decision == '3':
        opposing_team_list = celtics_list
        opposing_team = 'Boston Celtics'
    elif user_decision == '4':
        opposing_team_list = knicks_list
        opposing_team = 'New York Knicks'

elif user_team == 'Los Angeles Lakers':
    print('Select your opposing team! 1 for the LA Clippers, 3 for the Boston Celtics, 4 for the New York Knicks')
    user_decision = KermLib.get_user_input(['1', '3', '4'])
    if user_decision == '1':
        opposing_team_list = clippers_list
        opposing_team = 'LA Clippers'
    elif user_decision == '3':
        opposing_team_list = celtics_list
        opposing_team = 'Boston Celtics'
    elif user_decision == '4':
        opposing_team_list = knicks_list
        opposing_team = 'New York Knicks'

elif user_team == 'Boston Celtics':
    print('Select your opposing team! 1 for the LA Clippers, 2 for the Los Angeles Lakers, 4 for the New York Knicks')
    user_decision = KermLib.get_user_input(['1', '2', '4'])
    if user_decision == '1':
        opposing_team_list = clippers_list
        opposing_team = 'LA Clippers'
    elif user_decision == '2':
        opposing_team_list = lakers_list
        opposing_team = 'Los Angeles Lakers'
    elif user_decision == '4':
        opposing_team_list = knicks_list
        opposing_team = 'New York Knicks'

elif user_team == 'New York Knicks':
    print('Select your opposing team! 1 for the LA Clippers, 2 for the Los Angeles Lakers, 3 for the Boston Celtics')
    user_decision = KermLib.get_user_input(['1', '2', '3'])
    if user_decision == '1':
        opposing_team_list = clippers_list
        opposing_team = 'LA Clippers'
    elif user_decision == '2':
        opposing_team_list = lakers_list
        opposing_team = 'Los Angeles Lakers'
    elif user_decision == '3':
        opposing_team_list = celtics_list
        opposing_team = 'Boston Celtics'

combined_list = user_team_list + opposing_team_list

# DEFENDER INITILIAZTION (NEW)

for player in user_team_list:
    defender = KermLib.object_matcher(player, opposing_team_list, 'positionnumber')
    player.defender = defender
    defender.defender = player





position_number = 0

if user_team_list == clippers_list:
    print(clippers_logo)
elif user_team_list == lakers_list:
    print(lakers_logo)
elif user_team_list == celtics_list:
    print(celtics_logo) 
elif user_team_list == knicks_list:
    print(celtics_logo) #PLACEHOLDER FOR NYK LOGO


print('\n' + '\n')

print('Team selected:', user_team)

print('\n')

print('Choose your player!')

for player in user_team_list:
    position_number += 1
    print(player.name + ' -- ' + str(position_number))

player_decision = int(KermLib.get_user_input(['1', '2', '3', '4', '5']))


for player in user_team_list:
    if player.positionnumber == player_decision:
        player.isplayer = True
        player.haspossession = True
        current_player = player
        print('\n')
        print('Player selected: ' + player.name)
        print('Your defender:', current_player.defender.name)
        break



print('Game start!')

# -----------------------------------------------------------------------------------------

end_score = 15

opposing_team_score = 0
user_team_score = 0



while True:

    if opposing_team_score >= end_score:
        print('\n' + '\n' + '\n')
        print('---------------------------------------------------------------------------------------------------------')
        print(opposing_team + ' win! Final score:', opposing_team_score, '-', user_team_score)
        print('---------------------------------------------------------------------------------------------------------')
        if opposing_team == 'LA Clippers':
            print(clippers_logo)
        elif opposing_team == 'Los Angeles Lakers':
            print(lakers_logo)
        elif opposing_team == 'Boston Celtics':
            print(celtics_logo) 
        elif user_team_list == knicks_list:
            print(celtics_logo) #PLACEHOLDER FOR NYK LOGO


        highest_score = 0
        highest_scorer = None

        highest_interceptions = 0
        highest_interceptor = None

        highest_passes = 0
        highest_passer = None

        for player in combined_list:
            if player.pointsMade > highest_score:
                highest_score = player.pointsMade
                highest_scorer = player
            if player.passesMade > highest_passes:
                highest_passes = player.passesMade
                highest_passer = player
            if player.interceptionsMade > highest_interceptions:
                highest_interceptions = player.interceptionsMade
                highest_interceptor = player

        print('Most points scored:', highest_scorer.name, 'with', str(highest_score))
        print('Most passes performed:', highest_passer.name, 'with', str(highest_passes))
        print('Most interceptions:', highest_interceptor.name, 'with', str(highest_interceptions))

        time.sleep(5)
        break
    elif user_team_score >= end_score:
        print('\n' + '\n' + '\n')
        print('---------------------------------------------------------------------------------------------------------')
        print(user_team + ' win! Final score:', user_team_score, '-', opposing_team_score)
        print('---------------------------------------------------------------------------------------------------------')
        if user_team == 'LA Clippers':
            print(clippers_logo)
        elif user_team == 'Los Angeles Lakers':
            print(lakers_logo)
        elif user_team == 'Boston Celtics':
            print(celtics_logo) 
        elif user_team_list == knicks_list:
            print(celtics_logo) #PLACEHOLDER FOR NYK LOGO


        highest_score = 0
        highest_scorer = None

        highest_interceptions = 0
        highest_interceptor = None

        highest_passes = 0
        highest_passer = None

        for player in combined_list:
            if player.pointsMade > highest_score:
                highest_score = player.pointsMade
                highest_scorer = player
            if player.passesMade > highest_passes:
                highest_passes = player.passesMade
                highest_passer = player
            if player.interceptionsMade > highest_interceptions:
                highest_interceptions = player.interceptionsMade
                highest_interceptor = player
        print('Most points scored:', highest_scorer.name, 'with', str(highest_score))
        print('Most passes performed:', highest_passer.name, 'with', str(highest_passes))
        print('Most interceptions:', highest_interceptor.name, 'with', str(highest_interceptions))

        time.sleep(5)
        break

    print('\n')

    if user_team_score > opposing_team_score:
        print('---------------------------------------------------------------------------------------------------------')
        print('Current score:', user_team_score, '-', opposing_team_score,  ', ' + user_team, 'lead by',  (user_team_score - opposing_team_score))
        print('---------------------------------------------------------------------------------------------------------')
    elif user_team_score < opposing_team_score:
        print('---------------------------------------------------------------------------------------------------------')
        print('Current score:', opposing_team_score, '-', user_team_score,  ', ' + opposing_team, 'lead by',  (opposing_team_score - user_team_score))
        print('---------------------------------------------------------------------------------------------------------')
    else:
        print('---------------------------------------------------------------------------------------------------------')
        print('Tie game:',  user_team_score, '-', opposing_team_score)
        print('---------------------------------------------------------------------------------------------------------')
    position_number = 0

    print('\n')

    time.sleep(2.4)

    for player in combined_list:

        if player.haspossession is True:
            print(player.name, 'has the basketball!')

            if player.isplayer == True:
                print('What will you do? (pass), (drive), or shoot a (3pt)?')
                player_action_decision = KermLib.get_user_input(['pass', 'drive', '3pt'])
                print('\n' + '\n')
                print
                
                if player_action_decision in ['pass', 'Pass']:
                    print('Who will you pass to?')

                    for player in user_team_list:
                        if player == current_player:
                            position_number += 1
                            continue
                        position_number += 1
                        print(player.name + ' -- ' + str(position_number), '(defended by', player.defender.name + ')', '(Chance of turnover:', str(turn_over_chance(current_player, player.defender)) + '%)' )
                
                    while True:
                        player_decision = str(input())
                        if player_decision == str(current_player.positionnumber):
                            print('Decision not recognized. Please try again')
                            continue
                        elif player_decision not in ['1', '2', '3', '4', '5']:
                            print('Decision not recognized. Please try again')
                            continue
                        else:
                            player_decision = int(player_decision)
                            break


                    print('\n')

                    for player in user_team_list:
                        if player.positionnumber == player_decision:
                            pass_receiver = player
                            break
                    outcome, points = current_player.action_success('pass', 0, 0, pass_receiver, current_player.team)
                    if outcome == 'shot' and player.team == user_team:
                        user_team_score += points
                        break
                    elif outcome == 'shot' and player.team == opposing_team:
                        opposing_team_score += points
                        break
                    break
                elif player_action_decision in ['drive', 'Drive']:
                    outcome, points = current_player.action_success('drive', current_player.defender.perd, current_player.defender.intd, None, current_player.team)
                    if outcome == 'shot' and player.team == user_team:
                        user_team_score += points
                        break
                    elif outcome == 'shot' and player.team == opposing_team:
                        opposing_team_score += points
                        break
                    break   
                elif player_action_decision in ['3pt', '3PT', '3Pt']:
                    outcome, points = current_player.action_success('3pt', current_player.defender.perd, current_player.defender.intd, None, current_player.team)
                    if outcome == 'shot' and player.team == user_team:
                        user_team_score += points
                        break
                    elif outcome == 'shot' and player.team == opposing_team:
                        opposing_team_score += points
                        break
                    break   

        
            else:
                decision = player.decision()
                outcome, points = player.action_success(decision, player.defender.perd, player.defender.intd, None, player.team)
                if outcome == 'shot' and player.team == user_team:
                    user_team_score += points
                    break
                elif outcome == 'shot' and player.team == opposing_team:
                    opposing_team_score += points
                    break
                break   

                    
                            






