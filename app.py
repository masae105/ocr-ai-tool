import os
import sys

from flask import (
    Flask,
    render_template,
    request,
    send_file,
    session,
    redirect,
    url_for
)

sys.path.append(
    os.path.join(
        os.path.dirname(__file__),
        "src"
    )
)

from main import process_invoice
from excel import save_to_excel
from database import get_db, save_invoice_record, init_db
from datetime import datetime, timezone, timedelta
from werkzeug.security import check_password_hash

app = Flask(__name__)
app.secret_key = "ocr-ai-tool-secret-key"

init_db()

@app.route("/login", methods=["GET", "POST"])
def login():
    message = ""

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        conn = get_db()

        user = conn.execute(
            "SELECT * FROM users WHERE username = ?",
            (username,)
        ).fetchone()

        conn.close()

        if user and check_password_hash(
            user["password"],
            password
        ):
            session["user_id"] = user["id"]
            session["username"] = user["username"]

            return redirect(url_for("index"))

        message = "ユーザー名またはパスワードが違います"

    return render_template(
        "login.html",
        message=message
    )

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/history")
def history():

    if "username" not in session:
        return redirect(url_for("login"))

    conn = get_db()

    records = conn.execute("""
        SELECT *
        FROM invoice_records
        WHERE user_id = ?
        ORDER BY id DESC
    """, (session["user_id"],)).fetchall()

    conn.close()

    jst = timezone(timedelta(hours=9))

    records = [
        dict(record) | {
            "created_at": datetime.fromisoformat(
                record["created_at"]
            ).replace(tzinfo=timezone.utc).astimezone(jst).strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        }
        for record in records
    ]

    return render_template(
        "history.html",
        records=records
    )

@app.route("/history/<int:record_id>")
def history_detail(record_id):
    if "username" not in session:
        return redirect(url_for("login"))

    conn = get_db()

    record = conn.execute("""
        SELECT *
        FROM invoice_records
        WHERE id = ?
        AND user_id = ?
    """, (
        record_id,
        session["user_id"]
    )).fetchone()

    details = conn.execute("""
        SELECT *
        FROM invoice_details
        WHERE invoice_id = ?
        ORDER BY id
    """, (record_id,)).fetchall()

    conn.close()

    if record is None:
        return "解析履歴が見つかりません", 404

    jst = timezone(timedelta(hours=9))

    record = dict(record)
    record["created_at"] = datetime.fromisoformat(
        record["created_at"]
    ).replace(tzinfo=timezone.utc).astimezone(jst).strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    return render_template(
        "history_detail.html",
        record=record,
        details=details
    )

@app.route("/history/<int:record_id>/delete", methods=["POST"])
def delete_history(record_id):

    if "username" not in session:
        return redirect(url_for("login"))

    conn = get_db()

    record = conn.execute("""
        SELECT id
        FROM invoice_records
        WHERE id = ?
        AND user_id = ?
    """, (
        record_id,
        session["user_id"]
    )).fetchone()

    if record is None:
        conn.close()
        return "解析履歴が見つかりません", 404

    conn.execute("""
        DELETE FROM invoice_details
        WHERE invoice_id = ?
    """, (record_id,))

    conn.execute("""
        DELETE FROM invoice_records
        WHERE id = ?
        AND user_id = ?
    """, (
        record_id,
        session["user_id"]
    ))

    conn.commit()
    conn.close()

    return redirect(url_for("history"))

@app.route("/", methods=["GET", "POST"])
def index():

    if "username" not in session:
        return redirect(url_for("login"))

    message = ""
    message_type = ""
    results = []

    if request.method == "POST":

        files = request.files.getlist("files")

        if files:

            for file in files:

                if not file.filename:
                    continue

                print("受け取ったファイル:", file.filename)

                temp_dir = "temp"
                os.makedirs(temp_dir, exist_ok=True)

                file_path = os.path.join(
                    temp_dir,
                    file.filename
                )

                file.save(file_path)

                print("保存先:", file_path)

                try:

                    print("OCR処理開始")

                    data = process_invoice(file_path)

                    print("OCR処理終了")

                    print("OCR解析結果:")
                    print(data)

                    save_invoice_record(
                        session["user_id"],
                        file.filename,
                        data
                    )

                    print("DB保存完了")

                    results.append(data)

                    os.remove(file_path)

                    print(
                        "一時ファイル削除:",
                        file_path
                    )

                except Exception as e:

                    print("OCR処理エラー:", e)

                    message = "解析中にエラーが発生しました"
                    message_type = "error"

                    break

            if message_type != "error":

                if results:

                    message = f"{len(results)}件の解析が完了しました"
                    message_type = "success"

                    output_dir = "output"
                    os.makedirs(output_dir, exist_ok=True)

                    output_path = os.path.join(
                        output_dir,
                        "result.xlsx"
                    )

                    save_to_excel(
                        results,
                        output_path
                    )

                    print(
                        "Excel保存:",
                        output_path
                    )

                else:

                    message = "ファイルが選択されていません"
                    message_type = "error"

        else:

            print("ファイルが選択されていません")

            message = "ファイルが選択されていません"
            message_type = "error"

    return render_template(
        "index.html",
        message=message,
        message_type=message_type,
        results=results
    )


@app.route("/download")
def download():

    if "username" not in session:
        return redirect(url_for("login"))

    output_path = os.path.join(
        "output",
        "result.xlsx"
    )

    return send_file(
        output_path,
        as_attachment=True,
        download_name="invoice_result.xlsx"
    )


if __name__ == "__main__":
    app.run(debug=True)
