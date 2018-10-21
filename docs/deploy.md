# Deploy instructions

#### uWSGI
Install uWSGI,
```
$ source env/bin/activate
$ pip install uwsgi
```

Create a systemd startup config,
```
$ sudo cp docs/config/uwsgi.service /etc/systemd/system/uwsgi_tkapi.service
```

Create uwsgi log directory if it does not exist,
```
$ sudo mkdir /var/log/uwsgi
```

Start the uwsgi service and check its status,
```
$ sudo systemctl start uwsgi_tkapi
$ sudo systemctl status uwsgi_tkapi
```
In case of problems, start the uwsgi command `ExecStart` from `uwsgi_tkapi.service` manually to see what is wrong.

Enable on startup,
```
$ sudo systemctl enable uwsgi_tkapi
```
