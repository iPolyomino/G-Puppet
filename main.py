#!/usr/bin/env python3

import pychromecast
import socket
import http.server
import socketserver
import threading

from gtts import gTTS

def local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    address = s.getsockname()[0]
    s.close()
    return address

def create_server(ip, port):
    Handler = http.server.SimpleHTTPRequestHandler
    socketserver.TCPServer.allow_reuse_address = True
    server =  socketserver.TCPServer((ip,port), Handler)
    with server:
        server_thread = threading.Thread(target=server.serve_forever)
        server_thread.daemon = True
        server_thread.start()
        speech(ip,port)
        server.shutdown()

def create_audio(text):
    tts = gTTS(text, lang="ja")
    tts.save("speech.mp3")

def speech(ip,port):
    create_audio("今日もいい天気")

    audio_url= f"http://{ip}:{port}/speech.mp3";
    chromecasts, _ = pychromecast.get_chromecasts()

    if len(chromecasts) == 0:
        print("cannot find google home")
        exit()
    
    cast = chromecasts[0]
    
    cast.wait()
    mc = cast.media_controller
    mc = cast.media_controller
    mc.play_media(audio_url, "audio/mp3")


def main():
    ip = local_ip()
    port = 8080
    create_server(ip, port)


if __name__ == "__main__":
    main()
