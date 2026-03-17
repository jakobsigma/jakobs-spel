-- Supabase SQL-schema för Jakobs Spel
-- Kör detta i Supabase SQL Editor (https://supabase.com/dashboard)

CREATE TABLE IF NOT EXISTS accounts (
  username TEXT PRIMARY KEY,
  password_hash TEXT NOT NULL,
  is_admin BOOLEAN DEFAULT FALSE,
  banned BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS user_data (
  username TEXT PRIMARY KEY REFERENCES accounts(username) ON DELETE CASCADE,
  coins INTEGER DEFAULT 0,
  xp INTEGER DEFAULT 0,
  level INTEGER DEFAULT 1,
  favorites JSONB DEFAULT '[]',
  games_played INTEGER DEFAULT 0,
  settings JSONB DEFAULT '{}'
);

-- Tillåt offentlig läsning/skrivning (för ett enkelt spelbibliotek)
ALTER TABLE accounts ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_data ENABLE ROW LEVEL SECURITY;

CREATE POLICY "public_accounts" ON accounts FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "public_user_data" ON user_data FOR ALL USING (true) WITH CHECK (true);
