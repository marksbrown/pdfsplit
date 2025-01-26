BEGIN TRANSACTION;

CREATE TABLE IF NOT EXISTS "pages" (
	"id"	TEXT NOT NULL,
	"page"	INTEGER,
	"png"	BLOB NOT NULL,
	FOREIGN KEY("id") REFERENCES "pdfs"("id"),
	PRIMARY KEY("page","id")
);
CREATE TABLE IF NOT EXISTS "pdfs" (
	"id"	TEXT NOT NULL UNIQUE,
  "metadata" TEXT,
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "pagetags" (
	"tag"	TEXT,
	"id"	TEXT,
	"page"	INTEGER,
	FOREIGN KEY("page") REFERENCES "pages"("page"),
	FOREIGN KEY("id") REFERENCES "pages"("id"),
	PRIMARY KEY("tag","id","page")
);
COMMIT;
CREATE VIEW if not exists tags(tag, count)
as SELECT tag, COUNT(*) 
FROM pagetags 
GROUP BY tag
ORDER BY COUNT(*)
DESC
