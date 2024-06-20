COUNT_BUSINESSES_QUERY = '''
    CREATE TEMP FUNCTION RADIANS(x FLOAT64) AS (
        ACOS(-1) * x / 180
    );

    WITH distances AS (
        SELECT place_id,
            (6371 * ACOS(COS(RADIANS(@arglatitude)) * COS(RADIANS(CAST(JSON_EXTRACT(coordinates, '$.latitude') AS FLOAT64))) * COS(RADIANS(CAST(JSON_EXTRACT(coordinates, '$.longitude') AS FLOAT64)) - RADIANS(@arglongitude)) + SIN(RADIANS(@arglatitude)) * SIN(RADIANS(CAST(JSON_EXTRACT(coordinates, '$.latitude') AS FLOAT64))))) AS distance
        FROM `gmapsapi-c4dca.gmapsdata90.PLACE v4`
    )
    SELECT COUNT(*) AS count_of_places_within_4km
    FROM distances
    WHERE distance <= 4;
'''

GET_COMPETITOR_DETAILS_QUERY = '''
    SELECT *
    FROM `gmapsapi-c4dca.gmapsdata90.PLACE v4`
    WHERE place_id = @argplace_id;
'''

GET_COMPETITORS_QUERY = '''
    CREATE TEMP FUNCTION RADIANS(x FLOAT64) AS (
        ACOS(-1) * x / 180
    );

    WITH distances AS (
        SELECT `place_id`, `name`, `coordinates`, `main_category`, `nearest_competitor_place_id`, `nearest_competitor_distance`,
            `rating`, reviews_per_rating, `average_hour`, `std_hour`, `avg_popularity`, `top_hour_popularity`, 
            `top_average_popularity`, `featured_image`,
            (6371 * ACOS(COS(RADIANS(@arglatitude)) * COS(RADIANS(CAST(JSON_EXTRACT(coordinates, '$.latitude') AS FLOAT64))) * COS(RADIANS(CAST(JSON_EXTRACT(coordinates, '$.longitude') AS FLOAT64)) - RADIANS(@arglongitude)) + SIN(RADIANS(@arglatitude)) * SIN(RADIANS(CAST(JSON_EXTRACT(coordinates, '$.latitude') AS FLOAT64))))) AS distance
        FROM `gmapsapi-c4dca.gmapsdata90.PLACE v4`
    )
    SELECT *
    FROM distances
    WHERE distance <= 4;
'''

GET_TOP_COMPETITORS = '''
    CREATE TEMP FUNCTION RADIANS(x FLOAT64) AS (
        ACOS(-1) * x / 180
    );

    WITH distances AS (
        SELECT `place_id`, `coordinates`, `main_category`, `reviews`, `rating`, `featured_image`, `address`,
            (6371 * ACOS(COS(RADIANS(@arglatitude)) * COS(RADIANS(CAST(JSON_EXTRACT(coordinates, '$.latitude') AS FLOAT64))) * COS(RADIANS(CAST(JSON_EXTRACT(coordinates, '$.longitude') AS FLOAT64)) - RADIANS(@arglongitude)) + SIN(RADIANS(@arglatitude)) * SIN(RADIANS(CAST(JSON_EXTRACT(coordinates, '$.latitude') AS FLOAT64))))) AS distance
        FROM `gmapsapi-c4dca.gmapsdata90.PLACE v4`
    )
    SELECT *
    FROM distances
    WHERE distance <= 4
    ORDER BY reviews * rating DESC
    LIMIT 3;
'''

GET_ARTICLES = '''
    SELECT * FROM `gmapsapi-c4dca.gmapsdata90.ARTICLES` LIMIT 1000
'''


