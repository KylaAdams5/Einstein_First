import numpy as np
import pandas as pd
import xlsxwriter
import ImportScript as IS
from AnalysisFunctions import *

## Array of test items that are not included in any analysis
'''
List of items to exclude if needed:

'''

Exclude = []

## Import new label dictionaries (if needed - labels in AnalysisFunctions)

Pre_New_Index, Post_New_Index,  = Re_label_qns_to_items()

Pre_New_Index_Qns, Post_New_Index_Qns = Re_label_qns_to_items_Qns()

'''
##########
# Pre #
##########
'''

# Relabel the raw data from Qn number to Item number
dfScores_Pre = IS.dfScores_Pre.rename(Pre_New_Index, axis = 1)
dfScores_Pre, Marks_Pre = remove_items(Exclude, dfScores_Pre, IS.Marks_Pre)

dfQuestions_Pre = IS.dfQuestions_Pre.rename(Pre_New_Index_Qns, axis = 1)
dfQuestions_Pre, Marks_Pre = remove_items(Exclude, dfQuestions_Pre, IS.Marks_Pre)

#create data frame with full score amounts
dfScores_Pre_full = dfScores_Pre
#separate out the items with a score higher than 1, order into GP and recalculate the total scores
dfScores_Pre = GP_dataframe(dfScores_Pre, Marks_Pre, False)


#Separate into class groups if needed

C1_Pre_Scores = dfScores_Pre[dfScores_Pre.index.str.contains('ABC_KA')]
# C2_Pre_Scores = dfScores_Pre[dfScores_Pre_T2.index.str.contains('C2')]
# C3_Pre_Scores = dfScores_Pre[dfScores_Pre_T2.index.str.contains('C3')]


C1_Pre_Qns = dfQuestions_Pre[dfQuestions_Pre.index.str.contains('ABC_KA')]
# C2_Pre_Qns = dfQuestions_Pre[dfQuestions_Pre_T2.index.str.contains('C2')]
# C3_Pre_Qns = dfQuestions_Pre[dfQuestions_Pre_T2.index.str.contains('C3')]

'''
###########
# Post #
###########
'''

dfScores_Post = IS.dfScores_Post.rename(Post_New_Index, axis = 1)
dfScores_Post, Marks_Post = remove_items(Exclude, dfScores_Post, IS.Marks_Post)

dfQuestions_Post = IS.dfQuestions_Post.rename(Post_New_Index_Qns, axis = 1)
dfQuestions_Post, Marks_Post = remove_items(Exclude, dfQuestions_Post, IS.Marks_Post)

dfScores_Post_full = dfScores_Post
dfScores_Post = GP_dataframe(dfScores_Post, Marks_Post, False)

C1_Post_Scores = dfScores_Post[dfScores_Post.index.str.contains('ABC_KA')]
# C2_Post_Scores = dfScores_Post[dfScores_Post.index.str.contains('C2')]
# C3_Post_Scores = dfScores_Post[dfScores_Post.index.str.contains('C3')]


C1_Post_Qns = dfQuestions_Post[dfQuestions_Post.index.str.contains('ABC_KA')]
# C2_Post_Qns = dfQuestions_Post[dfQuestions_Post_T2.index.str.contains('C2')]
# C3_Post_Qns = dfQuestions_Post[dfQuestions_Post_T2.index.str.contains('C3')]


#########################

## Create excel of test number data
RevisedScores = ['Revised Total', sum(Marks_Pre.values()), sum(Marks_Post.values())]
array = [IS.Order, IS.AllTests, IS.Ethics, IS.Both, IS.TestScore, RevisedScores]

workbook = xlsxwriter.Workbook(r'Test Numbers Info.xlsx')
worksheet = workbook.add_worksheet()

row = 0

for col, data in enumerate(array):
    worksheet.write_column(row,col, data)

workbook.close()

########################

'''
## Export filtered and sorted scores to read_excel
'''

writer = pd.ExcelWriter(r'Knowledge_Scores_Only_Ethics_both.xlsx', engine='xlsxwriter')
dfScores_Pre.to_excel(writer, sheet_name='Pre', index=True)
dfScores_Post.to_excel(writer, sheet_name='Post', index=True)
writer.save()



##########################
'''
# Export Questions
'''


writer = pd.ExcelWriter(r'Knowledge_Questions_Only_Ethics_both.xlsx', engine='xlsxwriter')
IS.dfQuestions_Pre.to_excel(writer, sheet_name='Pre', index=True)
IS.dfQuestions_Post.to_excel(writer, sheet_name='Post', index=True)
writer.save()
