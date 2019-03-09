-- psql -d music -t -A -F"," -c "

WITH prelim AS(
    SELECT 
        CONCAT(performer_id, producer_id) AS new_id 
    FROM produce_songs
)

, secondary AS (
    SELECT 
        performer_id, 
        producer_id, 
        CONCAT(performer_id, producer_id) AS c 
    FROM producers 
    CROSS JOIN performers 
    ORDER BY performer_id
) 

SELECT 
    DISTINCT s.performer_id, 
        s.producer_id, 
CASE WHEN p.new_id = s.c THEN 1 else 0 END AS score 
     FROM secondary s 
LEFT JOIN prelim AS p 
      ON s.c = p.new_id

-- " > scores.csv