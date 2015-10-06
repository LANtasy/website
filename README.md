# Lantasy Website
[![Circle CI](https://circleci.com/gh/BCGamer/website/tree/master.svg?style=shield)](https://circleci.com/gh/BCGamer/website/tree/master)

## Variables
These can be defined as either as environment variables or local_settings.py

### Django / Mezzanine
* [SECRET_KEY](https://docs.djangoproject.com/en/1.8/ref/settings/#secret-key)
* [NEVERCACHE_KEY](https://github.com/stephenmcd/mezzanine/issues/802)
* [DEBUG](https://docs.djangoproject.com/en/1.8/ref/settings/#debug)

### Mailgun
The following variables are used for sending emails through mailgun.
* MAILGUN_ACCESS_KEY = 'ACCESS-KEY'
* MAILGUN_SERVER_NAME = 'SERVER-NAME'

### Stripe Payments
You must collect these variables from a stripe account to test.
* DJANGO_STRIPE_SECRET
* DJANGO_STRIPE_PUBLISHABLE

## Install
Install the required python components
> pip install -r requirements/requirements.txt

Migrate the database of schema
> python manage.py syncdb

Make sure the server hostname is set to what you want, the default mailer will tie to this name.
