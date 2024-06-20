import socket
import threading
import pickle
from cinema_system import CinemaSystem
from database import create_tables

def handle_client(client_socket, cinema_system):
    try:
        while True:
            data = b""
            while True:
                part = client_socket.recv(4096)
                data += part
                if len(part) < 4096:
                    break
            if not data:
                print("No data received. Closing connection.")
                break
            request = pickle.loads(data)
            print("Request received from client:", request)
            response = handle_request(request, cinema_system)
            client_socket.sendall(pickle.dumps(response))
            print("Response sent to client:", response)
    except Exception as e:
        print("Error handling client:", e)
    finally:
        client_socket.close()

def handle_request(request, cinema_system):
    action = request.get("action")
    try:
        if action == "register":
            username = request.get("username")
            email = request.get("email")
            password = request.get("password")
            birth_date = request.get("birth_date")
            phone_number = request.get("phone_number")
            user = cinema_system.register_user(username, email, password, birth_date, phone_number)
            return f"کاربر {user.username} با موفقیت ثبت نام شد"
        elif action == "login":
            username = request.get("username")
            user = cinema_system.get_user(username)
            if user:
                return f"خوش آمدید {user.username}"
            else:
                return "کاربر یافت نشد"
        elif action == "view_cinemas":
            cinemas = cinema_system.view_cinemas()
            return cinemas
        elif action == "make_reservation":
            user_id = request.get("user_id")
            movie_id = request.get("movie_id")
            showtime_id = request.get("showtime_id")
            seat_number = request.get("seat_number")
            reservation = cinema_system.make_reservation(user_id, movie_id, showtime_id, seat_number)
            return f"رزرو {reservation.reservation_id} با موفقیت انجام شد"
        elif action == "view_reservations":
            user_id = request.get("user_id")
            user = cinema_system.get_user(user_id)
            if user:
                reservations = cinema_system.view_reservations(user)
                return reservations
            else:
                return "کاربر یافت نشد"
        else:
            return "عملیات نامعتبر"
    except Exception as e:
        print("Error handling request:", e)
        return "خطا در پردازش درخواست"

def server():
    cinema_system = CinemaSystem()
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("0.0.0.0", 9999))
    server_socket.listen(5)
    print("سرور در پورت 9999 منتظر است")

    while True:
        try:
            client_socket, addr = server_socket.accept()
            print(f"اتصال از {addr} پذیرفته شد")
            client_handler = threading.Thread(target=handle_client, args=(client_socket, cinema_system))
            client_handler.start()
        except Exception as e:
            print("Error accepting connections:", e)

if __name__ == "__main__":
    create_tables()
    server()
