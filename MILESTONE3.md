
# Milestone 3 : CSC510 Project : Team 12

## [WORKSHEET.md](https://github.ncsu.edu/dpdodiya/csc510-project/blob/master/WORKSHEET.md#milestone-3)

## Screen cast: https://drive.google.com/file/d/1-ti5uGYGegD34ebMKQLvYSJBSX2T6KJ9/view?usp=sharing
(YouTube didn't support this resolution well so uploaded to Google Drive)

## Demo: [https://gitanalyze.herokuapp.com/](https://gitanalyze.herokuapp.com/)

## Milestone 3 : Services
In the [Milestone 2](https://github.ncsu.edu/dpdodiya/csc510-project/blob/master/MILESTONE2.md), of the project, we already had a working data pipeline, we didn't use mock data. In this Milestone 3, our approach was to enhance the internal logic to produce as accurate data as possible. 

As we were already working with real data, we worked on following additional tasks:

 - Refine internal analysis algorithm of all use cases
 - Move the use case implementation services from Jupyter Notebook to standalone reusable Python scripts 
 - Create a Flask app and deploying it to [Heroku](https://gitanalyze.herokuapp.com/)
 - Migrate front-end to Flask app
 - Create PostgreSQL instance on Heroku
 - Move local PostgreSQL instance to Heroku
 - Verify integration of Heroku with Tableau Online

Specific to this milestone, the implementation of each use case has been explained below. 


## Services Implementation

### Applicable to all use cases
A common service implementation across all use cases was to move the code base from experimental IPython notebooks to structured and modular [Python code](https://github.ncsu.edu/dpdodiya/csc510-project/blob/master/code_base/git_access/Use_Case.py).  

This code to analyze any given repository is now standalone and can be called by any service. 

Another enhancement across all use cases is elimination of intermediate CSV file. In the earlier version, the data flow diagram was:
![Earlier Data Flow Diagram](DFD.png)

From this flow, the entire step involving CSV files has been removed. In the new approach, the data is returned via Pandas Dataframe to the calling script. This data frame can be directly consumed by the caller without having to deal with any form of intermediate data. 

In addition, the final data output has been normalized for all use cases. This eliminated problem of skewed data due to outliers/missing data points. 

Non important files such as .gitignore, .class are now also skipped during analysis. 

## Use case 1 implementation: Displaying subject matter expert
**Description:** 
User selects a particular file of interest to get list of top contributors. Portal will display the information and analysis of subject matter expert for selected file.

**Implementation:** 
The score of top experts for a given file is calculated by using below formula:

**Score** = ΣLOC * [((t<sub>i</sub> - t<sub>o</sub>)/(t<sub>L</sub>-t<sub>i</sub>))/(t<sub>L</sub> - t<sub>o</sub>)] <br/>
where LOC = Number of lines added by the developer <br/>
      t<sub>i</sub> = Time stamp of current commit <br/>
      t<sub>o</sub> = Time stamp of oldest commit <br/>
      t<sub>L</sub> = Time stamp of lastest commit <br/>

All commits for any given file are analyzed to calculate the score. 

In addition to this, the score was normalized too. The normalization was based on ratio between delta of oldest change and latest change. In simple terms, this would mean that a developer with commits in recent time frame will be given more priority than a developer who has same number of commits but in older time frame. 


## Use case 2 implementation: Displaying possible file dependency
**Description:** 
User selects a particular file of interest to get list of files which are most likely to be modified together.

**Implementation:** 
This use case has relatively simple implementation.

Every commit for a given repository is analyzed to see which files were changed in that particular commit. A map of this change is created. For instance, 

If commit `abcdef` has changed 3 files, 
A.java
B.java
C.java

A map will be created in the form of:

|File1|File 2|NoOfTimesChanged|
|---|---|---|
|  A| B |1|
|  A| C |1|
|  B| A |1|
|  B| C |1|
|  C| A |1|
|  C| B |1|



And commit `abcxyz` has changed 2 files, 
B.java
C.java

Then the map will be updated to:
A map will be created in the form of:

|File1|File 2|NoOfTimesChanged|
|---|---|---|
|  A| B |1|
|  A| C |1|
|  B| A |1|
|  **B**| **C** |**2**|
|  C| A |1|
|  **C**| **B** |**2**|


Now when asked about which file is most likely to be changes together with File B, the data will be:

|FileSource|LikelyToChange|NoOfTimesChanged|
|---|---|---|
|  **B**| **C** |**2**|
|  B| A |1|

This data is further normalized by NoOfTimesChanged/TotalTimeChanged to eliminate outliers and bring consistency. 


## Use case 3 implementation: Displaying possible file dependency
**Description:** 
User selects a particular file of interest to get an idea about how bug prone the files or sees the files which has the highest percentages of bugs in project history.

**Implementation:** 
The implementation for this use case involves iterating over all commits of the repository and checking the commits messages to see if they contain specific keywords. In most open source projects, commit messages follow some format. 

Some examples of keywords which could indicate that a commit was bug fix are:

> bug, fix, issue, error, correct, proper, deprecat, broke, optimize,
> patch, solve, slow, obsolete, vulnerab, debug, perf, memory, minor,
> wart, better, complex, break, investigat, compile, defect, inconsist,
> crash, problem, resol

Based on the keywords, if a commit is determined to be a bug fix, the files involved in that commit are marked as bug-prone files. 

This data is accumulated over all commits to represent the overall bugginess of any given file. 
