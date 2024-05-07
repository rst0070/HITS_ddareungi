from pyspark import RDD
from typing import Dict, Tuple

class StopInfo(object):
    
    def __init__(self, data_rdd:RDD[str]):
        """_summary_

        Args:
            data_rdd (RDD[str]): ddareungi stop informations. each element has info of each stop.
        """
        def filterHead(seq:str):
            ### remove head of the csv info file ###
            
            return not seq.startswith('"대여소')
        
        def infoMapper(seq:str):
            ### crop the seq to make tuple ###
            
            x = seq.split(',')
            ## x = ['"stop_id"', '"addr1"', '"addr2"', '"latitude"', '"longitude"']
            for i in range(0, len(x)):
                x[i] = x[i][1:-1]
            
            return x[0], x[1]+x[2], float(x[3]), float(x[4])
            
        self.data = data_rdd \
            .filter(filterHead) \
            .map(infoMapper)
        
        
    def getStopInfo(self) -> RDD[Tuple[str, Tuple[str, float, float]]]:
        """
        Returns ddareungi stop information
        
        Returns:
            RDD[Tuple[str, Tuple[str, float, float]]]: ("stop_id", ("addr1+addr2", latitude, longitude))
        """
        info = self.data.map(lambda x: (x[0], (x[1:])))
        return info
    
    def getScoreVector(self) -> RDD[Tuple[str, float]]:
        """_summary_

        Returns:
            RDD[Tuple[str, float]]: each element is like (stop_id, 1.0)
        """
        return self.data.map(lambda x: (x[0], 1.))