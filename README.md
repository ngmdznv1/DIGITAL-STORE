# 🛍️ DIGITAL STORE

Веб-приложение на Django для управления магазином и продажами.  
Проект создан для учёта товаров, отображения ассортимента и удобного управления магазином.

---

## 🚀 Функционал
- Управление товарами (добавление, редактирование, удаление)  
- Отображение каталога  
- Работа с изображениями (поддержка `MEDIA`)  
- Панель администратора с улучшенным интерфейсом (**Jazzmin**)  
- Интеграция с платежной системой **Stripe** (тестовый режим)  

---

## 🛠️ Установка и запуск

```bash
git clone https://github.com/ngmdznv1/DIGITAL-STORE.git
cd DIGITAL-STORE
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
