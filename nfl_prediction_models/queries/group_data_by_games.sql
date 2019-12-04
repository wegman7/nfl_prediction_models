-- takes new average of stats each week for each game (no duplicate teams), and separates input (previous game data included w/l before game) and output (scores of both teams)
-- CREATE TEMP TABLE t AS (
SELECT * FROM (
SELECT A.week, A.team as team_A, A.home_or_away AS home_or_away_A, 
        AVG(A.team_qb_c) OVER(PARTITION BY A.team ORDER BY A.week ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING) AS team_qb_c_A, 
        AVG(A.team_qb_att) OVER(PARTITION BY A.team ORDER BY A.week ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING) AS team_qb_att_A, 
        AVG(A.team_qb_td) OVER(PARTITION BY A.team ORDER BY A.week ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING) AS team_qb_td_A, 
        AVG(A.team_qb_int) OVER(PARTITION BY A.team ORDER BY A.week ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING) AS team_qb_int_A, 
        AVG(A.team_qb_sack_total) OVER(PARTITION BY A.team ORDER BY A.week ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING) AS team_qb_sack_total_A, 
        AVG(A.rushing_car) OVER(PARTITION BY A.team ORDER BY A.week ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING) AS rushing_car_A, 
        AVG(A.rushing_yds) OVER(PARTITION BY A.team ORDER BY A.week ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING) AS rushing_yds_A, 
        AVG(A.rushing_td) OVER(PARTITION BY A.team ORDER BY A.week ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING) AS rushing_td_A, 
        AVG(A.sacks) OVER(PARTITION BY A.team ORDER BY A.week ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING) AS sacks_A, 
        AVG(A.ints) OVER(PARTITION BY A.team ORDER BY A.week ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING) AS ints_A, 
        AVG(A.lost) OVER(PARTITION BY A.team ORDER BY A.week ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING) AS lost_A, 
        AVG(A.score) OVER(PARTITION BY A.team ORDER BY A.week ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS score_A, 
        LAG(A.record_after_game) OVER(PARTITION BY A.team ORDER BY A.week) AS record_before_game_A, 
        B.team AS team_B, B.home_or_away AS home_or_away_B, 
        AVG(B.team_qb_c) OVER(PARTITION BY B.team ORDER BY A.week ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING) AS team_qb_c_B, 
        AVG(B.team_qb_att) OVER(PARTITION BY B.team ORDER BY A.week ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING) AS team_qb_att_B, 
        AVG(B.team_qb_td) OVER(PARTITION BY B.team ORDER BY A.week ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING) AS team_qb_td_B, 
        AVG(B.team_qb_int) OVER(PARTITION BY B.team ORDER BY A.week ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING) AS team_qb_int_B, 
        AVG(B.team_qb_sack_total) OVER(PARTITION BY B.team ORDER BY A.week ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING) AS team_qb_sack_total_B, 
        AVG(B.rushing_car) OVER(PARTITION BY B.team ORDER BY A.week ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING) AS rushing_car_B, 
        AVG(B.rushing_yds) OVER(PARTITION BY B.team ORDER BY A.week ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING) AS rushing_yds_B, 
        AVG(B.rushing_td) OVER(PARTITION BY B.team ORDER BY A.week ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING) AS rushing_td_B, 
        AVG(B.sacks) OVER(PARTITION BY B.team ORDER BY A.week ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING) AS sacks_B, 
        AVG(B.ints) OVER(PARTITION BY B.team ORDER BY A.week ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING) AS ints_B, 
        AVG(B.lost) OVER(PARTITION BY B.team ORDER BY A.week ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING) AS lost_B, 
        AVG(B.score) OVER(PARTITION BY B.team ORDER BY A.week ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS score_B, 
        LAG(B.record_after_game) OVER(PARTITION BY B.team ORDER BY A.week) AS record_before_game_B
FROM nfl_box_scores AS A
INNER JOIN nfl_box_scores AS B ON A.game_id = B.game_id
    WHERE A.team <> B.team
    GROUP BY A.week, A.team, A.home_or_away, A.team_qb_c, A.team_qb_att, A.team_qb_td, A.team_qb_int, A.team_qb_sack_total, 
            A.rushing_car, A.rushing_yds, A.rushing_td, A.sacks, A.ints, A.lost, A.score, A.record_after_game, B.team, 
             B.home_or_away, B.team_qb_c, B.team_qb_att, B.team_qb_td, B.team_qb_int, B.team_qb_sack_total, 
             B.rushing_car, B.rushing_yds, B.rushing_td, B.sacks, B.ints, B.lost, B.score, 
             B.record_after_game
    ORDER BY A.week
) AS foo
WHERE home_or_away_A = 'Away'
-- );


    