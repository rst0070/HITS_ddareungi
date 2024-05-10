# HITS_ddareungi
Ddareungi(따릉이) is a public bicycle sharing service of Seoul, South Korea.  
Using rental and return information of the bicycles by bicycle station, 
I modified and applied [HITS(Hub and Authority algorithm)](https://en.wikipedia.org/wiki/HITS_algorithm) to check hub and authority score of each rental stop.  

__Data algorithm__  
You can check the algorithm in the folder, `/data`. 
The algorithm uses *pyspark* library to transform data file, seoul city provides, to link matrix and score vectors.  
  
__Used Data__  
- [Rental and return number of each bicycle station](http://data.seoul.go.kr/dataList/OA-21229/F/1/datasetView.do)
- [Information of each bicycle station](http://data.seoul.go.kr/dataList/OA-21235/S/1/datasetView.do)
    - eg. latitude, longitude and address of each bicycle station

__Web App__  
I used Next.js to show the calculated information on a map with kakao map api.  
Check [here](https://rst0070.github.io/HITS_ddareungi/).