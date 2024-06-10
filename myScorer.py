MAX = 2500
ALPHA = 3.1
MU = 2
BETA = 2
SIGMA = 0.4
from tfNormalization import ritf, lrtf
from distributions import G

import lucene
import numpy as np
import math
import sys
from java.io import File

from org.apache.lucene.store import FSDirectory
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.search import BooleanQuery
from org.apache.lucene.search import BooleanClause
from org.apache.lucene.search.similarities import BooleanSimilarity
from org.apache.lucene.index import Term
from org.apache.lucene.search import TermQuery
from org.apache.lucene.util import BytesRef


lucene.initVM()
analyzer = StandardAnalyzer()
index_path = File("index_file/").toPath()
index_directory = FSDirectory.open(index_path)
index_reader = DirectoryReader.open(index_directory)
index_searcher = IndexSearcher(index_reader)

index_searcher.setSimilarity(BooleanSimilarity())
storedFields = index_searcher.storedFields()
termVecReader = index_reader.termVectors()




def docidTodocno(docid):        # Fetch the docno to write the rank of that perticular doc
    return storedFields.document(docid).get("DOCNO")


# directory = SimpleFSDirectory(Paths.get(index_path))
# index_reader = DirectoryReader.open(directory)
# with open("numDoc","r") as f:
#     numDoc = int(f.readline())

# def idf(term, field):
#     # Create a term instance
#     term = Term(field, term)
    
#     # Get the document frequency (number of documents containing the term)
#     doc_freq = index_reader.docFreq(term)
    
#     # Calculate IDF using the formula
#     idf = math.log((numDoc + 1) / (doc_freq + 1)) + 1
#     return idf

class Max_dist_score():
    def __init__(self, query, field):
        self.raw_query = query
        self.field = field
        self.numDoc = 523828  # Number of documents counted while making the intexer
        self.query = self.parse_query()
        #self.directory = FSDirectory(Paths.get(index_path))
        self.collection = index_searcher.collectionStatistics(field)
        self.adl = self.afl(self.collection)
        


    def parse_query(self):    # Returns parsed query with all terms seperated by space
        query = QueryParser(self.field, analyzer).parse(self.raw_query).toString(self.field)
        return query
    
    def idf(self, term):
    # Create a term instance
        term = Term(self.field, term)
        
        # Get the document frequency (number of documents containing the term)
        doc_freq = self.index_reader.docFreq(term)
        
        # Calculate IDF using the formula
        idf = math.log((self.numDoc + 1) / (doc_freq + 1)) + 1 # Here +1 is added to avoid having 0 in the denominator 
        return idf
    
    def afl(self,coll):         # Average field length
        return coll.sumTotalTermFreq() / coll.docCount()
    

    def rvl_doc_wrt_query(self):   # Gives docs where at least some query terms are present
        bqb = BooleanQuery.Builder()
        for term in self.query.split():
            bqb.add(TermQuery(Term(self.field, term)), BooleanClause.Occur.SHOULD)
        boolq = bqb.build()
        hits = index_searcher.search(boolq,MAX).scoreDocs
        docFreq = index_searcher.count(boolq)
        return hits, docFreq
    
    def mvd_score(self, docid):
        termVec = termVecReader.get(docid, self.field)
        termEnum = termVec.iterator()
        dl = termVec.getSumTotalTermFreq()
        c_terms = termVec.size() # Total number of terms in the doc
        mtf = dl / c_terms  # mean term freq
        adl = self.adl
        score = 0
        _, docFreq = self.rvl_doc_wrt_query()
        for term in self.query.split():
            _, docFreq = self.rvl_doc_wrt_query()
            if termEnum.seekExact(BytesRef(term)):
                tf = termEnum.totalTermFreq()
            else:
                continue
            
            _ritf = ritf(tf,mtf)
            _lrtf = lrtf(tf,adl,dl)
            _idf = np.log((1 + self.numDoc) / (1 + docFreq))
            p = BETA*_idf / (1+ BETA *_idf)
            score += _idf * (SIGMA * G(_ritf,MU, ALPHA, p) + (1-SIGMA) * G(_lrtf,MU, ALPHA, p))
        return score
    
    def scoreDoc(self):   # Gives a list of docs in descending order wrt to the query
        hits, _ = self.rvl_doc_wrt_query()
        scores = []
        for hit in hits:
            print("Working on it ...")
            docid = hit.doc
            score = self.mvd_score(docid)
            scoreDoc = (docid, score)
            scores.append(scoreDoc)
        scores = sorted(scores, key=lambda scoreDoc: scoreDoc[1], reverse=True)
        return scores
















# s = Max_dist_score("Indian, inst","TEXT")
# s.rvl_doc_wrt_query()


