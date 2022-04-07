# Multicontainer application

Codeching - video 9 - Multi container deployment kubernetes | React| Node.js | Postgres | Ingress Nginx | step by stepNo
Folder:
    Client-server: 
        1) This folder React client, Node.js backend, PostgreSQL and Nginx .
        2) Also Mock server which has dockerized APIs which used for mock service. contains of json token and async logic
k8S->dmfk8s_allservices:
    kubernete based deployment script for: mockserver, mongoserver,  React client, Node.js and postgres
k8s-> kubernetes-mongodb:
    for mongo based deploymet on k8s
Prereq for dmfk8s_allservices is to set password in k8s as follows:
 1)    kubectl  create secret generic pgpassword --from-literal PGPASSWORD=12345test
 2)    You should install Ingress Nginx with command:
       kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v0.46.0/deploy/static/provider/cloud/deploy.yaml

       After that you can use the following command to start in main folder:
        cd to <k8S>
       kubectl apply -f dmfk8s_allservices
