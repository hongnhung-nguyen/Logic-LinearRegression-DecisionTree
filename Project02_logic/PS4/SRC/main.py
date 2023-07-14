
import os

class Literal:
    def __init__(self, string):
        string=string.replace(' ','')
        
        if(string[0]== '-'):
            self.Positive= False
        else:
            self.Positive= True
        self.li=string[-1]
    
    
    def oppositeLiteral(self):
        literal=Literal(self.li)
        if self.Positive == True:
            literal.Positive = False
        else:
            literal.Positive = True 
        literal.li= self.li
        return literal


    def isNegativeOf(self, literal):
        return self.li == literal.li and self.Positive !=literal.Positive

    def __eq__(self, l):
        return self.li == l.li and self.Positive == l.Positive
    def __str__(self): 
        if self.Positive == 0:
            return '-' + self.li
        else:
            return self.li

class Clause:
    def __init__(self, string= "") :
        self.literals=[]
        string=string.replace('\n','')
        if( string != ""):
            list_temp=string.split("OR")
            # print(list_temp)
            # print(string)   
            for i in list_temp:
                self.addToListLiteral(Literal(i))
            # print(list_temp)
            self.literals.sort(key= lambda x: x.li)
            

    def addToListLiteral(self, li):
        self.literals.append(li)

    def reduceLiteralElements(self):
        temp_list=[]
        for i in self.literals:
            if i not in temp_list:
                temp_list.append(i)
        self.literals=temp_list
    
    
    def isTrue(self):
        for i in self.literals:
            for j in self.literals:
                if i.isNegativeOf(j)== True:
                    return True
        return False
    
    def isEqual(self, clause):
        self.literals.sort(key= lambda x: x.li)
        clause.literals.sort( key= lambda x: x.li)
        if(self.literals==clause.literals):
            return True
        else:
            return False
    def __str__(self): 
        if (len(self.literals) > 0):
            s = str(self.literals[0])
            for i in range(1, len(self.literals)):
                s += " OR "
                s += str(self.literals[i])
            return s
        else:
            return "{}"


def reduceClause(clauses):
    temp = set()
    for i in clauses:
        flag=0
        for j in temp:

            if i.isEqual(j):
                flag=1
                break
        if flag==0:
            temp.add(i)

    return temp
 
def addClauseToKB(clauses, KB):
    c=set()
    for i in clauses:
        flag=0
        for j in KB:
            if(i.isEqual(j)== True):
                flag =1 
                break
        if flag == 0:
            c.add(i)
    return c


def PL_RESOLVE(C1, C2):
    clause=Clause()
    count=0
    for i in C1.literals:
        for j in C2.literals:
            if i.isNegativeOf(j):
                count = count  +  1
                key=i

    if(count !=1):
        return False
    else:
        for i in C1.literals:
            if i !=key:
                clause.addToListLiteral(i)
                clause.reduceLiteralElements()
                clause.literals.sort(key= lambda x: x.li)
        for i in C2.literals:
            if i.oppositeLiteral() !=key:
                clause.addToListLiteral(i)
                clause.reduceLiteralElements()
                clause.literals.sort(key= lambda x: x.li)      
    
    if clause.isTrue():
        return False
    return clause   


def PL_RESOLUTION(KB, alpha):
    OUTPUT=""
    for i in range(len(alpha.literals)):
        negative=alpha.literals[i].oppositeLiteral()
        al_cl=Clause()
        al_cl.addToListLiteral(negative)
        KB.append(al_cl)
    
    flag=0
    while (True):
        new=set()
        for Ci in range(len(KB)-1):
            for Cj in range(Ci+1, len(KB)):
                resolvents=PL_RESOLVE(KB[Ci],KB[Cj])
                if resolvents != False:
                    if len(resolvents.literals) == 0:
                        flag =1
                    new.add(resolvents)
        
        new=reduceClause(new)
        new=addClauseToKB(new, KB)

        OUTPUT= OUTPUT + (str(len(new)) +'\n')
        for i in new:
            OUTPUT= OUTPUT+ str(i)+ '\n'

        if flag==1: 
            return OUTPUT, True
        if len(new)==0:
            return OUTPUT, False
        KB= list(set(KB).union(new))


def readFile(path):
    file=open(file=path, mode='r')
    alpha= Clause(file.readline())
    KB=[]
    numOfClause= int(file.readline())
    for i in range(numOfClause):
        KB.append(Clause(file.readline()))
    return alpha, KB

def writeFile(path, output, result):
    file = open(file=path, mode='w')
    file.write(output)
    if (result == True):
        file.write("YES")
    else:
        file.write("NO")


if __name__== '__main__':
    folder_path=".\\INPUT"
    FJoin = os.path.join
    files = [FJoin(folder_path, f) for f in os.listdir(folder_path)]

    for input_file in files:
        alpha, KB = readFile(input_file)

        OUTPUT, result= PL_RESOLUTION(KB, alpha)
        output_name=input_file[13 : -4]
        output_path= ".\\OUTPUT\\output"+ output_name +'.txt'
        writeFile(output_path, OUTPUT, result)