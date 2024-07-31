# Docker 支持

## Use docker-compose to quickly build a development environment (mysql / memcached)

We offer `dev-environment-setup.yml to quickly build the development environment.

`` `shell script
Docker-compose -f./docker-support/dev-environment-setup.yml up
`` `

After running this command, you can quickly build the following environment:

- MySQL 5.7 - Port `3306`, User Name` root`, Password` medblog
`, Automatic UTF8MB4 encoded creation` medblog` database
- Memcached - Port `11211`

## Build a mirror

`` `shell script
Docker -f. \ docker-support \ docker -t <your docker hub username> / django_blog: Latest.
`` `

## Run custom instructions (such as database migration)

`` `shell script
Docker Run -It --RM <Your Docker Hub User Name> / Django_blog: Latest <Instruction>
`` `
### django_mysql_host Get: Host Enter INET ADDR in IFCONFIG in IFCONFIG

E.g:

`` `shell script
Docker run -it --rm-e django_mysql_host = 192.168.231.50 Django_blog / django_blog: Latest Makemigrations
Docker run -it --rm-e django_mysql_host = 192.168.231.50 Django_blog / django_blog: Latest Migrate
Docker run -it --rm-e django_mysql_host = 192.168.231.50 Django_blog / django_blog: Latest CreateSuperuser
`` `

## Environment Variable List

| Environment Variable Name | Default | Remarks |
| --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- -------------------------------------------------- ----- | ------------------------------------------------------------------------------------------------------- -------------------------------------------------- - |
| Django_Debug | FALSE | |
| Django_secret_key | Django_blog_change_me | Be sure to modify, suggest [random build] (https://www.random.org/passwords/?num=5&len=24&format=html&rnd=new) |
| Django_Mysql_Database | medblog | |
| Django_Mysql_user | root |
| Django_mysql_password | password | |
| Django_Mysql_host | 127.0.0.1 | |
| Django_Mysql_port | 3306 |
| Django_memcached_enable | TRUE | |
| Django_memcached_location | 127.0.0.1:11211 | |
| Django_baidu_notify_url | http://data.zz.baidu.com/urls?site=https://www.example.org&token=change_me | Please in [Baidu Webmaster Platform] (https://ziyuan.baidu.com/ Linksubmit / index) Get the interface address                  |
| DJANGO_EMAIL_TLS          | False                                                                      |                                                                                                |
| DJANGO_EMAIL_SSL          | True                                                                       |                                                                                                |
| DJANGO_EMAIL_HOST         | smtp.example.org                                                           |                                                                                                |
| DJANGO_EMAIL_PORT         | 465                                                                        |                                                                                                |
| DJANGO_EMAIL_USER         | SMTP_USER_CHANGE_ME                                                        |                                                                                                |
| DJANGO_EMAIL_PASSWORD     | SMTP_PASSWORD_CHANGE_ME                                                    |                                                                                                |
| DJANGO_ADMIN_EMAIL        | admin@example.org                                                          |                                                                                                |
| DJANGO_WEROBOT_TOKEN      | DJANGO_BLOG_CHANGE_ME                                                      | Please use your own WeChat public signal token（Token）                                                        |
