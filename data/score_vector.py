from pyspark import RDD
from typing import Dict, Tuple

def _headFilter(seq:str):
    return not seq.startswith('"대여소')
    
def _mapperFunc(seq:str, rdd_size:float) -> Tuple[str, float]:
    """_summary_

    Args:
        seq (str): _description_

    Returns:
        Tuple[str, float]: _description_
    """
    return seq.split(',')[0][1:-1], 1.#/rdd_size

def getScoreVector(data_rdd:RDD) -> RDD:
    """_summary_

    Args:
        data_rdd (RDD): _description_

    Returns:
        tuple[Dict[str, float], Dict[str, float]]: _description_
    """
    rdd = data_rdd.filter(_headFilter)
    rdd_size = float(rdd.count())
    
    rdd = rdd.map(lambda seq: _mapperFunc(seq, rdd_size))
    vec1 = rdd
    
    return vec1