from collections.abc import Iterable
from collections import defaultdict
from typing import Dict, List, Tuple
from pyspark import RDD

class Calculator(object):
    
    
    def _multiplyMapper(self, x:Tuple[str, Tuple[Tuple[str, float], float]]):
        assert type(x) == type(x[1]) == type(x[1][0]), f"actual value: {x}"
        assert type(x[0]) == type(x[1][0][0]) == str, f"actual value: {x}"
        assert type(x[1][0][1]) == type(x[1][1]) == float, f"actual value: {x}"
        
        return x[1][0][0], x[1][0][1] * x[1][1]
    
    def _multiplyReducer(self, x:float, y:float):
        assert type(x) == type(y) == float
        return x+y
    
    def multiplyWithT(self, 
        t_matrix: RDD[Tuple[str, Tuple[str, float]]],
        vector: RDD[Tuple[str, Tuple[str, float]]]
        ) -> RDD[Tuple[str, float]]:
        """_summary_
        Does matrix and vector multiplication.
        But The input t_matrix is transposed matrix.
        eg. for A*x the input is A_t = transpose(A)
        
        result = transpose(t_matrix) * vector
        
        Args:
            t_matrix (RDD[Tuple[str, Tuple[str, float]]]): Transposed matrix
            vector (RDD[Tuple[str, Tuple[str, float]]]): vector

        Returns:
            RDD[Tuple[str, float]]: result vector
        """
        ## t_matrix : (j, (i, v_1))
        ## vector   : (j, v_2)
        ## joined   : (j, ((i, v_1), v_2))
        joined = t_matrix.join(vector)
        
        ## multiplied   : (i, sum(v_1 * v_2))
        ## x[1][0][0]: i, x[1][0][1]: v_1, x[1][1]: v_2
        multiplied = joined \
            .map(self._multiplyMapper) \
            .reduceByKey(self._multiplyReducer)
            
        return multiplied
    
    def _normalizeMapper(self, x:Tuple[str, float]):
        assert type(x) == tuple, f"actual value: {x}"
        assert type(x[1]) == float        
        return x[1]
    
    def normalizeVector(self, vector:RDD[Tuple[str, float]]) -> RDD[Tuple[str, float]]:
        """_summary_
        1. find maximum value among dimensions of the vector
        2. divide each value of dimensions by the maximum value
        Args:
            vector (RDD[Tuple[str, float]]): _description_

        Returns:
            RDD[Tuple[str, float]]: _description_
        """        
        max_val = vector\
            .map(self._normalizeMapper)\
            .reduce(lambda x, y: x+y)
        
        return vector.map(lambda x: (x[0], x[1]/max_val))
    
    def calculate(self,
        iteration:int,
        A: RDD[Tuple[str, Tuple[str, float]]],
        A_t: RDD[Tuple[str, Tuple[str, float]]],
        vec_h: RDD[Tuple[str, float]],
        vec_a: RDD[Tuple[str, float]]
        ) -> Tuple[RDD[Tuple[str, float]], RDD[Tuple[str, float]]]:
        """_summary_

        Args:
            iteration (int): _description_
            A (RDD[Tuple[str, Tuple[str, float]]]): _description_
            A_t (RDD[Tuple[str, Tuple[str, float]]]): _description_
            vec_h (RDD[Tuple[str, float]]): _description_
            vec_a (RDD[Tuple[str, float]]): _description_

        Returns:
            Tuple[RDD[Tuple[str, float]], RDD[Tuple[str, float]]]: h_score, a_score
        """
        h_score = vec_h
        a_score = vec_a
        
        for it in range(0, iteration):
            h_score = self.multiplyWithT(A_t, a_score)
            h_score = self.normalizeVector(h_score)
            
            a_score = self.multiplyWithT(A, h_score)
            a_score = self.normalizeVector(a_score)
        
        return h_score, a_score
            