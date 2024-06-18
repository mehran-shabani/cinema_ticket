import subprocess
import threading
import time


def run_server():
    subprocess.run(["python", "server.py"])


def run_client():
    while True:
        subprocess.run(["python", "client.py"])
        time.sleep(5)  # اجرای کلاینت هر 5 ثانیه یکبار


def main():
    # ابتدا ایجاد جداول پایگاه داده
    result = subprocess.run(["python", "database.py"], capture_output=True, text=True)
    if result.returncode == 0:
        print(f"'database.py' با موفقیت اجرا شد.")
    else:
        print(f"خطا در اجرای 'database.py':")
        print(result.stderr)
        return

    # اجرای سرور در نخ جداگانه
    server_thread = threading.Thread(target=run_server)
    server_thread.daemon = True
    server_thread.start()

    # اجرای کلاینت به صورت متناوب
    run_client()


if __name__ == "__main__":
    main()
