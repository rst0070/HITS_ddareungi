from pyspark.sql import SparkSession
from collections.abc import Iterable
from collections import defaultdict
from typing import List


def fiilterHead(seq:str):
    if seq.startswith('"기준'):
        return False
    return True


def extractRdd(iterator:Iterable[str]):
    hash_map = defaultdict(int)
    
    for seq in iterator:
        seq = seq.split(',')
        start, end, num = seq[3][1:-1], seq[5][1:-1], int(seq[7][1:-1])
        
        hash_map[start+','+end] += num
    
    result = [(k, v) for k, v in hash_map.items()]
    return result

def extractMatrixA(iterator:Iterable[tuple[str, int]]):
    
    hash_map = defaultdict(List)
    
    for tup in iterator:
        start, end = tup[0].split(',')
        num = tup[1]
        
        if start not in hash_map:
            hash_map[start] = []
            
        hash_map[start].append((end, num))
    
    result = [(end_node, num_sum) for end_node, num_sum in hash_map.items()]
    return result

def extractMatrixA_t(iterator:Iterable[tuple[str, int]]):
    
    hash_map = defaultdict(List)
    
    for tup in iterator:
        start, end = tup[0].split(',')
        num = tup[1]
        
        if end not in hash_map:
            hash_map[end] = []
            
        hash_map[end].append((start, num))
    
    result = [(start_node, num_sum) for start_node, num_sum in hash_map.items()]
    return result

    


## RDD is like below
## (start stop, [(end stop, number of bikes used that route), ....])
matA_t.take(25)


def main():
    
    spark = SparkSession \
    .builder \
    .master('local') \
    .appName('demo') \
    .config("spark.driver.memory", "2g") \
    .config('spark.executor.memory', '2g') \
    .getOrCreate()
    
    sc = spark.sparkContext
    data_rdd = sc.textFile('./test.csv')
    rdd = data_rdd.filter(fiilterHead).mapPartitions(extractRdd)
    
    matA = rdd.mapPartitions(extractMatrixA)
    matA_t = rdd.mapPartitions(extractMatrixA_t)
