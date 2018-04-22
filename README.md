# LogAnalysis
Explores a large news database with over a million rows and uses refined sql queries them to draw business conclusions from the data.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. 

### Installing

Clone the project to a local directory and then follow the following steps.

- Install a virtual machine.

The VM is a Linux server system that runs on top of your own computer. 
You can share files easily between your computer and the VM; and you'll be running a web service inside the VM 
which you'll be able to access from your regular browser.

We're using tools called Vagrant and VirtualBox to install and manage the VM. 

- Install Virtual Box from [here](https://www.virtualbox.org/wiki/Download_Old_Builds_5_1)
- Vagrant is the software that configures the VM and lets you share files between your host computer and the VM's filesystem. 
   Download it from [here](https://www.vagrantup.com/downloads.html) for your OS.
- Download the news database file from [here](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip)
- Now, open your shell terminal, (git bash for windows users) and cd to the project directory.
- Move the database file to this directory.
- We will now boot our virtual box using the following vagrant command.
 
```
$ vagrant up
```

### Navigating the shared directory
- First connect to the server on the virtual machine as follows:
```
$ vagrant ssh
```
- Go to the shared directory on the virtual system cd to the /vagrant directory.

```
$ cd /vagrant

```
### Load and connect to the news database
To load the news database onto the psql server run the following in the terminal (once you are in the /vagrant directory)
```
$ psql -d news -f newsdata.sql
```
To connect to the database simply execute 
```
$ psql news
```
### Creating the views required to execute solution queries.

Some additional views were created on top of the existing relations to help put together the comlex queries 
required to run the application.

Copy paste the following into the psql terminal once you are connected to the news database.

```
create view view1 as (Select substring(path,10,length(path)) as slug,id as logid from log);


create view view2 as (Select authors.id as authorid,view1.logid,Articles.id as Articleid from Authors 
LEFT JOIN Articles on Authors.id=Articles.author LEFT JOIN view1 on Articles.slug=view1.slug);


create view view3 as (Select Articles.author,Articles.title, count(log.path) as views from
Articles LEFT JOIN view2 on Articles.id=view2.articleid LEFT JOIN log on view2.logid=log.id 
group by Articles.title,Articles.author order by views DESC);

create view view4 as (Select to_char(time, 'Mon DD, YYYY') as dayte,status from log);

```

### Execute the application.
- cd into the /vagrant directory.
- simply run the python script LogAnalyzer.py to get the results.

### Description of the project structure.

LogAnalyzer makes use of a python script deployed on a virtual server to extract news related information from the news database deployed
on the psql server.

The news database consists of 3 relations namely:

1. Articles (Details of the Articles including title, author, lead, slug, id and time).
2. Author   (Details about the various authors who write the news including id, name and bio).
3. Log      (Details like path tothe articles, ip addresses of connecting clients, status code displayed, time and id).

- View 1 retrieves the article paths as slugs and the log id from the log relation so that we can connect the articles and log relations.
- View 2 forms a relation that consists of the ids of all the relations.
- View 3 forms a table that contains the author id, number of views per article and the title of that article.
- View 4 retrieves the data column(formats it into Month DD, YYYY format) along with the status codes from the log relation.

- QUERY1: Simply fetched the title and the views from the view1.
- QUERY2: Joins view3 and the Authors table to retrieve author names and the number of views corresponding to their name.
- QUERY3: Uses view4 to retrieve the percentage of requests where the status code was 404 more than 1%.
