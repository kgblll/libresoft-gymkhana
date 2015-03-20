NameVirtualHost test.libregeosocial.libresoft.es:80

<VirtualHost test.libregeosocial.libresoft.es>

  ServerAdmin webmaster@localhost
  DocumentRoot /var/www/libregeosocial/
  ServerName test.libregeosocial.libresoft.es

  RedirectMatch ^/(social/user/login/) https://test.libregeosocial.libresoft.es/$1

  <Location />

    SetHandler python-program
    PythonHandler django.core.handlers.modpython
    SetEnv DJANGO_SETTINGS_MODULE settings

    PythonPath "['/var/www/libregeosocial/'] + sys.path"

    PythonDebug On
  </Location>

   ErrorLog /var/log/apache2/error.log

   Alias /media /usr/share/python-support/python-django/django/contrib/admin/media


    <Location "/media/">
            SetHandler None
    </Location>

        <Location "/proxy">
            SetHandler None
        </Location>


   # Possible values include: debug, info, notice, warn, error, crit,
   # alert, emerg.
   LogLevel warn

   CustomLog /var/log/apache2/access.log combined

</VirtualHost>

