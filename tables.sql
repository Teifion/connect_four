BEGIN;

CREATE TABLE connect_four_profiles (
    "user" INTEGER NOT NULL,
    preferred_colour BOOLEAN,
    PRIMARY KEY ("user"),
    FOREIGN KEY("user") REFERENCES users (id)
);
CREATE INDEX ix_connect_four_profiles_user ON connect_four_profiles ("user");

CREATE TABLE connect_four_games (
    id SERIAL NOT NULL,
    turn INTEGER,
    started TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    player1 INTEGER NOT NULL,
    player2 INTEGER NOT NULL,
    winner INTEGER,
    current_state VARCHAR NOT NULL,
    rematch INTEGER,
    source INTEGER,
    PRIMARY KEY (id),
    FOREIGN KEY(player1) REFERENCES users (id),
    FOREIGN KEY(player2) REFERENCES users (id),
    FOREIGN KEY(winner) REFERENCES users (id),
    FOREIGN KEY(rematch) REFERENCES connect_four_games (id),
    FOREIGN KEY(source) REFERENCES connect_four_games (id)
);
CREATE INDEX ix_connect_four_games_player2 ON connect_four_games (player2);
CREATE INDEX ix_connect_four_games_player1 ON connect_four_games (player1);

CREATE TABLE connect_four_moves (
    id SERIAL NOT NULL,
    game INTEGER NOT NULL,
    player INTEGER NOT NULL,
    move INTEGER NOT NULL,
    timestamp TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY(game) REFERENCES connect_four_games (id),
    FOREIGN KEY(player) REFERENCES users (id)
);
CREATE INDEX ix_connect_four_moves_player ON connect_four_moves (player);

COMMIT;