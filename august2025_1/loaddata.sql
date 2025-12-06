INSERT INTO factories(name) VALUES('factory1');
INSERT INTO factories(name) VALUES('factory2');
INSERT INTO factories(name) VALUES('factory3');

INSERT INTO sites(name, factoryId) 
SELECT 'site1', id FROM factories WHERE name = 'factory1';

INSERT INTO sites(name, factoryId) 
SELECT 'site2', id FROM factories WHERE name = 'factory1';

INSERT INTO equipment(name) VALUES('equipment1');
INSERT INTO equipment(name) VALUES('equipment2');
INSERT INTO equipment(name) VALUES('equipment3');

INSERT INTO sites_equipment(siteId, equipmentId)
SELECT
(SELECT id FROM sites WHERE name = 'site1'),
(SELECT id FROM equipment WHERE name = 'equipment1');

INSERT INTO sites_equipment(siteId, equipmentId)
SELECT
(SELECT id FROM sites WHERE name = 'site1'),
(SELECT id FROM equipment WHERE name = 'equipment2');

INSERT INTO sites_equipment(siteId, equipmentId)
SELECT
(SELECT id FROM sites WHERE name = 'site1'),
(SELECT id FROM equipment WHERE name = 'equipment3');

INSERT INTO sites_equipment(siteId, equipmentId)
SELECT
(SELECT id FROM sites WHERE name = 'site2'),
(SELECT id FROM equipment WHERE name = 'equipment2');
