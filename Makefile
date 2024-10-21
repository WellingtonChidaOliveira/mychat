
api-down:
	cd ./back && docker-compose down

api-up: 
	cd ./back && docker-compose up --build -d

seed-embeddings:
	python3 -m back.src.embeddings.api.routes.embedding_populate

