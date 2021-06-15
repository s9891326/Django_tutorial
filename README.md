# hello Django

## outline
1. [第一階段](#第一階段)
    1. [初始化專案](#初始化專案)
    2. [專案目錄結構說明](#專案目錄結構說明)
    3. [執行簡易版的server](#執行簡易版的server)
    4. [創建App](#創建app)
1. [第二階段](#第二階段)
    1. [資料庫配置](#資料庫配置)
    2. [檢查App設置](#檢查app設置)
    3. [使用模型](#使用模型)
    4. [初試api](#初試api)
    5. [創建管理者帳號](#創建管理者帳號)
    6. [使用管理頁面](#使用管理頁面)
1. [第三階段](#第三階段)
    1. [快捷函數](#快捷函數)
    2. [改善模板硬編碼url](#改善模板硬編碼url)
    3. [為url名稱添加命名空間](#為url名稱添加命名空間)
1. [第四階段](#第四階段)
    1. [使用通用模板](#使用通用模板)
1. [第五階段](#第五階段)
    1. [自動化測試是什麼?](#自動化測試是什麼?)
    2. [為甚麼需要寫測試](#為甚麼需要寫測試)
    
### 第一階段
#### 初始化專案
- cd到專案資料夾下
```
django-admin startproject mysite
```
#### 專案目錄結構說明
- 最外層的 mysite/ 根目錄只是你項目的容器
- manage.py: 讓你用各種方式管理Django
- mysite/__init__.py：空文件。告訴Python這個目錄應該被視為一個Python package
- mysite/settings.py：Django配置文件
- mysite/urls.py：Django裡的URL配置設定
- [mysite/asgi.py](https://docs.djangoproject.com/zh-hans/3.1/howto/deployment/asgi/)：運行在ASGI(非同步)兼容的Web伺服器上的街口
- [mysite/wsgi.py](https://docs.djangoproject.com/zh-hans/3.1/howto/deployment/wsgi/)：運行在WSGI兼容的Web伺服器上的街口
#### 執行簡易版的server
```
python manage.py runserver
```
#### 創建app
```
python manage.py startapp polls
```
- 創建完即可開始編輯app

### 第二階段
#### 資料庫配置
- mysite/setting.py中，預設使用SQLite當作資料庫，如果想更改也更改setting.py內的設定
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
```
#### 檢查app設置
- 啟用所有Django裡的App能用的django套件
- django.contrib.admin -- 管理員站點
- django.contrib.auth -- 認證授權系統
- django.contrib.contenttypes -- 內容類型框架
- django.contrib.sessions -- 會話框架
- django.contrib.messages -- 消息框架
- django.contrib.staticfiles -- 管理靜態文件的框架
```
python manage.py migrate
```
#### 使用模型
- 編輯models.py，改變模型
```python
from django.db import models


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
```
- 使用模型的方式進行交互的Python資料庫API
```
# mysite/setting.py
INSTALLED_APPS = [
    'polls.apps.PollsConfig',  <-- 增加這行，因為PollsConfig這class寫在polls/app.py中
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
```
- 現在Django項目包含polls應用，運行下面語句，為模型的改變生成遷移文件(polls/migrations/0001_initial.py)
```
python manage.py makemigrations polls
```
- 應用資料庫遷移
```
python manage.py migrate
```
#### 初試api
- 進入shell運行python程式碼，可以測試model內的資料庫測試
```
python manage.py shell  
```
#### 創建管理者帳號
- 創建一個能登陸管理頁面的用戶，並創建使用者帳號密碼等等資訊
```
python manage.py createsuperuser
```
- 在啟動服務器，並進入/admin頁面並登入
```
python manage.py runserver
```
#### 使用管理頁面
- 把上面創建的資料庫model加入到管理頁面(polls/admin.py)
```
from django.contrib import admin

from .models import Question

admin.site.register(Question)
```

### 第三階段
#### 快捷函數
1. render(): 載入模板，填充上下文，再返回由他生成的HttpResponse對象
2. get_object_or_404(): 用來簡化取對象時，對象不存在拋出Http404這一個普遍的流程
3. 
#### 改善模板硬編碼url
- 原本
```
<li><a href="/polls/{{ question.id }}/">{{ question.question_text }}</a></li>
```
- 改善後，其中`detail`對應到的是url.py內的path('<int:question_id>/', views.detail, name='detail' <-- 這個)
- 這樣的好處: 我們可以在url.py內隨意更改url，並不會影響到html的url連結
```
<li><a href="{% url 'detail' question.id %}">{{ question.question_text }}</a></li>
```
#### 為url名稱添加命名空間
- 在一個Django專案中，會有很多個應用，Django如何分辨重名的url?
- Ans: 設置命名空間app_name
- 在polls/url.py，增加app_name
```
app_name = 'polls'
```

### 第四階段
#### 使用通用模板
- 有些views只是單純的顯示某個html而已，不需要寫得太複雜，會存在冗余問題
- 通用模板就是一個用來精簡程式碼的方式
    1. 轉換URL conf
    2. 刪除一些舊的，不需要的views
    3. 基於Django的通用模板引入新的模板
- 常見的模板是
    1. [ListView](https://docs.djangoproject.com/zh-hans/3.1/ref/class-based-views/generic-display/#django.views.generic.list.ListView)
        - context_object_name: 告訴Django你想使用的變量名，對應到html上面
        - 需要override `get_queryset()` method，會回傳模型物件(models object)
    2. [DetailView](https://docs.djangoproject.com/zh-hans/3.1/ref/class-based-views/generic-display/#django.views.generic.detail.DetailView)
        - 會從URL中抓取`PK`的主健值，所以更改URL conf => pk

### 第五階段
#### 自動化測試是什麼?
- 用來自動檢測你的code是否能正常運行，當你建立好一系列測試，每次修改code後，就可以自動檢測出修改後的code是否像你曾經預期的那樣運行，就不需要花費大量時間來手動測試
#### 為甚麼需要寫測試
- 測試將節省你的時間
    - 在複雜的演算法中，能夠判斷出此code是否正常，就算是令人滿意的了，即可大大節省時間
- 測試不僅能發現錯誤，還能預防錯誤
    - 如果沒有測試，整個演算法的意圖會變得更加不清晰。就算你自己沒有意識到哪裡寫錯了，測試也會發現
- 測試使你的code更有吸引力
    - 沒有測試的code不值得信任，也能讓其他開發人員透過測試來了解前人的程式碼
- 測試有利於團隊合作
    - 複雜的程式可能由團隊來維護，測試的存在保證了協作者不會不小心破壞了你的程式
#### 開始進行測試
- 撰寫在tests.py內
```python
import datetime

from django.test import TestCase
from django.utils import timezone

from .models import Question


class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)
```
- 運行測試
```
python manage.py test polls
```
