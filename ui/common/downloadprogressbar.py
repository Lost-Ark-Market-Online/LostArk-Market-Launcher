

import traceback
from threading import Thread
from urllib.request import urlopen
from PySide6.QtWidgets import QProgressBar
from PySide6.QtCore import Signal
from modules.invoker import invoke_in_main_thread


class DownloadProgressBar(QProgressBar):
    finished = Signal()
    error = Signal()

    def __init__(self, *args, **kwargs):
        QProgressBar.__init__(self, *args, **kwargs)

    def download_file(self, url, file_name):
        DownloadThread(url, file_name, self).start()


class DownloadThread(Thread):
    def __init__(self, url, file_name, progress_bar):
        Thread.__init__(self)
        self.url = url
        self.file_name = file_name
        self.progress_bar = progress_bar

    def run(self):
        try:
            u = urlopen(self.url)
            meta = u.info()
            file_size = int(meta.get('Content-Length'))
            f = open(self.file_name, 'wb')
            downloaded_bytes = 0
            block_size = 1024*8
            while True:
                buffer = u.read(block_size)
                if not buffer:
                    break
                f.write(buffer)
                downloaded_bytes += block_size
                value = float(downloaded_bytes) / file_size * 100
                invoke_in_main_thread(self.progress_bar.setValue, value)
            f.close()
            invoke_in_main_thread(self.progress_bar.finished.emit)
        except:
            traceback.print_exc()
            invoke_in_main_thread(self.progress_bar.error.emit)
