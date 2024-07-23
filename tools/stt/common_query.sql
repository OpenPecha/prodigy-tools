-- find a specific record
SELECT json_extract(content, '$.text'),
	json_extract(content, '$._session_id')
FROM example
WHERE json_extract(content, '$.text') like 'STT_TT00017_05%'
	AND json_extract(content, '$._session_id') = 'stt_tt_gc-thoesam';
--
--
-- transcribed files in a dataset
SELECT json_extract (content, '$.text') AS file_name
FROM example
	JOIN link ON example.id = link.example_id
	JOIN dataset ON dataset.id = link.dataset_id
WHERE dataset.name = 'stt_tt_ga'
	AND json_extract (content, '$.answer') = 'accept';
--
--
-- reviewed files in a dataset
SELECT json_extract (content, '$.text') AS file_name
FROM example
	JOIN link ON example.id = link.example_id
	JOIN dataset ON dataset.id = link.dataset_id
WHERE dataset.name = 'stt_tt_ga_review'
	AND json_extract (content, '$.answer') = 'accept';
--
--
-- reviewed transcripts
SELECT review.audio AS file_name,
	review.session_id AS reviewer,
	annotation.session_id AS transcriber,
	CASE
		WHEN review.transcript = annotation.transcript THEN 1
		ELSE 0
	END AS correct,
	review.transcript AS reviewed_transcript,
	annotation.transcript AS original_transcript
FROM (
		SELECT json_extract (content, '$.text') AS audio,
			json_extract (content, '$._session_id') AS session_id,
			json_extract (content, '$.transcript') AS transcript
		FROM example
			JOIN link ON example.id = link.example_id
			JOIN dataset ON dataset.id = link.dataset_id
		WHERE dataset.name = 'stt_tt_ga_review'
			AND json_extract (content, '$.answer') = 'accept'
	) AS review
	LEFT JOIN (
		SELECT json_extract (content, '$.text') AS audio,
			json_extract (content, '$._session_id') AS session_id,
			json_extract (content, '$.transcript') AS transcript
		FROM example
			JOIN link ON example.id = link.example_id
			JOIN dataset ON dataset.id = link.dataset_id
		WHERE dataset.name = 'stt_tt_ga'
			AND json_extract (content, '$.answer') = 'accept'
	) AS annotation ON annotation.audio = review.audio
ORDER BY review.audio;
--
--
-- records in a dataset
SELECT json_extract(content, '$.text') AS file_name,
	json_extract(content, '$._session_id') AS
FROM example
	JOIN link ON example.id = link.example_id
	JOIN dataset ON dataset.id = link.dataset_id
WHERE dataset.name = 'stt_tt_gg';
--
--
-- delete all examples in a dataset
DELETE a dataset
DELETE FROM example
WHERE id IN (
		SELECT example.id
		FROM example
			JOIN link ON example.id = link.example_id
			JOIN dataset ON dataset.id = link.dataset_id
		WHERE dataset.name = 'stt_tt_gg'
	);
--
--
-- delete all links in a dataset
DELETE FROM link
WHERE id IN (
		SELECT link.id
		FROM link
			JOIN dataset ON dataset.id = link.dataset_id
		WHERE dataset.name = 'stt_tt_gg'
	);
--
--
-- number of examples in each dataset
select dataset.name,
	count(*) as total
from example
	JOIN link ON example.id = link.example_id
	JOIN dataset ON dataset.id = link.dataset_id
GROUP BY dataset.name;
--
--
--- *  SQL * --------

--- reviewed transcripts

        SELECT 
            annotation.audio AS file_name, 
            review.session_id AS reviewer, 
            annotation.session_id AS transcriber, 
            CASE WHEN review.transcript = annotation.transcript THEN 1 ELSE 0 END AS correct, 
            review.transcript AS reviewed_transcript, 
            annotation.transcript AS original_transcript, 
            FROM_UNIXTIME(review.timestamp) AS reviewed_on, 
            FROM_UNIXTIME(annotation.timestamp) AS transcribed_on, 
            review.answer AS reviewer_answer, 
            annotation.answer AS transcriber_answer 
        FROM 
            (
                SELECT 
                    CAST(content ->> '$.text' AS CHAR CHARACTER SET utf8mb4) AS audio, 
                    CAST(content ->> '$._session_id' AS CHAR CHARACTER SET utf8mb4) AS session_id, 
                    CAST(content ->> '$.transcript' AS CHAR CHARACTER SET utf8mb4) AS transcript, 
                    CAST(content ->> '$._timestamp' AS UNSIGNED) AS timestamp, 
                    CAST(content ->> '$.answer' AS CHAR CHARACTER SET utf8mb4) AS answer 
                FROM 
                    example 
                    JOIN link ON example.id = link.example_id 
                    JOIN dataset ON dataset.id = link.dataset_id 
                WHERE 
                    dataset.name = 'stt_tt_ga'
            ) AS annotation 
        LEFT JOIN 
            (
                SELECT 
                    CAST(content ->> '$.text' AS CHAR CHARACTER SET utf8mb4) AS audio, 
                    CAST(content ->> '$._session_id' AS CHAR CHARACTER SET utf8mb4) AS session_id, 
                    CAST(content ->> '$.transcript' AS CHAR CHARACTER SET utf8mb4) AS transcript, 
                    CAST(content ->> '$._timestamp' AS UNSIGNED) AS timestamp, 
                    CAST(content ->> '$.answer' AS CHAR CHARACTER SET utf8mb4) AS answer 
                FROM 
                    example 
                    JOIN link ON example.id = link.example_id 
                    JOIN dataset ON dataset.id = link.dataset_id 
                WHERE 
                    dataset.name = 'stt_tt_ga_review'
            ) AS review 
        ON annotation.audio = review.audio 
        ORDER BY annotation.timestamp;