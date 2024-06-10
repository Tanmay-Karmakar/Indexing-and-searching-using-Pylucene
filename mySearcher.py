import xml.etree.ElementTree as ET
import myScorer
import os

try:
    os.remove("rank_file")
except:
    pass

topics = ET.parse('trec678rb/topics/robust.xml').getroot() # Give the appropriate path
rank_file = open("rank_file",'a')
field = "TEXT"
print(f"Retrieving {myScorer.MAX} ranked documents for each query--")

for top in topics:
    query_num = top[0].text  # this is query number
    title = top[1].text  # this will be our query
    mscore = myScorer.Max_dist_score(title, field)

    print(query_num, title)
    rank = 1
    for scoredDoc in mscore.scoreDoc():
        print(f"Ranking docno {myScorer.docidTodocno(scoredDoc[0])}",end="...")
        rank_file.write(f"{query_num}\t-RD-\t{myScorer.docidTodocno(scoredDoc[0])}\t{scoredDoc[1]}\t {rank}\n")
        print("Done...")
        rank += 1

rank_file.close()