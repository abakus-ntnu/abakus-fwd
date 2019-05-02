# abakus-fwd

> Post messages across Slack workspaces, a docker image built to be deployed as a function in OpenFaaS

The container needs the following environment variables to work:
 * `SIGNING_SECRET` - the Slack app signing secret
 * `TARGET_WEBHOOK`- webhook for the workspace you want to post to
 * `OAUTH_TOKEN` - the Slack app OAuth token

Start and run the image locally: 
```
docker build -t abakus-fwd . && docker run --rm -p 4000:8080 --env="SIGNING_SECRET=BLABLABLA" --env="TARGET_WEBHOOK=BLABLABLA" --env="OAUTH_TOKEN=BLABLABLA" abakus-fwd
```
