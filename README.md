# Sporple (codename elites)

## Wiki
Refer to Wiki for helpful documents about the development:
[https://github.com/jainankit/elites/wiki](https://github.com/jainankit/elites/wiki)


## Setup
Sporple infrastructure is entirely built on AWS, mostly using EC2.

The deployment is built on ansible, for instance to deploy, now we just need to do:

`ansible ankitjain$ ansible-playbook -i hosts/prod webserver.yml`

Worth reading the [Ansible-Playbook documentation](http://docs.ansible.com/ansible/playbooks.html)

The platform is distributed as follows:


__1. Frontend and backend tasks__
Each of the following boxes runs a frontend servers and backend servers. By changing and executing the ansible scripts, these can be changed over time.
- `prod_node1: node1.corp.sporple.com`
- `prod_node2: node2.corp.sporple.com`
- `prod_node3: node3.corp.sporple.com`


__2. Db server__
We are only running a single db instance on one instance. The only thing to remember here is that the server is not managed by ansible. This was setup once.
The backup of database is done via a cron script installed on the server that is run once a day. The gziped db version is uploaded on S3.
- `db.corp.sporple.com`


__3. Push server__
This is primarily used to run python scripts on the prod server. Also used for migration scripts. This server does not run frontend or backend servers but it does run the __cron jobs__. The key differentiator here is that the code is never pushed to this server but rathere it has a git repository checked out. So you can pull in a new branch, run venv.
- `push.corp.sporple.com`


__4. Elasticsearch__
Simply just runs elasticsearch. Ansible is used to deploy elasticsearch here.
- `es.corp.sporple.com`


__5. Staging__
As name suggests, it runs the staging box. everything runs on one single box for staging. It also houses the staging elasticsearch that is used in local dev boxes.
- `staging.sporple.com`
Username: ankit
password: staging

__6. Redis__
Redis is a in-memory cache service that is currently used to manage user sessions and also manage message queue for backend task. There is only one instance of redis that is run on `node2.corp.sporple.com`


## Local Development Environment
Development environment has to be setup manually. There is no ansible script to do this. There are a few key components to the development:
- webserver: flask
- db: postgres
- redis: for sessions and backend queue
- backend server: celery
- http server: nginx

All these have to be manually startup.
### Mac
- Install Postgres from here: [https://www.postgresql.org/download/macosx/](https://www.postgresql.org/download/macosx/) or anywhere else
- Install redis directly if you have brew: `brew install redis`
- Install nginx: `brew install nginx`
- Setup nginx, copy the config file at `server/misc/nginx.conf` to `/usr/local/etc/nginx/nginx.conf`. Make sure to replace the static path in file to the static path to your repo.
- Start nginx: `sudo nginx` or reload: `sudo nginx -s reload`

### Linux
- Download and install Postgres: [http://tecadmin.net/install-postgresql-server-on-ubuntu/](http://tecadmin.net/install-postgresql-server-on-ubuntu/) or anywhere else
- Install redis: [http://redis.io/topics/quickstart](http://redis.io/topics/quickstart)
- Install nginx: `sudo apt-get install nginx`
- Setup nginx, copy the config file at `server/misc/nginx.conf` to `/etc/nginx/nginx.conf`. Make sure to replace the static path in file to the static path to your repo.
- Restart nginx: `sudo service nginx reload`

### Mac & Linux
- Once you have the git repo cloned, create virtual environment:
```
~$ cd elites/server/
server$ pip install virtualenv
server$ virtualenv --no-site-packages -p /usr/bin/python2.7 venv
server$ source venv/bin/activate
server(venv)$ cd src/
src(venv)$ pip install -r requirements.txt
```
- Now start postgres and redis (just starting the vanilla services for both should work)
- Setup database on postgres:
  - 1. get a dump of database from s3, unzip it: `gunzip <filename>`
  - 2. create database on postgres: `createdb sporple`
  - 3. now import this using pg_restore: `pg_restore -Fc -h localhost -p 5432 -U postgres -d sporple -v <filename>`
  - 4. create a user with all access: `createuser -P -s -e sporple`, enter password: `1q2w3e4r`
  
- The webserver is ready to go:
```
src(venv)$ python application.py
### If everything worked fine, the server should start here. Press Ctrl+C to kill the server at any time.
```
- Set the `/etc/hosts` with `local.sporple.com` to localhost:

`127.0.0.1 local.sporple.com`

- Optionally you can start the backend tasks as celery as well, this is only required if you want to test emails.
```
src(venv)$ celery -A main.celery worker
### IF everything worked fine, the server should start here.
```

### Local Frontend Development Compilation
We use `gulp` to compile frontend javascript and css. Follow these steps to install gulp.
- download `node.js` from here: [https://nodejs.org/en/download/](https://nodejs.org/en/download/)
- install npm dependencies from `src` directory: `src(venv)$ sudo npm install`
- now run `gulp dev`. This will start the server that uses the original server as proxy.
- (optional) if you get the error that gulp is not found, soft-link the local gulp to a registered path:
```
src(venv)$ ln -s /Users/ankitjain/dev/elites/server/src/node_modules/.bin/gulp  /usr/local/bin/gulp
src(venv)$ gulp dev
```
- any changes done now in frontend are compiled instantly and can be directly accessed using http://localhost:8000
- make sure you commit all __compiled__ changes to the branch when ready. These changes are not recompiled automatically during deployment to save time.

### Restarting servers
After the first time setup, next time just postgres, redis, nginx and webserver need to be started. Make sure virtual enviornment is started before starting webserver.
```
src(venv)$ source ../venv/bin/activate
src(venv)$ python application.py
### If everything worked fine, the server should start here. Press Ctrl+C to kill the server at any time.
```


# Migrations
All database migrations are stored in `src/migrations/versions/*.py`.
Every time db/__init__.py is updated, make sure to run migration:

`src(venv)$ python manage.py db migrate`

This will generate a new migrations file in `migrations/versions/`. Make sure the file is as expected. Commit the migration file:

`src(venv)$ git add migrations/versions/<file_name.py> -f`

The file has to be forced committed since otherwise the migration folder is ignored (to avoid committing a migration file by mistake).
To apply these changes to local database:

`src(venv)$ python manage.py db upgrade`


To apply the changes to prod, login to push server:
```
$ ssh push.corp.sporple.com
$ cd /home/www/elites/server/src
$ git checkout <branch_name>
src$ act
src(venv)$ python manage.py db upgrade
```
