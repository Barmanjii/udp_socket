# Python Import
import threading
from network_call.api import healthz

# FastAPI Imports
from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware

# Uvicorn Import
import uvicorn

# Local Imports
from network_call.logging import logger
from network_call.udp_socket import UDPSocket


# FastAPI Instance
app = FastAPI(title="File Sharing PPMT")
app.include_router(healthz.router)


def start():
    # Starts the uvicorn backend server
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)


def run_udp_socket():
    socket_create = UDPSocket()
    try:
        while True:
            received_data, return_address = socket_create.sock.recvfrom(
                1024)  # Buffer size is 1024 bytes

            if received_data.decode().upper() == "IP":  # can change this string to make it more secure
                logger.info("Client Request for Server IP")
                socket_create.sock.sendto(
                    socket_create.reply(), return_address)

    except KeyboardInterrupt as e:
        # Close the socket
        socket_create.sock.close()
        logger.error("Closing the Socket!!")


if __name__ == "__main__":
    try:
        thread = threading.Thread(target=run_udp_socket)
        thread.start()

        start()

    except KeyboardInterrupt as e:
        logger.error("Closing the Socket!!")
