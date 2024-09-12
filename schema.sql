DROP TABLE IF EXISTS deck;
CREATE TABLE deck (
deck_id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT,
parent_id INTEGER,
created_timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
updated_timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
FOREIGN KEY(parent_id) references deck(deck_id));

DROP TABLE IF EXISTS card;
CREATE TABLE card (
card_id INTEGER PRIMARY KEY AUTOINCREMENT,
content TEXT,
deck_id integer references deck(deck_id),
created_timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
updated_timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
FOREIGN KEY(deck_id) references deck(deck_id));




INSERT INTO deck (name, parent_id) VALUES ('deck1', NULL);
INSERT INTO deck (name, parent_id) VALUES ('deck2', NULL);
INSERT INTO deck (name, parent_id) VALUES ('deck3', 1);

INSERT INTO card (content, deck_id) VALUES ('card 1', 1);
INSERT INTO card (content, deck_id) VALUES ('card 2', 1);
INSERT INTO card (content, deck_id) VALUES ('card 3', 1);
INSERT INTO card (content, deck_id) VALUES ('card 4', 1);


