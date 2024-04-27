from collections.abc import Iterable
from collections import defaultdict
from typing import Dict, List, Tuple
from pyspark import RDD


def _fiilterHead(seq:str):
    """
    filter head of the csv file
    """
    return not seq.startswith('"기준')

def _mapToSplitted(seq:str) -> Tuple[Tuple[str, str], int]:
    """
    Map string sequence to tuple
    '"start_id", "end_id", "num"'
    --> ((start_id, end_id), num)
    """
    seq = seq.split(',')
    start, end, num = seq[3][1:-1], seq[5][1:-1], int(seq[7][1:-1])    
    return (start, end), num

def _filterTrashData(x):
    return x[0][0] != 'X' and x[0][1] != 'X'
        

def _reduceLink(x:int, y:int) -> int:
    """
    sum duplicated data like below
    ((start, end), x), ((start, end), y)
    --> ((start, end), x+y)
    """
    return x+y

def _mapToMatrixA(link:Tuple[Tuple[str, str], int]) -> Tuple[str, List[Tuple[str, int]]]:
    """
    ( (start, end), num )
    --> ( start, [(end, num)] )
    """
    return link[0][0], [ (link[0][1], link[1]) ]


def _reduceMatrix(x, y):
    """
    ( start, [(end1, num1)] ), ( start, [(end2, num2)] ) --> ( start, [(end1, num1), (end2, num2)] )
    """
    for v in y:
        x.append(v)
    return x

def _mapToNomalize(x):
    """ 
    
    """
    total_links = 0
    for node, num_links in x[1]:
        total_links += num_links
    
    total_links = float(total_links)
    links = [(node, num_links/total_links) for node, num_links in x[1]]
    
    return x[0], links

def _flatmapToTranspose(x):
    """
    <normalized>
    ( start, [(end1, num1), (end2, num2)] ) --> ( end1, [(start, num1)] ), ( end2, [(start, num2)] ) --> 
    """
    return [ 
            ( end, [ (x[0], link_rate) ] ) 
            for end, link_rate in x[1]
    ]
    

def getLinkMatrices(data_rdd) -> Tuple[RDD, RDD]:
    rdd_links = data_rdd \
        .filter(_fiilterHead) \
        .map(_mapToSplitted) \
        .filter(_filterTrashData) \
        .reduceByKey(_reduceLink)
    
    matA = rdd_links \
        .map(_mapToMatrixA) \
        .reduceByKey(_reduceMatrix) \
        .map(_mapToNomalize) \
        
    matA_t = matA \
        .flatMap(_flatmapToTranspose) \
        .reduceByKey(_reduceMatrix)

    return matA, matA_t
