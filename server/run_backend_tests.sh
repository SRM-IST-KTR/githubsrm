echo "[STARTING-DJANGO-SERVER]"
python3 githubsrm/manage.py runserver &

sleep 5

python3 -m unittest tests/test_apis.py
python3 -m unittest tests/test_admin.py
python3 -m unittest tests/test_maintainer.py
python3 -m unittest tests/test_full_flow.py 

echo "[RUNNING-CLEANUP-JOBS]"
fuser -k 8000/tcp
