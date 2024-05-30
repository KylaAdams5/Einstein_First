'''
### Script that imports data, question banks, filters for ethics approvals
### Change file path to match current
'''
import pandas as pd

from AnalysisFunctions import *

##---##---##---##---##---##---
##---##---##---##---##---##---

## Import the data

## Import the question bank
## Pre
file_name = "~/OneDrive - The University of Western Australia/UWA - E-F Research/Yr 3 Atom Frenzy/Paper - Atom and Molecules/Mark_Guides/Pre_test_questions_T22023_Example.xlsx"
Questions_Pre, Marks_Pre, Item_Pre, KeyWord_Pre, KeyWord2_Pre = import_questions(file_name)

# Post
file_name = "~/OneDrive - The University of Western Australia/UWA - E-F Research/Yr 3 Atom Frenzy/Paper - Atom and Molecules/Mark_Guides/Post_test_questions_T22023_Example.xlsx"
Questions_Post, Marks_Post, Item_Post, KeyWord_Post, KeyWord2_Post = import_questions(file_name)


## Import the parent permissions
file_name = "Ethics_forms_template.xlsx"
sheet_name = "Parent Permission"
Video, Photo, Test, Interview, Student_gender = import_approval(file_name,sheet_name)

## Import the student permissions
file_name = "Ethics_forms_template.xlsx"
sheet_name = "Student Permission"

Signed = import_approval(file_name,sheet_name)

##---##---##---##---##---##---##---##---
##---##---##---##---##---##---##---##---

'''
Import the data from the knowledge test excel files
- trials are separated by file Name
- The data is anonymised when imported
- matching codes are the only identifiers
'''
# Number of completed Tests
AllTests = ['Completed']
### T2

## Import the anomised data
file_name_Pre = 'knowledge_pre_raw_data_Example.xlsx'
dfQuestions_Pre, dfScores_Pre = import_raw_data(file_name_Pre,True)
AllTests.append(len(dfScores_Pre))


file_name_Post = "knowledge_post_raw_data_Example.xlsx"
dfQuestions_Post, dfScores_Post = import_raw_data(file_name_Post,True)
AllTests.append(len(dfScores_Post))



##---##---##---##---##---##---##---##---
##---##---##---##---##---##---##---##---

'''
Filter the anon data for those only with test ethics approval
Needs complete data sets from both Pre and Post test to work
'''

# empty array to append test numbers for ethics only
Order = ['Order', 'Pre', 'Post']# 'Pre T3 Gen', 'Post T3 Gen', 'Post T3 Ext', 'Pre T2 2023', 'Post T2 2023', 'Pre T3 Filter', 'Post T3 Filter' ]
Ethics = ['Ethics']

### 2022 ###
# Term 2
dfScores_Pre, dfScores_Post = filter_ethics(Test, dfScores_Pre, dfScores_Post)
dfQuestions_Pre, dfQuestions_Post = filter_ethics(Test, dfQuestions_Pre, dfQuestions_Post)
Ethics.append(len(dfScores_Pre))
Ethics.append(len(dfScores_Post))


##---##---##---##---##---##---##---##---
##---##---##---##---##---##---##---##---

'''
Filter tests for students who completed both the pre and post tests
'''

## Filter the tests so only have students who did both
### 2022 ###

#array of number did both + ethics
Both = ['Both']
# Term 2
dfScores_Pre, dfScores_Post = filter_both_tests(dfScores_Pre, dfScores_Post)
dfQuestions_Pre, dfQuestions_Post = filter_both_tests(dfQuestions_Pre, dfQuestions_Post)
# print('Term 2 all 2022 \n Number of tests with Ethics approval and student did both tests \n', 'Pre:', len(dfScores_Pre_T2), '\n', 'Post:', len(dfScores_Post_T2))
Both.append(len(dfScores_Pre))
Both.append(len(dfScores_Post))

##---##---##---##---##---##---##---##---
##---##---##---##---##---##---##---##---

'''
Print the total scores available

'''

#Blank array for Test scorers
TestScore = ['Max Total']

Total_Pre = sum(Marks_Pre.values())
Total_Post = sum(Marks_Post.values())

TestScore.append(Total_Pre)
TestScore.append(Total_Post)

##---##---##---##---##---##---##---##---
##---##---##---##---##---##---##---##---
