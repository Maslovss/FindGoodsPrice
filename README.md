# FindGoodsPrice
Поиск лучшей цены на товары в ближайших продуктовых магазинах.

Сборка состоит из 4-х Docker контейнеров, объединенных в deployment:
* Python scraper изпользующий Beautifulsoup4;
* Postgres базы данных;
* Rest сервера на Node.js;
* Fron-end веб приложение на React + Nginx;

Для инициализации AWS EC2 инстанса используется Terraform скрипт.

Текущая версия в стадии Alpha, пока данные загружаются только из одного магазина 
и работает только отображение списка цен и поиск товара по названию.

