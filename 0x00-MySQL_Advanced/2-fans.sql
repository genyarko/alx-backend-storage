-- Task: Rank country origins of bands by the number of (non-unique) fans

-- Rank countries by the number of fans in descending order
SELECT origin, SUM(nb_fans) as nb_fans
FROM metal_bands
GROUP BY origin
ORDER BY nb_fans DESC;
