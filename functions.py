group_3_clubs = [
    "Paris Saint-Germain",
    "Roma",
    "Chelsea",
    "Real Madrid",
    "Juventus",
    "Manchester United",
    "Arsenal",
    "Barcelona",
    "Bayern Munich",
    "Manchester City",
    "AC Milan",
    "Liverpool",
    "Tottenham Hotspur",
    "Atletico Madrid",
    "Napoli",
]

group_2_clubs = [
    "Monaco",
    "Everton",
    "Sevilla",
    "Borussia Dortmund",
    "Lyon",
    "Atletico Madrid",
    "Napoli",
    "Marseille",
    "Leicester City",
    "Lazio",
    "Inter Milan",
    "Bayer Leverkusen",
    "Newcastle United",
]

def get_level(teams):
    level = 6
    for team in teams:
        if team in group_3_clubs:
            level -= 2
        elif team in group_2_clubs:
            level -= 1
    return level

def get_indication(player_object, kind='first_letter'):
    if kind == 'first_letter':
        return player_object['ShortName'][0]