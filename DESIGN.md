# Problem Statement
Most software projects, be it open source or enterprise projects, tend to grow in size and become more and more complex with time. Also it is often the case that developers on a project never meet in person or via any meeting platform. GitHub is primary source of communication. In this case, when a developer wants to modify certain files, develop new functionality or fix some bugs, it is a challenge to get started with the codebase. This is especially challenging for new developers or developers not familiar with certain parts of the code. Also different projects can have different coding style and standards, thus making it harder for the developer to understand the code. So, finding what a certain file does, which are important methods in a file and whom to reach out for help is certainly a problem. 

Also, in most software projects, there are dependencies between files. Modification is one file can have unwarranted effects in some other files. With large codebases it is very hard to find out the dependencies. Forgetting to modify those dependent files can result in bugs and regressions. Similarly in Software Projects certain files are more error prone than others, this can be because of their complex nature or other code smells . 


# Solution Description
Our solution to the problems faced in development teams as mentioned above is an analytical portal. The portal allow user to select a GitHub repository from a list, after which it will analyse data for each file of the repository. The analytics data for a single repository file will consist of 3 parts. One to solve the issue of finding the right person to get help on codebase, by listing down most relevant contributors. Second to present list of files that are frequently modified together. Third, it will list out important methods in a file by measuring how frequently they were used elsewhere in the code. 

For the repository file analysis data, links between developers, commits and files need to be created. A number of factors like number of file edits, lines of code change, commit messages, frequency of commits will be leveraged. The analytics portal would collect data of every file and every commit of the repository. With this data we can create a scoring mechanism that can be representative of developer’s experience with the file. By creating a matrix structure using the commits and committed file data, related files can be grouped. This will help developers to find the most suitable person to ask help for and group files which are most likely to be modified together. In addition to analysing the commits data, the portal will also go through every file present in the codebase and rank them by their bugginess by calculating how many times they those files had bugs before and use some scoring mechanism to indicate their bugginess.

  
  

# Use Cases

## Use Case 1 : Displaying subject matter expert

### Pre-conditions

1.  The project selected needs to be hosted in GitHub as a public repo and need to have enough git history to analyze to be useful in scoring mechanism.
    
2.  The project selected needs to be a software development project.
    

### Main Flow

1.  User selects a repository from the available list. [S1]

2.	User selects a particular file of interest to get list of top contributors.[S2]

3.	Portal will display the results for selected file.[S3]    

### Sub Flows

[S1]: The list of available repositories for analysis will be pre-populated.

[S2]: Portal will display the tabs for all the use cases for selected file which will be expandable.

[S3]: After expanding "Subject matter expert" tab, portal will return the possible results from tableau. The tableau graph will show the contribution of every user in the form of blocks where the size of block will represent the contribution of users for selected file.  

[S4]: On hovering over specific block, the contact information will be displayed consisting of the email ID and name of the contributor. 

  

## Use Case : Displaying possible file dependency

### Pre-conditions
1.  The project selected needs to be hosted in GitHub as a public repo and need to have enough git history to analyze to be useful in scoring mechanism.
    
2.  The project selected needs to be a software development project.  
     
### Main Flow

1.  User selects a repository from the available list. [S1]
        
2.  User selects a particular file of interest to get list of files which are most likely to be modified together.[S2]

3.	Portal will display the results for selected file.[S3]   

### Sub Flows

[S1]: The list of available repositories for analysis will be pre-populated.

[S2]: Portal will display the tabs for all the use cases for selected file which will be expandable.

[S3]: After expanding "Possible file dependency" tab, portal will return the possible results from tableau. The tableau graph will show the number of times and percentage of time dependent files are changed. The ring in graph represents each file.

[S4]: On hovering over specific ring, information will be displayed consisting of dependent file name, number of times and percentage of times files were changed together. 

## Use Case : Showing probable bugginess of a files

### Pre-conditions
1.  The project selected needs to be hosted in GitHub as a public repo and need to have enough git history to analyze to be useful in scoring mechanism.
    
2.  The project selected needs to be a software development project.  
      
### Main Flow

1.  User selects a repository from the available list. [S1]
 
2.  User selects a particular file of interest to get an idea about how bug prone the files or sees the files which has the highest percentages of bugs in project history.[S2]

3.	Portal will display the results for selected file.[S3]
    
    
### Sub Flows 
    
[S1]: The list of available repositories for analysis will be pre-populated.

[S2]: Portal will display the tabs for all the use cases for selected file which will be expandable.

[S3]: After expanding "File bugginess" tab, portal will return the possible results from tableau. The tableau list will show the file names and some information of files.

[S4]: On hovering over file information, file name, number and percentage of buggy commits and number of times file is changed will be displayed.


# Architecture Design
This section describes the architectural design for the solution mentioned in the solution description part. To achieve the goal and implement this solution as a dashboard for development teams to use it need to have a front end portal that will allow us to display the mined and analyzed data to the user, database system to store the raw data and analyzed data, a data mining system to download the data and an analyzer system to analyze the mined raw data to get the analytical solutions.

Below is an overall simplified diagram of the Data Flow and Application flow of the whole system -

## The Data Flow Diagram -
![alt text](https://github.ncsu.edu/dpdodiya/csc510-project/blob/master/SE1.jpg)

## The Architectural Diagram of the application - 
![alt text](https://github.ncsu.edu/dpdodiya/csc510-project/blob/master/SE2.jpg)

## Application Control Flow Diagram -
![alt text](https://github.ncsu.edu/dpdodiya/csc510-project/blob/master/New_SE_chart.jpeg)

## Data Components - 

### GitHub Miner:
The first part of the system is to create a GitHub miner. The system will be separated into two parts - 

  1) The first part of the system will be done using python codebase utilizing GitHub APIs and request library for python. In this part we will use several GitHub API calls to download GutHub users, Issues and events for a certain GitHub repo which will under analysis. The GitHub sends the data using json format, we will ingest the json format, keep the relevant information and store that into a pandas DataFrame and convert it to pickle file to be stored into a database.
  
  2) The Second part of the system will use python code and pygit2 library. The system will clone the GitHub repo locally, then use the library methods to analyze the git logs to identify git commits throughout the project history. Then we will use the git commits to get the committed files. The relevant information from commits and committed files will be converted to a pandas DataFrame and then stored as a pickle format.
  
### Mined Data Analyzer:
This part of the system will ingest the raw data downloaded from GitHub APIs and data collected using the local git log analyze. Then using this data we will start by making a connection from issues to commits to committed files. This linking process of issues and commits will be done by analyzing the commit messages and issue events. The linking between commits and committed events can be found from git log directly. We will identify the developers who are responsible for each commit using the login id and link it to the developer name by using the user files downloaded by using the GitHub user API. Along with this we will use NLP to analyze the git commit messages to label them as  buggy or non-buggy. The data that we will get from this analysis  - 

  1) Commit data File
  2) Committed_file data File
  3) User data File


All these files will be linked together. Now using these data we will generate the analytical solutions that will be the input data for the portal.

1) We will group the data by each committed file on user and compute a weighted score on how much they have worked on       those files and how long ago. This will be the input for the first use case to show a developer who will be the most qualified person to answer certain questions. 

2) We will group the data on the committed files with commit to see for each file, what are the other files that were changed and how many times, and store that information using a matrix. This will be input to out second use case to show developers what are others files are generally changed along with a file they are modifying. 

3) We will use the commit data to identify the buggy commits and then link them to the committed files. This will give us an idea about how many time bugs were found in a certain file this data will be used as input to our solution to the 3rd use case, where we show the developers the files that are bug prone.


### Data Storage:
The data will be stored into a mongoDB or similar data storage. The First part of the GitHub miner will collect the data convert it to DataFrame and then store it in a pickle file in local system for further analysis, the system will store the data into mongoDB for future references as well, till the time we collect from the same repo again. The system will also store the results after the GitHub analyzer has analyzed the project and created 3 files mentioned in Mined data analyzer and the final set of results for each of the use cases. All these data will be stored into the database, but the final matrices created by analyzing all the data will be used to feed to the analytical portal. The storage will be updated updated with new data every week.


### Analytical Portal:
The analytical portal will be made using tableau or google analytics, which will ingest the data from the data storage and then show it to the user in a comprehensible way. User will load the portal and then use the initial interface to select a certain repo, in which they are interested in. If the requested repo is present in the database user is taken to the analytical portal page, else users is displayed a notification, saying the data is analyzing and user have to wait a certain amount of time before they can explore the repository.

When user is taken to analytical portal page for a certain repo, they are presented with an interface where they see all the structure of the repository they are trying to get information about. The structure of the repository will be similar to its code directory structure. User can either can search for a certain file, if they don’t know about the files exact location, else they can use the interactive directory structure to select the file. After selecting the file user will be able to see different details about the file, which will include details about the file and implemented solutions for 3 use cases, like -
1) File Name
2) File Size
3) Last Modified
4) A list of developers who are most qualified to clarify details about the file
5) A list of files which have been changed together in past and change frequencies.
6) A Bugginess of the file from previous commit history

User will also be able to see file list sorted by their bugginess.

# Wireframes

## Homepage with Repo List and Option to analyze new repos - 
![alt text](https://github.ncsu.edu/dpdodiya/csc510-project/blob/master/SS2.png)

## Selecting repository or Analyzing New repo will show the analysis page, with details about the use case solutions - 
![alt text](https://github.ncsu.edu/dpdodiya/csc510-project/blob/master/SS1.png)

  
