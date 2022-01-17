from invoke import task


@task
def test(c):
    c.run("docker-compose run --rm api python manage.py test")


@task
def deploy(c):
    c.run("docker-compose up")
