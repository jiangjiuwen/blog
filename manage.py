import os
from app import create_app, db
from app.models import User, Post, Category, Tag
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)

def make_shell_context():
    return dict(app=app, db=db, user=User, post=Post, category=Category, tag=Tag)

manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

@manager.command
def dev():
    pass

@manager.command
def test():
    pass

@manager.command
def deploy():
    pass

if __name__ == '__main__':
    manager.run()
