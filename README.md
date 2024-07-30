# bms
# A Book Management System Software
# The tech stacks
    > Python - The programming language
    > Django - The framework to serve APIs
    > Postgres - The DB
    > Docker - To orchestrate the microservices
    > Celery - For async tasks
    > Redis - For messging broker 

# Owner - Deepak Kumar (deepdeepak2222@gmail.com)
# Micro services
    > Backend: Written in Python with Django Rest framework
    > DB : Postgres
    > rec-sys(Recommended system): Currently it has an endpoint which takes content and summarises it and return

# Deploy: To deploy make sure to follow below steps
    > make sure to have docker installed, docker compose is also required
    > Navigate to deploy folder in this repo
    > run the command "docker-compose up --build" to run all the services
    > Have also given postman collection in deploy folder. The name is BMS.json
    > Import it in your postman and start using or running the endpoints

# Gitub repos used for code management
    > https://github.com/deepdeepak2222/bms: The repo for backend code
        > Written in python using django rest framework
        > CI workflow(pipeline) is configured. It will automatically make a docker build when anything is pushed into main branch
    > https://github.com/deepdeepak2222/basic_predict_knn: The repo for recommendation system. Currently it serves only one endpoint to summarise a book content
        > It uses transformers.pipeline to summarise a text. Its a lightweighted model. LLAMA is very heavy and was facing difficulty while running locally.
        > Written in python using flask framework
        > CI workflow(pipeline) is configured. It will automatically make a docker build when anything is pushed into main branch

# To Do
    > Automate deployment using Jenkins
    > Instead of transformers.pipeline to summarise, use LLAMA3 AI model