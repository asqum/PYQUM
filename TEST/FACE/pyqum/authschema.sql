-- Initialize the database (from __init__).
-- Drop any existing data and create empty tables.

DROP TABLE IF EXISTS "user";
DROP TABLE IF EXISTS "post";
DROP TABLE IF EXISTS data;

-- Last Updated below: 2022/07/06
-- Added activity

CREATE TABLE "user" (
	"id"	INTEGER,
	"username"	TEXT NOT NULL UNIQUE,
	"password"	TEXT NOT NULL,
	"status"	TEXT NOT NULL,
	"instrument"	TEXT,
	"measurement"	TEXT,
	"analysis"	TEXT,
	"management"	TEXT,
	"fullname"	TEXT NOT NULL UNIQUE,
	"affiliation"	TEXT NOT NULL,
	"email"	TEXT,
	"since"	TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	PRIMARY KEY("id" AUTOINCREMENT)
);

CREATE TABLE "sample" (
	"id"	INTEGER,
	"author_id"	INTEGER NOT NULL,
	"samplename"	TEXT NOT NULL UNIQUE,
	"location"	TEXT NOT NULL,
	"specifications"	TEXT,
	"description"	TEXT NOT NULL,
	"registered"	TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	"co_authors"	TEXT,
	"level"	TEXT NOT NULL,
	"history"	TEXT,
	"image"	BLOB UNIQUE,
	"references"	TEXT,
	"available"	INTEGER,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("author_id") REFERENCES "user"("id")
);

CREATE TABLE "queue" (
	"id"	INTEGER NOT NULL UNIQUE,
	"system"	TEXT NOT NULL UNIQUE,
	"mission"	TEXT NOT NULL,
	"samplename"	TEXT UNIQUE,
	FOREIGN KEY("samplename") REFERENCES "sample"("samplename"),
	PRIMARY KEY("id" AUTOINCREMENT)
);

CREATE TABLE "job" (
	"id"	INTEGER NOT NULL UNIQUE,
	"user_id"	INTEGER,
	"sample_id"	INTEGER,
	"task"	TEXT,
	"dateday"	TEXT,
	"wmoment"	INTEGER,
	"startime"	TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	"parameter"	TEXT,
	"perimeter"	TEXT,
	"instrument"	TEXT,
	"comment"	TEXT,
	"note"	TEXT,
	"progress"	INTEGER,
	"measureacheta"	TEXT,
	"tag"	TEXT,
	"queue"	TEXT NOT NULL CHECK("queue" IN ('CHAR0', 'QPC0', 'QPC1')),
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("sample_id") REFERENCES "sample"("id"),
	FOREIGN KEY("user_id") REFERENCES "user"("id")
);

CREATE TABLE "CHAR0" (
	"id"	INTEGER NOT NULL UNIQUE,
	"job_id"	INTEGER NOT NULL UNIQUE,
	"token"	TEXT UNIQUE,
	FOREIGN KEY("job_id") REFERENCES "job"("id"),
	PRIMARY KEY("id")
);

CREATE TABLE "CHAR1" (
	"id"	INTEGER NOT NULL UNIQUE,
	"job_id"	INTEGER NOT NULL UNIQUE,
	"token"	TEXT UNIQUE,
	FOREIGN KEY("job_id") REFERENCES "job"("id"),
	PRIMARY KEY("id")
);

CREATE TABLE "QPC0" (
	"id"	INTEGER NOT NULL UNIQUE,
	"job_id"	INTEGER NOT NULL UNIQUE,
	"token"	TEXT UNIQUE,
	PRIMARY KEY("id"),
	FOREIGN KEY("job_id") REFERENCES "job"("id")
);

CREATE TABLE "QPC1" (
	"id"	INTEGER NOT NULL UNIQUE,
	"job_id"	INTEGER NOT NULL UNIQUE,
	"token"	TEXT UNIQUE,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("job_id") REFERENCES "job"("id")
);

CREATE TABLE "machine" (
	"id"	INTEGER NOT NULL UNIQUE,
	"codename"	TEXT NOT NULL UNIQUE,
	"since"	DATE NOT NULL DEFAULT CURRENT_DATE,
	"user_id"	INTEGER,
	"connected"	BOOL NOT NULL,
	"address"	TEXT NOT NULL UNIQUE,
	"BDR"	INTEGER NOT NULL,
	"model"	TEXT NOT NULL,
	"owner"	TEXT NOT NULL,
	"category"	TEXT NOT NULL,
	"sequence"	INTEGER,
	"system"	TEXT,
	"driver"	TEXT,
	"note"	TEXT,
	"family"	TEXT NOT NULL,
	"online"	INTEGER,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("user_id") REFERENCES "user"("id"),
	FOREIGN KEY("system") REFERENCES "queue"("system")
);

CREATE TABLE "post" (
	"id"	INTEGER PRIMARY KEY AUTOINCREMENT,
	"author_id"	INTEGER NOT NULL,
	"created"	TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	"modified"	TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	"title"	TEXT NOT NULL,
	"body"	TEXT NOT NULL,
	FOREIGN KEY("author_id") REFERENCES "user"("id")
);

CREATE TABLE "activity" (
	"id"	INTEGER NOT NULL UNIQUE,
	"user_id"	INTEGER,
	"startime"	TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	"log"	TEXT,
	"comment"	TEXT,
	"note"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("user_id") REFERENCES "user"("id")
);

