# IYS CRM Modules for Odoo

## About this project
This project aim to deal with modules related to manage CRM in a generic way. You'll find modules that:

    - import CRM Lead apply from backend
    - ...

## Installing

### Installing via docker-compose

You can simply run project via docker-compose by the command below

```
docker-compose up --build
```

Related modules will be installed automatically. 

## Informing Backend

Backend container is responsible for both sending and receiving messages. 
When tracking statues changed in Odoo, app sends a message to backend queue that is consuming by backend receive.py file. 
You can check logs of consuming message from stdout.

## Importing Leads

You can use following command to push random lead data to odoo queue.

```
docker-compose exec backend python send.py 
```
receive.py will send lead data to Odoo via external api after received message from odoo queue.

## Demo Users

### Account Manager
User Name: demo_user
Password: demo

### Back-Office Manager
User Name: demo_manager
Password: demo