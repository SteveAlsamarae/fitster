# Fitster Deployment On Heroku

The following steps are required to deploy the application on Heroku:

## Step 1: Heroku Setup

1. Create a new Heroku account and login.
2. Download the Heroku CLI from [Heroku](https://devcenter.heroku.com/articles/heroku-cli).
3. Login to Heroku from the command line. You can do this by running the following command:

```bash
heroku login
```

## Step 2: Setup S3 Bucket

1. Navigate to Amazon Web Services and Create or Sign into your account.
2. Select “AWS Management Console” under “My Account” and search for S3.
3. Create a new bucket and select the region closest to you.(Write down the bucket name and region in a text file)
4. Uncheck `block all public access for this bucket` and confirm that the bucket will be public.
5. Select “Create Bucket”at the bottom of the page.
6. On the Permissions tab, at the top of the page, paste in this CORS Configuration.

    ```json
    [
        {
        "AllowedHeaders": [
            "*"
        ],
        "AllowedMethods": [
            "GET",
            "HEAD"
        ],
        "AllowedOrigins": [
            "*"
        ],
        "ExposeHeaders": [
            "ETag"
        ],
        "MaxAgeSeconds": 3000
        }
    ]
    ```

7. Create a policy for the bucket. Paste the following policy in the text box.

    ```json
    {
    "Version": "2012-10-17",
    "Statement": [
        {
        "Sid": "PublicReadGetObject",
        "Effect": "Allow",
        "Principal": "*",
        "Action": "s3:GetObject",
        "Resource": "arn:aws:s3:::fitster-bucket/*"
        }
    ]
    }
    ```

8. Create a new user from IAM and grant full access to the bucket.
9. Download the S3 access credentials from the IAM user.
10. Now set the environment variable `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` in your Heroku app from web or command line. You can do this by running the following command:

    ```bash
    heroku config:set AWS_ACCESS_KEY_ID=<your-access-key>
    heroku config:set AWS_SECRET_ACCESS_KEY=<your-secret-key>
    heroku config:set S3_BUCKET_NAME=<bucket-name>
    heroku config:set AWS_DEFAULT_REGION=<bucket-origin>
    ```

## Step 3: Setup SMTP Server

1. Create a gmail account and login.
2. Setup two-step authentication.
3. Generate an app password for your gmail account.
4. Note down the app password and the email address of the gmail account.
5. Now set the environment variable `SMTP_USER` and `SMTP_PASS` in your Heroku app from web or command line. You can do this by running the following command:

    ```bash
    heroku config:set EMAIL_HOST_USER=<your-gmail-email>
    heroku config:set EMAIL_HOST_PASSWORD=<your-gmail-app-password>
    ```

## Step 4: Setup Stripe

1. Create a Stripe account and login.
2. Install Dj-stripe using the following command:

   ```python
    pip install dj-stripe
   ```

3. Go to [Stripe Dashboard](https://dashboard.stripe.com/account/apikeys) and grab the `Secret key` and `Publishable key`.
4. Now set the environment variable `STRIPE_SECRET_KEY` and `STRIPE_PUBLISHABLE_KEY` in your Heroku app from web or command line. You can do this by running the following command:

    ```bash
    heroku config:set STRIPE_TEST_SECRET_KEY=<STRIPE_SECRET_KEY>
    heroku config:set STRIPE_PUBLIC_KEY=<STRIPE_PUBLISHABLE_KEY>
    ```

5. Set the following environment variables with correct value or any value in your Heroku app from web or command line:

    ```bash
    heroku config:set STRIPE_LIVE_SECRET_KEY=<STRIPE_SECRET_KEY>
    heroku config:set STRIPE_LIVE_MODE=<true or false>
    heroku config:set DJSTRIPE_WEBHOOK_SECRET=<DJSTRIPE_WEBHOOK_SECRET>
    ```

## Step 5: Deploy Application

1. Create a database addon for your application by running the following command:

    ```bash
    heroku addons:create heroku-postgresql:hobby-dev
    ```

2. Set DISABLE_COLLECTSTATIC to true in your Heroku app from web or command line. You can do this by running the following command:

    ```bash
    heroku config:set DISABLE_COLLECTSTATIC=true
    ```

3. Add your heroku app url to allowed hosts in your prod config file and commit it.

4. Push your application to Heroku by running the following command:

    ```bash
    git push heroku master
    ```

5. Run migrations by running the following command:

    ```bash
    heroku run python manage.py makemigrations
    heroku run python manage.py migrate
    ```

6. Now create a super user by running the following command:

    ```bash
    heroku run python manage.py createsuperuser
    ```

## Step 6: Setup Complete

The site is now live and you can open it in your browser.

## Alternative Deployment

- Set all the environment variables in your Heroku app from web or command line correctly.

To have your project automatically deploy to Heroku when you push the repository to Github you need to set up automatic deployment. To do this you need to:

1. Click the deploy tab on your Heroku App.
2. Select GitHub as the deployment method
3. Search for an select the GitHub repo you want to connect to
4. Click “Connect” and then “Enable Automatic Deploys”
5. Done!
