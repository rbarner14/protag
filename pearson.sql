-- psql -d music -t -A -F"," -c "WITH prelim AS(SELECT CONCAT(performer_id, producer_id) AS new_id FROM produce_songs), secondary AS (SELECT performer_id, producer_id, CONCAT(performer_id, producer_id) AS c FROM producers CROSS JOIN performers ORDER BY performer_id) SELECT DISTINCT s.performer_id, s.producer_id, CASE WHEN p.new_id = s.c THEN 1 else 0 END AS score FROM secondary s LEFT JOIN prelim AS p ON s.c = p.new_id" > query2.csv


SELECT  
        user1, user2,
        ((psum - (sum1 * sum2 / n)) / sqrt((sum1sq - pow(sum1, 2.0) / n) * (sum2sq - pow(sum2, 2.0) / n))) AS r,
        n
FROM
        (SELECT 
                n1.performer_id AS user1,
                n2.performer_id AS user2,
                SUM(n1.score) AS sum1,
                SUM(n2.score) AS sum2,
                SUM(n1.score * n1.score) AS sum1sq,
                SUM(n2.score * n2.score) AS sum2sq,
                SUM(n1.score * n2.score) AS psum,
                COUNT(*) AS n
        FROM
                scores AS n1
    LEFT JOIN
        scores AS n2
    ON
        n1.producer_id = n2.producer_id
        WHERE   
                n1.performer_id > n2.performer_id
    GROUP BY
        n1.performer_id, n2.performer_id) AS step1
ORDER BY
        r DESC,
        n DESC