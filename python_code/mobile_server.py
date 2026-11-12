"""Start the existing PixelLab API for the Android app on a local network."""
import argparse
import ipaddress
from pathlib import Path
import socket
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent / 'app_backend'))
from web_app import app


def local_addresses():
    values = set()
    try:
        entries = socket.getaddrinfo(socket.gethostname(), None, socket.AF_INET)
    except socket.gaierror:
        return []
    for entry in entries:
        address = ipaddress.ip_address(entry[4][0])
        if address.is_private and not address.is_loopback and not address.is_link_local:
            values.add(str(address))
    return sorted(values)


def available_port(host, first=5000):
    for port in range(first, min(first + 16, 65536)):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as probe:
            try:
                probe.bind((host, port))
            except OSError:
                continue
            return port
    raise RuntimeError('No free mobile-server port was found. Use --port to choose another port.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--host', default='0.0.0.0')
    parser.add_argument('--port', type=int, help='Use a specific port; otherwise choose a free port starting at 5000.')
    args = parser.parse_args()
    port = args.port if args.port is not None else available_port(args.host)
    print('\nPixelLab Android server', flush=True)
    print('Connect the phone and computer to the same Wi-Fi.', flush=True)
    print('Enter your Wi-Fi adapter address in the app:', flush=True)
    for address in local_addresses():
        print(f'  http://{address}:{port}', flush=True)
    print(f'Android emulator: http://10.0.2.2:{port}', flush=True)
    print('Keep this window open while processing images.\n', flush=True)
    app.run(host=args.host, port=port, debug=False)
