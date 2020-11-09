# Top Performed movies
Generate report in GRAFANA hosted in DOCKER on top performing movies by their budget to revenue ratio also Dashboard showing genres on those top 1000 movies that hosted in POSTGRES DB in Docker and through the process of calculation and processing public domain movies metadata and IMDB WIKI Data using Python3 and by PANDAS module that will run in Docker where the LOGS can be seen in LOKI from Grafana dashboard. 
Top performing 1000 movies that loaded in POSTGRES can be queried from GRAFANA using POSTGRES datasource on other datapoints on those movies like revenue, Companies, etc,.


## Dashboard

 [Grafana](http://localhost:9000/explore?orgId=1&left=%5B%22now-1h%22,%22now%22,%22postgres%22,%7B%22datasource%22:%22postgres%22,%22format%22:%22table%22,%22timeColumn%22:%22time%22,%22metricColumn%22:%22none%22,%22group%22:%5B%5D,%22where%22:%5B%7B%22type%22:%22macro%22,%22name%22:%22$__timeFilter%22,%22params%22:%5B%5D%7D%5D,%22select%22:%5B%5B%7B%22type%22:%22column%22,%22params%22:%5B%22value%22%5D%7D%5D%5D,%22rawQuery%22:true,%22rawSql%22:%22SELECT%5Cn*%5CnFROM%5Cnmovie_metadata%5Cnorder%20by%20ratio%20%20desc%5Cn%22%7D%5D) 

