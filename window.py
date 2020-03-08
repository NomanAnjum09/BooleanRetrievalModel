# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainPage.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from nltk.stem.porter import *
err=0
stemmer = PorterStemmer()
Ltoken = []
Lposting = []
Lposition = []
dictionary = []
position = []
answer = ''
class Ui_MainWindow(object):
 
#######################################################################################
    #Whole Query And Document Processing Is Done Here

######################################################################################

    #Takes Sorted Token and Position and Merge them    Complexity=O(n)
    def mergelists(self,x1,y1,x2,y2,ind,posting_list): 
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

###################################################################




    ######################mergesort###################################
        #To Sort Tokens And Postions Accordingly Of Every Document
        # Blocked Based Indexing Approach for each Document 

    def merge(self,arr,pos, l, m, r): 
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
  
    def mergeSort(self,arr,pos,l,r): 
        if l < r: 
            m = int((l+(r-1))/2)
            self.mergeSort(arr,pos, l, m) 
            self.mergeSort(arr,pos, m+1, r) 
            self.merge(arr,pos, l, m, r) 

###############################################################

#############Tokenizer######################################### 
    def tokenizer(self):
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
                
                    if((content[j] in [' ','.','\n',']']) and w!='' and w!="'"): #splitting token
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
            self.mergeSort(Ltoken,Lposition,0,len(Ltoken)-1) #Merge Sort Tokens Collecting From Each Document
            #block based rather than whole dcitionary               Complexity-> O(nlogn)
        
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

#######################################################################################

############## Soted Document Are Opened and Merged Via MergeList defined Above#########

#sort_i.txt are opened and final Collection Saved to sort.txt
    def Processor(self):

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
            x1,y1,posting_list=self.mergelists(x1,y1,x2,y2,i,posting_list)

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

##################################################################


######## NOT , AND ,OR Processor##### Processes Two Lists Via mERGE Funtion#####
#            Complexity -> O(n)

    def NOT_Process(self,list1):
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

    def OR_Processor(self,list1,list2):
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



    def AND_Processor(self,list1,list2):
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


###################################################################################



#Proximity Query Procssor

    def ProcessProximityQuery(self,parsed):
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
        try:   # Get Doument No and Its Posting for the two Inputted Words
            posting1 = Posting[lexicon.index(word1)-1].split('<')
        except:
            return str(parsed[0])+" Not Found In Dictionary"
        try:
            posting2 = Posting[lexicon.index(word2)-1].split('<')
        except:
            return str(parsed[1])+" Not Found In Dictionary"
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
            while posting1[i][k]!='>':    #Get Document No For word1
                num1+=(posting1[i][k])
                k+=1
            k=0
            while posting2[j][k]!='>':  #Get Docu number for word2
                num2+=(posting2[j][k])
                k+=1

            if (int(num1)<int(num2)):   #Checking Docnumber INtersection
                i+=1
            elif int(num1)>int(num2):
                j+=1
        
            else:
                ind = posting1[i].index('>')             #Document NO Matched  Pop Document No and get positions only
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
                while x<l1 and y<l2:            #Checking POsition Satisfaction
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
        return str(result)

########################################################################################################




######################Query With AND OR NOT processor##################################################
    def processSimpleQuery(self,parsed):

        if(parsed.__contains__('(')):       ##Qury Of Type NOT ( obama AND Clinton)
            if(parsed[0]=='NOT'):
                sub =parsed[parsed.index('(')+1:parsed.index(')')]
                return str(self.NOT_Process(processSimpleQuery(sub)))          #Recursively Resolve Part In Bracket
            else:
                ind = parsed.index('(')     #Query Of type    obama AND (hillary AND/OR clionton)
                if(parsed[ind-1]=='AND'):
                    sub1 = parsed[:ind-1]
                    sub2 = parsed[ind+1:parsed.index(')')]
                    return str(self.AND_Processor(self.processSimpleQuery(sub1),self.processSimpleQuery(sub2))) #Recusrosice Handling
                    
                if(parsed[ind-1]=='OR'):
                    sub1 = parsed[:ind-1]
                    sub2 = parsed[ind+1:parsed.index(')')]
                    return str(self.OR_Processor(self.processSimpleQuery(sub1),self.processSimpleQuery(sub2)))
                    





        if(len(parsed)==2 and parsed[0]!='NOT'): #Biword Query Via ProximityProcessor
            parsed.append('/0')
            return self.ProcessProximityQuery(parsed)
            


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
            try:
                word = lexicon.index(stemmer.stem(parsed[0].lower()))-1
                return Posting[word].split(',')
            except:
                return str(parsed[0])+" Not Found In Dictionary"

        global answer
        if(len(parsed)==2 and parsed[0]=='NOT'): #####Query Of Type    NOT hammer
            answer = str(self.NOT_Process(Posting[lexicon.index(stemmer.stem(parsed[1]))-1].split(',')))
            return answer

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
                    return str(parsed[i])+ " Not Found In Dictionary"
                    
        for i in range(len(counter2)-1,-1,-1):
            parsed.pop(counter2[i])
    

        andlist = []

        if ( not (parsed.__contains__('('))):        ####solve Query of type obama OR hillary AND clinton
            for i in range(len(parsed)):
                if(parsed[i]=='AND'):
                    if(len(andlist)==0):
                        andlist = self.AND_Processor(Plist[i].split(','),Plist[i+1].split(','))
                    else:
                        andlist = self.AND_Processor(andlist,Plist[i+1].split(','))
                elif (parsed[i]=='OR'):
                    if(len(andlist)==0):
                        andlist = self.OR_Processor(Plist[i].split(','),Plist[i+1].split(','))
                    else:
                        andlist = self.OR_Processor(andlist,Plist[i+1].split(','))
        
    
        return andlist

########################################################################################################################


# Funtion TO Parse Query based on [space,fullstop or brackets]
    def queryParser(self,query):
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




    #Query and Document Processing Done 
###############################################################




    
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(789, 743)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setSizeIncrement(QtCore.QSize(7, 7))
        self.label1 = QtWidgets.QLabel(self.centralwidget)
        self.label1.setSizeIncrement(QtCore.QSize(7, 7))
        font = QtGui.QFont()
        font.setFamily("MathJax_Fraktur")
        font.setBold(True)
        font.setPointSize(48)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label1.setFont(font)
        self.label1.setObjectName("label1")
        self.gridLayout_3.addWidget(self.label, 0, 0, 1, 1)
        self.gridLayout_3.addWidget(self.label1, 1.5, 0, 1, 1)
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setMaximumSize(QtCore.QSize(1255, 16777215))
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout_3.addWidget(self.lineEdit, 7, 0, 1, 2)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setMinimumSize(QtCore.QSize(0, 47))
        font = QtGui.QFont()
        font.setFamily("Quicksand Medium")
        font.setPointSize(28)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.gridLayout_3.addWidget(self.label_2, 5, 0, 1, 1, QtCore.Qt.AlignHCenter)
        self.radioButton = QtWidgets.QRadioButton(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.radioButton.setFont(font)
        self.radioButton.setTabletTracking(True)
        self.radioButton.setObjectName("radioButton")
        self.gridLayout_3.addWidget(self.radioButton, 3, 0, 1, 1)
        self.radioButton_2 = QtWidgets.QRadioButton(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.radioButton_2.setFont(font)
        self.radioButton_2.setTabletTracking(True)
        self.radioButton_2.setObjectName("radioButton_2")
        self.gridLayout_3.addWidget(self.radioButton_2, 2, 0, 1, 1)
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setObjectName("textBrowser")
        self.gridLayout_3.addWidget(self.textBrowser, 10, 0, 1, 2)
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Quicksand Medium")
        font.setPointSize(24)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.gridLayout_3.addWidget(self.label_3, 9, 0, 1, 1)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.Entertain)
        self.gridLayout_3.addWidget(self.pushButton, 8, 0, 1, 1, QtCore.Qt.AlignHCenter)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 789, 25))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Boolean Retrieval Model"))
        self.label.setStyleSheet("QLabel { background-color : #42cee5; color : #c41b6a; }")
        self.label_2.setText(_translate("MainWindow", "Enter Query Here"))
        self.radioButton.setText(_translate("MainWindow", "Run from scratch"))
        self.radioButton_2.setText(_translate("MainWindow", "Use Preprocessed Data"))
        self.label_3.setText(_translate("MainWindow", "Results : <img src=\"./emoji.png\">"))
        self.pushButton.setText(_translate("MainWindow", "Search Document"))
        self.label_2.setStyleSheet("QLabel { color: #c41b6a;}")
        self.label1.setText(_translate("MainWindow", "<img src=\"./Donald.png\">"))


    def Entertain(self):
        if self.radioButton_2.isChecked():
            text = self.lineEdit.text()
            Qtype,parsedQuery = self.queryParser(text)
            if(Qtype==1):
                self.textBrowser.setText(str(self.processSimpleQuery(parsedQuery)))
            else:
                self.textBrowser.setText(str(self.ProcessProximityQuery(parsedQuery)))
            
        else:
            self.textBrowser.setText("Please Wait While Processing")
            self.tokenizer()
            self.Processor()
            text = self.lineEdit.text()
            Qtype,parsedQuery = self.queryParser(text)
            if(Qtype==1):
                self.textBrowser.setText(str(self.processSimpleQuery(parsedQuery)))
            else:
                self.textBrowser.setText(str(self.ProcessProximityQuery(parsedQuery)))



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

