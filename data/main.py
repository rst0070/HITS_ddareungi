from pyspark.sql import SparkSession
from link_matrix import getLinkMatrices
from score_vector import getScoreVector
from typing import Dict, Tuple, List
from copy import deepcopy
from tqdm import trange

## RDD is like below
## (start stop, [(end stop, number of bikes used that route), ....])

def calculate(
    max_epoch:int,
    A:Dict[str, List[Tuple[str, float]]], 
    A_t:Dict[str, List[Tuple[str, float]]], 
    h_score:Dict[str, float], 
    a_score:Dict[str, float]):
    
    pbar = trange(0, max_epoch, desc="calculating score vectors")
    for epoch in pbar:
        
        ## update h_score
        max_val_of_vec = 1e-12
        for hub, out_links in A.items():
            score_sum = 0. # for hub node
            for authority, rate_link in out_links:
                score_sum += rate_link * a_score[authority]
            
            max_val_of_vec = max(max_val_of_vec, score_sum)
            h_score[hub] = score_sum
        
        ## normalize h_score
        for hub in h_score.keys():
            h_score[hub] /= max_val_of_vec
        
        
        ## update a_score
        max_val_of_vec = 1e-12
        for authority, in_links in A_t.items():
            score_sum = 0. # for authority node
            for hub, rate_link in in_links:
                score_sum += rate_link * h_score[hub]
                
            max_val_of_vec = max(max_val_of_vec, score_sum)
            a_score[authority] = score_sum
            
        for authority in a_score.keys():
            a_score[authority] /= max_val_of_vec
    
    #print(h_score)

def saveScoreVectorAsCsv(data:Dict[str, float], path:str):
    with open(path, 'w') as f:
        f.write("stop_id,score\n")
        for node, score in data.items():
            f.write(f"{node},{score}\n")
        f.close()



def main(
    train_epoch:int,
    link_data_path:str,
    id_data_path:str,
    save_h_path:str,
    save_a_path:str):
    
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
    
    calculate(
        max_epoch=train_epoch,
        A=A,
        A_t=A_t,
        h_score=h_score,
        a_score=a_score
    )
    
    saveScoreVectorAsCsv(a_score, save_a_path)
    saveScoreVectorAsCsv(h_score, save_h_path)
    
    
if __name__ == "__main__":
    main(
        train_epoch=10000,
        link_data_path='./encoded_data/20240421.csv',
        id_data_path='./encoded_data/stops.csv',
        save_h_path="./hub_score/20240421.csv",
        save_a_path="./authority_score/20240421.csv"
    )

