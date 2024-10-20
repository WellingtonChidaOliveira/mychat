
api-down:
	cd ./back && docker-compose down

api-up: 
	cd ./back && docker-compose up --build -d

