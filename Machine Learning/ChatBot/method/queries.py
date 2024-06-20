GET_PRIORITY_REVIEWS = '''
    CREATE TEMP FUNCTION RADIANS(x FLOAT64) AS (
        ACOS(-1) * x / 180
    );

    WITH unique_places AS (
        SELECT DISTINCT place_id,
            CAST(JSON_EXTRACT(coordinates, '$.latitude') AS FLOAT64) AS latitude,
            CAST(JSON_EXTRACT(coordinates, '$.longitude') AS FLOAT64) AS longitude
        FROM `capstone-project-ents-h110.Feedbacks.Feedback`
    ),
    distances AS (
        SELECT place_id,
            (6371 * ACOS(
                COS(RADIANS(@arglatitude)) * COS(RADIANS(latitude)) * COS(RADIANS(longitude) - RADIANS(@arglongitude)) + 
                SIN(RADIANS(@arglatitude)) * SIN(RADIANS(latitude))
            )) AS distance
        FROM unique_places
    ),
    filtered_feedback AS (
        SELECT f.english_review, d.distance, f.label
        FROM `capstone-project-ents-h110.Feedbacks.Feedback` f
        JOIN distances d ON f.place_id = d.place_id
    )
    SELECT english_review 
    FROM filtered_feedback
    WHERE distance <= 4 AND label = 1
    LIMIT 30;
'''