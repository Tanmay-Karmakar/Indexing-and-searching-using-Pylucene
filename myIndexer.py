"""There are many files and each file contains many documents and each document contains many fields. I am indexing the <text> field."""
"""Every file is HTML type so I'm using BeautifulSoup to parse them."""




# Essential imports:
import os
import pandas as pd
import lucene
from java.io import File
from bs4 import BeautifulSoup

# Indexer imports:
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.analysis.en import EnglishAnalyzer
from org.apache.lucene.index import IndexWriter, IndexWriterConfig
#from org.apache.lucene.store import SimpleFSDirectory, FSDirectory
from org.apache.lucene.store import FSDirectory
import org.apache.lucene.document as document

lucene.initVM()

# Create a new directory in the pwd to store the indeces and set up the index writer
indexPath = File("index_file/").toPath()
indexDir = FSDirectory.open(indexPath)
analyzer = StandardAnalyzer()
writerConfig = IndexWriterConfig(analyzer)
writer = IndexWriter(indexDir, writerConfig)

termvec_store_TextField = document.FieldType(document.TextField.TYPE_STORED)
termvec_store_TextField.setStoreTermVectors(True)


def indoc(text,docno):
    doc = document.Document()
    doc.add(document.Field("DOCNO", docno, document.StringField.TYPE_STORED))
    doc.add(document.Field("TEXT", text, termvec_store_TextField))
    writer.addDocument(doc)


count = 0  # To count the number of documents to index
#print(os.listdir("./trec678rb/documents/"))

for name in os.listdir("./trec678rb/documents/"):  # Give the appropriate path of the document directory
    f = open(f"./trec678rb/documents/{name}","r",encoding="ISO-8859-1") # opens each file in the document directory
    token = BeautifulSoup(f,"html.parser")
    doc = token.find("doc")
    while doc is not None:
        text = doc.findChildren("text")
        docno = doc.findChildren("docno")[0].get_text().strip()
        if text is None:
            doc = doc.findNext("doc")
            continue
        if len(text) == 0:
            doc = doc.findNext("doc")
            continue
        text = text[0].get_text().strip()
        print(f"Indexing {count}... ",end="")
        indoc(text,docno)
        print("Done...")
        doc = doc.findNext('doc')
        count = count + 1
    f.close()

writer.close()

numDoc = count

# Now store the total number of documents in a file 'numDoc'
with open("numDoc","w") as f:
    f.write(str(numDoc))




