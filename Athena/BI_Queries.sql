-- Who are the top 5 most followed artists as of today's date?

SELECT 
    * 
FROM 
    spotify.Artists_Silver artists_view
where
   CAST(artists_view.date as DATE)=CURRENT_DATE
ORDER BY 
    FOLLOWERS DESC;

-- Which artists are getting the highest increases in follower count per day?

SELECT 
    name as Artist,
    CAST(avg(Followers_Gained) as INT) as AVG_DAILY_FOLLOWERS_GAINED 
FROM 
    spotify.artists_silver
GROUP BY
    name
ORDER BY
   AVG_DAILY_FOLLOWERS_GAINED DESC;


-- During which date has Taylor Swift's followers increased the most?

SELECT 
    DATE, followers_gained
FROM
    spotify.artists_silver
WHERE 
    name='Taylor Swift'
AND
    Followers_Gained = (SELECT MAX(Followers_Gained) FROM spotify.artists_silver where name='Taylor Swift');
