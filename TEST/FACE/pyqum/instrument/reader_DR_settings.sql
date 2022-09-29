BEGIN TRANSACTION;
DROP TABLE IF EXISTS "PORT";
CREATE TABLE IF NOT EXISTS "PORT" (
	"Device"	TEXT UNIQUE,
	"Port"	INTEGER UNIQUE
);
DROP TABLE IF EXISTS "CHAR0";
CREATE TABLE IF NOT EXISTS "CHAR0" (
	"id"	INTEGER NOT NULL UNIQUE,
	"category"	TEXT NOT NULL UNIQUE,
	"designation"	TEXT NOT NULL UNIQUE,
	PRIMARY KEY("id" AUTOINCREMENT)
);
DROP TABLE IF EXISTS "CHAR1";
CREATE TABLE IF NOT EXISTS "CHAR1" (
	"id"	INTEGER NOT NULL UNIQUE,
	"category"	TEXT NOT NULL UNIQUE,
	"designation"	TEXT NOT NULL UNIQUE,
	PRIMARY KEY("id" AUTOINCREMENT)
);
DROP TABLE IF EXISTS "QPC0";
CREATE TABLE IF NOT EXISTS "QPC0" (
	"id"	INTEGER NOT NULL UNIQUE,
	"category"	TEXT NOT NULL UNIQUE,
	"designation"	TEXT NOT NULL UNIQUE,
	PRIMARY KEY("id" AUTOINCREMENT)
);
DROP TABLE IF EXISTS "QPC1";
CREATE TABLE IF NOT EXISTS "QPC1" (
	"id"	INTEGER NOT NULL UNIQUE,
	"category"	TEXT NOT NULL UNIQUE,
	"designation"	TEXT NOT NULL UNIQUE,
	PRIMARY KEY("id" AUTOINCREMENT)
);
DROP TABLE IF EXISTS "MACE";
CREATE TABLE IF NOT EXISTS "MACE" (
	"Commander"	TEXT NOT NULL UNIQUE,
	"Skills"	TEXT NOT NULL
);
DROP TABLE IF EXISTS "BDR";
CREATE TABLE IF NOT EXISTS "BDR" (
	"Name"	TEXT NOT NULL UNIQUE,
	"LogPath"	TEXT NOT NULL,
	"TPath"	TEXT NOT NULL,
	"Tname"	TEXT NOT NULL
);
INSERT INTO "PORT" ("Device","Port") VALUES ('TC',5602),
 ('RTP','http://192.168.1.139'),
 ('MXA',6618),
 ('URL','qum.phys.sinica.edu.tw'),
 ('USRLOG','D:/USRLOG'),
 ('PORTAL','C:/Users/ASQUM_2/HODOR/CONFIG/PORTAL'),
 ('BDR','Bob');
INSERT INTO "CHAR0" ("id","category","designation") VALUES (1,'DC','SDAWG_2'),
 (2,'SG','RSSGS_2'),
 (3,'NA','RSVNA_1'),
 (4,'ROLE','DC: Z2/Z12 >> SG:XY'),
 (5,'CH','DC: 3/4 >> SG:1');
INSERT INTO "QPC0" ("id","category","designation") VALUES (1,'SG','DDSLO_4,DDSLO_2'),
 (2,'DAC','SDAWG_3,SDAWG_1,SDAWG_2'),
 (3,'ADC','SDDIG_1'),
 (4,'CH','{"DAC": [[1,2],[1,2,3],[3,4]] ,
"DC":           [[1         ]            ,[1         ]]              }'),
 (5,'ROLE','{"DAC":[["I1","Q1"],["X1","Y1","Z1"],["Z2","ZC"]],
"DC":[["ZPA"],["ZC"]] }'),
 (6,'DC','');
INSERT INTO "QPC1" ("id","category","designation") VALUES (1,'ROLE','DAC:I1/Q1,X1/Y1/Z1/P1,Z2/Z12'),
 (2,'CH','DAC:1/2,1/2/3/4,3/4'),
 (3,'SG','DDSLO_3,DDSLO_1'),
 (4,'DAC','SDAWG_6,SDAWG_4,SDAWG_5'),
 (5,'ADC','SDDIG_2');
INSERT INTO "MACE" ("Commander","Skills") VALUES ('Acronym','Modular Assembly of Commander (Controllable. Continuous. Companion. Calibration. Computation) Execution'),
 ('Local Oscillator','Frequency, Power'),
 ('Random Benchmarking','Type, Sequence-length/m, Random-sampling/n');
INSERT INTO "BDR" ("Name","LogPath","TPath","Tname") VALUES ('Alice','\\BLUEFORSAS\BlueLogs','','T'),
 ('Bob','\\BLUEFORSAS2\dr_bob','\log-data\192.168.1.188','TEMPERATURE');
COMMIT;
