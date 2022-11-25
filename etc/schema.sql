CREATE TABLE bibliographics (

	id          TEXT,
	submitter   TEXT,
	author      TEXT,
	title       TEXT,
	date        TEXT,
	abstract    TEXT,
	comments    TEXT,
	journal     TEXT,
	doi         TEXT,
	report      TEXT,
	license     TEXT,
	landingPage TEXT,
	pdf         TEXT

);

CREATE TABLE categories (

	id       TEXT,
	category TEXT

);

CREATE TABLE authors (

	id           TEXT,
	firstName    TEXT,
	lastName     TEXT,
	affilitation TEXT
	
);

