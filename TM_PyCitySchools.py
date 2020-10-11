#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Dependencies
import pandas as pd
import numpy as np


# In[2]:


# Create paths to access both data files
schools_path = "Resources/schools_complete.csv"
students_path = "Resources/students_complete.csv"


# In[3]:


# Code to read the data files using pandas
schools_all = pd.read_csv(schools_path)
students_all = pd.read_csv(students_path)


# In[4]:


# code to verify schools data file was read
schools_all


# In[5]:


# code to verify students data file was read
students_all.head()


# In[6]:


# Combine the two dataframes into a single dataset.  
district_merged = pd.merge(students_all, schools_all, how="left", on=["school_name", "school_name"])
district_merged.head()


# In[7]:


# Code to pull column headings from merged data set
district_merged.columns


# In[8]:


# Getting a feel for merged data set, pulling names of high schools within the district
district_merged["school_name"].unique()


# In[9]:


# More 'getting the feel' of the merged data set
district_merged.describe()


# In[10]:


# Code to get average reading score across the district
avg_read = district_merged["reading_score"].mean()
avg_read


# In[11]:


# Code to get average math score across the district
avg_math = district_merged["math_score"].mean()
avg_math


# In[12]:


# code to get total number of students in the district
total_students = district_merged["Student ID"].count()
total_students


# In[13]:


# code to get total number of schools in the district
total_schools = len(district_merged["school_name"].unique())
total_schools


# In[14]:


# code to get the budget for each of the schools within the district
schools_budget = district_merged["budget"].unique()
schools_budget


# In[32]:


# more code to get total budget 
total_budget = schools_budget.sum()

#     ISSUE WITH MAP       - need to ask Daniel or Dr. Arrington why this isn't working
total_budget = total_budget.apply("${:.2f}".format)
total_budget


# In[19]:


studentID_DF = district_merged.set_index("Student ID")
studentID_DF.head()


# In[20]:


# code to get summary reading scores
pass_readDF = district_merged.loc[district_merged["reading_score"]>=70,["student_name","reading_score"]]
pass_readDF.head()


# In[25]:


# code to get summary statistics on math and reading scores

#total_students = studentID_DF["student_name"].count()
#total_students
#avg_math_score = studentID_DF["math_score"].mean()
#avg_math_score
pass_mathDF = district_merged.loc[district_merged["math_score"]>=70,["student_name","math_score"]]
pass_mathDF.head()


# In[26]:


# code to calculate percentage of students who pass math or reading 
over70math = pass_mathDF["math_score"].count()
#over70math
pct_pass_math = ((over70math)/total_students)*100
#pct_pass_math
over70read = pass_readDF["reading_score"].count()
pct_pass_read = ((over70read)/total_students)*100
pct_pass_read


# In[27]:


# code to get percentage of student who pass math and reading
pass_both = district_merged.loc[(district_merged["reading_score"]>=70) & (district_merged["math_score"]>=70),
                                ["student_name","reading_score","math_score"]]
pass_both.head()


# In[28]:


# code to get total number of students who pass both math and reading
over70both = pass_both["student_name"].count()
over70both


# In[29]:


# code to calculate percentage of students who pass both math and reading
pct_pass_both = (over70both/total_students)*100
pct_pass_both


# In[31]:


dist_sum = pd.DataFrame({"Total Schools": [total_schools],
                         "Total Students": total_students,
                         "Total Budget": total_budget.map("${:.2f}".format),
                         "Average Math Score": avg_math,
                         "Average Reading Score": avg_read,
                         "% Passing Math": pct_pass_math,
                         "% Passing Reading": pct_pass_read,
                         "% Overall Passing": pct_pass_both
                        })
dist_sum


# In[ ]:


school_name_DF = district_merged.groupby(['school_name'])
print(school_name_DF)


# In[ ]:


school_name_DF.mean()


# In[ ]:


per_school_budget = district_merged.groupby(["school_name"]).mean()["budget"]
#per_school_budget
per_school_count = district_merged["school_name"].value_counts()
#per_school_count
per_student_budget = per_school_budget/per_school_count
#per_student_budget

per_school_math = district_merged.groupby(["school_name"]).mean()["math_score"]
#per_school_math
per_school_reading = district_merged.groupby(["school_name"]).mean()["reading_score"]
#per_school_reading

pass_math = district_merged[(district_merged["math_score"] >= 70)]
#pass_math
pass_reading = district_merged[(district_merged["reading_score"] >= 70)]
#pass_reading

per_school_pass_math = pass_math.groupby(["school_name"]).count()["student_name"]/per_school_count
per_school_pass_math *= 100
#per_school_pass_math

per_school_pass_reading = pass_reading.groupby(["school_name"]).count()["student_name"]/per_school_count
per_school_pass_reading *= 100
#per_school_pass_reading



overall_passing_rate2 = district_merged[(district_merged["reading_score"] >= 70) & (district_merged["math_score"] >= 70)]
pct_overall_passing2 = overall_passing_rate2.groupby(["school_name"]).count()["student_name"]/per_school_count
pct_overall_passing2 = pct_overall_passing2 * 100

overall_passing_rate2.head()
#overall_passing_rate = (per_school_pass_reading + per_school_pass_math)/2 
#overall_passing_rate


school_type = school_name_DF["type"].unique()
#school_type.unique


# In[ ]:


#school_type.count()
overall_passing_rate2.head()


# In[ ]:


pct_overall_passing2.head()


# In[ ]:


#dist_sum = pd.DataFrame({"Total Schools": [total_schools],

school_sum = pd.DataFrame({"School Type": school_type,
                          
                          "Total Students": per_school_count,
                        "Total School Budget" : per_school_budget,
                         "Per Student Budget" : per_student_budget,
                          "Average Math Score": per_school_math,
                           "Average Reading Score": per_school_reading,
                           "% Passing Math": per_school_pass_math,
                           "% Passing Reading": per_school_pass_reading,
                           "% Overall Passing": pct_overall_passing2
                                               })

school_sum


# In[ ]:


top5_overall_passing = school_sum.sort_values("% Overall Passing",ascending=False)
#pass_math.groupby(["school_name"]).count()["student_name"]/per_school_count_

top5_overall_passing.head()


# In[ ]:


bottom5_overall_passing = school_sum.sort_values("% Overall Passing")

bottom5_overall_passing.head()


# In[ ]:


#per_school_math = district_merged.groupby(["school_name"]).mean()["math_score"]
#per_school_math


ninth_graders = district_merged.loc[district_merged["grade"] == "9th",["school_name","math_score"]]
group_9th = ninth_graders.groupby(["school_name"]).mean()["math_score"]
#ninth_graders.head()
#ninth_graders
#group_9th

tenth_graders = district_merged.loc[district_merged["grade"]== "10th",["school_name","math_score"]]
group_10th = tenth_graders.groupby(["school_name"]).mean()["math_score"]
#tenth_graders
#group_10th

eleventh_graders = district_merged.loc[district_merged["grade"]== "11th",["school_name","math_score"]]
group_11th = eleventh_graders.groupby(["school_name"]).mean()["math_score"]
#eleventh_graders
#group_11th

twelveth_graders = district_merged.loc[district_merged["grade"]== "12th",["school_name","math_score"]]
group_12th = twelveth_graders.groupby(["school_name"]).mean()["math_score"]
#twelveth_graders
#group_12th


# In[ ]:


# code to creat dataframe to display math scores by grade
math_by_grade_sum = pd.DataFrame({"9th": group_9th, "10th": group_10th, "11th": group_11th, "12th": group_12th })
math_by_grade_sum


# In[ ]:


# code to compile reading scores by grade

ninth_readers = district_merged.loc[district_merged["grade"] == "9th",["school_name","reading_score"]]
group_9th_readers = ninth_readers.groupby(["school_name"]).mean()["reading_score"]
#ninth_readers.head()
#ninth_readers
#group_9th_readers

tenth_readers = district_merged.loc[district_merged["grade"]== "10th",["school_name","reading_score"]]
group_10th_readers = tenth_readers.groupby(["school_name"]).mean()["reading_score"]
#tenth_readers
#group_10th_readers

eleventh_readers = district_merged.loc[district_merged["grade"]== "11th",["school_name","reading_score"]]
group_11th_readers = eleventh_readers.groupby(["school_name"]).mean()["reading_score"]
#eleventh_readers
#group_11th_readers

twelveth_readers = district_merged.loc[district_merged["grade"]== "12th",["school_name","reading_score"]]
group_12th_readers = twelveth_readers.groupby(["school_name"]).mean()["reading_score"]
#twelveth_readers
#group_12th_readers


# In[ ]:


reading_by_grade_sum = pd.DataFrame({"9th": group_9th_readers,
                                     "10th": group_10th_readers,
                                     "11th": group_11th_readers,
                                     "12th": group_12th_readers })
reading_by_grade_sum

