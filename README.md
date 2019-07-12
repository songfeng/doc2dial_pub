
Doc2Dial
==============
Document-Grounded Dialog Composition Framework is an end-to-end
framework for generating conversational data grounded in the documents via crowdsourcing.

## Prerequisites

* MongoDB: On MacOS, `brew install mongodb-community@4.0`. Please refer to [MongoDB community edition installation instructions](https://docs.mongodb.com/manual/administration/install-community/) for other platforms.
* On MacOS, `homebrew` will automatically start the `mongodb` service. If not, open terminal & run `sudo mongod` from `home` directory.


## Installation
This package requires Python 3.6 or higher. We recommend creating a new virtual environment for this project (using virtualenv or conda). 

Run the following commands:

    pip install -r requirements.txt
    
    
## Get Started

### Prepare database
Please import the COLLNAME.json files to your local mongodb (use name "demodb") with commands such as,

    mongoimport --db demodb --collection COLLNAME --drop --file COLLNAME.json
    

We are in process of acquiring appropriate licences for the data consist of sample documents and crowd-sourced annotations. 
We plan to release it next couple of weeks. We will be releasing code to push that data in to a MongoDB instance as well. 


### Launch	
Run the following commands:

    python3 run.py -d demo -p 8081 

### Explore
1. Go to `http://localhost:8081`
2. Login as an `admin` with `password o replaced with 0` as password
3. Please make sure you select a task to explore before clicking `Start`

## Live Demo
You can visit `https://ibm.biz/doc2dial` to see the Doc2Dial in action. 

There is also a short video on [YouTube](https://youtu.be/Do_wb7rXXO4) demonstrating doc2dial's capabilities.

## Troubleshoots and Contributing
If you have any questions, bug reports, and feature requests, please [open an issue](https://github.com/doc2dial/doc2dial-crowd/issues/new) on Github.

We appreciate any kind of feedback or contribution.  Feel free to proceed with small issues like bug fixes, documentation improvement.  For major contributions and new features, please discuss with the collaborators in corresponding issues.  
