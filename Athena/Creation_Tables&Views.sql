CREATE EXTERNAL TABLE IF NOT EXISTS `spotify`.`Artists` (
  `json_string` string
)
LOCATION 's3://spotify-s3-poc/'



DROP VIEW IF EXISTS spotify.Artists_Silver;

CREATE VIEW spotify.Artists_Silver
AS
    WITH CTE AS (
        SELECT 
            SUBSTR("$path",21,10) as Date,
            json_extract_scalar(json_string,'$.name') as Name,
            CAST(json_extract_scalar(json_extract(json_string,'$.followers'),'$.total') as INT) as Followers
        FROM 
            spotify.Artists
    )
    SELECT
        *,
        followers - LAG(followers) OVER( PARTITION BY NAME ORDER BY followers) AS Followers_Gained
    FROM
        CTE
;


SELECT * FROM spotify.artists_silver;