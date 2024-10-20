db-up:
	cd ./back && docker-compose up --build -d
db-down:
	cd ./back && docker-compose down

api-up: db-up
	