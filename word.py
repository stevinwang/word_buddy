# -*- codinutf-8 -*-
"""
Created on Mon Oct 22 16:58:13 2018

@author: Zhou
"""

import pandas as pd

class parameterError(Exception):pass

class participle:
    def __init__(self,word):
        self.word=word
        self.tempword=word
        self.infos=[]
        self.loc=0

    @classmethod
    def get_data(cls,source='dict.csv',coding='gb18030'):
        cls.parts=pd.read_csv(source,encoding=coding)
        def get_table(source,name):
            location=0
            table=[]
            source=source[name]
            for i in range(26):
                for j in range(len(source)-location-1):
                    if str(source.values[j+location])[0] == chr(ord('a') + i):
                        table.append((chr(ord('a') + i), j+location))
                        location+=j
                        break
            return table
        cls.parts_table=get_table(cls.parts,'词根词缀')

    def __get_index(self,letter):
        for i in range(len(self.parts_table)):
            if self.parts_table[i][0]==letter:
                return i,self.parts_table[i][1]


#choice=0:前缀或者词根,choice=1:后缀
    def __get_part(self,choice):
        if self.tempword=='':
            return 0
        count = 0
        repeat=False
        part_message = ''
        part=''
        first_letter=self.tempword[0]
        table_index,begin_index=self.__get_index(first_letter)
        length=self.parts_table[table_index + 1][1] - begin_index
        for i in range(len(self.tempword)):
            if choice==1:
                part=self.tempword[len(self.tempword)-i-1:]
            else:
                part+=self.tempword[i]
            for j in range(length):
                if part==self.parts['词根词缀'][begin_index+j]:
                    for item in self.infos:
                        if item[0]==part:
                            repeat=True
                            break
                    if repeat==True:
                        repeat=False
                        break
                    count=len(part)
                    part_message='{}:\n   详细：{}\n'.format(part,self.parts['词根词缀'][begin_index+j]+'\n'+self.parts['含义'][begin_index+j]+'\n'+self.parts['示例'][begin_index+j])
                    self.infos.append((part,part_message))
                    return count
        return 0

    def split_withoutSuffix(self):
        count=self.__get_part(0)
        if count==0:
            return
        self.tempword=self.tempword[count:]
        self.split_withoutSuffix()

    def split_suffix(self):
        count=self.__get_part(1)
        if count==0:
            return
        self.tempword=self.tempword[:count]
        self.split_withoutSuffix()

    def show(self):
        print('分出的相关词根词缀为：')
        for message in self.infos:
            print(message[1])

def split(word,source='dict.csv',coding='gb18030'):
    w=participle(word)
    participle.get_data(source,coding)
    temp=-1
    choice=[]
    letters_count=0
    while temp!=len(w.infos):
        temp=len(w.infos)
        w.split_withoutSuffix()
        w.split_suffix()
        for item in w.infos[temp:]:
            letters_count+=len(str(item[0]))
        choice.append((letters_count,w.infos[temp:]))
        letters_count=0
        w.tempword=w.word
    counts=[]
    index=[]
    new_info=[]
    new_counts=[]
    new_index=[]
    for item in choice:
        counts.append(item[0])
    m=max(counts)
    for i in range(len(counts)):
        if counts[i]==m:
            index.append(i)
    if len(index)==1:
        print('分词结果为：')
        for message in choice[index[0]][1]:
            print(message[1])
    elif len(index)>1:
        for i in range(len(index)):
            new_info.append(choice[index[i]][1])
        for item in new_info:
            new_counts.append(len(item))
        m=min(new_counts)
        for i in range(len(new_counts)):
            if new_counts[i]==m:
                new_index.append(i)
        if len(new_index)==1:
            print('分词结果为：')
            for message in new_info[new_index[0]]:
                print(message[1])
        elif len(new_index)>1:
            print('分词有{}种可能：'.format(len(new_index)))
            for i in range(len(new_index)):
                print('第{}种分法：'.format(i+1))
                for message in new_info[new_index[i]]:
                    print(message[1])

def main():
    split('numerous')

if __name__ == '__main__':
    main()
