# Introduction
Capstone project for Food image segmentation. 


## Docker 
- build docker
```shell
docker-compose up --build
```

- Remove 
```shell
docker-compose down
```

## Demo
- Demo Video: [Watch here](https://drive.google.com/file/d/1a2u5NWGsyqHaUM_SYqZ5OD93Ff5U9OEO/view?usp=sharing)

## EC2 Brute force deployment
```shell
docker build -t nikeshthapa255/food-segmentation-classification:latest ./detection
docker build -t nikeshthapa255/food-segmentation-segmentation:latest ./segmentation
docker build -t nikeshthapa255/food-segmentation-volume_estimation:latest ./volume_estimation
docker build -t nikeshthapa255/food-segmentation-frontend:latest ./frontend

docker push nikeshthapa255/food-segmentation-classification:latest
docker push nikeshthapa255/food-segmentation-segmentation:latest
docker push nikeshthapa255/food-segmentation-volume_estimation:latest
docker push nikeshthapa255/food-segmentation-frontend:latest

```


# Next step ideas
- Food recepie.
- allergic content. 
- classify the food to grain, dairy, protein.
