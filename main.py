import json

import endpoints.basketball.ncaam as ncaam
import utilities.api as utils

count = 0

if __name__ == "__main__":
    # ncaam.get_teams()
    json_data = utils.load_local_data('data\\basketball\\ncaam\\mens_college_basketball_teams.json')
    teams = json_data['sports'][0]['leagues'][0]['teams']
    for team in teams:
        count += 1
        # print(team['team']['displayName'], count)
        print(f"Team Name: {team['team']['displayName']}, Team ID: {team['team']['id']}, Count: {count}")
