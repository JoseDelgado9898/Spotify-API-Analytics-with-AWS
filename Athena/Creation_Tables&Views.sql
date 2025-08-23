
# Creation of Raw table from S3 location

CREATE EXTERNAL TABLE IF NOT EXISTS `spotify`.`Artists` (
  `json_string` string
)
LOCATION 's3://spotify-s3-poc/'


# Creation of Silver Iceberg table + parsed JSON

CREATE TABLE IF NOT EXISTS spotify.Artists_Silver
WITH(
   table_type = 'ICEBERG',
   location='s3://spotify-s3-poc/silver/',
   is_external=false
)
AS
(
    SELECT 
        SUBSTR("$path",21,10) as Date,
        json_extract_scalar(json_string,'$.name') as Name,
        CAST(json_extract_scalar(json_extract(json_string,'$.followers'),'$.total') as INT) as Followers
    FROM 
        spotify.Artists

)

# Creation of Gold view for analytical use cases

CREATE OR REPLACE VIEW Spotify_Gold_View AS 
(
    SELECT *, 
        followers - LAG(followers) OVER( PARTITION BY NAME ORDER BY followers) AS Followers_Gained
    FROM
        spotify.artists_silver
)

