This is the miniproject of ECS781P Cloud computing!  
My app aims to let guests check ships of spacex detail from my cassandra!  
The file getships.py is a algorithm which helps me get data from https://api.spacexdata.com/v3/ships by using REST API.Here is the main page of spacexdata: https://docs.spacexdata.com/#e520e500-0421-4774-8bcb-8d07b7dfa222  
Then I manually convert the data of json file into CSV format.  
The spacex.csv is the data which need to upload to cassandra.In this file, there are 6 feature(column) namely  id,ship_id,ship_name,ship_type,home_port,active.  
Here active means the ship is retired or not.  
the 3 cassandra files are used to build kubernetes sevice.  
Once the service is built, we can type IP/spacex/<id> in browser. the <id> range is from 1 to 20.  
Each feedback is the one specific ship's detail.   

  here are all the command used in Google Cloud Shell  
#Set the region and zone for our new cluster
```
gcloud config set compute/zone europe-west2-b
export PROJECT_ID="$(gcloud config get-value project -q)"
```
#creates a 3 node cluster named cassandra:
```
gcloud container clusters create cassandra --num-nodes=3 --machine-type "n1-standard-2"
```
#deploy the service among cassandra
```
kubectl create -f cassandra-peer-service.yml
kubectl create -f cassandra-service.yml
kubectl create -f cassandra-replication-controller.yml
````
#scale up cassandra to 3
#check pod status
```
kubectl get pods -l name=cassandra
```
#scale up
```
kubectl scale rc cassandra --replicas=3
```
#check node status
```
kubectl exec -it cassandra-xxxxx -- nodetool status
```
#create table in cassandra
```
kubectl cp spacex.csv cassandra-xxxxx:/spacex.csv
kubectl exec -it cassandra-xxxxx cqlsh
CREATE KEYSPACE spacex WITH REPLICATION = {'class' : 'SimpleStrategy', 'replication_factor' : 2};
CREATE TABLE spacex.stats (id int PRIMARY KEY, ship_id text, ship_name text, ship_type text, home_port text, active boolean);
COPY spacex.stats(id,ship_id,ship_name,ship_type,home_port,active) FROM '/spacex.csv' WITH DELIMITER=',' AND HEADER=TRUE;
select * from spacex.stats;
```
#build dock image
```
docker build -t gcr.io/${PROJECT_ID}/spacex-app:v1 .
docker push gcr.io/${PROJECT_ID}/spacex-app:v1
```
#run as service
```
kubectl run spacex-app --image=gcr.io/${PROJECT_ID}/spacex-app:v1 --port 8080
kubectl delete deployment spacex-app
kubectl expose deployment spacex-app --type=LoadBalancer --port 80 --target-port 8080
kubectl delete service spacex-app
kubectl get services
```
#scale up app
```
kubectl scale deployment spacex-app --replicas=3
kubectl get deployment spacex-app
kubectl get pods
```
