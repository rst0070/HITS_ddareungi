from pyspark.sql import SparkSession
from link_matrix import getLinkMatrices
from score_vector import getScoreVector
from typing import Dict, Tuple, List
from copy import deepcopy
from tqdm import trange

## RDD is like below
## (start stop, [(end stop, number of bikes used that route), ....])

def train(
    max_epoch:int,
    A:Dict[str, List[Tuple[str, float]]], 
    A_t:Dict[str, List[Tuple[str, float]]], 
    h_score:Dict[str, float], 
    a_score:Dict[str, float]):
    
    pbar = trange(0, max_epoch, desc="training")
    for epoch in pbar:
        
        ## update h_score
        for hub, out_links in A.items():
            score_sum = 0. # for hub node
            for authority, rate_link in out_links:
                score_sum += rate_link * a_score[authority]
            #print(score_sum)
            h_score[hub] = score_sum
        
        ## update a_score
        for authority, in_links in A_t.items():
            score_sum = 0. # for authority node
            for hub, rate_link in in_links:
                score_sum += rate_link * h_score[hub]
                
            a_score[authority] = score_sum
    
    # pbar = trange(0, max_epoch, desc="node ranking")
    # for epoch in pbar:
        
    #     ## update a_score
    #     for authority, in_links in A_t.items():
    #         score_sum = 0. # for authority node
    #         for hub, rate_link in in_links:
    #             score_sum += rate_link * a_score[hub]
                
    #         a_score[authority] = score_sum
    
    #print(h_score)



def main(train_epoch:int, link_data_path:str, id_data_path:str):
    
    spark = SparkSession \
    .builder \
    .master('local') \
    .appName('demo') \
    .config("spark.driver.memory", "5g") \
    .config('spark.executor.memory', '5g') \
    .getOrCreate()
    
    sc = spark.sparkContext
    link_data_rdd = sc.textFile(link_data_path)
    id_data_rdd = sc.textFile(id_data_path)
    
    A, A_t = getLinkMatrices(data_rdd=link_data_rdd)
    A, A_t = A.collectAsMap(), A_t.collectAsMap()
    
    h_score = getScoreVector(data_rdd=id_data_rdd)
    h_score = h_score.collectAsMap()
    a_score = deepcopy(h_score)
    
    train(
        max_epoch=train_epoch,
        A=A,
        A_t=A_t,
        h_score=h_score,
        a_score=a_score
    )
    #print(h_score[min(h_score, key=h_score.get)])
    print("------------------------------")
    print(a_score)
    #print(A_t)
    #print(h_score)
    
    
if __name__ == "__main__":
    main(
        train_epoch=1000,
        link_data_path='./encoded_data/20240421.csv',
        id_data_path='./encoded_data/stops.csv'
    )

