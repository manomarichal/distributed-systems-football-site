# build & start containers
sudo docker-compose -f docker-compose-dev.yml up -d --build

# create databases
sudo docker-compose -f docker-compose-dev.yml run teams python manage.py recreate-db
sudo docker-compose -f docker-compose-dev.yml run leagues python manage.py recreate-db
sudo docker-compose -f docker-compose-dev.yml run user-interface python manage.py recreate-db
sudo docker-compose -f docker-compose-dev.yml run referees python manage.py recreate-db

# create databases and add data
sudo docker-compose -f docker-compose-dev.yml run teams python manage.py add-teams-data
sudo docker-compose -f docker-compose-dev.yml run teams python manage.py add-clubs-data

sudo docker-compose -f docker-compose-dev.yml run leagues python manage.py add-divisions-data
sudo docker-compose -f docker-compose-dev.yml run leagues python manage.py add-status-data
sudo docker-compose -f docker-compose-dev.yml run leagues python manage.py add-matches-data

sudo docker-compose -f docker-compose-dev.yml run user-interface python manage.py add-user-data

sudo docker-compose -f docker-compose-dev.yml run referees python manage.py add-referees-data

# do one final restart
sudo docker-compose -f docker-compose-dev.yml restart
