# Use getSynset for get translation
import babelquery as bq
import hanzidentifier as hz

def getRelatedWords(text,pos,key):
    # Attempts to get a related translated word
    senses = bq.getSenses(text,"EN","ZH",None,key)
    related = []
    for x in senses:
        s = x["properties"]["synsetID"]
        if s["pos"]==pos:
            a = x["properties"]["simpleLemma"]
            b = x["properties"]["fullLemma"]
            if hz.identify(a)==hz.BOTH or hz.identify(a)==hz.SIMPLIFIED:
                related.append(a)
            if hz.identify(b)==hz.BOTH or hz.identify(b)==hz.SIMPLIFIED:
                related.append(b)
    related = list(dict.fromkeys(related))
    return related

print(getRelatedWords("print","VERB","9c7dbd16-9086-4b7b-82ee-d1393fda04e3")) # Still includes Japanese, non-simplified, fix later



def getRelatedByEdges(rid1,rid2,pos,limit,key):
    # Constantly yeets through edges until it finds something matching and immediately dies.
    if limit is None:
        limit = 2 # Probably self-destructive honestly
    score = 0 # Number of edges it has to go to to find something.
    common = []
    queue1 = [{"layer":0,"ids":[rid1]}]
    queue2 = [{"layer":0,"ids":[rid2]}]
    # Init the Queues
    for x in range (1,limit):
        queue1.append({"layer":x,"ids":[]})
        queue2.append({"layer":x,"ids":[]})
    while score<limit-1: # This is most definitely BAD
        #print(len(queue1[score]["ids"]))
        r1 = [bq.getEdges(x, key) for x in queue1[score]["ids"]]
        r1 = list(dict.fromkeys(r1[0]))
        r2 = [bq.getEdges(x, key) for x in queue2[score]["ids"]]
        r2 = list(dict.fromkeys(r2[0]))
        queue1[score+1]["ids"].extend(r1)
        queue2[score+1]["ids"].extend(r2)
        for x in queue1[score+1]["ids"]:
            for y in queue2[score+1]["ids"]:
                if x==y:
                    common.append(x)
        if len(common)!=0:
            return {"common":common,"score":score}
            break
        score+=1
    return None
        


key = "9c7dbd16-9086-4b7b-82ee-d1393fda04e3"
#r1 = open("1.txt","w",encoding = "utf-8")
#r2 = open("2.txt","w",encoding = "utf-8")
#a = bq.getEdges("bn:00022678n",key)
#for x in a:
#    r1.write(str(x["target"])+"\n")
#b = bq.getEdges("bn:00067717n",key)
#for y in b:
#    r2.write(str(y["target"]+"\n"))
#r1.close()
#r2.close()

#bq.getEdges("bn:00022678n",key)

print(getRelatedByEdges("bn:00022678n","bn:00067717n",None,3,key))



# getSenses: List containing dictionaries
#{'type': 'BabelSense', 'properties': {'fullLemma': '苹果树', 'simpleLemma': '苹果树', 'source': 'OMWN_ZH', 'senseKey': '1', 'frequency': 0, 'language': 'ZH', 'pos': 'NOUN', 'synsetID': {'id': 'bn:00005076n', 'pos': 'NOUN', 'source': 'BABELNET'}, 'translationInfo': '', 
# 'pronunciations': {'audios': [], 'transcriptions': []}, 'bKeySense': False, 'idSense': 36201886}}

# getSynset: Dictionary with keys senses,wnOffsets,glosses,examples,images,synsetType,categories,translations,domains,lnToCompound,lnToOtherForm,FilterLangs,bkeyConcepts
# senses: [{'type': 'BabelSense', 'properties': {'fullLemma': '蘋果移動應用處理器', 'simpleLemma': '蘋果移動應用處理器', 'source': 'WIKIDATA', 'senseKey': 'Q406283', 'frequency': 0, 'language': 'ZH', 'pos': 'NOUN', 'synsetID': {'id': 'bn:14792761n', 'pos': 'NOUN', 'source': 'BABELNET'}, 'translationInfo': '', 'pronunciations': {'audios': [], 'transcriptions': []}, 'bKeySense': False, 'idSense': 274490353}}]
# wnOffsets: []
# glosses: []
# examples: []
# synsetType: CONCEPT
# categories: []
# translations: {}
# domains: {'COMPUTING': 0.40721815824508667}
# lnToCompound: {}
# lnToOtherForm: {}
# filterLangs: ['ZH']
# bkeyConcepts: False

#getSynsetIds: List containing dictionaries
#{'id': 'bn:00289737n', 'pos': 'NOUN', 'source': 'BABELNET'}

#wikiSynset: List containing dictionaries, same format as above
#[{'id': 'bn:00005054n', 'pos': 'NOUN', 'source': 'BABELNET'}]

#wnSynset: Same format.

# Edges: List containing dictionaries
# {'language': 'EN', 'pointer': {'fSymbol': '~wds', 'name': 'Hyponym', 'shortName': 'has-kind', 'relationGroup': 'HYPONYM', 'isAutomatic': False}, 'target': 'bn:00497248n', 'weight': 0.0, 'normalizedWeight': 0.0}