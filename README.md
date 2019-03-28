This is the miniproject of ECS781P Cloud computing!
My app aims to let guests check the spacex' ship detail from my cassandra!
The file getships.py is a algorithm which helps me get data from https://docs.spacexdata.com/#e520e500-0421-4774-8bcb-8d07b7dfa222' by using REST API.
Then I manually convert the data of json file into CSV format.
The spacex.csv is the data which need to upload to cassandra.In this file, there are 6 feature(column) namely id,ship_id,ship_name,ship_type,home_port,active.
Here active means the ship is retired or not.
the 3 cassandra files are used to build kubernetes sevice.
Once the service is built, we can type IP/spacex/<id> in browser. the <id> range is from 1 to 20.
Each feedback is the one specific ship's detail. 
