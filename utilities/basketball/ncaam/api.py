import random
import time
import inspect

import pandas as pd

import utilities.api as utils

stats_column_headers = [
    "ID",
    "NAME",
    "GP",
    "W",
    "L",
    "PTS",
    "AST",
    "REB",
    "OREB",
    "DREB",
    "FG%",
    "FGM",
    "FGA",
    "2P%",
    "2PM",
    "2PA",
    "3P%",
    "3PM",
    "3PA",
    "FT%",
    "FTM",
    "FTA",
    "BLK",
    "STL",
    "TO",
    "AST/TO",
    "PF",
    "SC-EFF",
    "SH-EFF",
]


def locate_team_entry(team_id):
    conferences = utils.load_local_data(
        "data\\basketball\\ncaam\mens_college_basketball_data.json"
    )

    for conference in conferences["children"]:
        for team in conference["standings"]["entries"]:
            if team["team"]["id"] == team_id:
                return team["team"]


def convert_json_stats_to_dataframe(team_id, df):
    team = locate_team_entry(team_id)
    team_name = team["displayName"].lower().replace(" ", "_")
    file_path = f"data\\basketball\\ncaam\\team_stats\\{team_name}_team_stats.json"
    team_stats = utils.load_local_data(file_path)["results"]["stats"]["categories"]
    record = utils.load_local_data(file_path)["team"]["recordSummary"].split('-')
    
    row_data = {
        "ID": team_id,
        "NAME": team["displayName"],
        "GP": team_stats[0]["stats"][3]["value"],
        "W": record[0],
        "L": record[1],
        "PTS": team_stats[1]["stats"][7]["value"],
        "AST": team_stats[1]["stats"][9]["value"],
        "REB": team_stats[0]["stats"][0]["value"],
        "OREB": team_stats[1]["stats"][8]["value"],
        "DREB": team_stats[2]["stats"][0]["value"],
        "FG%": team_stats[1]["stats"][14]["value"],
        "FGM": team_stats[1]["stats"][5]["value"],
        "FGA": team_stats[1]["stats"][6]["value"],
        "2P%": team_stats[1]["stats"][11]["value"],
        "2PM": team_stats[1]["stats"][15]["value"],
        "2PA": team_stats[1]["stats"][16]["value"],
        "3P%": team_stats[1]["stats"][27]["value"],
        "3PM": team_stats[1]["stats"][3]["value"],
        "3PA": team_stats[1]["stats"][4]["value"],
        "FT%": team_stats[1]["stats"][0]["value"],
        "FTM": team_stats[1]["stats"][5]["value"],
        "FTA": team_stats[1]["stats"][6]["value"],
        "BLK": team_stats[2]["stats"][1]["value"],
        "STL": team_stats[2]["stats"][2]["value"],
        "TO": team_stats[1]["stats"][10]["value"],
        "AST/TO": team_stats[0]["stats"][1]["value"],
        "PF": team_stats[0]["stats"][2]["value"],
        "SC-EFF": team_stats[1]["stats"][12]["value"],
        "SH-EFF": team_stats[1]["stats"][13]["value"],
    }

    df = pd.concat([df, pd.DataFrame([row_data]).set_index("ID")], ignore_index=False)
    return df


def iterate_conferences(
    *endpoints, conference_selector: list = None, wait: bool = True, df = None
):
    conference_json = utils.load_local_data(
        "data\\basketball\\ncaam\\mens_college_basketball_conference_list.json"
    )

    if df is None:
        df = pd.DataFrame(columns=stats_column_headers).set_index("ID")

    if conference_selector:
        conferences = conference_selector
    else:
        conferences = conference_json.keys()

    for conference in conferences:
        try:
            for team_id in conference_json[conference]:
                for endpoint in endpoints:
                    if 'df' in inspect.signature(endpoint).parameters:
                        df = endpoint(team_id, df)
                    else:
                        endpoint(team_id)
                if wait:
                    time.sleep(random.uniform(0.75, 1.3))
        except Exception as e:
            print(f"Error: {e}")
        if wait:
            time.sleep(random.uniform(9.75, 10.3))

    if 'df' in inspect.signature(endpoint).parameters:
        df.to_csv("data\\basketball\\ncaam\\mens_college_basketball_stats.csv")
