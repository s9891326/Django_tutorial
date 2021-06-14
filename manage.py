#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Django.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()

"""
asgi.py - 全名為Asynchronous Server Gateway Interface(非同步伺服器閘道介面)，是Django3.0新增加的檔案，用來提供非同步的功能。
settings.py - Django專案的設定檔。
urls.py - 定義Django專案中，各個應用程式(APP)的網址。
wsgi.py - 全名為Web Server Gateway Interface(網站伺服器閘道介面)，提供Django網站和伺服器間的標準介面。
manage.py - 用來管理整個Django專案，像是啟動本地端伺服器、連接資料庫及建立應用程式(APP)等。
"""
