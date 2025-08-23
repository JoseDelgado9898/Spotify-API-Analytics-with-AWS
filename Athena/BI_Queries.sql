
-- Who are the top 5 most followed artists as of today's date?

SELECT 
    * 
FROM 
    spotify.spotify_gold_view gv
where
   CAST(gv.date as DATE)=CURRENT_DATE
ORDER BY 
    FOLLOWERS DESC
LIMIT 5;

-- Which artists are getting the highest increases in follower count per day?

SELECT 
    name as Artist,
    CAST(avg(Followers_Gained) as INT) as AVG_DAILY_FOLLOWERS_GAINED 
FROM 
    spotify.spotify_gold_view
GROUP BY
    name
ORDER BY
   AVG_DAILY_FOLLOWERS_GAINED DESC;


-- During which date has Taylor Swift's followers increased the most?

SELECT 
    DATE, followers_gained
FROM
    spotify.spotify_gold_view
WHERE 
    name='Taylor Swift'
AND
    Followers_Gained = (SELECT MAX(Followers_Gained) FROM spotify.spotify_gold_view where name='Taylor Swift');
