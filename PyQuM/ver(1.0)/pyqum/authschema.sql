-- Initialize the database.
-- Drop any existing data and create empty tables.

DROP TABLE IF EXISTS "user";
DROP TABLE IF EXISTS "post";
DROP TABLE IF EXISTS data;

-- CREATE TABLE user (
--   id INTEGER PRIMARY KEY AUTOINCREMENT,
--   username TEXT UNIQUE NOT NULL,
--   password TEXT NOT NULL,
--   status TEXT NOT NULL
-- );

CREATE TABLE "user" (
	"id"	INTEGER PRIMARY KEY AUTOINCREMENT,
	"username"	TEXT NOT NULL UNIQUE,
	"password"	TEXT NOT NULL,
	"status"	TEXT NOT NULL,
	"measurement"	TEXT,
	"instrument"	TEXT,
  "analysis"    TEXT
);

CREATE TABLE "post" (
	"id"	INTEGER PRIMARY KEY AUTOINCREMENT,
	"author_id"	INTEGER NOT NULL,
	"created"	TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	"title"	TEXT NOT NULL,
	"body"	TEXT NOT NULL,
	FOREIGN KEY("author_id") REFERENCES "user"("id")
);

CREATE TABLE "sample" (
	"id"	INTEGER PRIMARY KEY AUTOINCREMENT,
	"author_id"	INTEGER NOT NULL,
	"samplename"	TEXT NOT NULL UNIQUE,
	"created"	TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	"measured"	TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	"co_authors"	TEXT,
	FOREIGN KEY("author_id") REFERENCES "user"("id")
);

CREATE TABLE "note" (
	"id"	INTEGER PRIMARY KEY AUTOINCREMENT,
	"author_id"	INTEGER NOT NULL,
	"created"	TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	"modified"	TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	"analysis"	TEXT,
	"conclusion"	TEXT,
	"reference"	TEXT,
	FOREIGN KEY("author_id") REFERENCES "user"("id")
);
