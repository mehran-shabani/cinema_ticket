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
    # اجرای سرور در نخ جداگانه
    server_thread = threading.Thread(target=run_server)
    server_thread.daemon = True
    server_thread.start()

    # کمی صبر کردن تا سرور به درستی شروع به کار کند
    time.sleep(2)

    # اجرای کلاینت به صورت متناوب
    run_client()


if __name__ == "__main__":
    main()
