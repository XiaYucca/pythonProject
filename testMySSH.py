from login_ali import Ali_ssh as ssh

s= ssh()
s.exec_command('unzip -o /var/www/html/phpProject/icon.zip -d /var/www/html/phpProject/','A')


