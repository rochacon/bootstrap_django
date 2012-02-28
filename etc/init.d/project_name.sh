#!/bin/sh

### BEGIN INIT INFO
# Provides:          uwsgi
# Required-Start:    $all
# Required-Stop:     $all
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: starts the uwsgi app server
# Description:       starts uwsgi app server using start-stop-daemon
### END INIT INFO
PATH=/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin
DAEMON=/usr/local/bin/uwsgi

OWNER={{ uid }}

NAME=uwsgi
DESC="uwsgi: {{ project_name }}"
UWSGI_INI="--ini {{ uwsgi_inifile }}"
PIDFILE="{{ uwsgi_pidfile }}"

test -x $DAEMON || exit 0

set -e # ???

case "$1" in
  start)
        echo -n "Starting $DESC: "
        start-stop-daemon --start --chuid $OWNER:$OWNER --user $OWNER \
                --exec $DAEMON -- $UWSGI_INI
        echo "$NAME."
        ;;
  stop)
        echo -n "Stopping $DESC: "
        start-stop-daemon --user $OWNER --quiet --retry 2 --stop \
                --exec $DAEMON -- --stop $PIDFILE
        echo "$NAME."
        ;;
  reload)
        kill -1 $(cat $PIDFILE)
        ;;
  force-reload)
        kill -15 $(cat $PIDFILE)
       ;;
  restart)
        echo -n "Restarting $DESC: "
        start-stop-daemon --user $OWNER --quiet --retry 2 --stop \
                --exec $DAEMON -- --stop $PIDFILE
        sleep 1
        start-stop-daemon --start --chuid $OWNER:$OWNER --user $OWNER \
                --exec $DAEMON -- $UWSGI_INI
        echo "$NAME."
        ;;
  status)
        kill -10 $(cat $PIDFILE)
        ;;
  *)
        N=/etc/init.d/$NAME
        echo "Usage: $N {start|stop|restart|reload|force-reload|status}" >&2
        exit 1
        ;;
esac
exit 0

