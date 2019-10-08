# IGSN registry provider MVP

Registering your samples with bespoke organic PIDs since July 2019

[![Build Status](https://travis-ci.com/IGSN/igsn-registry-mvp.svg?branch=master)](https://travis-ci.com/IGSN/igsn-registry-mvp)

### Installing dependencies

We're using pipenv to make this easy. If you already have a system Python installed, you should be able to do:


```bash
$ pip install pipenv
```

or alternatively on MacOS

```bash
$ brew install pipenv
```

and then configure dependencies and a virtualenv using

```bash
$ pipenv install
Running $ pipenv lock then $ pipenv sync.
Locking [dev-packages] dependencies…
Locking [packages] dependencies…
✔ Success!
Updated Pipfile.lock (3ce347)!
Installing dependencies from Pipfile.lock (3ce347)…
  🐍   ▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉ 39/39 — 00:00:23
To activate this project's virtualenv, run pipenv shell.
Alternatively, run a command inside the virtualenv with pipenv run.
All dependencies are now up-to-date!
```

You can drop into a shell in the pipenv environment using `pipenv shell`. You'll need to do this to run all of the following commands. To make things easier to follow we'll prefix all commands inside the pipenv shell with the `>` symbol

You first need to create and update the database using the flask migrate commands:

```bash
$ pipenv shell
> flask db upgrade
flask db upgrade
INFO  [alembic.runtime.migration] Context impl SQLiteImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> 0ab4a25dfb6e, Initial migration
```

You can then run the test flask server using

```bash
> flask run
Loading .env environment variables…
 * Serving Flask app "app:create_app" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:8182/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 393-443-831
```

If you want to modify the parameters for the test server, take a look at the `.env` file in the root directory. Once your server is running you can start making requests (I recommend `pip instal httpie`)

```bash
$ http :8182/users
HTTP/1.0 200 OK
Content-Length: 115
Content-Type: application/vnd.api+json
Date: Fri, 04 Oct 2019 09:52:51 GMT
Server: Werkzeug/0.16.0 Python/3.6.8

{
    "data": [],
    "jsonapi": {
        "version": "1.0"
    },
    "links": {
        "self": "http://localhost:8182/users"
    },
    "meta": {
        "count": 0
    }
}
```

or posting JSON:

```bash
$ http --json POST :8182/igsn/foo8128 url="http://example.com/path/to/igsn" registrant="jess"
HTTP/1.0 200 OK
Content-Length: 41
Content-Type: application/json
Date: Tue, 02 Jul 2019 04:06:49 GMT
Server: Werkzeug/0.15.4 Python/3.6.8

{
    "message": "Registered sample foo8128"
}
```

Alternatively you can fire up the Swagger endpoint HTML in your browser by going to `http://localhost:8182` which will let you fire off querties to your locally running endpoint.

### Testing and development

If you're going to run the tests then you need to install all the development packages:

```bash
$ pipenv install --dev
# snip pipenv output
```

and then we can run `pytest`:

```bash
$ pipenv run pytest
# pytest output follows...
```

There's a few doctests for simple functions, and then most tests live in the `tests` folder. You can get coverage metrics by going to `./tests/reports/coverage.html/index.html`.

If you want to build an iPython kernel for Jupyter - you can build a kernel using the pipenv using

```bash
$ pipenv shell
> python -m ipykernel install --user --name=igsn-registry"
```

and you should be able to see the igsn-registry kernel in jupyter.

### Deploy

We just deploy with zappa. Prior to deploying you probably want to remove all the dev
packages from the virtualenv (otherwise you'll be well over the 50 Mb lambda limit). Note that `pipenv uninstall --dev` [doesn't work at time of writing but might have changed](https://github.com/pypa/pipenv/issues/3385) so we do a full uninstall/reinstall as a workaround.

```bash
$ pipenv uninstall --all
$ pipenv install   # won't install dev
```

Then we can deploy/update/undeploy etc etc

```bash
$ pipenv run zappa deploy dev  # or update or prod
# snip output
```

**Note that if you are doing a clean deploy you will have to go to AWS API Gateway > Usage Plans and add the 'portal' API key to the gateway.**

If you need to see the status of your function you can do

```bash
$ zappa status
```