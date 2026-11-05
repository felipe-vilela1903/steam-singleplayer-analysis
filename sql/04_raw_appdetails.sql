CREATE TABLE raw_appdetails (
    appid        INTEGER PRIMARY KEY,
    collected_at TIMESTAMPTZ NOT NULL,
    payload      JSONB NOT NULL
);