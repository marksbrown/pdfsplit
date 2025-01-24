BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "tags" (
	"tag"	TEXT NOT NULL UNIQUE,
	PRIMARY KEY("tag")
);
CREATE TABLE IF NOT EXISTS "Pages" (
	"id"	TEXT NOT NULL,
	"page"	INTEGER,
	"png"	BLOB NOT NULL,
	FOREIGN KEY("id") REFERENCES "pdfs"("id"),
	PRIMARY KEY("page","id")
);
CREATE TABLE IF NOT EXISTS "pdfs" (
	"id"	TEXT NOT NULL UNIQUE,
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "PageTags" (
	"tag"	TEXT,
	"id"	TEXT,
	"page"	INTEGER,
	FOREIGN KEY("page") REFERENCES "Pages"("page"),
	PRIMARY KEY("tag","id","page"),
	FOREIGN KEY("id") REFERENCES "Pages"("id"),
	FOREIGN KEY("tag") REFERENCES "tags"("tag")
);
COMMIT;
