import asyncio, asyncpg

FRANKFURT_URL = "postgresql://neondb_owner:npg_mONv8dTcRuZ2@ep-rapid-star-aszbsk55.c-4.eu-central-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
LONDRA_URL = "postgresql://neondb_owner:npg_GtTYZs3elJU0@ep-bold-leaf-zatatmr6.c-2.eu-west-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

CREATE_SQL = """
CREATE TABLE IF NOT EXISTS emails (
    id SERIAL PRIMARY KEY,
    sender VARCHAR(255) NOT NULL,
    subject VARCHAR(500) NOT NULL,
    body TEXT,
    received_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_read BOOLEAN DEFAULT FALSE,
    ai_summary TEXT
);

INSERT INTO emails (sender, subject, body, ai_summary)
SELECT 'destek@sirket.com', 'Sistem Bakım Bildirimi', 'Sunucu bakımı bu gece 02:00da yapılacaktır.', 'Sunucu bakım bildirimi'
WHERE NOT EXISTS (SELECT 1 FROM emails);

INSERT INTO emails (sender, subject, body, ai_summary)
SELECT 'muhasebe@sirket.com', 'Ağustos Ayı Fatura Özeti', 'Ağustos ayı sunucu faturaları ektedir.', 'Ağustos faturaları'
WHERE (SELECT count(*) FROM emails) < 2;

INSERT INTO emails (sender, subject, body, ai_summary)
SELECT 'guvenlik@sirket.com', 'Güvenlik Uyarısı: Yeni Giriş', 'Frankfurt sunucusuna yeni bir SSH girişi tespit edildi.', 'Güvenlik uyarısı'
WHERE (SELECT count(*) FROM emails) < 3;
"""

async def setup_email_tables():
    for name, url in [("Frankfurt", FRANKFURT_URL), ("Londra", LONDRA_URL)]:
        try:
            conn = await asyncpg.connect(url)
            await conn.execute(CREATE_SQL)
            count = await conn.fetchval("SELECT count(*) FROM emails")
            print(f"SUCCESS {name}: emails table created with {count} rows")
            await conn.close()
        except Exception as e:
            print(f"FAILED {name}: {e}")

asyncio.run(setup_email_tables())
