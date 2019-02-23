install cookiecutter
pip install -e ".[testing]"
alembic -c development.ini revision --autogenerate -m "init"
alembic -c development.ini upgrade head
initialize_tutorial_db development.ini