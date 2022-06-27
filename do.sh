cd gateway_kong
./run-db.sh
./migrate-db.sh
./run-kong.sh
./run-konga.sh
cd ..
cd api1
./run.sh
cd ..
cd api2
./run.sh
cd ..
cd api3
./run.sh
cd ..
cd db
./run-db.sh
./run-express.sh
cd ..
cd api_management
./run.sh
cd ..
cd session_db
./run.sh
cd ..
cd frontend
./run.sh
cd ..
cd tyk
./run.sh
cd ..

