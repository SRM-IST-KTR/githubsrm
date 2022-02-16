start=$(date +%s)
a=15

echo "[STARTING-DJANGO-SERVER]"
python3 githubsrm/manage.py runserver &

sleep $a
python3 -m unittest -v tests/test_schema.py

sleep $a
python3 -m unittest -v tests/test_apis.py

sleep $a
python3 -m unittest -v tests/test_admin.py

sleep $a
python3 -m unittest -v tests/test_maintainer.py

sleep $a
python3 -m unittest -v tests/test_full_flow.py

echo "[RUNNING-CLEANUP-JOBS]"
fuser -k 8000/tcp

end=$(date +%s)

echo "Runtime:- $((end - start)) seconds"
