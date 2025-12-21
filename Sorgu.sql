/*
Proje: NASA Exoplanet Analysis
Dosya: final_12_gezegen.sql
Açıklama: Bu sorgu, proje için belirlenen özel 12 gezegeni (The Chosen 12)
          NASA HWC veri setinden bilimsel kriterlere göre filtreleyerek
          'Final_12_Gezegen' tablosunu oluşturur.
*/

CREATE OR REPLACE TABLE `NASA_Exoplanet_Archive.HWC DATA.12_Gezegen` AS
-- 1. GRUP: KOMŞULAR
(
  SELECT 
    P_NAME AS Planet_Name, 
    P_ESI AS ESI_Score, 
    P_RADIUS AS Radius_Earth, 
    P_YEAR AS Discovery_Year, 
    S_DISTANCE AS Distance_Parsec, 
    'En Yakın Komşu' AS Category
  FROM `NASA_Exoplanet_Archive.HWC DATA`
  WHERE S_DISTANCE < 5 
  AND P_RADIUS < 1.15 
  AND P_HABITABLE > 0
  ORDER BY S_DISTANCE ASC
  LIMIT 3
)

UNION ALL

-- 2. GRUP: TRAPPIST 
(
  SELECT 
    P_NAME, P_ESI, P_RADIUS, P_YEAR, S_DISTANCE, 
    'Yüksek Benzerlik' AS Category
  FROM `NASA_Exoplanet_Archive.HWC DATA`
  WHERE P_NAME LIKE 'TRAPPIST%' AND P_RADIUS > 0.85
  LIMIT 1
)

UNION ALL

-- 3. GRUP: MODERN KEŞİFLER 
(
  SELECT 
    P_NAME, 
    P_ESI, 
    P_RADIUS, 
    P_YEAR, 
    S_DISTANCE, 
    'Yüksek Benzerlik' AS Category
  FROM `NASA_Exoplanet_Archive.HWC DATA`
  WHERE P_NAME LIKE 'Kepler%' 
    AND P_YEAR >= 2015 
    AND P_ESI > 0.82 
  ORDER BY P_ESI DESC
  LIMIT 4
)

UNION ALL

-- 4. GRUP: SÜPER DÜNYA 
(
  SELECT 
    P_NAME, 
    P_ESI, 
    P_RADIUS, 
    P_YEAR, 
    S_DISTANCE, 
    'Yüksek Benzerlik' AS Category
  FROM `NASA_Exoplanet_Archive.HWC DATA`
  WHERE P_NAME LIKE 'LHS%' 
  AND P_HABITABLE > 0
  LIMIT 1
)

UNION ALL

-- 5. GRUP: TARİHİ EFSANELER 
-- Her yılın (2011, 2013, 2014) en küçük yarıçaplı (en iyi) adayını alıyoruz.
(SELECT 
   P_NAME, 
   P_ESI, 
   P_RADIUS, 
   P_YEAR, 
   S_DISTANCE, 
   'Tarihi Keşif' AS Category 
 FROM `NASA_Exoplanet_Archive.HWC DATA`
 WHERE P_NAME LIKE 'Kepler%' 
 AND P_YEAR = 2011 
 AND P_HABITABLE > 0 
 LIMIT 1)

UNION ALL

(SELECT 
    P_NAME, 
    P_ESI, 
    P_RADIUS, 
    P_YEAR, 
    S_DISTANCE, 
    'Tarihi Keşif' AS Category 
 FROM `NASA_Exoplanet_Archive.HWC DATA` 
 WHERE P_NAME LIKE 'Kepler%' 
 AND P_YEAR = 2013 
 AND P_HABITABLE > 0 
 ORDER BY P_RADIUS ASC 
 LIMIT 1)

UNION ALL

(SELECT 
    P_NAME, 
    P_ESI, 
    P_RADIUS, 
    P_YEAR, 
    S_DISTANCE, 
    'Tarihi Keşif' AS Category 
 FROM `NASA_Exoplanet_Archive.HWC DATA` 
 WHERE P_NAME LIKE 'Kepler%' 
 AND P_YEAR = 2014 
 AND P_HABITABLE > 0 
 ORDER BY P_RADIUS ASC 
 LIMIT 1)
 ;
