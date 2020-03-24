# abakus-fwd

> Post messages across Slack workspaces, a docker image built to be deployed as a function in OpenFaaS

The container needs the following environment variables to work:
 * `SIGNING_SECRET` - the Slack app signing secret
 * `TARGET_WEBHOOK` - webhook for the workspace you want to post to
 * `OAUTH_TOKEN` - the Slack app OAuth token

Start and run the image locally: 
```
docker build -t abakus-fwd . && docker run --rm -p 4000:8080 --env="SIGNING_SECRET=BLABLABLA" --env="TARGET_WEBHOOK=BLABLABLA" --env="OAUTH_TOKEN=BLABLABLA" abakus-fwd
```
Can easily be tested using serveo.net with `ssh -R SOME-SUBDOMAIN:80:localhost:4000 serveo.net`, and using the URL returned as the request URL for interactive components in your Slack app.


Can be deployed using `faas-cli deploy` to also set env variables.


To use this with a new Slack app you need to:
1. Enable Interactivity in your app
2. Set the Request URL to where this app is running
3. Create a new shortcut (on messages), pick a name and description, and set the callback ID to `x_publish`
4. Check that your app has the appropriate permission scopes ("Add slash commands and add actions to messages (and view related content)")
