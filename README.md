# Deletion Queue App
Author: Kevin Stine
Created: Dec. 7, 2022

## Resources used in this project:
* [Alvin Lee's Medium article on setting up Kafka on K8s](https://levelup.gitconnected.com/how-to-deploy-apache-kafka-with-kubernetes-9bd5caf7694f)
* [Wojciech Pratkowiecki's simple Kafka setup based on Confluence](https://blog.datumo.io/setting-up-kafka-on-kubernetes-an-easy-way-26ae150b9ca8)

Also see the resources on Kubernetes, Flask and Minikube under trainings/kubernetes/custom_k8s_03

---

## What is this?
This deletion_queue_app is a personal project to implement a solution to a real-world business problem that I have observed in my day job: on-demand data deletion of sensitive customer information.

### What exactly is the problem?
All companies in countries with data protection laws (particularly GDPR, as in this case) need to comply with the deletion of customer data in a potentially on-demand manner.<br>
A data deletion request could come in from a variety of systems. When it does, the request needs to be propogated to all relevant systems, and the consequences for failure can be high (legal action if data is not deleted within a specific time frame).<br>
This is a particularly difficult problem in my experience because it combines a huge breadth (ALL systems with customer data are affected) with a very low tolerance for error. However, the time frames required to process these requests are often generous in the scope of regular latency concerns - we often have weeks rather than seconds.<br>
This kind of system therefore can afford to be slow or asynchronous, although data-checking procedures need to be comprehensive.

### How should this be built?
I'll start by listing out the requirements and tolerances of what we need:
- Speed: **days to weeks**
- Fault tolerance: **very low**
- Input sources: **very broad, can change quickly**
- Output sources: **very broad, can change quickly**
<br>
We can also divide the application we need to build into 3 pieces:
1. Receive requests from input systems (API ingress)
2. Store requests (persistent database)
3. Forward requests to output systems (scheduled procedure)
<br>

These 3 tasks will translate into three distinct parts of the application.

---

## Architecture

### API ingress
The 'API' part of the application will receive requests for deletion through one of its endpoints. The API will also modify existing records as needed (e.g., by using an endpoint to 'approve' or 'reject' existing requests) and list requests.

### Persistent database
The database part of the application will simply store the data - likely in a single table. If volume becomes high, indexing or sorting can be implemented (by request date?) to slice the dataset.
>Note: We will also need to indicate which requests are not yet dealt with + which requests are finished. This might be best achieved by creating an 'archive' table within this database where references to processed records are stored. Not clear yet how long these records would be stored.

### Forwarding procedure
This part of the application will be responsible for checking the existing requests and forwarding them for further processing based on some rules. The rules and the destinations requests are forwarded to will both be configurable.
>Note: In some special cases, the rules and destinations overlap (e.g., only certain types of requests get forwarded to certain destinations. Need to ensure this structure is very clear and easy to configure.

Requests will be stored in a neighboring Kafka instance within the same Kubernetes cluster.
> Idea: A future version could store requests via an external, low-cost database to make the application more fault-tolerant.

---

## Development Steps

### 1. Build API V1.0

#### a. Endpoint proof-of-concept
- [X] Define the endpoints needed and what data is required from client (use Swagger doc as planning area)
- [X] Define payload data structure for all endpoints
- [X] Implement in Flask
- [X] Migrate to FastAPI
- [X] Test endpoints

#### b. Class setup
- [X] Define overall class structure(s) for the API
  - Basic could be a simple 'database_connection' class that connects to persistent database and has abstracted methods for storing / retrieving data from it
  - We could also implement a class for handling / checking incoming payloads from endpoints
  - We could also implement an error class for better errors generally
- [X] Implement class definition(s)
- [X] Connect class(es) to API endpoints and to a **local database (JSON?) for testing**
- [X] Test endpoints
  - [X] Test malformed payloads

#### c. Deploy
- [X] Change credential storing to be more secure (i.e., not in standard config file)
- [X] Deploy API to Minikube and test
  - [X] Make local image for Docker: https://www.stereolabs.com/docs/docker/creating-your-image/
  - [X] Test on Docker
  - [X] Make K8s deployment with postgres + api services
- [X] Deploy API to production environment
- [X] Re-test

---

### 2. Build persistent database

#### a. Database setup
- [X] Create database in production environment
  - [X] Decide whether to use Postgres as persistent K8s volume or an external database
    - Notes: It might be more nicely self-contained if I just used a persistent volume in K8s - an external database would require additional setup and wouldn't be as 'clean'. I also don't have experience with setting up persistent k8s volumes, so that would be nice practice.
- [X] Define database schema:
  - I think we only need 2 tables: [pending requests] and [finished requests].
    - pending requests:
      - UUID (string)
      - Date Added (date)
      - identifier (string)
      - input reason (string)
      - rejected (boolean)
        - Note: I don't think there is a need to show approval - all requests are approved by default - only explicit rejection is relevant.
    - finished requests:
      - < Same as pending >
      - Date processed (date)
- [X] Test connections to database 

#### b. Connect API to database
- [X] Edit API to use production database
- [X] Test API
  - [X] Test adding, modifying, and removing from database

#### c. Test persistence
- [ ] Restart API runtime - ensure data is still persisted
- [ ] Stress-test database (e.g., if implemented using distributed database, take some replicas offline and ensure no data was lost)

---

### 3. Build forwarding procedure

#### a. Define structure of rules + destinations
- [ ] List out probable rules for forwarding to different destinations
- [ ] List out probable destinations
- [ ] Decide how to separate rules from forwarding

#### b. Deploy
- [ ] Deploy forwarding procedure to production environment
- [ ] Set up connection to persistent database & test connection
  - Note: Can I re-use database-connection class from API?

#### c. Test resilience
- [ ] Test what happens when a single destination fails
- [ ] Test what happens when multiple - or all destinations fail
- [ ] Test that confirmations of forwarding are recorded correctly to database
- [ ] Test what happens when data is RE-FORWARDED (i.e., are duplicates handled correctly)

---

### 4. Setup Production environment
- [ ] Provision Kubernetes (install on an EC-2 cluster?)

## Dev Notes:

> Feb. 5, 2023:
> Finished working on testing 'get_finished_by_date' method in our database connection class
> **Note:** Can no longer test database connection class as standalone script due to configparser using relative paths to load
> config file - use `start_app.sh` instead.
> Next step is to implement the marshmallow validation.py script so that I can check my incoming POST request bodies in app.py

---

> Feb. 7, 2023:
> Finished implementing validation for POST requests.
> Next steps are:
> 1. Doing more testing with malformed requests (try to break the system) - check out error codes returned
> 2. Get postgres working on K8s
> 3. Deploy api to K8s
> 4. Integrate api on k8s with database on k8s

---

> Feb. 18, 2023:
> Finished migration to FastAPI and all API unit tests.
> ready to deploy to Minikube, and then move on to a K8s instance

---

> Feb. 21, 2023:
> Trying to convert my code into a container-ready format and get it to run on Docker.
> My postgres DB was already running on Docker, and I think I got my api to connect o.k. (at least did not get
> any errors when container booted up).
> However, I'm having a hard time connecting to the API - I keep getting a 'connection reset' error.
> I did make a test API in trainings/docker-example - and it worked like a charm with this setup:
> ```
> docker build -t test_fastapi:v1 .
> docker run -d -p 8080:8080 test_fastapi:v1
> curl localhost:8080
> ```
> I need to see what might be happening here and why I can't get my bigger version to work...
> Next to-dos:
> - Once it runs on Docker, tweak dockerfile - can I get rid of copy commands?
> - create minikube deployment
> - Once it runs on minikube, configure so that secrets work correctly.
>
> **SOLUTION:**
> There were 2 issues with my initial build:
> - 'pydantic' had a dependency 'email-validator' - which was not installed for some reason. Adding this to the requirements to install fixed this
> - My docker containers were not on the same network, so my initialization of my databaseConnection class ended up trying to connect to the database container and getting no response. This was solved by making sure the containers were on the same network"
> `docker run --network test_db_setup_default -d -p 8080:8080 requestprocessor_api:v1`

---

> Feb. 23, 2023
> I've now gotten my api + database working on 2 networked docker containers.
> My next step is to convert this into a Kubernetes deployment and set it up on Minikube:
> 1. Make deployment file with postgres + api images
> 2. Network my kubernetes instance on Minikube to API
> 3. Test
> 4. (stretch) set up better secrets management using K8s secrets.

---

> Mar 3, 2023
> I've gotten a postgres instance up-and-running. Need to now deploy my API and see if it can connect (try to use basic version first?)
> I've also gotten a basic version of the API running on another container - but I haven't activated the database connection yet.
> Next, I need to set up an internal service on K8s so that my API can feasibly connect to postgres - and then I can try activating the database class and seeing if it works o.k.
> ---
> Steps for deploying to minikube:
> 1. boot up minikube
> 2. (re)start postgres deployment
> 3. tell minikube to look elsewhere for its images: `eval $(minikube -p minikube docker-env)`
> 4. Navigate to API folder and rebuild docker image for API: `docker build -t requestprocessor_api:v1 .`
> 5. (re)start API deployment
> 6. (re)start external service
> 7. Tell minikube to give me a URL for external service! `minikube service requestprocessor-api-external-service --url`
> 8. Use external service URL to test application

---

> Mar 4, 2023
> I've gotten the application working on Kubernetes! **AND ALL OF MY TESTS PASSED!!**
> Today is a glorious day.
> Now that I've basically gotten my app working, I need to do some cleanup before I move on to building the 3rd part of the app,
> which will process the requests periodically (this is basically a skeleton structure anyway)

**Clean up:**
1. Rewrite my code into a format that is Kubernetes-friendly, but also allows local testing (no need to support Docker testing) - this is going to take some planning and should include:
   1. Appropriate protection of credentials in secrets file
      1. I'm working on this now. I ran into an issue with re-starting the postgres instance - something about the persistent volume wasn't working so I deleted the volume and it needs to be re-initialized. Once that's done, edit the commented-out sections of the deployment file to figure out how to use secret values as environment variables.
   2. Credentials should not be part of GH upload (although since this is testing, maybe just note in the file that credentials would be normally excluded)
   3. Remove (or archive) unnecessary Docker files (e.g., for building postgres setup for local Docker)
   4. Clean up "DatabaseConnection.py"
   5. ~~**Remove Kafka folder** - a RDBMS is the best choice for this kind of low-volume, simple application. Plan to play with Kafka next time.~~
   6. Changing 'config' file: for Kubernetes we need a K8s config file, for local testing, we can keep the local version?
      1. Will testing be affected if we use localhost for local testing vs. K8s URL?

**Optimize:**
1. Completely wipe and re-create postgres and api deployments (images removed from docker, delete minikube deployments)
2. Restart applications in clean environment and *TEST that they still work*
3. Try to break postgres instance - kill the pod and see if data is lost
   1. If data IS lost, figure out how to make pod resistant to data loss (replicas?)
4. **IMPLEMENT AUTHENTICATION SYSTEM**
   1. I'm not sure the best way - let's try to start with 

---
---
### Project Learnings:

##### Set up your production environment - and test in it - ASAP
I started developing this app completely locally - I set up some nice scripts to connect my API (run from CLI) to postgres (on Docker) and I then used a 2nd terminal to do testing. Very nice! BUT: when it came to move this to Kubernetes, it was a pain in the butt.
I first opted to move it to my local Docker instance to make sure I could build the API image without having to deal with services and deployments. This worked, but then I had to migrate twice - from local to Docker, and then from Docker to K8s (this 2nd one wasn't a big deal, but still).
I think I would have been much better served by doing this:
1. Set up *absolute basic version of my app* - and deploy it to the production environment. Then, I have all of my infrastructure there and I can choose where to develop.
2. Develop locally for convenience, but after getting something working, immediately deploy it to the production environment and test again

---

##### Continuously record the CLI commands I'm using
Everything from building docker images to deploying on Kubernetes - there are a lot of commands I'm running from the command line when setting up my app. And I keep forgetting which ones I used! I'm continuously scrolling through the command history to find them again, which is not great.
What I should instead do is this: once I set up my production environment with my first version of my app, I need to record all steps to set up the app in that environment. And if I add new features (e.g., I require a new internal K8s service), then I simply add those to the running list.
One issue that I'm running into this time is that I have such a complex testing system (e.g., build docker container, make available to minikube, etc.) that I don't bother to record all of the steps.