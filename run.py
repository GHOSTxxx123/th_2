from app import app
import socket

ip_addres = socket.gethostbyname(socket.gethostname())

if __name__ == '__main__':
    app.run(host=f'{ip_addres}', port=8003, debug=True)
