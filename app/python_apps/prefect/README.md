I think the architecture of prefect is


prefect instance --PREFECT_API_URL--> prefect server

Initially, prefect server will run ephemeral mode.


# Typical Scenarios

Switch back to ephemeral mode by `prefect profile use ephemeral`

You'll see `PREFECT_SERVER_ALLOW_EPHEMERAL_MODE='true'` in `prefect config view`
