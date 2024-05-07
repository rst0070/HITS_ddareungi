from typing import Dict, List, Tuple
from pyspark import RDD
from tqdm import trange

class HITSCalculator(object):
    
    
    def _reduceMatrixValue(self, x, y):
            assert type(x) == type(y) == list
            for str_float in y:
                x.append(str_float)
            return x
        
    def _matrixToDict(self, matrix: RDD[Tuple[str, Tuple[str, float]]]):
        
        result:Dict[str, List[Tuple[str, float]]] \
            = matrix.mapValues(lambda x: [x])\
                .reduceByKey(self._reduceMatrixValue)\
                .collectAsMap()
        
        return result
                
    def calculate(self,
        iteration:int,
        A: RDD[Tuple[str, Tuple[str, float]]],
        A_t: RDD[Tuple[str, Tuple[str, float]]],
        vec_h: RDD[Tuple[str, float]],
        vec_a: RDD[Tuple[str, float]]
        ) -> Tuple[Dict[str, float], Dict[str, float]]:
        """
        calculate HITS algorithm on ddareungi link matrix
        
        Args:
            iteration (int): _description_
            A (RDD[Tuple[str, Tuple[str, float]]]): _description_
            A_t (RDD[Tuple[str, Tuple[str, float]]]): _description_
            vec_h (RDD[Tuple[str, float]]): _description_
            vec_a (RDD[Tuple[str, float]]): _description_

        Returns:
            Tuple[RDD[Tuple[str, float]], RDD[Tuple[str, float]]]: h_score, a_score
        """
        
        A:Dict[str, List[Tuple[str, float]]] = self._matrixToDict(A)
        A_t:Dict[str, List[Tuple[str, float]]] = self._matrixToDict(A_t)
        
        h_score:Dict[str, float] = vec_h.collectAsMap()
        a_score:Dict[str, float] = vec_a.collectAsMap()
        
        pbar = trange(0, iteration, desc="calculating score vectors")
        
        for epoch in pbar:

            ## update h_score
            max_val_of_vec = 1e-12
            for hub, out_links in A.items():
                score_sum = 0. # for hub node
                for authority, rate_link in out_links:
                    score_sum += rate_link * a_score[authority]
                #print(score_sum)

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
        
        return h_score, a_score