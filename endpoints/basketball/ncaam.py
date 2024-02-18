import pandas as pd
import requests

import config
import utilities.api as utils
import utilities.basketball.ncaam as ncaam_utils

conference_column_headers = [
    "ID",
    "NAME",
    "SHORT_NAME",
]

team_column_headers = [
    "ID",
    "GROUP_ID",
    "DISPLAY_NAME",
    "SLUG",
    "ABBREVIATION",
    "SHORT_NAME",
    "TEAM_NAME",
    "COLOR",
    "ALT_COLOR",
]

stats_column_headers = [
    "ID",
    "GP",
    "PTS",
    "REB",
    "AST",
    "STL",
    "BLK",
    "TO",
    "FG%",
    "3P%",
    "FT%",
    "FGM",
    "FGA",
    "3PM",
    "3PA",
    "FTM",
    "FTA",
    "OR",
    "DR",
    "OR%",
    "TO%",
    "AST/TO",
    "PF",
    "SC_EFF",
    "SH_EFF",
    "FT_RATE",
    "PACE",
    "OPP_PTS",
    "OPP_REB",
    "OPP_AST",
    "OPP_STL",
    "OPP_BLK",
    "OPP_TO",
    "OPP_FG%",
    "OPP_3P%",
    "OPP_FT%",
    "OPP_FGM",
    "OPP_FGA",
    "OPP_3PM",
    "OPP_3PA",
    "OPP_FTM",
    "OPP_FTA",
    "OPP_OR",
    "OPP_DR",
    "OPP_OR%",
    "OPP_TO%",
    "OPP_AST/TO",
    "OPP_PF",
    "OPP_SC_EFF",
    "OPP_SH_EFF",
    "OPP_FT_RATE",
    "OFF_EFF",
    "DEF_EFF",
    "NET_RTG",
    "EFF_FG%",
    "4FAC",
]


def get_teams(refresh=False):
    if refresh:
        data = utils.fetch_data(config.mens_college_basketball_teams_url)
        df = pd.DataFrame(columns=team_column_headers)
        conferences = data["sports"][0]["leagues"][0]["groups"]
        for conference in conferences:
            print(conference["name"])
            for teams in conference["teams"]:
                row_data = {
                    "ID": teams["id"],
                    "GROUP_ID": conference["uid"].split("g:")[1],
                    "DISPLAY_NAME": teams["displayName"],
                    "SLUG": teams["slug"],
                    "ABBREVIATION": teams["abbreviation"],
                    "SHORT_NAME": teams["shortDisplayName"],
                    "TEAM_NAME": teams["name"],
                    "COLOR": (
                        teams["color"] if "alternateColor" in teams.keys() else "000000"
                    ),
                    "ALT_COLOR": (
                        teams["alternateColor"]
                        if "alternateColor" in teams.keys()
                        else "ffffff"
                    ),
                }

                df = pd.concat([df, pd.DataFrame([row_data])], ignore_index=False)

        df.set_index("ID", inplace=True)
        df.to_csv("data\\basketball\\ncaam\\mens_college_basketball_teams.csv")
    else:
        return pd.read_csv(
            "data\\basketball\\ncaam\\mens_college_basketball_teams.csv", index_col="ID"
        )


def get_conferences(refresh=False):
    if refresh:
        conference_list = utils.fetch_data(config.mens_college_basketball_groups_url)
        df = pd.DataFrame(columns=conference_column_headers)
        for conference in conference_list["conferences"]:
            row_data = {
                "ID": conference["groupId"],
                "NAME": conference["name"],
                "SHORT_NAME": conference["shortName"].replace(" ", "-").lower(),
            }

            df = pd.concat([df, pd.DataFrame([row_data])], ignore_index=False)

        df.set_index("ID", inplace=True)
        df.to_csv("data\\basketball\\ncaam\\mens_college_basketball_conferences.csv")
    else:
        return pd.read_csv(
            "data\\basketball\\ncaam\\mens_college_basketball_conferences.csv",
            index_col="ID",
        )


def get_team_stats(refresh=False, year=2024):
    if refresh:
        teams_list = utils.fetch_data(
            config.mens_college_basketball_team_stats_url.replace("*", str(year))
        )
        df = pd.DataFrame(columns=stats_column_headers)
        for team in teams_list["teams"]:

            TO_PCT = team["categories"][4]["values"][4] / (
                team["categories"][4]["values"][7]
                + 0.44 * team["categories"][4]["values"][11]
                + team["categories"][4]["values"][4]
            )
            FT_RATE = (
                team["categories"][4]["values"][11] / team["categories"][4]["values"][7]
            )
            PACE = 0.5 * (
                (
                    team["categories"][4]["values"][7]
                    + 0.4 * team["categories"][4]["values"][11]
                    - 1.07
                    * (
                        team["categories"][4]["values"][12]
                        / (
                            team["categories"][4]["values"][12]
                            + team["categories"][3]["values"][1]
                        )
                    )
                    * (
                        team["categories"][4]["values"][7]
                        - team["categories"][4]["values"][6]
                    )
                    + team["categories"][4]["values"][4]
                )
                + 0.5
                * (
                    (
                        team["categories"][5]["values"][7]
                        + 0.4 * (team["categories"][5]["values"][11])
                        - 1.07
                        * (team["categories"][5]["values"][12])
                        / (
                            team["categories"][5]["values"][12]
                            + team["categories"][2]["values"][1]
                        )
                    )
                    * (
                        team["categories"][5]["values"][7]
                        - team["categories"][5]["values"][8]
                    )
                    + team["categories"][5]["values"][4]
                )
            )
            OPP_TO_PCT = team["categories"][5]["values"][4] / (
                team["categories"][5]["values"][7]
                + 0.44 * team["categories"][5]["values"][11]
                + team["categories"][5]["values"][4]
            )
            OPP_FT_RATE = (
                team["categories"][5]["values"][11] / team["categories"][5]["values"][7]
            )
            OFF_EFF = 100 * (team["categories"][4]["values"][0] / PACE)
            DEF_EFF = 100 * (team["categories"][5]["values"][0] / PACE)
            NET_RTG = OFF_EFF - DEF_EFF
            EFF_FG_PCT = (
                team["categories"][4]["values"][6]
                + 0.5 * team["categories"][4]["values"][8]
            ) / team["categories"][4]["values"][7]
            OPP_EFF_FG_PCT = (
                team["categories"][5]["values"][6]
                + 0.5 * team["categories"][5]["values"][8]
            ) / team["categories"][5]["values"][7]
            FOUR_FAC = (
                0.4 * EFF_FG_PCT
                + 0.25 * TO_PCT
                + 0.2 * team["categories"][4]["values"][23]
                + 0.15 * FT_RATE
            )

            row_data = {
                "ID": team["team"]["id"],
                "GP": team["categories"][0]["values"][7],
                "PTS": team["categories"][4]["values"][0],
                "REB": team["categories"][0]["values"][1],
                "AST": team["categories"][4]["values"][13],
                "STL": team["categories"][2]["values"][2],
                "BLK": team["categories"][2]["values"][3],
                "TO": team["categories"][4]["values"][4],
                "FG%": team["categories"][4]["values"][1],
                "3P%": team["categories"][4]["values"][2],
                "FT%": team["categories"][4]["values"][3],
                "FGM": team["categories"][4]["values"][6],
                "FGA": team["categories"][4]["values"][7],
                "3PM": team["categories"][4]["values"][8],
                "3PA": team["categories"][4]["values"][9],
                "FTM": team["categories"][4]["values"][10],
                "FTA": team["categories"][4]["values"][11],
                "OR": team["categories"][4]["values"][12],
                "DR": team["categories"][2]["values"][1],
                "OR%": team["categories"][4]["values"][23],
                "TO%": TO_PCT,
                "AST/TO": team["categories"][0]["values"][6],
                "PF": team["categories"][0]["values"][8],
                "SC_EFF": team["categories"][4]["values"][24],
                "SH_EFF": team["categories"][4]["values"][25],
                "FT_RATE": FT_RATE,
                "PACE": PACE,
                "OPP_PTS": team["categories"][5]["values"][0],
                "OPP_REB": team["categories"][1]["values"][1],
                "OPP_AST": team["categories"][5]["values"][13],
                "OPP_STL": team["categories"][3]["values"][2],
                "OPP_BLK": team["categories"][3]["values"][3],
                "OPP_TO": team["categories"][5]["values"][4],
                "OPP_FG%": team["categories"][5]["values"][1],
                "OPP_3P%": team["categories"][5]["values"][2],
                "OPP_FT%": team["categories"][5]["values"][3],
                "OPP_FGM": team["categories"][5]["values"][6],
                "OPP_FGA": team["categories"][5]["values"][7],
                "OPP_3PM": team["categories"][5]["values"][8],
                "OPP_3PA": team["categories"][5]["values"][9],
                "OPP_FTM": team["categories"][5]["values"][10],
                "OPP_FTA": team["categories"][5]["values"][11],
                "OPP_OR": team["categories"][5]["values"][12],
                "OPP_DR": team["categories"][3]["values"][1],
                "OPP_OR%": team["categories"][5]["values"][23],
                "OPP_TO%": OPP_TO_PCT,
                "OPP_AST/TO": team["categories"][1]["values"][6],
                "OPP_PF": team["categories"][1]["values"][8],
                "OPP_SC_EFF": team["categories"][5]["values"][24],
                "OPP_SH_EFF": team["categories"][5]["values"][25],
                "OPP_FT_RATE": OPP_FT_RATE,
                "OFF_EFF": OFF_EFF,
                "DEF_EFF": DEF_EFF,
                "NET_RTG": NET_RTG,
                "EFF_FG%": EFF_FG_PCT,
                "OPP_EFF_FG%": OPP_EFF_FG_PCT,
                "4FAC": FOUR_FAC,
            }

            df = pd.concat([df, pd.DataFrame([row_data])], ignore_index=False)

        df.set_index("ID", inplace=True)
        df = df.loc[df["GP"] > 5]
        df.to_csv("data\\basketball\\ncaam\\mens_college_basketball_team_stats.csv")
    else:
        return pd.read_csv(
            "data\\basketball\\ncaam\\mens_college_basketball_team_stats.csv",
            index_col="ID",
        )


def get_team_photos(team_id):
    picture = requests.get(
        config.mens_college_basketball_team_picture_url.replace("*", team_id)
    )
    team = ncaam_utils.locate_team_entry(team_id)
    team_name = team["displayName"].lower().replace(" ", "_")

    output_file = f"data\\basketball\\ncaam\\team_logos\\{team_name}_logo.png"

    utils.save_local_logo(picture.content, output_file)
