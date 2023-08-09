python3 -m flask --app test/server/app run &
fuser -k 5000/tcp
child_pid=$!
echo "Started flask server with pid ${child_pid}"
sleep 2
echo "Killing server with pid ${child_pid}"
kill ${child_pid}
echo "successfully killed? (0=success)": ${?}

