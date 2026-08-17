import os
import sqlite3

def run_migration():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, "fastapi_app.db")
    
    if not os.path.exists(db_path):
        print("Veritabanı bulunamadı. Migration atlanıyor.")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 1. Add metric_table column to projects
    try:
        cursor.execute("ALTER TABLE projects ADD COLUMN metric_table VARCHAR(100)")
        print("metric_table kolonu projects tablosuna eklendi.")
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e).lower():
            print("metric_table kolonu zaten mevcut.")
        else:
            print(f"Kolon ekleme hatası: {e}")
            
    # 2. Fix Node 10 role
    try:
        cursor.execute("UPDATE nodes SET role = 'Standby' WHERE id = 10 AND role = 'Primary'")
        if cursor.rowcount > 0:
            print("Node 10 rolü Standby olarak düzeltildi.")
        else:
            print("Node 10 için güncelleme gerekmedi (Zaten Standby veya bulunamadı).")
    except Exception as e:
        print(f"Node 10 güncelleme hatası: {e}")
        
    conn.commit()
    conn.close()

if __name__ == "__main__":
    run_migration()
