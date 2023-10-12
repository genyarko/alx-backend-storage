-- Task: List all bands with Glam rock as their main style, ranked by longevity

-- Calculate lifespan based on the 'formed' and 'split' attributes
SELECT band_name, IF(splitted = 0, 0, 2022 - formed) as lifespan
FROM (
    -- Select bands with 'Glam rock' as their main style
    SELECT band_name, formed, IFNULL(split_year, 0) as splitted
    FROM metal_bands
    WHERE main_style = 'Glam rock'
) AS glam_rock_bands
ORDER BY lifespan DESC;
