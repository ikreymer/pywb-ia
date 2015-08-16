FROM ikreymer/pywb

ADD . /webarchive

ADD uwsgi.ini /uwsgi/uwsgi.ini

CMD uwsgi uwsgi.ini

