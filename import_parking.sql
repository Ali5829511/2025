-- استيراد بيانات المواقف
BEGIN;


INSERT INTO parking_spots (spot_number, parking_area, building_id, is_occupied)
SELECT '1-1', 'G . L . P - 7',
       (SELECT id FROM buildings WHERE building_number = 'A1' LIMIT 1),
       false
WHERE NOT EXISTS (SELECT 1 FROM parking_spots WHERE spot_number = '1-1');

INSERT INTO parking_spots (spot_number, parking_area, building_id, is_occupied)
SELECT '1-2', 'G . L . P - 7',
       (SELECT id FROM buildings WHERE building_number = 'A1' LIMIT 1),
       false
WHERE NOT EXISTS (SELECT 1 FROM parking_spots WHERE spot_number = '1-2');

INSERT INTO parking_spots (spot_number, parking_area, building_id, is_occupied)
SELECT '1-3', 'G . L . P - 7',
       (SELECT id FROM buildings WHERE building_number = 'A1' LIMIT 1),
       false
WHERE NOT EXISTS (SELECT 1 FROM parking_spots WHERE spot_number = '1-3');

INSERT INTO parking_spots (spot_number, parking_area, building_id, is_occupied)
SELECT '1-4', 'G . L . P - 7',
       (SELECT id FROM buildings WHERE building_number = 'A1' LIMIT 1),
       false
WHERE NOT EXISTS (SELECT 1 FROM parking_spots WHERE spot_number = '1-4');

INSERT INTO parking_spots (spot_number, parking_area, building_id, is_occupied)
SELECT '1-11', 'G . L . P - 7',
       (SELECT id FROM buildings WHERE building_number = 'A1' LIMIT 1),
       false
WHERE NOT EXISTS (SELECT 1 FROM parking_spots WHERE spot_number = '1-11');

INSERT INTO parking_spots (spot_number, parking_area, building_id, is_occupied)
SELECT '1-12', 'G . L . P - 7',
       (SELECT id FROM buildings WHERE building_number = 'A1' LIMIT 1),
       false
WHERE NOT EXISTS (SELECT 1 FROM parking_spots WHERE spot_number = '1-12');

INSERT INTO parking_spots (spot_number, parking_area, building_id, is_occupied)
SELECT '1-13', 'G . L . P - 7',
       (SELECT id FROM buildings WHERE building_number = 'A1' LIMIT 1),
       false
WHERE NOT EXISTS (SELECT 1 FROM parking_spots WHERE spot_number = '1-13');

INSERT INTO parking_spots (spot_number, parking_area, building_id, is_occupied)
SELECT '1-14', 'G . L . P - 7',
       (SELECT id FROM buildings WHERE building_number = 'A1' LIMIT 1),
       false
WHERE NOT EXISTS (SELECT 1 FROM parking_spots WHERE spot_number = '1-14');

INSERT INTO parking_spots (spot_number, parking_area, building_id, is_occupied)
SELECT '1-21', 'G . L . P - 7',
       (SELECT id FROM buildings WHERE building_number = 'A1' LIMIT 1),
       false
WHERE NOT EXISTS (SELECT 1 FROM parking_spots WHERE spot_number = '1-21');

INSERT INTO parking_spots (spot_number, parking_area, building_id, is_occupied)
SELECT '1-22', 'G . L . P - 7',
       (SELECT id FROM buildings WHERE building_number = 'A1' LIMIT 1),
       false
WHERE NOT EXISTS (SELECT 1 FROM parking_spots WHERE spot_number = '1-22');

INSERT INTO parking_spots (spot_number, parking_area, building_id, is_occupied)
SELECT '1-23', 'G . L . P - 7',
       (SELECT id FROM buildings WHERE building_number = 'A1' LIMIT 1),
       false
WHERE NOT EXISTS (SELECT 1 FROM parking_spots WHERE spot_number = '1-23');

INSERT INTO parking_spots (spot_number, parking_area, building_id, is_occupied)
SELECT '1-24', 'G . L . P - 7',
       (SELECT id FROM buildings WHERE building_number = 'A1' LIMIT 1),
       false
WHERE NOT EXISTS (SELECT 1 FROM parking_spots WHERE spot_number = '1-24');

INSERT INTO parking_spots (spot_number, parking_area, building_id, is_occupied)
SELECT '1-31', 'G . L . P - 7',
       (SELECT id FROM buildings WHERE building_number = 'A1' LIMIT 1),
       false
WHERE NOT EXISTS (SELECT 1 FROM parking_spots WHERE spot_number = '1-31');

INSERT INTO parking_spots (spot_number, parking_area, building_id, is_occupied)
SELECT '1-32', 'G . L . P - 7',
       (SELECT id FROM buildings WHERE building_number = 'A1' LIMIT 1),
       false
WHERE NOT EXISTS (SELECT 1 FROM parking_spots WHERE spot_number = '1-32');

INSERT INTO parking_spots (spot_number, parking_area, building_id, is_occupied)
SELECT '1-33', 'G . L . P - 7',
       (SELECT id FROM buildings WHERE building_number = 'A1' LIMIT 1),
       false
WHERE NOT EXISTS (SELECT 1 FROM parking_spots WHERE spot_number = '1-33');

INSERT INTO parking_spots (spot_number, parking_area, building_id, is_occupied)
SELECT '1-34', 'G . L . P - 7',
       (SELECT id FROM buildings WHERE building_number = 'A1' LIMIT 1),
       false
WHERE NOT EXISTS (SELECT 1 FROM parking_spots WHERE spot_number = '1-34');

INSERT INTO parking_spots (spot_number, parking_area, building_id, is_occupied)
SELECT '1-41', 'G . L . P - 7',
       (SELECT id FROM buildings WHERE building_number = 'A1' LIMIT 1),
       false
WHERE NOT EXISTS (SELECT 1 FROM parking_spots WHERE spot_number = '1-41');

INSERT INTO parking_spots (spot_number, parking_area, building_id, is_occupied)
SELECT '1-42', 'G . L . P - 7',
       (SELECT id FROM buildings WHERE building_number = 'A1' LIMIT 1),
       false
WHERE NOT EXISTS (SELECT 1 FROM parking_spots WHERE spot_number = '1-42');

INSERT INTO parking_spots (spot_number, parking_area, building_id, is_occupied)
SELECT '1-43', 'G . L . P - 7',
       (SELECT id FROM buildings WHERE building_number = 'A1' LIMIT 1),
       false
WHERE NOT EXISTS (SELECT 1 FROM parking_spots WHERE spot_number = '1-43');

INSERT INTO parking_spots (spot_number, parking_area, building_id, is_occupied)
SELECT '1-44', 'G . L . P - 7',
       (SELECT id FROM buildings WHERE building_number = 'A1' LIMIT 1),
       false
WHERE NOT EXISTS (SELECT 1 FROM parking_spots WHERE spot_number = '1-44');

INSERT INTO parking_spots (spot_number, parking_area, building_id, is_occupied)
SELECT '2-1', 'G . L . P - 7',
       (SELECT id FROM buildings WHERE building_number = 'A2' LIMIT 1),
       false
WHERE NOT EXISTS (SELECT 1 FROM parking_spots WHERE spot_number = '2-1');

INSERT INTO parking_spots (spot_number, parking_area, building_id, is_occupied)
SELECT '2-2', 'G . L . P - 7',
       (SELECT id FROM buildings WHERE building_number = 'A2' LIMIT 1),
       false
WHERE NOT EXISTS (SELECT 1 FROM parking_spots WHERE spot_number = '2-2');

INSERT INTO parking_spots (spot_number, parking_area, building_id, is_occupied)
SELECT '2-3', 'G . L . P - 7',
       (SELECT id FROM buildings WHERE building_number = 'A2' LIMIT 1),
       false
WHERE NOT EXISTS (SELECT 1 FROM parking_spots WHERE spot_number = '2-3');

INSERT INTO parking_spots (spot_number, parking_area, building_id, is_occupied)
SELECT '2-4', 'G . L . P - 7',
       (SELECT id FROM buildings WHERE building_number = 'A2' LIMIT 1),
       false
WHERE NOT EXISTS (SELECT 1 FROM parking_spots WHERE spot_number = '2-4');

INSERT INTO parking_spots (spot_number, parking_area, building_id, is_occupied)
SELECT '2-11', 'G . L . P - 7',
       (SELECT id FROM buildings WHERE building_number = 'A2' LIMIT 1),
       false
WHERE NOT EXISTS (SELECT 1 FROM parking_spots WHERE spot_number = '2-11');

INSERT INTO parking_spots (spot_number, parking_area, building_id, is_occupied)
SELECT '2-12', 'G . L . P - 7',
       (SELECT id FROM buildings WHERE building_number = 'A2' LIMIT 1),
       false
WHERE NOT EXISTS (SELECT 1 FROM parking_spots WHERE spot_number = '2-12');

INSERT INTO parking_spots (spot_number, parking_area, building_id, is_occupied)
SELECT '2-13', 'G . L . P - 7',
       (SELECT id FROM buildings WHERE building_number = 'A2' LIMIT 1),
       false
WHERE NOT EXISTS (SELECT 1 FROM parking_spots WHERE spot_number = '2-13');

INSERT INTO parking_spots (spot_number, parking_area, building_id, is_occupied)
SELECT '2-14', 'G . L . P - 7',
       (SELECT id FROM buildings WHERE building_number = 'A2' LIMIT 1),
       false
WHERE NOT EXISTS (SELECT 1 FROM parking_spots WHERE spot_number = '2-14');

INSERT INTO parking_spots (spot_number, parking_area, building_id, is_occupied)
SELECT '2-21', 'G . L . P - 7',
       (SELECT id FROM buildings WHERE building_number = 'A2' LIMIT 1),
       false
WHERE NOT EXISTS (SELECT 1 FROM parking_spots WHERE spot_number = '2-21');

INSERT INTO parking_spots (spot_number, parking_area, building_id, is_occupied)
SELECT '2-22', 'G . L . P - 7',
       (SELECT id FROM buildings WHERE building_number = 'A2' LIMIT 1),
       false
WHERE NOT EXISTS (SELECT 1 FROM parking_spots WHERE spot_number = '2-22');

INSERT INTO parking_spots (spot_number, parking_area, building_id, is_occupied)
SELECT '2-23', 'G . L . P - 7',
       (SELECT id FROM buildings WHERE building_number = 'A2' LIMIT 1),
       false
WHERE NOT EXISTS (SELECT 1 FROM parking_spots WHERE spot_number = '2-23');

INSERT INTO parking_spots (spot_number, parking_area, building_id, is_occupied)
SELECT '2-24', 'G . L . P - 7',
       (SELECT id FROM buildings WHERE building_number = 'A2' LIMIT 1),
       false
WHERE NOT EXISTS (SELECT 1 FROM parking_spots WHERE spot_number = '2-24');

INSERT INTO parking_spots (spot_number, parking_area, building_id, is_occupied)
SELECT '2-31', 'G . L . P - 7',
       (SELECT id FROM buildings WHERE building_number = 'A2' LIMIT 1),
       false
WHERE NOT EXISTS (SELECT 1 FROM parking_spots WHERE spot_number = '2-31');

INSERT INTO parking_spots (spot_number, parking_area, building_id, is_occupied)
SELECT '2-32', 'G . L . P - 7',
       (SELECT id FROM buildings WHERE building_number = 'A2' LIMIT 1),
       false
WHERE NOT EXISTS (SELECT 1 FROM parking_spots WHERE spot_number = '2-32');

INSERT INTO parking_spots (spot_number, parking_area, building_id, is_occupied)
SELECT '2-33', 'G . L . P - 7',
       (SELECT id FROM buildings WHERE building_number = 'A2' LIMIT 1),
       false
WHERE NOT EXISTS (SELECT 1 FROM parking_spots WHERE spot_number = '2-33');

INSERT INTO parking_spots (spot_number, parking_area, building_id, is_occupied)
SELECT '2-34', 'G . L . P - 7',
       (SELECT id FROM buildings WHERE building_number = 'A2' LIMIT 1),
       false
WHERE NOT EXISTS (SELECT 1 FROM parking_spots WHERE spot_number = '2-34');

INSERT INTO parking_spots (spot_number, parking_area, building_id, is_occupied)
SELECT '2-41', 'G . L . P - 7',
       (SELECT id FROM buildings WHERE building_number = 'A2' LIMIT 1),
       false
WHERE NOT EXISTS (SELECT 1 FROM parking_spots WHERE spot_number = '2-41');

INSERT INTO parking_spots (spot_number, parking_area, building_id, is_occupied)
SELECT '2-42', 'G . L . P - 7',
       (SELECT id FROM buildings WHERE building_number = 'A2' LIMIT 1),
       false
WHERE NOT EXISTS (SELECT 1 FROM parking_spots WHERE spot_number = '2-42');

INSERT INTO parking_spots (spot_number, parking_area, building_id, is_occupied)
SELECT '2-43', 'G . L . P - 7',
       (SELECT id FROM buildings WHERE building_number = 'A2' LIMIT 1),
       false
WHERE NOT EXISTS (SELECT 1 FROM parking_spots WHERE spot_number = '2-43');

INSERT INTO parking_spots (spot_number, parking_area, building_id, is_occupied)
SELECT '2-44', 'G . L . P - 7',
       (SELECT id FROM buildings WHERE building_number = 'A2' LIMIT 1),
       false
WHERE NOT EXISTS (SELECT 1 FROM parking_spots WHERE spot_number = '2-44');

INSERT INTO parking_spots (spot_number, parking_area, building_id, is_occupied)
SELECT '3-1', 'G . L . P - 7',
       (SELECT id FROM buildings WHERE building_number = 'A3' LIMIT 1),
       false
WHERE NOT EXISTS (SELECT 1 FROM parking_spots WHERE spot_number = '3-1');

INSERT INTO parking_spots (spot_number, parking_area, building_id, is_occupied)
SELECT '3-2', 'G . L . P - 7',
       (SELECT id FROM buildings WHERE building_number = 'A3' LIMIT 1),
       false
WHERE NOT EXISTS (SELECT 1 FROM parking_spots WHERE spot_number = '3-2');

INSERT INTO parking_spots (spot_number, parking_area, building_id, is_occupied)
SELECT '3-3', 'G . L . P - 7',
       (SELECT id FROM buildings WHERE building_number = 'A3' LIMIT 1),
       false
WHERE NOT EXISTS (SELECT 1 FROM parking_spots WHERE spot_number = '3-3');

INSERT INTO parking_spots (spot_number, parking_area, building_id, is_occupied)
SELECT '3-4', 'G . L . P - 7',
       (SELECT id FROM buildings WHERE building_number = 'A3' LIMIT 1),
       false
WHERE NOT EXISTS (SELECT 1 FROM parking_spots WHERE spot_number = '3-4');

INSERT INTO parking_spots (spot_number, parking_area, building_id, is_occupied)
SELECT '3-11', 'G . L . P - 7',
       (SELECT id FROM buildings WHERE building_number = 'A3' LIMIT 1),
       false
WHERE NOT EXISTS (SELECT 1 FROM parking_spots WHERE spot_number = '3-11');

INSERT INTO parking_spots (spot_number, parking_area, building_id, is_occupied)
SELECT '3-12', 'G . L . P - 7',
       (SELECT id FROM buildings WHERE building_number = 'A3' LIMIT 1),
       false
WHERE NOT EXISTS (SELECT 1 FROM parking_spots WHERE spot_number = '3-12');

INSERT INTO parking_spots (spot_number, parking_area, building_id, is_occupied)
SELECT '3-13', 'G . L . P - 7',
       (SELECT id FROM buildings WHERE building_number = 'A3' LIMIT 1),
       false
WHERE NOT EXISTS (SELECT 1 FROM parking_spots WHERE spot_number = '3-13');

INSERT INTO parking_spots (spot_number, parking_area, building_id, is_occupied)
SELECT '3-14', 'G . L . P - 7',
       (SELECT id FROM buildings WHERE building_number = 'A3' LIMIT 1),
       false
WHERE NOT EXISTS (SELECT 1 FROM parking_spots WHERE spot_number = '3-14');

INSERT INTO parking_spots (spot_number, parking_area, building_id, is_occupied)
SELECT '3-21', 'G . L . P - 7',
       (SELECT id FROM buildings WHERE building_number = 'A3' LIMIT 1),
       false
WHERE NOT EXISTS (SELECT 1 FROM parking_spots WHERE spot_number = '3-21');

INSERT INTO parking_spots (spot_number, parking_area, building_id, is_occupied)
SELECT '3-22', 'G . L . P - 7',
       (SELECT id FROM buildings WHERE building_number = 'A3' LIMIT 1),
       false
WHERE NOT EXISTS (SELECT 1 FROM parking_spots WHERE spot_number = '3-22');

INSERT INTO parking_spots (spot_number, parking_area, building_id, is_occupied)
SELECT '3-23', 'G . L . P - 7',
       (SELECT id FROM buildings WHERE building_number = 'A3' LIMIT 1),
       false
WHERE NOT EXISTS (SELECT 1 FROM parking_spots WHERE spot_number = '3-23');

INSERT INTO parking_spots (spot_number, parking_area, building_id, is_occupied)
SELECT '3-24', 'G . L . P - 7',
       (SELECT id FROM buildings WHERE building_number = 'A3' LIMIT 1),
       false
WHERE NOT EXISTS (SELECT 1 FROM parking_spots WHERE spot_number = '3-24');

INSERT INTO parking_spots (spot_number, parking_area, building_id, is_occupied)
SELECT '3-31', 'G . L . P - 7',
       (SELECT id FROM buildings WHERE building_number = 'A3' LIMIT 1),
       false
WHERE NOT EXISTS (SELECT 1 FROM parking_spots WHERE spot_number = '3-31');

INSERT INTO parking_spots (spot_number, parking_area, building_id, is_occupied)
SELECT '3-32', 'G . L . P - 7',
       (SELECT id FROM buildings WHERE building_number = 'A3' LIMIT 1),
       false
WHERE NOT EXISTS (SELECT 1 FROM parking_spots WHERE spot_number = '3-32');

INSERT INTO parking_spots (spot_number, parking_area, building_id, is_occupied)
SELECT '3-33', 'G . L . P - 7',
       (SELECT id FROM buildings WHERE building_number = 'A3' LIMIT 1),
       false
WHERE NOT EXISTS (SELECT 1 FROM parking_spots WHERE spot_number = '3-33');

INSERT INTO parking_spots (spot_number, parking_area, building_id, is_occupied)
SELECT '3-34', 'G . L . P - 7',
       (SELECT id FROM buildings WHERE building_number = 'A3' LIMIT 1),
       false
WHERE NOT EXISTS (SELECT 1 FROM parking_spots WHERE spot_number = '3-34');

INSERT INTO parking_spots (spot_number, parking_area, building_id, is_occupied)
SELECT '3-41', 'G . L . P - 7',
       (SELECT id FROM buildings WHERE building_number = 'A3' LIMIT 1),
       false
WHERE NOT EXISTS (SELECT 1 FROM parking_spots WHERE spot_number = '3-41');

INSERT INTO parking_spots (spot_number, parking_area, building_id, is_occupied)
SELECT '3-42', 'G . L . P - 7',
       (SELECT id FROM buildings WHERE building_number = 'A3' LIMIT 1),
       false
WHERE NOT EXISTS (SELECT 1 FROM parking_spots WHERE spot_number = '3-42');

INSERT INTO parking_spots (spot_number, parking_area, building_id, is_occupied)
SELECT '3-43', 'G . L . P - 7',
       (SELECT id FROM buildings WHERE building_number = 'A3' LIMIT 1),
       false
WHERE NOT EXISTS (SELECT 1 FROM parking_spots WHERE spot_number = '3-43');

INSERT INTO parking_spots (spot_number, parking_area, building_id, is_occupied)
SELECT '3-44', 'G . L . P - 7',
       (SELECT id FROM buildings WHERE building_number = 'A3' LIMIT 1),
       false
WHERE NOT EXISTS (SELECT 1 FROM parking_spots WHERE spot_number = '3-44');

INSERT INTO parking_spots (spot_number, parking_area, building_id, is_occupied)
SELECT '4-1', 'G . L . P - 6',
       (SELECT id FROM buildings WHERE building_number = 'A4' LIMIT 1),
       false
WHERE NOT EXISTS (SELECT 1 FROM parking_spots WHERE spot_number = '4-1');

INSERT INTO parking_spots (spot_number, parking_area, building_id, is_occupied)
SELECT '4-2', 'G . L . P - 6',
       (SELECT id FROM buildings WHERE building_number = 'A4' LIMIT 1),
       false
WHERE NOT EXISTS (SELECT 1 FROM parking_spots WHERE spot_number = '4-2');

INSERT INTO parking_spots (spot_number, parking_area, building_id, is_occupied)
SELECT '4-3', 'G . L . P - 6',
       (SELECT id FROM buildings WHERE building_number = 'A4' LIMIT 1),
       false
WHERE NOT EXISTS (SELECT 1 FROM parking_spots WHERE spot_number = '4-3');

INSERT INTO parking_spots (spot_number, parking_area, building_id, is_occupied)
SELECT '4-4', 'G . L . P - 6',
       (SELECT id FROM buildings WHERE building_number = 'A4' LIMIT 1),
       false
WHERE NOT EXISTS (SELECT 1 FROM parking_spots WHERE spot_number = '4-4');

INSERT INTO parking_spots (spot_number, parking_area, building_id, is_occupied)
SELECT '4-11', 'G . L . P - 6',
       (SELECT id FROM buildings WHERE building_number = 'A4' LIMIT 1),
       false
WHERE NOT EXISTS (SELECT 1 FROM parking_spots WHERE spot_number = '4-11');

INSERT INTO parking_spots (spot_number, parking_area, building_id, is_occupied)
SELECT '4-12', 'G . L . P - 6',
       (SELECT id FROM buildings WHERE building_number = 'A4' LIMIT 1),
       false
WHERE NOT EXISTS (SELECT 1 FROM parking_spots WHERE spot_number = '4-12');

INSERT INTO parking_spots (spot_number, parking_area, building_id, is_occupied)
SELECT '4-13', 'G . L . P - 6',
       (SELECT id FROM buildings WHERE building_number = 'A4' LIMIT 1),
       false
WHERE NOT EXISTS (SELECT 1 FROM parking_spots WHERE spot_number = '4-13');

INSERT INTO parking_spots (spot_number, parking_area, building_id, is_occupied)
SELECT '4-14', 'G . L . P - 6',
       (SELECT id FROM buildings WHERE building_number = 'A4' LIMIT 1),
       false
WHERE NOT EXISTS (SELECT 1 FROM parking_spots WHERE spot_number = '4-14');

INSERT INTO parking_spots (spot_number, parking_area, building_id, is_occupied)
SELECT '4-21', 'G . L . P - 6',
       (SELECT id FROM buildings WHERE building_number = 'A4' LIMIT 1),
       false
WHERE NOT EXISTS (SELECT 1 FROM parking_spots WHERE spot_number = '4-21');

INSERT INTO parking_spots (spot_number, parking_area, building_id, is_occupied)
SELECT '4-22', 'G . L . P - 6',
       (SELECT id FROM buildings WHERE building_number = 'A4' LIMIT 1),
       false
WHERE NOT EXISTS (SELECT 1 FROM parking_spots WHERE spot_number = '4-22');

INSERT INTO parking_spots (spot_number, parking_area, building_id, is_occupied)
SELECT '4-23', 'G . L . P - 6',
       (SELECT id FROM buildings WHERE building_number = 'A4' LIMIT 1),
       false
WHERE NOT EXISTS (SELECT 1 FROM parking_spots WHERE spot_number = '4-23');

INSERT INTO parking_spots (spot_number, parking_area, building_id, is_occupied)
SELECT '4-24', 'G . L . P - 6',
       (SELECT id FROM buildings WHERE building_number = 'A4' LIMIT 1),
       false
WHERE NOT EXISTS (SELECT 1 FROM parking_spots WHERE spot_number = '4-24');

INSERT INTO parking_spots (spot_number, parking_area, building_id, is_occupied)
SELECT '4-31', 'G . L . P - 6',
       (SELECT id FROM buildings WHERE building_number = 'A4' LIMIT 1),
       false
WHERE NOT EXISTS (SELECT 1 FROM parking_spots WHERE spot_number = '4-31');

INSERT INTO parking_spots (spot_number, parking_area, building_id, is_occupied)
SELECT '4-32', 'G . L . P - 6',
       (SELECT id FROM buildings WHERE building_number = 'A4' LIMIT 1),
       false
WHERE NOT EXISTS (SELECT 1 FROM parking_spots WHERE spot_number = '4-32');

INSERT INTO parking_spots (spot_number, parking_area, building_id, is_occupied)
SELECT '4-33', 'G . L . P - 6',
       (SELECT id FROM buildings WHERE building_number = 'A4' LIMIT 1),
       false
WHERE NOT EXISTS (SELECT 1 FROM parking_spots WHERE spot_number = '4-33');

INSERT INTO parking_spots (spot_number, parking_area, building_id, is_occupied)
SELECT '4-34', 'G . L . P - 6',
       (SELECT id FROM buildings WHERE building_number = 'A4' LIMIT 1),
       false
WHERE NOT EXISTS (SELECT 1 FROM parking_spots WHERE spot_number = '4-34');

INSERT INTO parking_spots (spot_number, parking_area, building_id, is_occupied)
SELECT '4-41', 'G . L . P - 6',
       (SELECT id FROM buildings WHERE building_number = 'A4' LIMIT 1),
       false
WHERE NOT EXISTS (SELECT 1 FROM parking_spots WHERE spot_number = '4-41');

INSERT INTO parking_spots (spot_number, parking_area, building_id, is_occupied)
SELECT '4-42', 'G . L . P - 6',
       (SELECT id FROM buildings WHERE building_number = 'A4' LIMIT 1),
       false
WHERE NOT EXISTS (SELECT 1 FROM parking_spots WHERE spot_number = '4-42');

INSERT INTO parking_spots (spot_number, parking_area, building_id, is_occupied)
SELECT '4-43', 'G . L . P - 6',
       (SELECT id FROM buildings WHERE building_number = 'A4' LIMIT 1),
       false
WHERE NOT EXISTS (SELECT 1 FROM parking_spots WHERE spot_number = '4-43');

INSERT INTO parking_spots (spot_number, parking_area, building_id, is_occupied)
SELECT '4-44', 'G . L . P - 6',
       (SELECT id FROM buildings WHERE building_number = 'A4' LIMIT 1),
       false
WHERE NOT EXISTS (SELECT 1 FROM parking_spots WHERE spot_number = '4-44');

INSERT INTO parking_spots (spot_number, parking_area, building_id, is_occupied)
SELECT '5-1', 'G . L . P - 6',
       (SELECT id FROM buildings WHERE building_number = 'A5' LIMIT 1),
       false
WHERE NOT EXISTS (SELECT 1 FROM parking_spots WHERE spot_number = '5-1');

INSERT INTO parking_spots (spot_number, parking_area, building_id, is_occupied)
SELECT '5-2', 'G . L . P - 6',
       (SELECT id FROM buildings WHERE building_number = 'A5' LIMIT 1),
       false
WHERE NOT EXISTS (SELECT 1 FROM parking_spots WHERE spot_number = '5-2');

INSERT INTO parking_spots (spot_number, parking_area, building_id, is_occupied)
SELECT '5-3', 'G . L . P - 6',
       (SELECT id FROM buildings WHERE building_number = 'A5' LIMIT 1),
       false
WHERE NOT EXISTS (SELECT 1 FROM parking_spots WHERE spot_number = '5-3');

INSERT INTO parking_spots (spot_number, parking_area, building_id, is_occupied)
SELECT '5-4', 'G . L . P - 6',
       (SELECT id FROM buildings WHERE building_number = 'A5' LIMIT 1),
       false
WHERE NOT EXISTS (SELECT 1 FROM parking_spots WHERE spot_number = '5-4');

INSERT INTO parking_spots (spot_number, parking_area, building_id, is_occupied)
SELECT '5-11', 'G . L . P - 6',
       (SELECT id FROM buildings WHERE building_number = 'A5' LIMIT 1),
       false
WHERE NOT EXISTS (SELECT 1 FROM parking_spots WHERE spot_number = '5-11');

INSERT INTO parking_spots (spot_number, parking_area, building_id, is_occupied)
SELECT '5-12', 'G . L . P - 6',
       (SELECT id FROM buildings WHERE building_number = 'A5' LIMIT 1),
       false
WHERE NOT EXISTS (SELECT 1 FROM parking_spots WHERE spot_number = '5-12');

INSERT INTO parking_spots (spot_number, parking_area, building_id, is_occupied)
SELECT '5-13', 'G . L . P - 6',
       (SELECT id FROM buildings WHERE building_number = 'A5' LIMIT 1),
       false
WHERE NOT EXISTS (SELECT 1 FROM parking_spots WHERE spot_number = '5-13');

INSERT INTO parking_spots (spot_number, parking_area, building_id, is_occupied)
SELECT '5-14', 'G . L . P - 6',
       (SELECT id FROM buildings WHERE building_number = 'A5' LIMIT 1),
       false
WHERE NOT EXISTS (SELECT 1 FROM parking_spots WHERE spot_number = '5-14');

INSERT INTO parking_spots (spot_number, parking_area, building_id, is_occupied)
SELECT '5-21', 'G . L . P - 6',
       (SELECT id FROM buildings WHERE building_number = 'A5' LIMIT 1),
       false
WHERE NOT EXISTS (SELECT 1 FROM parking_spots WHERE spot_number = '5-21');

INSERT INTO parking_spots (spot_number, parking_area, building_id, is_occupied)
SELECT '5-22', 'G . L . P - 6',
       (SELECT id FROM buildings WHERE building_number = 'A5' LIMIT 1),
       false
WHERE NOT EXISTS (SELECT 1 FROM parking_spots WHERE spot_number = '5-22');

INSERT INTO parking_spots (spot_number, parking_area, building_id, is_occupied)
SELECT '5-23', 'G . L . P - 6',
       (SELECT id FROM buildings WHERE building_number = 'A5' LIMIT 1),
       false
WHERE NOT EXISTS (SELECT 1 FROM parking_spots WHERE spot_number = '5-23');

INSERT INTO parking_spots (spot_number, parking_area, building_id, is_occupied)
SELECT '5-24', 'G . L . P - 6',
       (SELECT id FROM buildings WHERE building_number = 'A5' LIMIT 1),
       false
WHERE NOT EXISTS (SELECT 1 FROM parking_spots WHERE spot_number = '5-24');

INSERT INTO parking_spots (spot_number, parking_area, building_id, is_occupied)
SELECT '5-31', 'G . L . P - 6',
       (SELECT id FROM buildings WHERE building_number = 'A5' LIMIT 1),
       false
WHERE NOT EXISTS (SELECT 1 FROM parking_spots WHERE spot_number = '5-31');

INSERT INTO parking_spots (spot_number, parking_area, building_id, is_occupied)
SELECT '5-32', 'G . L . P - 6',
       (SELECT id FROM buildings WHERE building_number = 'A5' LIMIT 1),
       false
WHERE NOT EXISTS (SELECT 1 FROM parking_spots WHERE spot_number = '5-32');

INSERT INTO parking_spots (spot_number, parking_area, building_id, is_occupied)
SELECT '5-33', 'G . L . P - 6',
       (SELECT id FROM buildings WHERE building_number = 'A5' LIMIT 1),
       false
WHERE NOT EXISTS (SELECT 1 FROM parking_spots WHERE spot_number = '5-33');

INSERT INTO parking_spots (spot_number, parking_area, building_id, is_occupied)
SELECT '5-34', 'G . L . P - 6',
       (SELECT id FROM buildings WHERE building_number = 'A5' LIMIT 1),
       false
WHERE NOT EXISTS (SELECT 1 FROM parking_spots WHERE spot_number = '5-34');

INSERT INTO parking_spots (spot_number, parking_area, building_id, is_occupied)
SELECT '5-41', 'G . L . P - 6',
       (SELECT id FROM buildings WHERE building_number = 'A5' LIMIT 1),
       false
WHERE NOT EXISTS (SELECT 1 FROM parking_spots WHERE spot_number = '5-41');

INSERT INTO parking_spots (spot_number, parking_area, building_id, is_occupied)
SELECT '5-42', 'G . L . P - 6',
       (SELECT id FROM buildings WHERE building_number = 'A5' LIMIT 1),
       false
WHERE NOT EXISTS (SELECT 1 FROM parking_spots WHERE spot_number = '5-42');

INSERT INTO parking_spots (spot_number, parking_area, building_id, is_occupied)
SELECT '5-43', 'G . L . P - 6',
       (SELECT id FROM buildings WHERE building_number = 'A5' LIMIT 1),
       false
WHERE NOT EXISTS (SELECT 1 FROM parking_spots WHERE spot_number = '5-43');

INSERT INTO parking_spots (spot_number, parking_area, building_id, is_occupied)
SELECT '5-44', 'G . L . P - 6',
       (SELECT id FROM buildings WHERE building_number = 'A5' LIMIT 1),
       false
WHERE NOT EXISTS (SELECT 1 FROM parking_spots WHERE spot_number = '5-44');

COMMIT;
