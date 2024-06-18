import socket
import threading
import pickle
from user import User
from cinema import Cinema
from movie import Movie
from reservation import Reservation
from review import Review
from database import create_tables

class CinemaSystem:
    def __init__(self):
        self.users = []
        self.cinemas = []
        self.reservations = []

    def register_user(self, username, email, password, birth_date, phone_number=None):
        new_user = User(username, email, password, birth_date, phone_number)
        self.users.append(new_user)
        return new_user

    def add_cinema(self, cinema_name):
        new_cinema = Cinema(cinema_name)
        self.cinemas.append(new_cinema)
        return new_cinema

    def make_reservation(self, user_id, movie_id, showtime_id, seat_number):
        new_reservation = Reservation(user_id, movie_id, showtime_id, seat_number)
        self.reservations.append(new_reservation)
        return new_reservation

    def get_user(self, username):
        return User.get_user(username)

    def get_cinema(self, cinema_name):
        for cinema in self.cinemas:
            if cinema.name == cinema_name:
                return cinema
        return None

    def display_menu(self):
        print("به سیستم رزرو بلیط سینما خوش آمدید")
        print("1. ثبت نام")
        print("2. ورود")
        print("3. خروج")
        choice = input("لطفا یک گزینه را انتخاب کنید: ")
        return choice

    def user_menu(self, user):
        print(f"خوش آمدید {user.username}")
        print("1. مشاهده سینماها")
        print("2. رزرو بلیط")
        print("3. مشاهده رزروها")
        print("4. خروج")
        choice = input("لطفا یک گزینه را انتخاب کنید: ")
        return choice

    def admin_menu(self):
        print("منوی مدیر")
        print("1. افزودن سینما")
        print("2. مشاهده سینماها")
        print("3. خروج")
        choice = input("لطفا یک گزینه را انتخاب کنید: ")
        return choice

    def start(self):
        while True:
            choice = self.display_menu()
            if choice == "1":
                username = input("نام کاربری: ")
                email = input("ایمیل: ")
                password = input("گذرواژه: ")
                birth_date = input("تاریخ تولد (YYYY-MM-DD): ")
                phone_number = input("شماره تلفن (اختیاری): ")
                user = self.register_user(username, email, password, birth_date, phone_number)
                print(f"کاربر {user.username} با موفقیت ثبت نام شد")
            elif choice == "2":
                username = input("نام کاربری: ")
                user = self.get_user(username)
                if user:
                    print(f"خوش آمدید {user.username}")
                    while True:
                        user_choice = self.user_menu(user)
                        if user_choice == "1":
                            self.view_cinemas()
                        elif user_choice == "2":
                            cinema_name = input("نام سینما: ")
                            cinema = self.get_cinema(cinema_name)
                            if cinema:
                                movie_title = input("نام فیلم: ")
                                showtime_id = input("سانس (YYYY-MM-DD HH:MM): ")
                                seat_number = input("شماره صندلی: ")
                                reservation = self.make_reservation(user.user_id, cinema.movie_id, showtime_id, seat_number)
                                print(f"رزرو {reservation.reservation_id} با موفقیت انجام شد")
                        elif user_choice == "3":
                            self.view_reservations(user)
                        elif user_choice == "4":
                            break
                        else:
                            print("گزینه نامعتبر، لطفا دوباره تلاش کنید.")
                else:
                    print("کاربر یافت نشد.")
            elif choice == "3":
                print("خداحافظ!")
                break
            else:
                print("گزینه نامعتبر، لطفا دوباره تلاش کنید.")

    def view_cinemas(self):
        if not self.cinemas:
            print("هیچ سینمایی موجود نیست.")
        for cinema in self.cinemas:
            print(f"سینما: {cinema.name}")
            for movie in cinema.movies:
                print(f" - فیلم: {movie.title}, امتیاز: {movie.rating}, سانس‌ها: {movie.showtimes}")

    def view_reservations(self, user):
        user_reservations = [r for r in self.reservations if r.user_id == user.user_id]
        if not user_reservations:
            print("هیچ رزروی یافت نشد.")
        for reservation in user_reservations:
            print(f"رزرو: {reservation.reservation_id}, شناسه فیلم: {reservation.movie_id}, سانس: {reservation.showtime_id}, صندلی: {reservation.seat_number}, وضعیت: {reservation.status}")

# منطق سرور برای مدیریت چند کاربر
def handle_client(client_socket, cinema_system):
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                break
            request = pickle.loads(data)
            response = handle_request(request, cinema_system)
            client_socket.send(pickle.dumps(response))
        except:
            break
    client_socket.close()

def handle_request(request, cinema_system):
    action = request.get("action")
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

def server():
    cinema_system = CinemaSystem()
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", 9999))
    server_socket.listen(5)
    print("سرور در پورت 9999 منتظر است")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"اتصال از {addr} پذیرفته شد")
        client_handler = threading.Thread(target=handle_client, args=(client_socket, cinema_system))
        client_handler.start()

if __name__ == "__main__":
    create_tables()
    cinema_system = CinemaSystem()
    server_thread = threading.Thread(target=server)
    server_thread.start()
    cinema_system.start()
