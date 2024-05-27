echo "BUILD START"

python3.12 -m pip install -r todolist/requirements.txt
python3.12 todolist/manage.py collectstatic --noinput --clear

echo "BUILD END"