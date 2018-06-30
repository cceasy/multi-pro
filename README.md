## mock server tests

### first, start server
uwsgi --ini uwsgi.ini

### second, start fake client
run fake_uwsgi_client.py

### remarks
please install Redis server, and config params in config.py