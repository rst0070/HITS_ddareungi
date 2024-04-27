from pyspark.sql import SparkSession
from link_matrix import getLinkMatrices
from score_vector import getScoreVectors
from typing import Dict, Tuple, List

## RDD is like below
## (start stop, [(end stop, number of bikes used that route), ....])

def train(
    epoch:int,
    A:Dict[str, List[Tuple[str, float]]], 
    A_t:Dict[str, List[Tuple[str, float]]], 
    h_score:Dict[str, float], 
    a_score:Dict[str, float]):
    pass

def main():
    
    spark = SparkSession \
    .builder \
    .master('local') \
    .appName('demo') \
    .config("spark.driver.memory", "2g") \
    .config('spark.executor.memory', '2g') \
    .getOrCreate()
    
    sc = spark.sparkContext
    link_data_rdd = sc.textFile('./encoded_data/test.csv')
    id_data_rdd = sc.textFile('./encoded_data/stops.csv')
    
    A, A_t = getLinkMatrices(data_rdd=link_data_rdd)
    h_score, a_score = getScoreVectors(data_rdd=id_data_rdd)
    
    print(A)
    #print(A_t)
    #print(h_score)
    
    
if __name__ == "__main__":
    main()

