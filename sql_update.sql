DROP TABLE IF EXISTS maps;

CREATE TABLE "maps" (
	"md5"	TEXT NOT NULL,
	"id"	INTEGER NOT NULL,
	"set_id"	INTEGER NOT NULL,
	"artist"	TEXT,
	"title"	TEXT,
	"version"	TEXT,
	"creator"	TEXT,
	"last_update"	TEXT,
	"total_length"	INTEGER,
	"max_combo"	INTEGER,
	"status"	INTEGER NOT NULL,
	"mode"	INTEGER NOT NULL,
	"bpm"	INTEGER NOT NULL,
	"cs"	INTEGER NOT NULL,
	"od"	INTEGER NOT NULL,
	"ar"	INTEGER NOT NULL,
	"hp"	INTEGER NOT NULL,
	"star"	INTEGER NOT NULL
);
