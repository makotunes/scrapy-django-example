docker exec -it scraper python mysite/manage.py makemigrations nutrition
docker exec -it scraper python mysite/manage.py migrate