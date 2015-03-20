NameVirtualHost *:443

<VirtualHost *:443>

  ServerAdmin webmaster@localhost
  DocumentRoot /var/www/libregeosocial/
  ServerName test.libregeosocial.libresoft.es

  RewriteEngine on
  RewriteCond "%{REQUEST_URI}" "!^/social/user/login/$" 
  RewriteRule "^/(.*)" http://test.libregeosocial.libresoft.es/$1 [L]

  <Location /social/user/login/>
    
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

   LogLevel warn

   CustomLog /var/log/apache2/access.log combined

   SSLEngine on
   SSLCertificateFile /etc/apache2/server.crt
   SSLCertificateKeyFile /etc/apache2/server.key

   SSLProtocol all
 #  SSLCipherSuite HIGH:MEDIUM

</VirtualHost>
