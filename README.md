# Preparation

Clone repo

```
git clone https://fzzybllz:<token>@github.com/fzzybllz/racketservice
```
https://github.com/settings/tokens

Fix permissions -> go to dir racketservice

```
sudo chmod 755 app/ && sudo chmod 644 app/public/index.php && udo chown www-data:www-data app/*
```

# Installation

```
composer install
```
.env anpassen
```
php artisan config:cache
```
```
php artisan key:generate
```
```
php artisan migrate
```

# Dev Server
```
php artisan serve
```
