import sqlite3

conn = sqlite3.connect('toi.db', timeout=10)  # Timeout sekundlarda


def create_users_table(conn):
    with conn:
        conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            telegram_id INTEGER UNIQUE NOT NULL,
            username TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        ''')
    print("Users table created.")

def create_bot_admin_table(conn):
    with conn:
        conn.execute('''
        CREATE TABLE IF NOT EXISTS bot_admin (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            telegram_id INTEGER UNIQUE NOT NULL,
            username TEXT
        );
        ''')
    print("Bot_admin table created.")

def create_clients_table(conn):
    with conn:
        conn.execute('''
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            loyiha TEXT NOT NULL,
            full_name TEXT NOT NULL,
            username TEXT,
            phone_number TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        ''')
    print("Clients table created.")




def main():
    # Ma'lumotlar bazasiga ulanish
    conn = sqlite3.connect('toi.db')
    
    # Jadvallarni yaratish
    create_users_table(conn)
    create_bot_admin_table(conn)
    create_clients_table(conn)
    
    # Ulanishni yopish
    conn.close()

if __name__ == '__main__':
    main()
