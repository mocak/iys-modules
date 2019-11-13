# IYS CRM Modules for Odoo

## About this project
This project aim to deal with modules related to manage CRM in a generic way. You'll find modules that:

    - import CRM Lead apply from backend
    - ...

## Installing

### Installing via docker-compose

You can simply run project via docker-compose by executing the following command:

```
docker-compose up --build
```

Related modules will be installed automatically. 

## Informing Backend

Backend container is responsible for both sending and receiving messages. When tracking statues changes in Odoo, app sends a message to backend queue which is being consumed by backend's receive.py script. 
You can check the logs of consumed messages from stdout.

## Importing Leads

Use following command to push random lead data to odoo queue.

```
docker-compose exec backend python send.py 
```

receive.py script which is also consuming the odoo queue will send lead data to Odoo via external api after message was received.

## Demo Users

### Account Manager

User Name: demo_user

Password: demo

### Back-Office Manager

User Name: demo_manager

Password: demo