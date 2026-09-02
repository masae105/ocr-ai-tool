import os
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash


DATABASE = "database.db"

ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "1234")


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS invoice_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            filename TEXT,
            company_name TEXT,
            invoice_date TEXT,
            total_amount INTEGER,
            amount_check TEXT,
            document_type TEXT,
            ai_status TEXT,
            ai_severity TEXT,
            ai_issues TEXT,
            ai_recommendation TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS invoice_details (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            invoice_id INTEGER NOT NULL,
            product_name TEXT,
            amount INTEGER,
            FOREIGN KEY (invoice_id) REFERENCES invoice_records(id)
        )
    """)

    try:
        conn.execute(
            "ALTER TABLE invoice_records ADD COLUMN ai_issues TEXT"
        )
    except sqlite3.OperationalError:
        pass

    try:
        conn.execute(
            "ALTER TABLE invoice_records ADD COLUMN ai_recommendation TEXT"
        )
    except sqlite3.OperationalError:
        pass

    # 管理者ユーザーが存在しない場合は作成
    user = conn.execute(
        "SELECT id FROM users WHERE username = ?",
        (ADMIN_USERNAME,)
    ).fetchone()

    if user is None:
        password_hash = generate_password_hash(ADMIN_PASSWORD)

        conn.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (ADMIN_USERNAME, password_hash)
        )

    conn.commit()
    conn.close()


def create_user(username, password):
    conn = get_db()

    password_hash = generate_password_hash(password)

    conn.execute(
        "INSERT INTO users (username, password) VALUES (?, ?)",
        (username, password_hash)
    )

    conn.commit()
    conn.close()


def update_password(username, password):
    conn = get_db()

    password_hash = generate_password_hash(password)

    conn.execute(
        """
        UPDATE users
        SET password = ?
        WHERE username = ?
        """,
        (password_hash, username)
    )

    conn.commit()
    conn.close()


def save_invoice_record(
    user_id,
    filename,
    data
):
    conn = get_db()

    ai_result = data.get("ai_result", {})

    issues = ai_result.get("issues", [])

    if isinstance(issues, list):
        issues = "\n".join(issues)

    cursor = conn.execute("""
        INSERT INTO invoice_records (
            user_id,
            filename,
            company_name,
            invoice_date,
            total_amount,
            amount_check,
            document_type,
            ai_status,
            ai_severity,
            ai_issues,
            ai_recommendation
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        user_id,
        filename,
        data.get("会社名", ""),
        data.get("請求日", ""),
        data.get("合計金額", 0),
        data.get("金額チェック", ""),
        data.get("書類タイプ", ""),
        ai_result.get("status", ""),
        ai_result.get("severity", ""),
        issues,
        ai_result.get("recommendation", "")
    ))

    invoice_id = cursor.lastrowid

    for item in data.get("明細", []):

        conn.execute("""
            INSERT INTO invoice_details (
                invoice_id,
                product_name,
                amount
            )
            VALUES (?, ?, ?)
        """, (
            invoice_id,
            item.get("商品名", ""),
            item.get("金額", 0)
        ))

    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()

    conn = get_db()

    records = conn.execute("""
        SELECT
            id,
            user_id,
            filename,
            company_name,
            invoice_date,
            total_amount,
            amount_check,
            document_type,
            ai_status,
            ai_severity,
            ai_issues,
            ai_recommendation,
            created_at
        FROM invoice_records
        ORDER BY id DESC
    """).fetchall()

    print("===== 解析履歴 =====")

    for record in records:
        print(
            record["id"],
            record["user_id"],
            record["filename"],
            record["company_name"],
            record["invoice_date"],
            record["total_amount"],
            record["amount_check"],
            record["document_type"],
            record["ai_status"],
            record["ai_severity"],
            record["ai_issues"],
            record["ai_recommendation"],
            record["created_at"]
        )

    conn.close()