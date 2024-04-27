# 


```python
try:
    data_rdd = sc.textFile('D:/DevWork/workspace_folders/ddareungi/data/20240421.csv')
    data_rdd.take(5)
except Exception as exc:
    print(exc)
```

```
try:
    data_rdd = sc.textFile('D:/DevWork/workspace_folders/ddareungi/data/20240421.csv')
    data_rdd.take(5)
except Exception as exc:
    print(exc)
```

i found that it is usually caused by lack of memory space. so i tried like below but it didn't work.  
```python
from pyspark.sql import SparkSession
spark = SparkSession \
    .builder \
    .master('local') \
    .appName('demo') \
    .config("spark.driver.memory", "10g") \
    .config('spark.executor.memory', '2g') \
    .getOrCreate()
    
```
after that i found the solution on stackoverflow, and im sharing that on this post.  
  
```

```