# IGSN registry provider MVP

Registring your samples with bespoke organic PIDs since July 2019

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

You can then run the test flask server using

```bash
$  pipenv run ./run_api.py --port 8182  # or whatever
 * Environment: production
   WARNING: Do not use the development server in a production environment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://127.0.0.1:8182/ (Press CTRL+C to quit)
```

and start making requests (I recommend `pip instal httpie`)

```bash
$ http :8182/igsn/
HTTP/1.0 200 OK
Content-Length: 50
Content-Type: application/json
Date: Tue, 02 Jul 2019 04:05:35 GMT
Server: Werkzeug/0.15.4 Python/3.6.8

{
    "message": "IGSN Demo Resolver up and running!"
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
$ pipenv run "python -m ipykernel install --user --name=igsn-registry-mvp"
```

and you should be able to see the igsn-registry-mvp kernel in jupyter.

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