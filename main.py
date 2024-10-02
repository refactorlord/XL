from qt.main import *

def main():
    app = QApplication(sys.argv) 
    window = MyApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()