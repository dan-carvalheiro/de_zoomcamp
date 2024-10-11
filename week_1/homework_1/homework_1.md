
# DE Zoomcamp Homework 1

- Dan Carvalheiro
- 2024-09-12


### Question 1
Which tag has the following text? - Automatically remove the container when it exits

#### Answer:
To answer this question, I used the following bash command:
```commandline
docker run --help
```
The command output showed that the `--rm` has the specified text.

### Question 2
Run docker with the python:3.9 image in an interactive mode and the entrypoint of bash. Now check the python modules that are installed ( use pip list ).

What is version of the package wheel ?

#### Answer:

I created the python image with the following bash commands:
```commandline
docker run -it python:3.9 bash
root@b1e6ebc88ab3:/# pip list
```
The output showed that the current version of the "wheel" package is 0.44.0

### Prepare Postgres
Run Postgres and load data as shown in the videos We'll use the green taxi trips from September 2019:

wget https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-09.csv.gz

You will also need the dataset with zones:

wget https://s3.amazonaws.com/nyc-tlc/misc/taxi+_zone_lookup.csv

Download this data and put it into Postgres (with jupyter notebooks or with a pipeline)

#### Answer:

I created a container for the postgres database with this command:

```commandline
docker run -it \
    -e POSTGRES_USER="root" \
    -e POSTGRES_PASSWORD="root" \
    -e POSTGRES_DB="ny_taxi" \
    -v C:/Users/dlc13002/projects/de_zoomcamp/week_1/homework_1/ny_taxi:/var/lib/postgresql/data \
    -p 5432:5432 \
    --network=pg-network \
    --name pg-database \
postgres:17
```

and pgadmin4 with this command:

```commandline
docker run -it \
    -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
    -e PGADMIN_DEFAULT_PASSWORD="root" \
    -p 8080:80 \
    --network=pg-network \
    --name pgadmin \
    dpage/pgadmin4
```

I also created seperate ingenstion scripts for the green taxi trips data (upload_trips.py) and the zones look-up data (upload_zones.py). Both python scripts can be found in this repository.

### Question 3: Count records
How many taxi trips were totally made on September 18th 2019?

Tip: started and finished on 2019-09-18.

Remember that lpep_pickup_datetime and lpep_dropoff_datetime columns are in the format timestamp (date and hour+min+sec) and not in date.
- 15767 
- 15612 
- 15859 
- 89009

#### Answer
I executed the following SQL command in pgadmin
```text
SELECT 
	COUNT (*)
FROM trips
WHERE 
	CAST (lpep_pickup_datetime as DATE) = date '2019-09-18'
	AND CAST (lpep_dropoff_datetime as DATE) = date '2019-09-18';
```
which indicated that there were 15,612 trips made on 2019-09-18.

### Question 4. Longest trip for each day

Which was the pick up day with the longest trip distance? Use the pick up time for your calculations.

Tip: For every trip on a single day, we only care about the trip with the longest distance.

- 2019-09-18
- 2019-09-16
- 2019-09-26
- 2019-09-21

#### Answer
I executed the following SQL command in pgadmin
```text
SELECT 
	CAST (lpep_pickup_datetime as DATE) as day,
	MAX(trip_distance) as max_distance
FROM trips
WHERE CAST (lpep_pickup_datetime as DATE) IN (
    date '2019-09-18', 
    date '2019-09-16',
    date '2019-09-26',
    date '2019-09-21'
    )
GROUP BY CAST (lpep_pickup_datetime as DATE)
ORDER BY max_distance DESC;
```
which indicated that the day with the longest trip was 2019-09-26 with a max distance trip of 341.64

### Question 5. Three biggest pick up Boroughs

Consider lpep_pickup_datetime in '2019-09-18' and ignoring Borough has Unknown

Which were the 3 pick up Boroughs that had a sum of total_amount superior to 50000?

- "Brooklyn" "Manhattan" "Queens"
- "Bronx" "Brooklyn" "Manhattan"
- "Bronx" "Manhattan" "Queens"
- "Brooklyn" "Queens" "Staten Island"

#### Answer
I executed the following SQL command in pgadmin
```text
SELECT
	"Borough",
	SUM(total_amount)
FROM trips
INNER JOIN zones on trips."PULocationID" = zones."LocationID"
WHERE CAST (lpep_pickup_datetime as DATE) = date '2019-09-18'
GROUP BY "Borough"
HAVING SUM(total_amount) > 50000;
```
which showed that the three boroughs meeting the requested criteria were "Brooklyn", "Manhattan", and "Queens".

### Question 6. Largest tip

For the passengers picked up in September 2019 in the zone name Astoria which was the drop off zone that had the largest tip? We want the name of the zone, not the id.

Note: it's not a typo, it's tip , not trip

- Central Park
- Jamaica
- JFK Airport
- Long Island City/Queens Plaza

#### Answer

I executed the following SQL command in pgadmin
```text
SELECT
	"Zone" as dropoff_zone,
	MAX(tip_amount) as largest_tip
FROM trips
INNER JOIN zones on trips."DOLocationID" = zones."LocationID"
WHERE CAST (lpep_pickup_datetime as DATE) >= date '2019-09-01'
	AND CAST (lpep_pickup_datetime as DATE) < date '2019-10-01'
	AND (SELECT "Zone"
	     FROM zones
	     WHERE trips."PULocationID" = zones."LocationID") = 'Astoria'
GROUP BY "Zone"
ORDER BY MAX(tip_amount) DESC;
```
which showed that the largest tip given for a trip from Astoria was for a trip to JFK Airport with a tip of $62.31 