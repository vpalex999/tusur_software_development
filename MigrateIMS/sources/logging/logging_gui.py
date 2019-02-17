""" Попытка отобразить логирование в виджет Tk """

import os
import logging
from tkinter import *
from tkinter.scrolledtext import ScrolledText
import queue
import _thread
import time

LEVEL_TAG = ['INFO', 'DEBUG', 'WARNING', 'ERROR', 'CRITICAL']


class ConsoleUi:
    """ Класс отображает содержимое лог файла в виджет """

    def __init__(self, frame):
        self.frame = frame
        # Create a ScrolledText wdiget
        self.scrolled_text = ScrolledText(frame, state='disabled', height=12)
        self.scrolled_text.pack(expand=YES, fill=BOTH)
        self.scrolled_text.configure(font='TkFixedFont')
        self.scrolled_text.tag_config('INFO', foreground='blue')
        self.scrolled_text.tag_config('DEBUG', foreground='gray')
        self.scrolled_text.tag_config('WARNING', foreground='orange')
        self.scrolled_text.tag_config('ERROR', foreground='red')
        self.scrolled_text.tag_config('CRITICAL', foreground='red', underline=1)
        # Обработчик очереди
        self.log_queue = queue.Queue()
        #  Запуск потоков
        self.threads()
        # запуск циклического обновления виджета и чтения донных из очереди
        self.frame.after(100, self.poll_log_queue)

    def read_log(self, log_queue):
        """ Читать лог-файл в бесконечном цикле """
        logfile = os.open('migrate_info.log', os.O_RDONLY|os.O_NONBLOCK)
        fo = os.fdopen(logfile)
        while True:
            line = fo.readline()
            if line:
                self.log_queue.put(line)
            else:
                time.sleep(0.1)

    def threads(self):
        _thread.start_new_thread(self.read_log, (self.log_queue,))

    def get_color(self, log_row):
        for level in LEVEL_TAG:
            if level in log_row:
                return level
        return 'INFO'

    def display(self, record):
        """ Функция добавления новой строки в виджет """
        self.scrolled_text.configure(state='normal')
        self.scrolled_text.insert(END, str(record), self.get_color(str(record)))
        self.scrolled_text.configure(state='disabled')
        self.scrolled_text.yview(END)

    def poll_log_queue(self):
        # Проверка каждые 100ms если есть новое сообщение, то отображаем
        while True:
            try:
                record = self.log_queue.get(block=False)
            except queue.Empty:
                break
            else:
                self.display(record)
        self.frame.after(100, self.poll_log_queue)


def main():

    class TestApp:
        def __init__(self, root):
            self.root = root
            self.root.title('Logging Handler')
            self.console = ConsoleUi(self.root)

    logging.basicConfig(level=logging.DEBUG)
    root = Tk()
    app = TestApp(root)
    app.root.mainloop()


# Для тестирования
if __name__ == '__main__':
    main()
