from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import create_app
from models import db, Actor, Movie

app = create_app()

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


@manager.command
def seed():
    Movie(title='The Aviator', release_date='2004-05-06').insert()
    Movie(title='The Departed', release_date='2006-05-06').insert()
    Movie(title='Salt', release_date='2010-05-06').insert()

    Actor(name='Leonardo DiCaprio', age=30, gender='male').insert()
    Actor(name='Leonardo DiCaprio', age=32, gender='male').insert()
    Actor(name='Angelina Jolie', age=35, gender='female').insert()


if __name__ == '__main__':
    manager.run()
