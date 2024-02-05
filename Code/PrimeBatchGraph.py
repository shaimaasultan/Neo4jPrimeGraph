import logging
from logging.handlers import MemoryHandler ,RotatingFileHandler
lg = logging.getLogger("Nodes")
lg.setLevel(logging.INFO)
hnd=logging.FileHandler("PrimeGraph\Graph.cypher","w")
#hnd= RotatingFileHandler("PrimeGraph\Graph.log","w", maxBytes=20000000, backupCount=150)
memory_handler = MemoryHandler(100, flushLevel=logging.INFO, target=hnd, flushOnClose=True)
hnd.setLevel(logging.INFO)
lg.addHandler(hnd)

lgr = logging.getLogger("Relations")
lgr.setLevel(logging.INFO)
hndr=logging.FileHandler("PrimeGraph\GraphRelations.cypher","w")
#hndr = RotatingFileHandler("PrimeGraph\GraphRelations.log","w", maxBytes=200000000, backupCount=150)
memory_handlerr = MemoryHandler(100, flushLevel=logging.INFO, target=hndr, flushOnClose=True)
hndr.setLevel(logging.INFO)
lgr.addHandler(hndr)

lgclass = logging.getLogger("ClassRelations")
lgclass.setLevel(logging.INFO)
hndclass=logging.FileHandler("PrimeGraph\ClassGraphRelations.cypher","w")
memory_handler_class = MemoryHandler(100, flushLevel=logging.INFO, target=hndclass, flushOnClose=True)
hndclass.setLevel(logging.INFO)
lgclass.addHandler(hndclass)

'''  
Branch  = 1 for branch(7) 
Branch  = 5 for branch(11)
'''
def Node (Index , CompositOrder  , Label1 , Label2 = ''   , IsPrime = 0 ,Branch = 1):
        NodeValue = Index * 6 + Branch
        NodeIndex = 'I'+str(NodeValue) 
        ChildNodeIndex =  Index + NodeValue * CompositOrder
        ChildNodeValue = ChildNodeIndex * 6 + Branch
        if CompositOrder == 0 :
            ChildNodeRelationIndex = NodeIndex
        else:
            ChildNodeRelationIndex = NodeIndex + '+'+ str(ChildNodeIndex) 

        ''' merge nodes'''
        NodeProperties =''' ID : {ID} , CompositeIndex : {CompositeIndex} '''.format(
                            ID = str(ChildNodeValue)
                            ,CompositeIndex=str(ChildNodeIndex) )


        NodeVar = "n"+str(NodeValue)+str(ChildNodeValue)+str(ChildNodeIndex)
        create_nodes = ''';MERGE (n:{} {}) 
                            ON MATCH SET n.Factors = replace(toString(n.Factors),toString(";") + toString({}),'') + ';' + toString({})
                                , n :{}
                                , n :{}
                            ON CREATE SET n.Factors = '1 ; ' + {} 
                                , n :{}
                                , n: {} '''.format( Label1 ,'{'+ NodeProperties +'}' 
                                                ,NodeValue 
                                                ,NodeValue
                                                ,NodeIndex
                                                ,"Class"+str(Branch)
                                                ,'toString('+str(NodeValue)+')' if str(NodeValue) == str(ChildNodeValue) else  ' toString('+str(NodeValue)+') + ";" + toString('+str(ChildNodeValue)+')'
                                                ,NodeIndex
                                                ,"Class"+str(Branch))

        ''' log graph relations [FactoredBy]'''
        rel = ''';MATCH (a:{}), (b:{}) WHERE a.ID = {} AND b.ID = {}
        MERGE (a)-[r:FactoredBy {}]->(b) '''.format(Label1,Label1
                                                        ,ChildNodeValue,NodeValue
                                                        ,'{name : "'+ChildNodeRelationIndex+'" , Factor : '+str(NodeValue)+'}'
                                                        )
        
        lg.info(create_nodes)
        lgr.info(rel)

def CreateClassEnterRelation (node1Label , node2label, batch_start_index= 1 , batch_end_index = 40 , Graph_depth = 20 ):
    for i in range(batch_start_index,(batch_start_index + batch_end_index)):
        NodeValue = (i * 6 + 1)
        if NodeValue%5 == 0 : continue
        else:
             ChildNodeValue = NodeValue + 4
             for M in range(batch_start_index,(batch_end_index + batch_end_index)):
                fromNode = ChildNodeValue * NodeValue
                ChildNodeRelationIndex = 'I'+str(fromNode)+'_[C5-C1]_I'+str(NodeValue)
                if  (fromNode) %5 == 0 : continue
                
                ''' log graph relations [FactoredBy] '''
                interel = ''';MATCH (a:{}), (b:{}) WHERE a.ID = {} AND b.ID = {}
                                SET a.Factors = replace(toString(a.Factors),toString(";") + toString({}),'') + toString(";") + toString({})
                                SET a:InterClass:{}
                                SET b:InterClass:{}
                                MERGE (a)-[r:FactoredBy {}]->(b) '''.format(node1Label,node2label
                                                        ,fromNode,NodeValue,NodeValue,NodeValue
                                                        ,'I'+str(NodeValue),'I'+str(fromNode)
                                                        ,'{name : "'+ChildNodeRelationIndex+'" , Factor : '+str(NodeValue)+'}'
                                                        )
                lgclass.info(interel)
                ChildNodeValue = ChildNodeValue + 6


def CreateGraph (batch_start_index= 1 , batch_end_index = 40 , Graph_depth = 20 , batch_branch = 1):
    for i in range(batch_start_index,(batch_start_index +batch_end_index)):
        NodeValue = (i * 6 + batch_branch)
        if NodeValue%5 == 0 : continue
        else:
            '''Parent Nodes'''
            Node(Index = i, CompositOrder = 0 ,Label1 =  'Number' , Branch=batch_branch)
        
        for M in range(batch_start_index,(batch_end_index +batch_end_index)):
            ChildNodeValue = (i + (i * 6 + batch_branch) * M) * 6 + batch_branch
            if  ChildNodeValue %5 == 0 : continue
            '''Child Nodes'''
            Node(Index = i , CompositOrder = M ,Label1 =  'Number' , Branch = batch_branch)


lg.info(';match ()-[r:FactoredBy]->() delete r')
lg.info(';match (n) delete n') 
CreateGraph(batch_start_index= 1 , batch_end_index = 40 , Graph_depth = 10 ,batch_branch = 1)
CreateGraph(batch_start_index= 1 , batch_end_index = 40 , Graph_depth = 10,batch_branch = 5)
CreateGraph(batch_start_index= 1000 , batch_end_index = 40 , Graph_depth = 10 ,batch_branch = 1)
CreateGraph(batch_start_index= 1000 , batch_end_index = 40 , Graph_depth = 10,batch_branch = 5)
#CreateGraph(batch_start_index= 6 , batch_end_index = 10 , Graph_depth = 10 ,batch_branch = 1)
#CreateGraph(batch_start_index= 6 , batch_end_index = 10 , Graph_depth = 10,batch_branch = 5)
CreateClassEnterRelation ('Number' , 'Number', batch_start_index= 1 , batch_end_index = 40 , Graph_depth = 10 )
CreateClassEnterRelation ('Number' , 'Number', batch_start_index= 1000 , batch_end_index = 40 , Graph_depth = 10 )



        
       

        