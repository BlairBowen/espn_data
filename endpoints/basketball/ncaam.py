import time
import random
import requests

import config
import utilities.api as utils


def get_teams():
    utils.save_local_data(
        utils.fetch_data(config.mens_college_basketball_standings_url),
        "data\\basketball\\ncaam\mens_college_basketball_teams.json",
    )


def get_conferences():
    conference_list = utils.load_local_data(
        "data\\basketball\\ncaam\mens_college_basketball_teams.json"
    )

    conference_dict = {}

    for conference in conference_list["children"]:
        team_list = []
        for team in conference["standings"]["entries"]:
            team_list.append(team["team"]["id"])
        conference_dict[conference["abbreviation"]] = team_list

    utils.save_local_data(
        conference_dict,
        "data\\basketball\\ncaam\\mens_college_basketball_conference_list.json",
    )


def get_team_stats(team_id):
    response = utils.fetch_data(
        config.mens_college_basketball_team_stats_url.replace("*", team_id)
    )
    team_name = response["team"]["displayName"].lower().replace(" ", "_")
    utils.save_local_data(
        response, f"data\\basketball\\ncaam\\team_stats\\{team_name}_team_stats.json"
    )


def get_team_photos(team_id):
    picture = requests.get(
        config.mens_college_basketball_team_picture_url.replace("*", team_id)
    )
    conferences = utils.load_local_data(
        "data\\basketball\\ncaam\mens_college_basketball_teams.json"
    )

    team_name = ""
    break_flag = False

    for conference in conferences["children"]:
        for team in conference["standings"]["entries"]:
            if team["team"]["id"] == team_id:
                team_name = team["team"]["displayName"].lower().replace(" ", "_")
                break_flag = True
                break
        if break_flag:
            break
    
    output_file = f"data\\basketball\\ncaam\\team_logos\\{team_name}_logo.png"

    with open(output_file, "wb") as f:
        f.write(picture.content)
        print(f"Logo saved to {output_file}")


def get_resources_from(resource, conference_selector: list = None):
    conference_json = utils.load_local_data(
        "data\\basketball\\ncaam\\mens_college_basketball_conference_list.json"
    )

    if conference_selector:
        conferences = conference_selector
    else:
        conferences = conference_json.keys()

    for conference in conferences:
        try:
            for team_id in conference_json[conference]:
                if resource == "logos":
                    get_team_photos(team_id)
                elif resource == "stats":
                    get_team_stats(team_id)
                elif resource == "both":
                    get_team_photos(team_id)
                    get_team_stats(team_id)
                time.sleep(random.uniform(.75, 1.3))
        except Exception as e:
            print(f"Error: {e} {conferences}")
        
