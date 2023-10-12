-- Task: List all bands with Glam rock as their main style, ranked by longevity

-- Calculate lifespan based on the 'formed' and 'split' attributes
SELECT band_name, (IFNULL(split, '2020') - formed) AS lifespan
    FROM metal_bands
    WHERE FIND_IN_SET('Glam rock', IFNULL(style, "")) > 0
    ORDER BY lifespan DESC;
