CREATE TABLE sqlite_sequence(name,seq);
CREATE TABLE Phrases (
    user_id INTEGER REFERENCES User(user_id),
    phrase VARCHAR(128),
	session CHARACTER(36) UNIQUE NOT NULL,
	push_key CHARACTER(36) UNIQUE NOT NULL,
	verified BOOLEAN DEFAULT FALSE,
    created_at DATETIME DEFAULT GETDATE
);
CREATE TABLE User (
	user_id INTEGER PRIMARY KEY AUTOINCREMENT,
	first_name VARCHAR(100),
	last_name VARCHAR(100),
	email VARCHAR(100) UNIQUE NOT NULL,
    salt CHARACTER(36) NOT NULL,
    password CHARACTER(128)
, push_token VARCHAR(100));
