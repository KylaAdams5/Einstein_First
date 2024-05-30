import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def import_questions(file_name):

    """
    import the pre-test questions, marks, question type and keywords for marking/analysis

    input
    ----

    file_name: str

    Returns
    ---
    Questions: dict
    Marks: dict

    """
    df = pd.read_excel(file_name)
    df = df.fillna(value = 0)

    Questions = {}
    Marks = {}
    Item = {}
    KeyWord = {}
    KeyWord2 = {}


    for i, number in enumerate(df["Item"]):
        Questions[number] = df["Question"][i]
        Marks[number] = df["Marks"][i]
        Item[number] = df["Item"][i]
        KeyWord[number] = df["KeyWord"][i]
        KeyWord2[number] = df["KeyWord2"]

    return Questions, Marks, Item, KeyWord, KeyWord2



    #---------#

def import_approval(file_name, sheet_name):

    '''
    Import the Ethics approval data. Sheeet name specifies parent or student approvals 'Parent Permission'
    or 'Student Permission'

    input
    ---
    file_name: str
    sheet_name: str

    Returns
    ---
    if sheet name = 'Parent Permission'
    Matching_Code: dict
    Video: dict
    Photo: dict
    Test: dict
    Interview: dict
    Student_gender: dict


    if sheet name = 'Student Permission'


    '''

    df = pd.read_excel(file_name, sheet_name = sheet_name)

    df = df.set_index('Matching_Code')
    df = df.fillna(value = 0)

    if sheet_name == 'Parent Permission':

        Video = {}
        Photo = {}
        Test = {}
        Interview = {}
        Student_gender = {}

        for i, number in enumerate(df.index):
            Video[number] = df['Video'][i]
            Photo[number] = df['Photo'][i]
            Test[number] = df['Tests'][i]
            Interview[number] = df['Interview'][i]
            Student_gender[number] = df['Student_gender'][i]

        return Video, Photo, Test, Interview, Student_gender

    else:
        Signed = {}

        for i, number in enumerate(df["First_Name"]):
            Signed[number] = df['Signed'][i]

        return Signed


    #---------#

def import_raw_data(file_name, questions):

    '''
    Import the raw data from the test scores
    This is the file that has the most up to date grades and answers - any typos are fixed in this document,
    then the others are updated from there.
    Removes the identifying data, leaving only the matching code.
    Removes rows 2 and 3 - the question numbers and the mode.

    input
    ---
    file_name: str

    returns
    ---
    dfQuestions: dataframe of question responses
    dfScores: dataframe of scores
    '''

    df = pd.read_excel(file_name)

    # remove the first two rows (question totals and mode)
    df = df.drop([0,1])

    df = df.set_index('Matching Code')

    #anonomise the data
    df = df.drop(['First Name'], axis = 1)
    df = df.drop(['Last Name'], axis = 1)
    df = df.drop(['Year'], axis = 1)
    df = df.drop(['Class Code'], axis = 1)

    ## Separate data into scores and questions
    if questions == True:
        dfQuestions = df[df.columns[::2]]
        dfScores = df[df.columns[1::2]]
    else:
        dfQuestions = []
        dfScores = df[df.columns[::]]
        print('No')
    #Total score is in the Questions Frame

    return dfQuestions, dfScores

#---------#

def remove_items(ExcludedItems, Test, MarkGuide):

    '''
    Filters the RELABELLED data to remove the chosen items and update the mark guide

    input
    ---
    ExcludedItems: array of strings
    Test: pandas DataFrame
    MarkGuide: dictionary

    Returns:
    Test: dataframe with excluded columns removed
    MarkGuide: dict with excluded items removed
    '''

    Test = Test.filter(Test.columns.difference(ExcludedItems))


    for key in ExcludedItems:
        MarkGuide.pop(int(key), None)

    return Test, MarkGuide

#---------#

def HistPlotMulti(data, marks, alpha):

    '''
    creates simple histogram of the score questions.

    Input
    ---
    data: df question#_Score
    marks: Marks dict

    Returns
    plt binned by question
    '''
    right_bin_edge = marks + 1; # right edge is one greater than the total marks
    no_bins = round(marks*0.5) # plus 2 to include zero and edge of last bin
    bin_edges = np.linspace(0,right_bin_edge,no_bins).astype(int)
    plt.hist(data, bins = bin_edges, align = 'left', alpha = alpha) #bin_edges
    plt.ylabel('Frequency')
    if marks < 5:
        plt.xticks(bin_edges[0:no_bins-1]) # minus one to remove display of extra bin - product of hist type with 3 date sets
    else:
        plt.xlim([0, marks])

#--------#

def calc_proportions(df, no_CIs, mark_dict):
    '''
    Returns a data frame of the clas proportions - scalled where appropriate using the mark disctionary

    Input
    ---

    df: DataFrame full dataframe of scores, including the total score
    no_CIs: int the number of Class intervals required
    mark_dict: dict dictionary containg the question numbers and the total marks per question

    Returns:
    CI_Proportion: date frame
    '''
    df = df.drop(['Total score'], axis = 1)
    no_CIs = 3
    CI_start = 0
    CILength = round(len(df)/no_CIs)
    CIIndex = CILength-1
    CI_Total = np.zeros((no_CIs,len(df.columns)))


    for j in range(no_CIs):
        CI_Total[j,:] = df.iloc[CI_start:CIIndex, 0:len(df.columns)].sum()

        CI_start  = CIIndex+1
        CIIndex = CIIndex+CILength

    CI_Total = pd.DataFrame(CI_Total, columns = df.columns[0:len(df.columns)], index = None)
    #CI_Pre_Total

    CI_Proportion = CI_Total

    for each in df.columns:

        question = str(each)
        CI_Proportion[question] = CI_Total[question]/(CILength)

    return CI_Proportion

#----------#

def filter_ethics(dictionary, dfPre, dfPost):

    '''
    Uses the dictionary containing approvals from the parent permission form to filter the pre and post tests

    input
    ---
    dictionary: dict
    dfPre: the anon pre test data
    dfPst: the anon post test data

    returns
    ---
    dfPre: the anon pre test data with ethics approval
    dfPost: the anon post test data with the ethics approval
    '''


    # Use the Test approvals to filter anon data

    Approvaldict = dict([(key, value) for key, value in dictionary.items() if value == 'Y'])
    dfPre = dfPre[dfPre.index.isin(Approvaldict.keys()) == True]
    dfPost = dfPost[dfPost.index.isin(Approvaldict.keys()) == True]

    return dfPre, dfPost

    #----------#

def filter_both_tests(dfPre, dfPost):
    '''
    takes the matching codes from both tests, creates new dataframe that contains those who only did one test
    returns the data from pre and post test that only contains those who did both

    input
    ---

    dfPre: the pre test data frame with the ethics approvals
    dfPost: the post test data frame with ethics approvals

    returns
    ---
    dfPre: the pre test data that contains only those who did both tests
    dfPost: the post test data that contains only those who did both tests
    '''
    # If matching codes are the same will have in both,
    # no sanity check yet

    dfPre_both = dfPre[dfPre.index.isin(dfPost.index) == True]
    dfPost_both = dfPost[dfPost.index.isin(dfPre.index) == True]

    return dfPre_both, dfPost_both

    #----------#

def fraction_of_scores(data, Marks):

    '''
    takes the data frame and mark dictionary and calculates the percentage of marks for each kind.

    Returns
    ---
    fraction_full: Pandas Series of the percentage fraction of full marks (adjusted for max 2 marks)
    fraction_partial: Pandas Series of the percentage fraction of partial marks - will be zero if question is only worth 1 mark
    fraction_zeros: Pandas Series of the percentage fraction of zero marks per question
    '''
    df_of_Threes = data[data == 3]
    df_of_Twos= data[data == 2]
    df_of_Ones = data[data == 1]
    df_of_Zeros = data[data == 0]

    Number_three_Marks = df_of_Threes.count()
    Number_two_Marks = df_of_Twos.count()
    Number_single_Marks = df_of_Ones.count()
    Number_zero_Marks = df_of_Zeros.count()

    Number_full_marks = pd.Series(index = data.columns, dtype = int)
    Number_two_partial_marks = pd.Series(index = data.columns, dtype = int)
    Number_partial_marks = pd.Series(index = data.columns, dtype = int)

    for key, value in Marks.items():

        if value == 2:
            question = str(key)
            Number_full_marks[question] = Number_two_Marks[question]
            Number_partial_marks[question] = Number_single_Marks[question]

        if value == 1:
            question = str(key)
            Number_full_marks[question] = Number_single_Marks[question]
            Number_partial_marks[question] = 0

        if value == 3:
            question = str(key)
            Number_full_marks[question] = Number_three_Marks[question]
            Number_two_partial_marks[question] = Number_two_Marks[question]
            Number_partial_marks[question] = Number_single_Marks[question]

        if value > 3:
            error = 'FUNCTION CANNOT DO MARKS >3 YET'
            print(error)
            break

    fraction_full = (Number_full_marks/len(data)*100)
    fraction_two_partial = (Number_two_partial_marks/len(data)*100)
    fraction_partial = (Number_partial_marks/len(data)*100)
    fraction_zeros = (Number_zero_Marks/len(data)*100)


    return fraction_full, fraction_two_partial, fraction_partial, fraction_zeros, Number_full_marks


#----------#


def GP_dataframe(Test, MarkGuide, Qn_ordering_bool):
    '''
    # take those questions from the test that have 2 marks
    # separates the scores of students who got two marks into two different columns
    # rename to Qn_Score, Qn_2_Score
    # does not use key words to determine the columns.

    ---
    Returns
    dfScores_GP: dataframe with additional columns sepatating the 2 points
    x_labels: array labels for GP plot

    '''
    dfScores_GP = Test.copy()

    for key, value in MarkGuide.items():

            if value == 3:

                df_of_Marks = Test[str(key)][Test[str(key)] == value]

                # Use those Matching codes to make new array of ones to replace the two's
                df_separated_three_scores = pd.DataFrame(np.ones(shape = (len(df_of_Marks))), index = df_of_Marks.index, columns = [str(key)])
                df_separated_two_scores = pd.DataFrame(np.ones(shape = (len(df_of_Marks))), index = df_of_Marks.index, columns = [str(key)])

                # replace the twos with ones
                dfScores_GP.update(df_separated_three_scores)
                dfScores_GP.update(df_separated_two_scores)


                #make a new dataframe of zeros the length of the Test data
                df_separated_three_scores_3 = pd.DataFrame(np.zeros(shape = len(Test)), index = Test.index, columns = [str(key)+'_3'])
                df_separated_three_scores = df_separated_three_scores.rename(columns ={str(key):str(key)+'_3'})#, inplace = True)

                df_separated_two_scores_2 = pd.DataFrame(np.zeros(shape = len(Test)), index = Test.index, columns = [str(key)+'_2'])
                df_separated_two_scores = df_separated_two_scores.rename(columns ={str(key):str(key)+'_2'})#, inplace = True)

                # update the matching codes for those who got two marks to have 1 instead of zero (now two columns for questions worth two marks)
                df_separated_three_scores_3.update(df_separated_three_scores)
                df_separated_two_scores_2.update(df_separated_two_scores)
#
                #update the GP dataframe with new column for students who got two marks
                dfScores_GP[str(key)+'_3'] = df_separated_three_scores_3
                dfScores_GP[str(key)+'_2'] = df_separated_two_scores_2

                dfScores_GP.loc[dfScores_GP[str(key)]== 2, [str(key)+'_2']] = 1
                dfScores_GP.loc[dfScores_GP[str(key)]== 2, [str(key)]] = 1
            if value == 2:
                # Make new data frame that contains the Matching code of those who got full marks
                df_of_Marks = Test[str(key)][Test[str(key)] == value]

                # Use those Matching codes to make new array of ones to replace the two's
                df_separated_two_scores = pd.DataFrame(np.ones(shape = (len(df_of_Marks))), index = df_of_Marks.index, columns = [str(key)])

                # replace the twos with ones
                dfScores_GP.update(df_separated_two_scores)

                #make a new dataframe of zeros the length of the Test data
                df_separated_two_scores_2 = pd.DataFrame(np.zeros(shape = len(Test)), index = Test.index, columns = [str(key)+'_2'])
                df_separated_two_scores = df_separated_two_scores.rename(columns ={str(key):str(key)+'_2'})#, inplace = True)

                # update the matching codes for those who got two marks to have 1 instead of zero (now two columns for questions worth two marks)
                df_separated_two_scores_2.update(df_separated_two_scores)

                #update the GP dataframe with new column for students who got two marks
                dfScores_GP[str(key)+'_2'] = df_separated_two_scores_2


    dfScores_GP['Total score'] =  dfScores_GP[list(dfScores_GP.columns)].sum(axis=1)
    if Qn_ordering_bool == True:
        dfScores_GP.loc['Total Qn'] = dfScores_GP.sum(numeric_only=True)

    dfScores_GP = dfScores_GP.sort_values('Total score')
    if Qn_ordering_bool == True:
        dfScores_GP = dfScores_GP.sort_values('Total Qn', axis = 1, ascending = False)
        dfScores_GP = dfScores_GP.drop(['Total Qn'], axis = 0)
        dfScores_GP = dfScores_GP.drop(['Total score'], axis = 1)

    return dfScores_GP

def item_diffifulty_single_test(data, Marks, switch):
    data2 = data.copy()
    Total_attempt = len(data2)
    if 'Total score' in data2.columns:
        data2 = data2.drop(['Total score'], axis = 1)
    Number_Correct = data2.sum(axis = 0)


    P = Number_Correct/Total_attempt

    return P


def Item_discrimination(data, Marks, quartile):

    '''
    Calculates the item discrimination index using the 50% (CURRENTLY at the
    25% set up rather than 50%, may not be working, C1 looks strange) of scorers
    Counts partial marks as fully correct

    ---
    returns
    D: array of item discrimination index for single test
    '''
    data2 = data.copy()

    if data2.columns.str.contains('Total score').any() == False:
        data2['Total score'] = data2.sum(axis=1)
        data2 = data2.sort_values('Total score')

    if quartile == 50:
        if len(data2)%2 == 0:
            Low = data2.iloc[0:round(len(data2)/2)]
            High = data2.iloc[round(len(data2)/2):len(data2)]
        else:
            Low = data2.iloc[0:round(len(data2)/2)]
            High = data2.iloc[round(len(data2)/2)-1:len(data2)]

    if quartile == 25:
        Low = data2.iloc[0:round(len(data2)/4)]
        High = data2.iloc[(len(data2)-round(len(data2)/4)):len(data2)]

    Divide = len(Low)
    Number_correct_low = Low.sum(axis=0)#np.zeros(len(Number_incorrect_low))
    Number_correct_high = High.sum(axis=0)#np.zeros(len(Number_incorrect_high))

    D = (Number_correct_high - Number_correct_low)/ Divide#2)

    D.drop(['Total score'], axis = 0, inplace = True)

    return D

def PointBiserial(data, Marks, Difficulty):
    '''
    Calculates the Point biserial coefficient for each data sets
    uses the separated column for full marks (e.g. if item work 3, remove 9, 9_2 and use 9_3 renamed as 9)
    Total calcualted from the total with data from columns that are dropped
    '''
    CorrectMean = []
    data2 = data.copy()

    for each in data2.columns:
            TotalCorrect = data2.loc[data2[each] == 1,'Total score']
            if pd.isna(TotalCorrect.mean()) == True:
                CorrectMean.append(0)
            else:
                CorrectMean.append(TotalCorrect.mean()) # array for each item

    Multiplier = np.sqrt(Difficulty/(1-Difficulty))

    MeanTEST = data2['Total score'].mean()
    STDTEST = data2['Total score'].std()

    CorrectMeanSer = pd.Series(data = CorrectMean, index = data2.columns)
    CorrectMeanSer.drop('Total score', inplace=True)

    CorrectMeanSerSort = sort(CorrectMeanSer)

    PBS = ((CorrectMeanSerSort-MeanTEST)/STDTEST)*Multiplier

    return PBS


def KR_20(data, marks):
    '''
    Calculates the Kuder-Richardson reliability formula 20
    For items witha  variance in responses (not binary answers)

    Not very useful for tests with multiple 2+ point questions
    Return: KR_21: int
    '''

    cols = data.columns[:-1]
    STD = data[cols].sum(axis = 1).std()
    STD_item = data[cols].std()
    K = len(marks.items())
    TO_SUM = STD_item**2
    SUM = TO_SUM.sum()
    First = (K/(K-1))
    Second = (1-(SUM/STD**2))

    KR_20 = First*Second
    return KR_20

def KR_21(data, marks, difficulty):
    '''
    Calculates the Kuder-Richardson reliability formula 21
    Assumes that the two mark questions are fully correct with 2 marks
    uses the diffuculty index and Input

    Not very useful for tests with multiple 2+ point questions
    Return: KR_21: int
    '''

    cols = data.columns[:-1]
    STD = data[cols].sum(axis = 1).std()
    K = len(marks.items())
    TO_SUM = difficulty*(1-difficulty)
    SUM = TO_SUM.sum()
    First = (K/(K-1))
    Second = (1-(SUM/STD**2))

    KR_21 = First*Second
    return KR_21

def ferguson_delta(data, marks):

    data = data.copy()
    for key, value in marks.items():
        if value == 2:
            data.drop(str(key), axis = 1, inplace = True)
        if value ==3:
            data.drop(str(key), axis = 1, inplace = True)
            data.drop(str(key)+'_2', axis = 1, inplace = True)

    N = len(data)
    K = len(marks.items())

    cols = data.columns[:-1]
    New = data[cols].sum(axis = 1)
    f = New.value_counts()
    f_squared = f**2
    f_sum = f_squared.sum()

    delta = (N**2 - f_sum)/(N**2 - (N**2/(K+1)))

    return delta


def avg_norm_gain(mean_pre, mean_post):
    g = (mean_post - mean_pre)/(100-mean_pre)
    return g

def label_wavelengths(row):
    if row['29'] + row['30']+row['31'] + row['32'] ==4:
        return 1
    else:
        return 0

def rename_simplify(data):
    for each in data.index:#P_C5_Post_T2.index:
        if '_1' in each:
            data.drop(str(each), inplace = True)
        if '_2' in each:
            data.drop(str(each), inplace = True)
    return data

def Re_label_qns_to_items():
    '''
    Returns the conversion labels for test items
    Separated by test
    '''

    Pre_New_Index = { 'Q1A_Score': '1',
                    'Q1A_2_Score': '1_2',
                    'Q1B_Score': '2',
                    'Q1C_Score': '3',
                    'Q2_Score': '4',
                    'Q3_Score': '5'}

    Post_New_Index = {'Q1A_Score': '1',
                     'Q1B_Score': '2',
                     'Q1C_Score': '3',
                     'Q2_Score': '4',
                     'Q3_Score': '5'}


    return Pre_New_Index, Post_New_Index

def Re_label_qns_to_items_Qns():
    '''
    Returns the conversion labels for test items
    Separated by test
    '''
    Pre_New_Index_Qns = { 'Q1A': '1',
                        'Q1B': '2',
                        'Q1C': '3',
                        'Q2': '4',
                        'Q3': '5'}

    Post_New_Index_Qns = {'Q1A': '1',
                     'Q1B': '2',
                     'Q1C': '3',
                     'Q2': '4',
                     'Q3': '5'}

    return Pre_New_Index_Qns, Post_New_Index_Qns



def sort(series):
    a = series.index.to_series().astype(int).sort_values()
    PNew = series.reindex(index = a.index)
    return PNew

PublicationLabels = {}

PublicationLabelsA = {}
