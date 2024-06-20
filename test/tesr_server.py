import unittest
from unittest.mock import MagicMock, patch
import socket
import pickle
from server import handle_request, handle_client
from cinema_system import CinemaSystem


class TestServer(unittest.TestCase):
    @patch('server.socket')
    @patch('server.CinemaSystem')
    def test_handle_client(self, MockCinemaSystem, MockSocket):
        cinema_system = MockCinemaSystem.return_value
        client_socket = MagicMock()
        client_socket.recv = MagicMock(side_effect=[pickle.dumps(
            {"action": "register", "username": "test", "email": "test@test.com", "password": "1234",
             "birth_date": "1990-01-01", "phone_number": "1234567890"}), b''])
        handle_client(client_socket, cinema_system)

        cinema_system.register_user.assert_called_with("test", "test@test.com", "1234", "1990-01-01", "1234567890")
        client_socket.sendall.assert_called()

    def test_handle_request_register(self):
        cinema_system = CinemaSystem()
        request = {
            "action": "register",
            "username": "test",
            "email": "test@test.com",
            "password": "1234",
            "birth_date": "1990-01-01",
            "phone_number": "1234567890"
        }
        response = handle_request(request, cinema_system)
        self.assertIn("کاربر", response)

    def test_handle_request_login(self):
        cinema_system = CinemaSystem()
        cinema_system.register_user("test", "test@test.com", "1234", "1990-01-01", "1234567890")
        request = {
            "action": "login",
            "username": "test"
        }
        response = handle_request(request, cinema_system)
        self.assertIn("خوش آمدید", response)

    def test_handle_request_view_cinemas(self):
        cinema_system = CinemaSystem()
        request = {
            "action": "view_cinemas"
        }
        response = handle_request(request, cinema_system)
        self.assertIsInstance(response, list)

    def test_handle_request_make_reservation(self):
        cinema_system = CinemaSystem()
        user = cinema_system.register_user("test", "test@test.com", "1234", "1990-01-01", "1234567890")
        cinema = cinema_system.add_cinema("Cinema One")
        movie = cinema_system.add_movie("Inception", cinema.cinema_id)
        showtime = cinema_system.add_showtime(movie.movie_id, "2024-12-31 20:00:00")

        request = {
            "action": "make_reservation",
            "user_id": user.user_id,
            "movie_id": movie.movie_id,
            "showtime_id": showtime.showtime_id,
            "seat_number": "A1"
        }
        response = handle_request(request, cinema_system)
        self.assertIn("رزرو", response)

    def test_handle_request_view_reservations(self):
        cinema_system = CinemaSystem()
        user = cinema_system.register_user("test", "test@test.com", "1234", "1990-01-01", "1234567890")
        request = {
            "action": "view_reservations",
            "user_id": user.user_id
        }
        response = handle_request(request, cinema_system)
        self.assertIsInstance(response, list)


if __name__ == '__main__':
    unittest.main()
