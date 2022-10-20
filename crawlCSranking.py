import pandas as pd
from utils import *
import os
from lxml import etree
choices = "ai&vision&mlmining&nlp&ir&arch&comm&sec&mod&hpc&mobile&metrics&ops&plan&act&crypt&log&graph&chi&robotics&bio&da&bed&visualization&ecom&visualization".split(
    '&')
names = '''
Artificial intelligence
Computer vision
Machine learning & data mining
Natural language processing
The Web & information retrieval     
Computer architecture
Computer networks
Computer security
Databases
Design automation
Embedded & real-time systems  
High-performance computing
Mobile computing
Measurement & perf. analysis 
Operating systems
Programming languages
Software engineering
Algorithms & complexity
Cryptography
Logic & verification
Comp. bio & bioinformatics
Computer graphics
Economics & computation
Human-computer interaction
Robotics
Visualization
'''
if __name__ == '__main__':
    choiceMap = {names.strip().split('\n')[i]: choices[i]
                 for i in range(len(choices))}
    printChoice = '\n'.join([item[0].strip()+'\t\t\t\t'+item[1]
                            for item in choiceMap.items()])
    print('choices are:\n\n ', printChoice)

    for to_year in range(2010, 2023):
        for sub in 'ai&vision&mlmining&inforet&arch&comm&sec&mod&hpc&mobile&metrics&ops&plan&soft&act&crypt&log&graph&chi&robotics&bio&da&bed&visualization&ecom&nlp'.split('&'):
            userChoices = sub
            userChoicesFromYear = str(to_year)
            userChoicesToYear = str(to_year)



            # userChoices = input('input your choices(e.g. nlp&arch&sec): ').lower()
            # userChoicesToYear = input('input your choices(e.g. nlp&arch&sec): ')
            # userChoicesFromYear = input('input your choices(e.g. nlp&arch&sec): ')

            path = userChoices
            if not os.path.exists(path):
                os.mkdir(path)

            base_url = 'https://csrankings.org/#/index?northamerica&'
            trs = crawlPage(userChoices, base_url, userChoicesToYear, userChoicesFromYear)

            Universities = []
            for i in range(0, len(trs), 3):
                uBlock = trs[i:i+3]
                Universities.append([uBlock[0]])

            # get university information
            Universities = pd.DataFrame(Universities)
            Universities.columns = ['school']
            Universities.school = Universities.school.apply(lambda x: getUInfo(x))
            Universities = pd.concat([Universities.school.str.split(
                '@', expand=True)], axis=1)
            Universities.columns = ['rank', 'Uni', 'count', 'n_faculty']
            print(Universities.head())

            # save University information
            Universities.iloc[:, [0, 1, 2, 3]].to_csv(
                os.path.join(path, 'universities_{}_{}_{}.csv'.format(userChoices, userChoicesFromYear, userChoicesToYear)), index=False)
            print('successfully save university infos')
