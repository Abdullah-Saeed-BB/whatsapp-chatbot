DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS offers;

-- Customers table
CREATE TABLE IF NOT EXISTS customers (
    id TEXT PRIMARY KEY,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    name TEXT NOT NULL,
    phone_num TEXT UNIQUE,
    plan TEXT CHECK(plan IN ('free', 'learning', 'pro')) NOT NULL DEFAULT 'Free',
    pay_style TEXT CHECK(pay_style IN ('None', 'monthly', 'yearly')) NOT NULL DEFAULT 'None',
    valid_until DATETIME,
    is_from_whatsapp BOOLEAN 
);

-- Offers table
CREATE TABLE IF NOT EXISTS offers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    title TEXT NOT NULL,
    description TEXT,
    valid_from DATE NOT NULL,
    valid_until DATE NOT NULL
);
