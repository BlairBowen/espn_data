import random
import time

import utilities.api as utils


def locate_team_entry(team_id):
    conferences = utils.load_local_data(
        "data\\basketball\\ncaam\mens_college_basketball_data.json"
    )

    for conference in conferences["children"]:
        for team in conference["standings"]["entries"]:
            if team["team"]["id"] == team_id:
                return team["team"]


def convert_json_stats_to_dataframe(team_id):
    team = locate_team_entry(team_id)
    team_name = team["displayName"].lower().replace(" ", "_")
    print(team_name)


def iterate_conferences(
    conference_selector: list = None,
    wait: bool = True,
    **endpoints,
):
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
                for _, endpoint in endpoints.items():
                    endpoint(team_id)
                if wait:
                    time.sleep(random.uniform(0.75, 1.3))
        except Exception as e:
            print(f"Error: {e} {conferences}")
        if wait:
            time.sleep(random.uniform(9.75, 10.3))
