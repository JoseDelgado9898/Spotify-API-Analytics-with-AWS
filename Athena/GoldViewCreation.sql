CREATE OR REPLACE VIEW Spotify_Gold_View AS 
(
    SELECT *, 
        cast(followers as INT) - cast(LAG(followers) OVER(PARTITION BY NAME ORDER BY followers) as INT) AS Followers_Gained
    FROM
       silver_glue_table
)

