DROP TABLE IF EXISTS deck;
CREATE TABLE deck (
deck_id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT,
parent_id INTEGER,
created_timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
updated_timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
order_value INTEGER NOT NULL,
CONSTRAINT name_constraint UNIQUE (name),
FOREIGN KEY(parent_id) references deck(deck_id))
;

DROP TABLE IF EXISTS card;
CREATE TABLE card (
card_id INTEGER PRIMARY KEY AUTOINCREMENT,
content TEXT,
deck_id integer references deck(deck_id),
created_timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
updated_timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
order_value INTEGER NOT NULL,
CONSTRAINT content_constraint UNIQUE (content),
FOREIGN KEY(deck_id) references deck(deck_id))
;




INSERT INTO deck (name, parent_id, order_value) VALUES ('deck1', NULL, 1);
INSERT INTO deck (name, parent_id, order_value) VALUES ('deck2', NULL, 1);
INSERT INTO deck (name, parent_id, order_value) VALUES ('deck3', 1, 1);

INSERT INTO card (content, deck_id, order_value) VALUES ('card 1', 1, 2);
INSERT INTO card (content, deck_id, order_value) VALUES ('card 2', 1, 3);
INSERT INTO card (content, deck_id, order_value) VALUES ('card 3', 1, 4);
INSERT INTO card (content, deck_id, order_value) VALUES ('card 4', 1, 5);


