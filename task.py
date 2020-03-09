
def mergelists(x1,y1,x2,y2,ind,posting_list): 
    n1 = len(x1) 
    n2 = len(x2)
    word = []
    posting = []
    Plist = []
    # Merge the temp arrays back into arr[l..r] 
    i = 0     # Initial index of first subarray 
    j = 0     # Initial index of second subarray 
    k = 0     # Initial index of merged subarray 
  


    #word->dictionary, Plist->PostingList, posting-> <DocumentNumber>position of word
    while i < n1-1 and j < n2-1 : 
        if x1[i] < x2[j]: 
            word.append(x1[i])    #Send Word To Dictionary
            if(ind==1):
                y1[i]="<{}>".format(ind-1)+y1[i] #Attach Document Number in <docNo> and positionList if Very First and Secod List are merged
                Plist.append(str(ind-1)+',') 
            posting.append(y1[i])             #Attach Document Number in <docNo> and positionList other than initial list are merged 
            if(ind!=1):
                Plist.append(posting_list[i]) 
            i += 1
        elif x1[i]>x2[j]:                      #Attach Document and Position since Second list's doc is smaller
            word.append(x2[j])
            Plist.append(str(ind)+',')
            y2[j]="<{}>".format(ind)+y2[j]
            posting.append(y2[j]) 
            j += 1
        else:
            word.append(x1[i])                  #Documewnts are same so join <docNo> and both postion Lists
            if(ind==1):
                y1[i]="<{}>".format(ind-1)+y1[i]
                Plist.append(str(ind-1)+','+str(ind)+',')
            posting.append(y1[i]+','+"<{}>".format(ind)+y2[j])
            if(ind>1):
                Plist.append(posting_list[i]+','+str(ind))
            i+=1
            j+=1
  
    # Copy the remaining elements of list1, if there 
    # are any 
    while i < n1-1: 
        word.append(x1[i])
        if(ind==1):
            Plist.append(str(ind-1)+',') 
            y1[i]="<{}>".format(ind-1)+y1[i]
        posting.append(y1[i])
        if(ind>1):
            Plist.append(posting_list[i]+',') 
        i += 1
  
    # Copy the remaining elements of list2, if there 
    # are any 
    while j < n2-1: 
        word.append(x2[j])
        Plist.append(str(ind)+',')
        posting.append("<{}>".format(ind)+y2[j])
        j += 1      
    return word,posting,Plist





from nltk.stem.porter import *
err=0
stemmer = PorterStemmer()
Ltoken = []
Lposting = []
Lposition = []
dictionary = []
position = []



######################mergesort###################################


def merge(arr,pos, l, m, r): 
    n1 = m - l + 1
    n2 = r- m 
  
    L = [0] * (n1) 
    R = [0] * (n2) 
    LP = [0] * (n1) 
    RP = [0] * (n2)
    # Copy data to temp arrays L[] and R[] 
    for i in range(0 , n1): 
        L[i] = arr[l + i] 
        LP[i] = pos[l + i]
    for j in range(0 , n2): 
        R[j] = arr[m + 1 + j] 
        RP[j] = pos[m + 1 + j] 

    # Merge the temp arrays back into arr[l..r] 
    i = 0     # Initial index of first subarray 
    j = 0     # Initial index of second subarray 
    k = l     # Initial index of merged subarray 
  
    while i < n1 and j < n2 : 
        if L[i] <= R[j]: 
            arr[k] = L[i] 
            pos[k] = LP[i]
            i += 1
        else: 
            arr[k] = R[j] 
            pos[k] = RP[j]
            j += 1
        k += 1
  
    while i < n1: 
        arr[k] = L[i] 
        pos[k] = LP[i]
        i += 1
        k += 1
  
    while j < n2: 
        arr[k] = R[j]
        pos[k] = RP[j] 
        j += 1
        k += 1
  
def mergeSort(arr,pos,l,r): 
    if l < r: 
        m = int((l+(r-1))/2)
        mergeSort(arr,pos, l, m) 
        mergeSort(arr,pos, m+1, r) 
        merge(arr,pos, l, m, r) 








def tokenizer():
    global err
    global Ltoken
    stopwords=[]
    s = open('Stopword-List.txt','r')
    stopdoc=s.read()
    w=''
    for i in range(len(stopdoc)):
        if(stopdoc[i]=='\n'):
            if(w!=''):
                stopwords.append(w)
            w=''
        elif stopdoc[i]!=' ':
            w+=stopdoc[i]
    s.close()
    #Tokenize stem fold case and find position of words
    
    for i in range(56):
        f = open('./Trump Speechs/speech_{}.txt'.format(i))
        if f.mode =='r':
            content = f.read()
        
            w = ''
            counter=1
            for j in range(len(content)):
                
                if((content[j] in [' ','.','\n',']']) and w!='' and w!="'"):
                    if(w in stopwords):
                        counter+=1
                    if(w not in stopwords ):#removing stopwords
                        tk = stemmer.stem(w)
                        Ltoken.append(tk)
                        Lposition.append(counter)
                        counter+=1
                    

                    w=''
                
                elif content[j] not in ['',' ','[',',',':','?','(',')','—','"',';',"'"]:
                    if(content[j]>='A' and content[j]<='Z'):#Case folding
                        w=w+chr(ord(content[j])+32)
                    else:
                        w+=content[j]



        #quickSort(Ltoken,Lposition,0,len(Ltoken)-1)
        mergeSort(Ltoken,Lposition,0,len(Ltoken)-1)
        
        ST = open('./sortedToken/sort_{}.txt'.format(i),'w')
        SPo = open('./sortedPosition/sort_{}.txt'.format(i),'w')
        ST.write(Ltoken[0])
        ST.write(',')
        SPo.write(str(Lposition[0]))
        
        for l in range(1,len(Ltoken)):
            if Ltoken[l]!=Ltoken[l-1]:
                ST.write(Ltoken[l])
                ST.write(',')
                SPo.write('|')
                SPo.write(str(Lposition[l]))
            else:
                SPo.write(',')
                SPo.write(str(Lposition[l]))
               
 
        Ltoken.clear()
        Lposting.clear()
        Lposition.clear()
        ST.close()
        SPo.close()

#Document as a BLOCK sorting done



def Processor():

    ST = open('./sortedToken/sort_{}.txt'.format(0),'r')
    txt = ST.read()
    x1=txt.split(',')
    So = open('./sortedPosition/sort_{}.txt'.format(0),'r')
    txt = So.read()
    y1=txt.split('|')
    posting_list=[]

    for i in range(1,56):

        ST = open('./sortedToken/sort_{}.txt'.format(i),'r')
        txt = ST.read()
        x2=txt.split(',')
        So = open('./sortedPosition/sort_{}.txt'.format(i),'r')
        txt = So.read()
        y2=txt.split('|')
        x1,y1,posting_list=mergelists(x1,y1,x2,y2,i,posting_list)

    file = open('./sortedToken/sort.txt','w')
    for i in range(len(x1)):
        file.write(x1[i])
        file.write('\n')
    file.close()
    file = open('./sortedPosition/sort.txt','w')
    for i in range(len(y1)):
        file.write(y1[i])
        file.write('\n')
    file.close()
    file = open('./sortedPosting/sort.txt','w')
    for i in range(len(posting_list)):
        file.write(posting_list[i])
        file.write('\n')
    file.close()


def NOT_Process(list1):
    all = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55]
    n1 = 56
    n2 = len(list1)
    i=0
    j=0
    result = []
    while i<n1 and j<n2:
        if(list1[j]==''):
            j+=1
        if(j==n2):
            break

        if(int(list1[j])==all[i]):
            i+=1
            j+=1
        else:
            result.append(all[i])
            i+=1
    while i<n1:
        result.append(all[i])
        i+=1

    return result

def OR_Processor(list1,list2):
    result = []
    n1 = len(list1)
    n2 = len(list2)
    i=0
    j=0

    while i<n1 and j<n2:
        if(list1[i]==''):
            i+=1
        if(list2[j]==''):
            j+=1
        if(i==n1 or j == n2):
            break
        if(int(list1[i])<int(list2[j])):
            result.append(list1[i])
            i+=1
        elif int(list1[i])>int(list2[j]):
            result.append(list2[j])
            j+=1
        else:
            result.append(list2[j])
            i+=1
            j+=1
    while i<n1:
        result.append(list1[i])
        i+=1
    while j<n2:
        result.append(list2[j])
        j+=1

        
    return result



def AND_Processor(list1,list2):
    n1 = len(list1)
    n2 = len(list2)
    i=0
    j=0
    result=[]
    while i<n1 and j<n2:
        if (list1[i]==''):
            i+=1
            continue
        if(list2[j]==''):
            j+=1
            continue
        if(i==n1 or j == n2):
            break
        if(list1[i]==list2[j]):
            result.append(list1[i])
            i+=1
            j+=1
        elif int(list1[i])<int(list2[j]):
            i+=1
        else:
            j+=1

    return result






#Proximity Query Procssor

def ProcessProximityQuery(parsed):
    #LOading List and dictionary
    diff = int(parsed[len(parsed)-1].replace('/',''))
    file = open('./sortedPosition/sort.txt','r')
    data = file.read()
    Posting = data.split('\n')
    file.close()
    file = open('./sortedToken/sort.txt','r') 
    data = file.read()
    lexicon = data.split('\n')
    file.close()

    #Stemming and casefolding Query
    word1 = stemmer.stem(parsed[0].lower())
    word2 = stemmer.stem(parsed[1].lower())
    try:
        posting1 = Posting[lexicon.index(word1)-1].split('<')
        posting2 = Posting[lexicon.index(word2)-1].split('<')
    except:
        print("Word Not Found In Dictionary")
        exit()
    # for i in range(len(posting1)):
    #     print(posting1[i])

    n1 = len(posting1)-1
    n2 = len(posting2)-1

    i=1
    j=1
    result = []
    
    while i<n1 and j<n2:
        k=0
        num1 = ''
        num2 = ''
        while posting1[i][k]!='>':
            num1+=(posting1[i][k])
            k+=1
        k=0
        while posting2[j][k]!='>':
            num2+=(posting2[j][k])
            k+=1

        if (int(num1)<int(num2)):
            i+=1
        elif int(num1)>int(num2):
            j+=1
        
        else:
            ind = posting1[i].index('>')
            posting1[i] = posting1[i][ind+1:]
            ind = posting2[j].index('>')
            posting2[j] = posting2[j][ind+1:]
            i+=1
            j+=1
            list1 = posting1[i-1].split(',')
            list2 = posting2[j-1].split(',')
            
            l1=len(list1)
            l2=len(list2)
            
            x=0
            y=0
            while x<l1 and y<l2:
                if list1[x]!='' and list2[y]!='':
                    if((int(list1[x])<int(list2[y]) and int(list1[x])-int(list2[y])==-diff-1)):
                        result.append(num1)
                        break
                    elif int(list1[x])<int(list2[y]):
                        x+=1
                    elif int(list1[x])>=int(list2[y]):
                        while(list2[y]!=''and int(list1[x])>=int(list2[y])):
                            y+=1
                        if(y==l2 or list2[y]==''):
                            break
                elif list1[x]=='':
                    x+=1
                else:
                    y+=1
    print(result)




#Query With AND OR NOT processor
def processSimpleQuery(parsed):

    if(parsed.__contains__('(')):
        if(parsed[0]=='NOT'):
            sub =parsed[parsed.index('(')+1:parsed.index(')')]
            print(NOT_Process(processSimpleQuery(sub)))
            exit()
        else:
            ind = parsed.index('(')
            ind2 = parsed.index(')')

            if(ind!=0 and parsed.index(')')==len(parsed)-1):
                sub1 = parsed[:ind-1]
                sub2 = parsed[ind+1:parsed.index(')')]
                if(parsed[ind-1]=='AND'):    
                    print(AND_Processor(processSimpleQuery(sub1),processSimpleQuery(sub2)))
                    exit()
                if(parsed[ind-1]=='OR'):
                    print(OR_Processor(processSimpleQuery(sub1),processSimpleQuery(sub2)))
                    exit()
            elif ind==0 and parsed.index(')')!=len(parsed)-1:
                sub1 = parsed[ind+1:ind2]
                sub2 = parsed[ind2+2:]
                if(parsed[ind2+1]=='AND'):    
                    print(AND_Processor(processSimpleQuery(sub1),processSimpleQuery(sub2)))
                    exit()
                if(parsed[ind2+1]=='OR'):
                    print(OR_Processor(processSimpleQuery(sub1),processSimpleQuery(sub2)))
                    exit()
            else:
                sub1 = parsed[:ind-1]
                sub2 = parsed[ind+1:ind2]
                sub3 = parsed[ind2+2:]

                if(parsed[ind-1]=='AND' and parsed[ind2+1]=='AND'):
                    print(AND_Processor(processSimpleQuery(sub1),AND_Processor(processSimpleQuery(sub2),processSimpleQuery(sub3))))
                if(parsed[ind-1]=='OR' and parsed[ind2+1]=='OR'):
                    print(OR_Processor(processSimpleQuery(sub1),OR_Processor(processSimpleQuery(sub2),processSimpleQuery(sub3))))
                if(parsed[ind-1]=='AND' and parsed[ind2+1]=='OR'):
                    print(AND_Processor(processSimpleQuery(sub1),OR_Processor(processSimpleQuery(sub2),processSimpleQuery(sub3))))
                if(parsed[ind-1]=='OR' and parsed[ind2+1]=='AND'):
                    print(OR_Processor(processSimpleQuery(sub1),AND_Processor(processSimpleQuery(sub2),processSimpleQuery(sub3))))






    if(len(parsed)==2 and parsed[0]!='NOT'):
        parsed.append('/0')
        ProcessProximityQuery(parsed)
        exit()


    file = open('./sortedPosting/sort.txt','r')
    data = file.read()
    Posting = data.split('\n')
    file.close()
    file = open('./sortedToken/sort.txt','r') 
    data = file.read()
    lexicon = data.split('\n')
    file.close()


    #Single Word Query
    if(len(parsed)==1):
        return Posting[lexicon.index(stemmer.stem(parsed[0].lower()))-1].split(',')
        


    if(len(parsed)==2 and parsed[0]=='NOT'):
        print(NOT_Process(Posting[lexicon.index(stemmer.stem(parsed[1]))-1].split(',')))
        exit()

    index = []
    counter1=[]
    counter2=[]
    op = []
    Plist = []
    for i in range(len(parsed)):
        if( parsed[i] not in ['AND','OR','NOT','(',')']):
            counter1.append(i) #Word NUmber to find in dictionary
            try:
                word = stemmer.stem(parsed[i])
                word = word.lower()
                ind = lexicon.index(word) #find word in dictionary
                Plist.append(Posting[ind-1]) #Get Posting Of word
                if (i!=len(parsed)-1):
                    op.append(parsed[i+1])  #get operation on word 
                counter2.append(i)  #Word Matched in dictioinary confirmation
            except:
                print(parsed[i]+ " Not Found In Dictionary")
                exit()
    for i in range(len(counter2)-1,-1,-1):
        parsed.pop(counter2[i])
    

    andlist = []

    if ( not (parsed.__contains__('('))):
        for i in range(len(parsed)):
            if(parsed[i]=='AND'):
                if(len(andlist)==0):
                    andlist = AND_Processor(Plist[i].split(','),Plist[i+1].split(','))
                else:
                    andlist = AND_Processor(andlist,Plist[i+1].split(','))
            elif (parsed[i]=='OR'):
                if(len(andlist)==0):
                    andlist = OR_Processor(Plist[i].split(','),Plist[i+1].split(','))
                else:
                    andlist = OR_Processor(andlist,Plist[i+1].split(','))
        
    
    return andlist

    #Remove query for word not in dictionary
    # for i in range(len(counter2)):
    #     if(i==len(counter2))
    #     if counter1[i]!=counter2[i]:
    #         parsed.pop(counter1[i])
    #         parsed.pop(counter1[i]+1)
    #         i-=1
    





# Funtion TO Parse Query based on [space,fullstop or brackets]
def queryParser(query):
    if(query.__contains__('/')):
        Qtype = 2
    else:
        Qtype = 1
    parsed = []
    word = ''
    for i in range(len(query)):
        if(query[i] in [' '] and word!=''):
            parsed.append(word)
            word = ''
        elif query[i] in ['(',')']:
                if(word!=''):
                    parsed.append(word)
                parsed.append(query[i])
                word = ''
        elif query[i]!=' ':
            word+=query[i]
    if(word!=''):
        parsed.append(word)
        
    return Qtype,parsed


# tokenizer()
# Processor()

query = input("Enter Query : ")
Qtype,parsedQuery = queryParser(query)
print(parsedQuery)
if(Qtype==1):
    print(processSimpleQuery(parsedQuery))
else:
    ProcessProximityQuery(parsedQuery)







        # token = re.findall("[A-Z]{2,}(?![a-z])|[A-Z][a-z]+(?=[A-Z])|[\'\w\-]+",content)