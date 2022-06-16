import os
from modules.config import Config


Config().version

if Config().debug:
  os.system(f'python -m nuitka --standalone --windows-icon-from-ico=assets/icons/favicon.ico --enable-plugin=pyside6 --include-data-dir=assets=assets --follow-imports --onefile --windows-file-version={Config().version} --windows-product-version={Config().version} --windows-company-name="Lost Ark Market Online" --windows-product-name="Lost Ark Market Online Launcher App" --windows-file-description="Lost Ark Market Online Launcher App" -o lamo-launcher-debug.exe index.py')
else:
  os.system(f'python -m nuitka --standalone --windows-icon-from-ico=assets/icons/favicon.ico --enable-plugin=pyside6 --include-data-dir=assets=assets --follow-imports --onefile --windows-disable-console --windows-file-version={Config().version} --windows-product-version={Config().version} --windows-company-name="Lost Ark Market Online" --windows-product-name="Lost Ark Market Online Launcher App" --windows-file-description="Lost Ark Market Online Launcher App" -o lamo-launcher.exe index.py')