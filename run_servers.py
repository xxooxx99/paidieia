from multiprocessing import Process
import os

def run_app():
    os.system("python app.py")

def run_epson_main():
    os.system("python epson_main.py")

if __name__ == "__main__":
    p1 = Process(target=run_app)
    p2 = Process(target=run_epson_main)

    p1.start()
    p2.start()

    p1.join()
    p2.join()
