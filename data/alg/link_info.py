from typing import List, Tuple
from pyspark import RDD

class LinkInfo(object):
    """
    Structs link information as RDD which represents link matrix
    Args:
        object (_type_): _description_
    """
    
    def __init__(self, data_rdd:RDD[str]) -> None:
        """
        Maps ddareungi information to link matrix
        Args:
            data_rdd (RDD[str]): the str rdd information from ddareungi csv file.
        """
        
        def filterHead(seq:str):
            """ filter head of the csv file """
            assert type(seq) == str
            
            return not seq.startswith('"기준')
        
        def mapToSplitted(seq:str) -> Tuple[Tuple[str, str], int]:
            """
            Map string sequence to tuple
            '"start_id", "end_id", "num"'
            --> ((start_id, end_id), num)
            """
            assert type(seq) == str
            
            seq = seq.split(',')
            start, end, num = seq[3][1:-1], seq[5][1:-1], int(seq[7][1:-1])    
            return (start, end), num
        
        def filterTrashData(x:Tuple[Tuple[str, str], int]) -> bool:
            """_summary_
            filters trash data which has  no end or no start id.
            Args:
                x (Tuple[Tuple[str, str], int]): each element of given RDD. it is like ((start_id, end_id), num)
            Returns:
                bool: result of filtering
            """
            assert type(x) == type(x[0]) == tuple
            assert type(x[1]) == int and len(x[0]) == 2
            assert type(x[0][0]) == type(x[0][1]) == str
            
            return x[0][0] != 'X' and x[0][1] != 'X'
        
        def reduceLink(x:int, y:int) -> int:
            """
            sum duplicated data like below
            ((start, end), x), ((start, end), y) --> ((start, end), x+y)
            """
            assert type(x) == type (y) == int
            
            return x+y
        
        def mapToLinkMatrix(link:Tuple[Tuple[str, str], int]) -> Tuple[str, List[Tuple[str, int]]]:
            """
            ( (start, end), num ) --> ( start, (end, num))
            """
            assert type(link) == type(link[0]) == tuple
            assert type(link[0][0]) == type(link[0][1]) == str
            assert type(link[1]) == int
            
            return link[0][0], (link[0][1], link[1])
        
        def normalizeLinkMatrix(x: Tuple[str, Tuple[ Tuple[str, int], int]]) -> Tuple[str, Tuple[str, float]]:
            """_summary_
            This is mapper function.
            from joined A, like (start_id, ((end_id, num_link), sum_of_num_link)),
            to (start_id, (end_id, nl/s_nl))
            Args:
                x (Tuple[str, Tuple[ Tuple[str, int], int]]): _description_
            Returns:
                Tuple[str, Tuple[str, float]]: _description_
            """
            assert type(x) == type(x[1]) == type(x[1][0]) == tuple
            assert type(x[0]) == type(x[1][0][0]) == str
            assert type(x[1][0][1]) == type(x[1][1]) == int, f"values: {x}"
            
            start, end, nl, sum_nl = x[0], x[1][0][0], x[1][0][1], x[1][1]
            normalized = float(nl) / float(sum_nl)
            return start, (end, normalized)
        
        ##
        ## link_info: ((start_id, end_id), num_link)
        ##
        link_info = data_rdd \
            .filter(filterHead) \
            .map(mapToSplitted) \
            .filter(filterTrashData) \
            .reduceByKey(reduceLink)
        
        ## each element: (start_id, (end_id, num_link))
        link_matrix = link_info \
            .map(mapToLinkMatrix)
        
        ## each element: (start_id, sum_of_num_link)
        sum_links = link_matrix \
            .map(lambda x: (x[0], x[1][1])) \
            .reduceByKey(lambda x, y: x+y)
        
        ## each element: (start_id, (end_id, nl/s_nl))
        self.norm_link_matrix:RDD[Tuple[str, Tuple[str, float]]] = link_matrix \
            .join(sum_links) \
            .map(normalizeLinkMatrix)
            
        ## each element: (end_id, (start_id, nl/s_nl))
        self.trans_norm_link_matrix:RDD[Tuple[str, Tuple[str, float]]] = self.norm_link_matrix \
            .map(lambda x: (x[1][0], (x[0], x[1][1])) )
        
    def getLinkMatrix(self) -> RDD[Tuple[str, Tuple[str, float]]]:
        """
        Get link information as matrix.
        each element is like (start_id, (end_id, nl/s_nl))
        - the links are from start_id to end_id
        - nl is number of the links
        - s_nl is total number of outlinks from start_id
        
        Thus nl/s_nl is normalized link weight by sum of links which are from start_id to end id
        
        Returns:
            RDD[Tuple[str, Tuple[str, float]]]: _description_
        """
        return self.norm_link_matrix
    
    def getTransposedLinkMatrix(self) -> RDD[Tuple[str, Tuple[str, float]]]:
        """
        Just transposed version of value from getLinkMatrix method
        The elements are like (end_id, (start_id, nl/s_nl))
        The normalized value nl/s_nl is normalized by number of out links from start_id
        
        Returns:
            RDD[Tuple[str, Tuple[str, float]]]: _description_
        """
        return self.trans_norm_link_matrix