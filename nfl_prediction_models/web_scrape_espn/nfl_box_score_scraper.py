from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import numpy as np

# fixes ssl error message
import os, ssl
if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
getattr(ssl, '_create_unverified_context', None)):
    ssl._create_default_https_context = ssl._create_unverified_context

url = 'https://www.espn.com/nfl/boxscore?gameId=401127954'

uClient = uReq(url)
page_html = uClient.read()
uClient.close()

page_soup = soup(page_html, "html.parser")

# normal
game_id = 401127913
# neutral
game_id = 401128134

# team 1 is the away team (even if it is a neutral game, team 1 will be webscraped as away, and team 2 as home)
home_or_away = page_soup.select('#gamepackage-matchup-wrap .record')[0].text
home_or_away = home_or_away.split()
# if the game is played at a neutral location, this list will only have length 2, else it will be specefied in home_or_away[2]
if len(home_or_away) < 3:
    home_or_away = 'Neutral'
else:
    home_or_away = home_or_away[2]

# record after game
record_after_game = page_soup.select('#gamepackage-matchup-wrap .record')[0].text
record_after_game = record_after_game.split(',')[0]

# team 1 quaterback 1 passing
team = page_soup.select('#gamepackage-box-score .boxscore-tabs .filter .team-name')[0].text
qb_with_most_yds_name = page_soup.select('#gamepackage-passing .col.column-one.gamepackage-away-wrap .name a span')[0].text
# qb_c_att = page_soup.select('#gamepackage-passing tbody .c-att')[0].text
# qb_yds = page_soup.select('#gamepackage-passing tbody .yds')[0].text
# qb_avg = page_soup.select('#gamepackage-passing tbody .avg')[0].text
# qb_td = page_soup.select('#gamepackage-passing tbody .td')[0].text
# qb_int = page_soup.select('#gamepackage-passing tbody .int')[0].text
# qb_sacks = page_soup.select('#gamepackage-passing tbody .sacks')[0].text
qb_with_most_yds_qbr = page_soup.select('#gamepackage-passing .col.column-one.gamepackage-away-wrap .qbr')[1].text
# qb_rtg = page_soup.select('#gamepackage-passing tbody .rtg')[0].text
# qb_c_att = str.split(qb_c_att, '/')
# qb_c, qb_att = qb_c_att[0], qb_c_att[1]
# qb_sacks = str.split(qb_sacks, '-')
# qb_sack_number = qb_sacks[0]
# qb_sack_yds = qb_sacks[1]

# team 1 overall passing
team_qb_c_att = page_soup.select('#gamepackage-passing .highlight .c-att')[0].text
team_qb_yds = page_soup.select('#gamepackage-passing .highlight .yds')[0].text
team_qb_avg = page_soup.select('#gamepackage-passing .highlight .avg')[0].text
team_qb_td = page_soup.select('#gamepackage-passing .highlight .td')[0].text
team_qb_int = page_soup.select('#gamepackage-passing .highlight .int')[0].text
team_qb_sacks = page_soup.select('#gamepackage-passing .highlight .sacks')[0].text
team_qb_rtg = page_soup.select('#gamepackage-passing .highlight .rtg')[0].text
team_qb_c_att = str.split(team_qb_c_att, '/')
team_qb_c, team_qb_att = team_qb_c_att[0], team_qb_c_att[1]
team_qb_sacks = str.split(team_qb_sacks, '-')
team_qb_sack_number = team_qb_sacks[0]
team_qb_sack_yds = team_qb_sacks[1]

# team 1 rushing
rushing_car = page_soup.select('#gamepackage-rushing .highlight .car')[0].text
rushing_yds = page_soup.select('#gamepackage-rushing .highlight .yds')[0].text
rushing_avg = page_soup.select('#gamepackage-rushing .highlight .avg')[0].text
rushing_td = page_soup.select('#gamepackage-rushing .highlight .td')[0].text
rushing_long = page_soup.select('#gamepackage-rushing .highlight .long')[0].text

# team 1 receiving
receivers_with_catch = len(page_soup.select('#gamepackage-receiving .col.column-one.gamepackage-away-wrap tbody .name')) - 1

# team 1 fumbles
if len(page_soup.select('#gamepackage-fumbles .col.column-one.gamepackage-away-wrap .highlight .fum')) != 0:
    fum = page_soup.select_one('#gamepackage-fumbles .col.column-one.gamepackage-away-wrap .highlight .fum').text
else:
    fum = 0
if len(page_soup.select('#gamepackage-fumbles .col.column-one.gamepackage-away-wrap .highlight .lost')) != 0:
    lost = page_soup.select_one('#gamepackage-fumbles .col.column-one.gamepackage-away-wrap .highlight .lost').text
else:
    lost = 0
if len(page_soup.select('#gamepackage-fumbles .col.column-one.gamepackage-away-wrap .highlight .rec')) != 0:
    rec = page_soup.select_one('#gamepackage-fumbles .col.column-one.gamepackage-away-wrap .highlight .rec').text
else:
    rec = 0

# team 1 sacks
sacks = page_soup.select_one('#gamepackage-defensive .col.column-one.gamepackage-away-wrap .highlight .sacks').text

# team 1 interceptions
if len(page_soup.select('#gamepackage-interceptions .col.column-one.gamepackage-away-wrap .highlight .int')) != 0:
    ints = page_soup.select_one('#gamepackage-interceptions .col.column-one.gamepackage-away-wrap .highlight .int').text
else:
    ints = 0

# team 1 results
score = page_soup.select_one('.game-strip.game-package.nfl.post.away-winner .team.away .score').text
opponent_score = page_soup.select_one('.game-strip.game-package.nfl.post.away-winner .team.home .score').text
if int(score) > int(opponent_score):
    result = 'W'
else:
    result = 'L'

first_team_data = [game_id, home_or_away, team, qb_with_most_yds_name, qb_with_most_yds_qbr, team_qb_c, team_qb_att, team_qb_yds, team_qb_avg, team_qb_td, team_qb_int, team_qb_sack_number, team_qb_sack_yds, team_qb_rtg, \
                    rushing_car, rushing_yds, rushing_avg, rushing_td, rushing_long, receivers_with_catch, \
                    fum, lost, rec, sacks, ints, score, opponent_score, result]
first_team_data = [str(i) for i in first_team_data]


#========================
# team 2 is the home team
home_or_away = page_soup.select('#gamepackage-matchup-wrap .record')[0].text
home_or_away = home_or_away.split()
# if the game is played at a neutral location, this list will only have length 2, else it will be specefied in home_or_away[2]
if len(home_or_away) < 3:
    home_or_away = 'Neutral'
else:
    home_or_away = home_or_away[2]

# team 2 quaterback 1 passing
team = page_soup.select('#gamepackage-box-score .boxscore-tabs .filter .team-name')[1].text
qb_with_most_yds_name = page_soup.select('#gamepackage-passing .col.column-two.gamepackage-home-wrap .name a span')[0].text
# qb_c_att = page_soup.select('#gamepackage-passing tbody .c-att')[2].text
# qb_yds = page_soup.select('#gamepackage-passing tbody .yds')[2].text
# qb_avg = page_soup.select('#gamepackage-passing tbody .avg')[2].text
# qb_td = page_soup.select('#gamepackage-passing tbody .td')[2].text
# qb_int = page_soup.select('#gamepackage-passing tbody .int')[2].text
# qb_sacks = page_soup.select('#gamepackage-passing tbody .sacks')[2].text
qb_with_most_yds_qbr = page_soup.select('#gamepackage-passing .col.column-two.gamepackage-home-wrap .qbr')[1].text
# qb_rtg = page_soup.select('#gamepackage-passing tbody .rtg')[2].text
# qb_c_att = str.split(qb_c_att, '/')
# qb_c, qb_att = qb_c_att[0], qb_c_att[1]
# qb_sacks = str.split(qb_sacks, '-')
# qb_sack_number = qb_sacks[0]
# qb_sack_yds = qb_sacks[1]

# team 2 overall passing
team_qb_c_att = page_soup.select('#gamepackage-passing .highlight .c-att')[1].text
team_qb_yds = page_soup.select('#gamepackage-passing .highlight .yds')[1].text
team_qb_avg = page_soup.select('#gamepackage-passing .highlight .avg')[1].text
team_qb_td = page_soup.select('#gamepackage-passing .highlight .td')[1].text
team_qb_int = page_soup.select('#gamepackage-passing .highlight .int')[1].text
team_qb_sacks = page_soup.select('#gamepackage-passing .highlight .sacks')[1].text
team_qb_rtg = page_soup.select('#gamepackage-passing .highlight .rtg')[1].text
team_qb_c_att = str.split(team_qb_c_att, '/')
team_qb_c, team_qb_att = team_qb_c_att[0], team_qb_c_att[1]
team_qb_sacks = str.split(team_qb_sacks, '-')
team_qb_sack_number = team_qb_sacks[0]
team_qb_sack_yds = team_qb_sacks[1]

# team 2 rushing
rushing_car = page_soup.select('#gamepackage-rushing .highlight .car')[1].text
rushing_yds = page_soup.select('#gamepackage-rushing .highlight .yds')[1].text
rushing_avg = page_soup.select('#gamepackage-rushing .highlight .avg')[1].text
rushing_td = page_soup.select('#gamepackage-rushing .highlight .td')[1].text
rushing_long = page_soup.select('#gamepackage-rushing .highlight .long')[1].text

# team 2 receiving
receivers_with_catch = len(page_soup.select('#gamepackage-receiving .col.column-two.gamepackage-home-wrap tbody .name')) - 1

# team 2 fumbles
if len(page_soup.select('#gamepackage-fumbles .col.column-two.gamepackage-home-wrap .highlight .fum')) != 0:
    fum = page_soup.select_one('#gamepackage-fumbles .col.column-two.gamepackage-home-wrap .highlight .fum').text
else:
    fum = 0
if len(page_soup.select('#gamepackage-fumbles .col.column-two.gamepackage-home-wrap .highlight .lost')) != 0:
    lost = page_soup.select_one('#gamepackage-fumbles .col.column-two.gamepackage-home-wrap .highlight .lost').text
else:
    lost = 0
if len(page_soup.select('#gamepackage-fumbles .col.column-two.gamepackage-home-wrap .highlight .rec')) != 0:
    rec = page_soup.select_one('#gamepackage-fumbles .col.column-two.gamepackage-home-wrap .highlight .rec').text
else:
    rec = 0

# team 2 sacks
sacks = page_soup.select_one('#gamepackage-defensive .col.column-two.gamepackage-home-wrap .highlight .sacks').text

# team 2 interceptions
if len(page_soup.select('#gamepackage-interceptions .col.column-two.gamepackage-home-wrap .highlight .int')) != 0:
    ints = page_soup.select_one('#gamepackage-interceptions .col.column-two.gamepackage-home-wrap .highlight .int').text
else:
    ints = 0

# team 2 results
score = page_soup.select_one('.game-strip.game-package.nfl.post.away-winner .team.home .score').text
opponent_score = page_soup.select_one('.game-strip.game-package.nfl.post.away-winner .team.away .score').text
if int(score) > int(opponent_score):
    result = 'W'
else:
    result = 'L'

second_team_data = [game_id, home_or_away, team, qb_with_most_yds_name, qb_with_most_yds_qbr, team_qb_c, team_qb_att, team_qb_yds, team_qb_avg, team_qb_td, team_qb_int, team_qb_sack_number, team_qb_sack_yds, team_qb_rtg, \
                    rushing_car, rushing_yds, rushing_avg, rushing_td, rushing_long, receivers_with_catch, \
                    fum, lost, rec, sacks, ints, score, opponent_score, result]
second_team_data = [str(i) for i in second_team_data]

print(first_team_data, '\n', second_team_data)
total_data = []
total_data.append(first_team_data)
total_data.append(second_team_data)
# np.savetxt('nfl_box_score_data/401127913.csv', total_data, delimiter = ',', fmt = '%s')