from prefect import flow
from datetime import timedelta

@flow(log_prints=True)
def my_job():
    print("hello world")

if __name__ == "__main__":
    my_job.serve(
        name="job-every-10min",
        interval=timedelta(minutes=10),
    )
    # you can access the run by `prefect server start  --host ep14.213428.xyz` via UI 
    # or `prefect deployment run 'my-job/job-every-10min'` via CLI
