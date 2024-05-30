from AnalysisFunctions import avg_norm_gain
import OrderAndLabel as OL
import scipy.stats
import xlsxwriter
import pandas as pd

# Responses indicate no effort - drop from data set



percentage_Pre = OL.dfScores_Pre['Total score'].div(sum(OL.Marks_Pre.values()))*100
percentage_Post = OL.dfScores_Post['Total score'].div(sum(OL.Marks_Post.values()))*100


## class separations
# Uncomment as needed for separate classes

C1_Pre = percentage_Pre[percentage_Pre.index.str.contains('ABC_KA')]
# C2_Pre = percentage_Pre[percentage_Pre.index.str.contains('C2')]
# C3_Pre = percentage_Pre[percentage_Pre.index.str.contains('C3')]


C1_Post = percentage_Post[percentage_Post.index.str.contains('ABC_KA')]
# C2_Post = percentage_Post[percentage_Post.index.str.contains('C2')]
# C3_Post = percentage_Post[percentage_Post.index.str.contains('C3')]


#create blank arrays
rows = ['Class', 'C1']#, 'C2', 'C3']
MeanPre = ['Mean Pre']
MeanPost = ['Mean Post']

MedianPre = ['Median Pre']
MedianPost = ['Median Post']

STDPre = ['STD Pre']
STDPost = ['STD Post']


avgNormGain = ['Gain']

#Term 2 2022
MeanPre.append(C1_Pre.mean())
MeanPost.append(C1_Post.mean())

# MeanPre.append(C2_Pre.mean())
# MeanPost.append(C2_Post.mean())
#
# MeanPre.append(C3_Pre.mean())
# MeanPost.append(C3_Post.mean())


STDPre.append(C1_Pre.std())
STDPost.append(C1_Post.std())

# STDPre.append(C2_Pre.std())
# STDPost.append(C2_Post.std())
#
# STDPre.append(C3_Pre.std())
# STDPost.append(C3_Post.std())


MedianPre.append(C1_Pre.median())
MedianPost.append(C1_Post.median())

# MedianPre.append(C2_Pre.median())
# MedianPost.append(C2_Post.median())
#
# MedianPre.append(C3_Pre.median())
# MedianPost.append(C3_Post.median())



for i in range(len(MeanPre)-1):
    avgNormGain.append(avg_norm_gain(MeanPre[i+1], MeanPost[i+1]))

DataArray = [rows, MeanPre, MeanPost, STDPre, STDPost, MedianPre, MedianPost, avgNormGain]

workbook = xlsxwriter.Workbook(r'DataSummaryState.xlsx')
worksheet = workbook.add_worksheet()

row = 0

for col, data in enumerate(DataArray):
    worksheet.write_column(row,col, data)

workbook.close()


C1_Pre2 = C1_Pre.to_frame()
C1_Post2 = C1_Post.to_frame()

# C2_Pre = C2_Pre.to_frame()
# C2_Post = C2_Post.to_frame()
#
# C3_Pre = C3_Pre.to_frame()
# C3_Post = C3_Post.to_frame()


Combined_C1 =pd.concat([C1_Pre2, C1_Post2], axis = 1)

# Combined_C2 =pd.concat([C2_Pre, C2_Post], axis = 1)
# Combined_C3 =pd.concat([C3_Pre, C3_Post], axis = 1)

writer = pd.ExcelWriter(r'Knowledge_Scores_Total_Classes.xlsx', engine = 'xlsxwriter')
Combined_C1.to_excel(writer, sheet_name = 'C1', index = True)
# Combined_C2.to_excel(writer, sheet_name = 'C2', index = True)
# Combined_C3.to_excel(writer, sheet_name = 'C3', index = True)
writer.save()
