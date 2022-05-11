__license__ = 'Junior (c) EPITA'
__docformat__ = 'reStructuredText'
__revision__ = '$Id: huffman.py 2022-04-17'

"""
Huffman homework
2022
@author: Micka-R
"""

from algopy import bintree
from algopy import heap


###############################################################################
# Do not change anything above this line, except your login!
# Do not add any import

###############################################################################
## COMPRESSION

def buildfrequencylist(dataIN):
    """
    Builds a tuple list of the character frequencies in the input.
    """
    dico=[0] * 256
    for symbol in dataIN:
        dico[ord(symbol)] +=1

    frequencyList = []
    for i in range(256):
        if dico[i] > 0:
            frequencyList.append((dico[i], chr(i)))
    return frequencyList

def buildHuffmantree(inputList):
    """
    Processes the frequency list into a Huffman tree according to the algorithm.
    """
    tree=None
    bool = True
    length = len(inputList)
    res = heap.Heap()
    for i in range(length):
        res.push((inputList[i][0],bintree.BinTree(inputList[i][1],None,None)))
    while bool:
        min1 = res.pop()
        if res.isempty():
            bool = False
            tree = min1[1]
        else:
            min2 = res.pop()
            temp = min1[0]+min2[0]
            res.push((temp,bintree.BinTree(None,min1[1],min2[1])))
    return tree
    

def __Correspondence(bin,str,list):
    """
    Build a list with a length of 256 where the value list[i] is the encoded version of the char corresponding to i in the ASCCI extended version.
    """
    if bin.key == None:
        if bin.left != None:
            __Correspondence(bin.left,str+"0",list)
        if bin.right != None:
            __Correspondence(bin.right,str+"1",list)
    else:
        index = ord(bin.key)
        list[index] = str

def encodedata(huffmanTree, dataIN):
    """
    Encodes the input string to its binary string representation.
    """
    str=""
    Board=[0] * 256
    __Correspondence(huffmanTree,"",Board)
    for char in dataIN:
        str += Board[ord(char)]
    return str

def __ChartoBin(char):
    """
    gives the binary value of a char from the ASSCI table
    """
    decimal = ord(char)
    resarray = [0] * 8
    i = 0
    res = ""
    while decimal > 0:
        resarray[i] = decimal % 2
        decimal = int(decimal/2)
        i += 1

    for e in range(7,-1,-1):
        res += str(resarray[e])

    return res
def __BintoChar(bin):
    """
    gives the char corresponding to a bin value in the ASSCI table
    """
    num = bin
    dec_value = 0
    base1 = 1
    len1 = len(num)
    for i in range(len1 - 1, -1, -1):
        if (num[i] == '1'):    
            dec_value += base1
        base1 = base1 * 2
    return chr(dec_value)

def __ParcourPrefix(HT,res):
    """
    Roam the Huffman tree in the prefix order
    """
    if HT.key == None:
        res.append("0")
    else:
        res.append("1" + str(__ChartoBin(HT.key)))
    if HT.left != None:
        __ParcourPrefix(HT.left,res)
    if HT.right != None:
        __ParcourPrefix(HT.right,res)


def encodetree(huffmanTree):
    """
    Encodes a huffman tree to its binary representation using a preOrder traversal:
        * each leaf key is encoded into its binary representation on 8 bits preceded by '1'
        * each time we go left we add a '0' to the result
    """
    res=""
    str = []
    __ParcourPrefix(huffmanTree,str)
    for e in str:
        res += e
    return res


def tobinary(dataIN):
    """
    Compresses a string containing binary code to its real binary value.
    """
    res=""
    align = 0
    temp=""
    count = 0
    for char in dataIN:
        if count == 8:
            count = 0
            res += __BintoChar(temp)
            temp = "" + char
            count += 1
        else:
            count += 1
            temp += char
    if count >0:
        align = 8 - count
        res += __BintoChar(temp)
    return (res,align)

def compress(dataIn):
    """
    The main function that makes the whole compression process.
    """
    freqlist = buildfrequencylist(dataIn)
    huffmanTree = buildHuffmantree(freqlist)
    encodedstr = encodedata(huffmanTree,dataIn)
    encodedtree = encodetree(huffmanTree)
    encodedtreebin = tobinary(encodedtree)
    encodedstrbin = tobinary(encodedstr)
    return (encodedstrbin,encodedtreebin)
    

    
################################################################################
## DECOMPRESSION

def decodedata(huffmanTree, dataIN):
    """
    Decode a string using the corresponding huffman tree into something more readable.
    """
    str=""
    Tree2 = huffmanTree
    for char in dataIN:
        if char == '0':
            Tree2 = Tree2.left
            if Tree2.key != None:
                str += Tree2.key
                Tree2 = huffmanTree
        else:
            Tree2 = Tree2.right
            if Tree2.key != None:
                str += Tree2.key
                Tree2 = huffmanTree
    return str
        
def __slice(str,x,y):
    res = ""
    for i in range(x,y):
        res += str[i]
    return res



def __decodetreeaux(dataIN,index,node):
    if dataIN[index] == '0':
        left,newindex = __decodetreeaux(dataIN,index+1,node)
        node = bintree.BinTree(None,left,__decodetreeaux(dataIN,newindex+1,node))

        return (node,index) 
    else:
        bin = __slice(dataIN,index+1,index+9)
        char = __BintoChar(bin)
        node = bintree.BinTree(char,None,None)
        return(node,index+8)
        
def __decodetree(dataIN, index):
    if dataIN[index] == '0':
        newindex,left =__decodetree(dataIN,index+1)
        newindex,right = __decodetree(dataIN,newindex) 
        tree = bintree.BinTree(None,left,right)
        return newindex,tree
    else:
        bin = __slice(dataIN,index+1,index+9)
        char = __BintoChar(bin)
        tree = bintree.BinTree(char,None,None)
        return index+9,tree
    

def decodetree(dataIN):
    """
    Decodes a huffman tree from its binary representation:
        * a '0' means we add a new internal node and go to its left node
        * a '1' means the next 8 values are the encoded character of the current leaf         
    """
    tree = __decodetree(dataIN,0)[1]
    return tree
    

def frombinary(dataIN, align):
    """
    Retrieve a string containing binary code from its real binary value (inverse of :func:`toBinary`).
    """
    l = len(dataIN)
    c = 0
    str = ""
    while c < l-1:
        str += __ChartoBin(dataIN[c])
        c+=1
    last = __ChartoBin(dataIN[l-1])
    str += __slice(last,align,len(last))
    return str


def decompress(data, dataAlign, tree, treeAlign):
    """
    The whole decompression process.
    """
    ToDecodeData = frombinary(data,dataAlign)
    toDecodeTree = frombinary(tree,treeAlign)
    HuffmanTree = decodetree(toDecodeTree)
    DecodedData = decodedata(HuffmanTree,ToDecodeData)
    return DecodedData
