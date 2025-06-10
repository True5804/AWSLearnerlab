--Account
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(30) NOT NULL,
    role ENUM('admin', 'supplier', 'hospital') NOT NULL
);

INSERT INTO users (username, password, role) VALUES
('admin1',    'scrypt:32768:8:1$zlkMb5Z7S4JlRXYz$82a8d2acffef70eccafab753edddbe62bec358606267e8ea01c84ab23b18bec358bdbb75045f8d3b744f2f0192d768fcd1a3f38e9b47a94a48b2e32d10eb90fd', 'admin'),
('supplier1', 'scrypt:32768:8:1$HJbi86TY8IN6O6By$69754f780772ab149c56417c3e79a2b4b839565b9cf45717d42d32690d1b9cffca20798aceebb484892a00da8596f19fa5c8b7e1456fd5519eccb13f6473a0df', 'supplier'),
('hospital1', 'scrypt:32768:8:1$6Les7ItRQbe2Ztjr$3a948c59006a1dfdf3661c773621251fca5d36421ca7d73fb7aba19a4c63a312fcb59fadaef93ca9645b7b497e8dabcf1a335f48225b572d1bf40a0401620362', 'hospital');

CREATE TABLE password_change_log ( 
  id INT AUTO_INCREMENT PRIMARY KEY,
  account_name VARCHAR(50),
  old_hash VARCHAR(100),
  new_hash VARCHAR(100),
  changed_by VARCHAR(50), -- self or admin
  change_time DATETIME
);

-- Suppliers
CREATE TABLE suppliers (
  supplier_name VARCHAR(50),
  tel_number VARCHAR(20),
  account_name VARCHAR(50) PRIMARY KEY NOT NULL,
  add_time DATETIME
);

INSERT INTO suppliers (supplier_name, tel_number, account_name, pwd, add_time) VALUES
('MediCore Technologies',      '0911222333', 'supplier1',    'supplier123',   '2025-06-04 08:31:00'),

('LifeWell Supplies Ltd.',     '0922344556', 'lifewell',    'lw1234',   '2025-06-03 15:27:00'),
('NovaHealth Group',           '0933455667', 'novahealth',  'nhpass',   '2025-06-01 10:14:00'),
('SureCare Medical Co.',       '0944566778', 'surecare',    'sc4567',   '2025-06-02 19:45:00'),
('GlobeMed Inc.',              '0955677889', 'globemed',    'gmsecure', '2025-06-04 13:05:00'),
('BioTrust Solutions',         '0966788990', 'biotrust',    'bt12345',  '2025-06-04 07:49:00'),
('EverGreen Diagnostics',      '0977899001', 'evergreen',   'eg8888',   '2025-06-03 21:17:00'),
('PrimeAid Medical',           '0988900112', 'primeaid',    'pa3210',   '2025-06-02 11:23:00'),
('NextGen Supplies',           '0999011223', 'nextgen',     'ngpass1',  '2025-06-01 17:36:00'),
('CareLink Systems Ltd.',      '0900122334', 'carelink',    'clmed99',  '2025-06-03 09:10:00');
--

-- Hospitals
CREATE TABLE hospitals (
  hospital_name VARCHAR(50),
  hospital_address VARCHAR(42),
  tel_number VARCHAR(20),
  account_name VARCHAR(50) PRIMARY KEY NOT NULL,
  add_time DATETIME
);

--Authorized
INSERT INTO hospitals (hospital_name, hospital_address, tel_number, account_name, add_time) VALUES
('Starlight Medical Center',     '123 Starlight Blvd, Los Angeles, CA',     '0911222333', 'starlight', '2025-06-04 08:15:00'),
('Greenfield General Hospital',  '456 Green Ave, Seattle, WA',              '0922333444', 'greenfield', '2025-06-03 14:22:00'),
('Riverstone Health Center',     '789 Riverstone Rd, Austin, TX',           '0933444555', 'riverstone', '2025-06-01 17:40:00'),
('SummitView Hospital',          '22 Summit View Dr, Denver, CO',           '0944555666', 'summitview', '2025-06-02 11:05:00'),
('Pinehill Medical Center',      '35 Pinehill St, Portland, OR',            '0955666777', 'pinehill', '2025-06-04 13:59:00'),
('Lakeview Community Hospital',  '88 Lakeview Ln, Chicago, IL',             '0966777888', 'lakeview', '2025-06-03 18:33:00'),
('Northbridge Medical Center',   '102 Northbridge Blvd, Boston, MA',        '0977888999', 'northbridge', '2025-06-02 09:47:00'),
('Oakridge General Hospital',    '77 Oakridge Dr, Phoenix, AZ',             '0988999000', 'oakridge', '2025-06-01 20:25:00'),
('Westfield Medical Institute',  '19 Westfield Way, Atlanta, GA',           '0999000111', 'westfield', '2025-06-03 10:11:00'),
('Silverline Healthcare Center', '66 Silverline Ave, New York, NY',         '0900111222', 'silverline', '2025-06-04 07:00:00');
--

-- Donors
CREATE TABLE donors (
  donorName VARCHAR(100),
  age INT,
  gender CHAR(1),
  phone_number VARCHAR(20),
  bloodGroup VARCHAR(5),
  bloodVolume INT,
  bloodUniqueId INT AUTOINCREMENT PRIMARY KEY,
  donatedTime DATETIME
);

INSERT INTO donors (donorName, age, gender, phone_number, bloodGroup, bloodVolume, bloodUniqueId, donatedTime) VALUES ('James Johnson', 45, 'M', 09685794338, 'B-', 200, 0, '2023-04-27 12:58:14');
INSERT INTO donors (donorName, age, gender, phone_number, bloodGroup, bloodVolume, bloodUniqueId, donatedTime) VALUES ('Jennifer Howell', 60, 'F', 9045890381, 'AB+', 350, 1, '2025-02-04 00:53:31');
INSERT INTO donors (donorName, age, gender, phone_number, bloodGroup, bloodVolume, bloodUniqueId, donatedTime) VALUES ('Andrew Sellers', 38, 'M', 9851219904, 'A-', 300, 2, '2023-05-20 09:39:31');
INSERT INTO donors (donorName, age, gender, phone_number, bloodGroup, bloodVolume, bloodUniqueId, donatedTime) VALUES ('Henry Parks', 37, 'M', 9045890381, 'O-', 500, 3, '2025-05-14 04:56:17');
INSERT INTO donors (donorName, age, gender, phone_number, bloodGroup, bloodVolume, bloodUniqueId, donatedTime) VALUES ('Charles Lawson', 27, 'M', 9509742858, 'AB+', 250, 4, '2022-06-17 00:18:27');
INSERT INTO donors (donorName, age, gender, phone_number, bloodGroup, bloodVolume, bloodUniqueId, donatedTime) VALUES ('Lauren Hernandez', 36, 'F', 9491917660, 'O+', 300, 5, '2024-05-19 15:51:22');
INSERT INTO donors (donorName, age, gender, phone_number, bloodGroup, bloodVolume, bloodUniqueId, donatedTime) VALUES ('Stephanie Carter', 51, 'F',9217990311, 'A+', 250, 6, '2023-02-21 08:51:09');

-- Patients 
CREATE TABLE patients (
  patientName VARCHAR(100),
  age INT,
  gender CHAR(1),
  phone_number VARCHAR(20),
  bloodGroup VARCHAR(5),
  usedBloodId INT,
  usedTime DATETIME
);

INSERT INTO patients (patientName, age, phone_number, bloodGroup, usedBloodId, usedTime) VALUES ('Shane Richardson', 18, 9020143516, 'AB+', 2, '2024-05-02 14:43:31');
INSERT INTO patients (patientName, age, phone_number, bloodGroup, usedBloodId, usedTime) VALUES ('Kevin Pearson', 39, 9247884597, 'A+', 6, '2023-01-31 03:25:42');
INSERT INTO patients (patientName, age, phone_number, bloodGroup, usedBloodId, usedTime) VALUES ('Elizabeth Johnson', 34, 9423193665, 'O+', 4, '2023-09-10 04:35:12');
--
INSERT INTO patients (patientName, age, phone_number, bloodGroup, usedBloodId, usedTime) VALUES ('Anthony Rojas', 48, 9116609752, 'AB-', 2003, '2024-12-02 11:07:38');
INSERT INTO patients (patientName, age, phone_number, bloodGroup, usedBloodId, usedTime) VALUES ('Melissa Brown', 51, 9729016284, 'B-', 2004, '2024-11-27 17:34:42');
INSERT INTO patients (patientName, age, phone_number, bloodGroup, usedBloodId, usedTime) VALUES ('Gary Hurst DDS', 7, 0013847377, 'A-', 2005, '2023-01-15 01:03:28');

-- Blood
CREATE TABLE blood (
  id INT AUTO_INCREMENT PRIMARY KEY,
  blood_group VARCHAR(5),
  donor_name VARCHAR(50),
  volume INT,
  status VARCHAR(20) DEFAULT 'Active'
);

INSERT INTO blood (id, blood_group, donor_name, volume, status) VALUES
(1, 'B-', 'James Johnson', 200, 'Active'),
(2, 'AB+', 'Jennifer Howell', 350, 'Shipped'),
(3, 'A-', 'Andrew Sellers', 300, 'Shipped'),
(4, 'O-', 'Henry Parks', 500, 'Fulfilled'),
(5, 'AB+', 'Charles Lawson', 250, 'Shipped'),
(6, 'O+', 'Lauren Hernandez', 300, 'Active'),
(7, 'A+', 'Nick', 500, 'Fulfilled'),
(8, 'B+', 'Lilly', 250, 'Fulfilled'),
(9, 'O-', 'John', 350, 'Active');
