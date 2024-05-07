from pyspark.sql import SparkSession
from alg.link_info import LinkInfo
from alg.stop_info import StopInfo
from alg.calculation import Calculator
from typing import Tuple, List
from pyspark import RDD

class Main(object):
    
    def __init__(self,
        hits_iteration:int,
        link_data_path:str,
        id_data_path:str):
        
        self.hits_iteration = hits_iteration
        
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
        
        ###
        ### A - link matrix, A_ij = ratio of i to j among outlinks from i
        ### A_t - transposed A
        ###
        link_info = LinkInfo(data_rdd=link_data_rdd)
        self.A:RDD[Tuple[str, Tuple[str, float]]] = link_info.getLinkMatrix()
        self.A_t:RDD[Tuple[str, Tuple[str, float]]] = link_info.getTransposedLinkMatrix()
        
        stop_info = StopInfo(data_rdd=id_data_rdd)
        self.h_score = stop_info.getScoreVector()
        self.a_score = stop_info.getScoreVector()
        self.stop_info = stop_info.getStopInfo()
        
        self.calculator = Calculator()
        
    def process(self,
        save_h_path:str,
        save_a_path:str) -> None:
        """
        calculates the hub and authority scores.
        saves that informations with given path.
        Args:
            save_h_path (str): save path for hub score
            save_a_path (str): save path for authority score

        Returns:
            None
        """
        
        self.h_score, self.a_score = self.calculator.calculate(
                                            iteration = self.hits_iteration,
                                            A=self.A,
                                            A_t=self.A_t,
                                            vec_h=self.h_score,
                                            vec_a=self.a_score
                                        )
        ### h and a score look like below
        ### (stop_id:str, score:float)
        
        ###
        ### join scores with information of stops
        ###
        h_score_and_info = self.h_score.join(self.stop_info)
        a_score_and_info = self.a_score.join(self.stop_info)
        
        def extract_values(x:Tuple[str, Tuple[float, Tuple[str, float, float]]]):
            return x[0], x[1][0], x[1][1][0], x[1][1][1], x[1][1][2]
            
        h_score_and_info = h_score_and_info.map(extract_values)
        a_score_and_info = a_score_and_info.map(extract_values)
        
        ###
        ### output to file
        ###
        self.saveInfoAsCsv(h_score_and_info, save_h_path)
        self.saveInfoAsCsv(a_score_and_info, save_a_path)
    
    def saveInfoAsCsv(self, data:RDD[tuple[str, float, str, float, float]], path:str):
        data = data.collect()
        with open(path, 'w') as f:
            f.write("stop_id,score,address,latitude,longitude\n")
            
            for stop_id, score, address, latitude, longitude in data:
                f.write(f"{stop_id},{score},{address},{latitude},{longitude}\n")
                
            f.close()
        
    
    
if __name__ == "__main__":
    
    main = Main(hits_iteration=1,
                link_data_path='./encoded_data/20240421.csv',
                id_data_path='./encoded_data/stops.csv'
            )
    
    main.process(
            save_h_path="./scores/20240421_h.csv",
            save_a_path="./scores/20240421_a.csv"
        )

