import config
import utilities.api as utils

def get_teams():
    utils.save_local_data(
        utils.fetch_data(config.mens_college_basketball_url),
        'data\\basketball\\ncaam\mens_college_basketball_teams.json')
    pass