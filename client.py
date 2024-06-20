import socket
import pickle


def send_request(request):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect(("localhost", 9999))
        client_socket.sendall(pickle.dumps(request))
        print("Request sent to server:", request)

        data = b""
        while True:
            part = client_socket.recv(4096)
            data += part
            if len(part) < 4096:
                break
        response = pickle.loads(data)

        print("Response received from server:", response)
        return response
    except Exception as e:
        print("Error during communication with server:", e)
    finally:
        client_socket.close()


def register():
    username = input("نام کاربری: ")
    email = input("ایمیل: ")
    password = input("گذرواژه: ")
    birth_date = input("تاریخ تولد (YYYY-MM-DD): ")
    phone_number = input("شماره تلفن (اختیاری): ")

    request = {
        "action": "register",
        "username": username,
        "email": email,
        "password": password,
        "birth_date": birth_date,
        "phone_number": phone_number
    }

    response = send_request(request)
    if response:
        print(response)


def login():
    username = input("نام کاربری: ")

    request = {
        "action": "login",
        "username": username
    }

    response = send_request(request)
    if response:
        print(response)
        if "خوش آمدید" in response:
            user_menu(username)


def view_cinemas():
    request = {
        "action": "view_cinemas"
    }

    response = send_request(request)
    if response:
        print(response)


def make_reservation(username):
    cinema_name = input("نام سینما: ")
    movie_title = input("نام فیلم: ")
    showtime_id = input("سانس (YYYY-MM-DD HH:MM): ")
    seat_number = input("شماره صندلی: ")

    request = {
        "action": "make_reservation",
        "username": username,
        "movie_title": movie_title,
        "showtime_id": showtime_id,
        "seat_number": seat_number
    }

    response = send_request(request)
    if response:
        print(response)


def view_reservations(username):
    request = {
        "action": "view_reservations",
        "username": username
    }

    response = send_request(request)
    if response:
        print(response)


def user_menu(username):
    while True:
        print(f"خوش آمدید {username}")
        print("1. مشاهده سینماها")
        print("2. رزرو بلیط")
        print("3. مشاهده رزروها")
        print("4. خروج")
        choice = input("لطفا یک گزینه را انتخاب کنید: ")

        if choice == "1":
            view_cinemas()
        elif choice == "2":
            make_reservation(username)
        elif choice == "3":
            view_reservations(username)
        elif choice == "4":
            break
        else:
            print("گزینه نامعتبر، لطفا دوباره تلاش کنید.")


def main_menu():
    while True:
        print("به سیستم رزرو بلیط سینما خوش آمدید")
        print("1. ثبت نام")
        print("2. ورود")
        print("3. خروج")
        choice = input("لطفا یک گزینه را انتخاب کنید: ")

        if choice == "1":
            register()
        elif choice == "2":
            login()
        elif choice == "3":
            print("خداحافظ!")
            break
        else:
            print("گزینه نامعتبر، لطفا دوباره تلاش کنید.")


if __name__ == "__main__":
    main_menu()
