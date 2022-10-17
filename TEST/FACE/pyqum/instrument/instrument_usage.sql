SELECT u.username, j.dateday, j.startime, j.instrument, j.comment
    FROM user u
    INNER JOIN job j ON j.user_id = u.id
    INNER JOIN sample s ON s.id = j.sample_id
    WHERE (j.startime BETWEEN "2021-08" AND "2022-08") AND (j.instrument LIKE "%ENAB_1%")
    ORDER BY j.id ASC