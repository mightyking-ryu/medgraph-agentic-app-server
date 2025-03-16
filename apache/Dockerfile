FROM php:7.4-apache

RUN docker-php-ext-install mysqli

RUN a2enmod rewrite

COPY ./www /var/www/html

COPY ./000-default.conf /etc/apache2/sites-available/000-default.conf

EXPOSE 80