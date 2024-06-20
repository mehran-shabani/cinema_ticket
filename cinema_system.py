import os
import threading
import socket
import pickle
from user import User
from cinema import Cinema
from movie import Movie
from reservation import Reservation
from database import create_tables


def clear_screen():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


def pause_and_clear():
    input("\nبرای ادامه کلیدی فشار دهید...")
    clear_screen()


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

    def add_movie(self, cinema_name, movie_title):
        cinema = self.get_cinema(cinema_name)
        if cinema:
            new_movie = Movie(title=movie_title, cinema_id=cinema.cinema_id)
            cinema.add_movie(new_movie)
            return new_movie
        return None

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
        clear_screen()
        print("به سیستم رزرو بلیط سینما خوش آمدید")
        print("1. ثبت نام")
        print("2. ورود")
        print("3. خروج")
        choice = input("لطفا یک گزینه را انتخاب کنید: ")
        return choice

    def user_menu(self, user):
        clear_screen()
        print(f"خوش آمدید {user.username}")
        print("1. مشاهده سینماها")
        print("2. رزرو بلیط")
        print("3. مشاهده رزروها")
        print("4. خروج")
        choice = input("لطفا یک گزینه را انتخاب کنید: ")
        return choice

    def admin_menu(self):
        clear_screen()
        print("منوی مدیر")
        print("1. افزودن سینما")
        print("2. افزودن فیلم به سینما")
        print("3. مشاهده سینماها")
        print("4. خروج")
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
                pause_and_clear()
            elif choice == "2":
                username = input("نام کاربری: ")
                user = self.get_user(username)
                if user:
                    print(f"خوش آمدید {user.username}")
                    pause_and_clear()
                    while True:
                        if username == 'admin':  # assuming 'admin' is the username for admin
                            user_choice = self.admin_menu()
                            if user_choice == "1":
                                cinema_name = input("نام سینما: ")
                                self.add_cinema(cinema_name)
                                print(f"سینما {cinema_name} با موفقیت اضافه شد")
                                pause_and_clear()
                            elif user_choice == "2":
                                cinema_name = input("نام سینما: ")
                                movie_title = input("نام فیلم: ")
                                new_movie = self.add_movie(cinema_name, movie_title)
                                if new_movie:
                                    print(f"فیلم {movie_title} با موفقیت به سینما {cinema_name} اضافه شد")
                                else:
                                    print("سینما یافت نشد.")
                                pause_and_clear()
                            elif user_choice == "3":
                                self.view_cinemas()
                            elif user_choice == "4":
                                break
                            else:
                                print("گزینه نامعتبر، لطفا دوباره تلاش کنید.")
                                pause_and_clear()
                        else:
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
                                    reservation = self.make_reservation(user.user_id, cinema.movie_id, showtime_id,
                                                                        seat_number)
                                    print(f"رزرو {reservation.reservation_id} با موفقیت انجام شد")
                                    pause_and_clear()
                            elif user_choice == "3":
                                self.view_reservations(user)
                            elif user_choice == "4":
                                break
                            else:
                                print("گزینه نامعتبر، لطفا دوباره تلاش کنید.")
                                pause_and_clear()
                else:
                    print("کاربر یافت نشد.")
                    pause_and_clear()
            elif choice == "3":
                print("خداحافظ!")
                break
            else:
                print("گزینه نامعتبر، لطفا دوباره تلاش کنید.")
                pause_and_clear()

    def view_cinemas(self):
        clear_screen()
        if not self.cinemas:
            print("هیچ سینمایی موجود نیست.")
        for cinema in self.cinemas:
            print(f"سینما: {cinema.name}")
            for movie in cinema.movies:
                print(f" - فیلم: {movie.title}, امتیاز: {movie.rating}, سانس‌ها: {movie.showtimes}")
        input("برای بازگشت به منو کلیدی فشار دهید...")
        clear_screen()

    def view_reservations(self, user):
        clear_screen()
        user_reservations = [r for r in self.reservations if r.user_id == user.user_id]
        if not user_reservations:
            print("هیچ رزروی یافت نشد.")
        for reservation in user_reservations:
            print(
                f"رزرو: {reservation.reservation_id}, شناسه فیلم: {reservation.movie_id}, سانس: {reservation.showtime_id}, صندلی: {reservation.seat_number}, وضعیت: {reservation.status}")
        input("برای بازگشت به منو کلیدی فشار دهید...")
        clear_screen()


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
    try:
        if action == "register":
            username = request.get("username")
            email = request.get("email")
            password = request.get("password")
            birth_date = request.get("birth_date")
            phone_number = request.get("phone_number")
            user = User.create_user(username, email, password, birth_date, phone_number)
            return f"کاربر {user.username} با موفقیت ثبت نام شد"
        elif action == "login":
            username = request.get("username")
            user = User.get_user_by_username(username)
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
            user = User.get_user_by_id(user_id)
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
