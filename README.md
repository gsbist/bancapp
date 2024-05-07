### RabbitMQ setup for development 
```
sudo docker run -it --rm --name user -p 5672:5672 -p 15672:15672 rabbitmq:3.13-management

```

### Running celery
```
make run-celery

```
