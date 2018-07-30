import os
from app import create_app
from app.models.base import db

from flask_script import Manager,Shell
from flask_migrate import Migrate,MigrateCommand

# from app.models.wordRepertory import CET4,CET6,Kaoyan
# import app.models.wordRepertory


app=create_app(os.getenv('FLASK_CONFIG') or 'default')

manager=Manager(app=app)
migrate=Migrate(app=app,db=db)

def make_shell_context():
    return dict(app=app,db=db)
manager.add_command('shell',Shell(make_context=make_shell_context))
manager.add_command('db',MigrateCommand)

@manager.command
def deploy():
    # run deployment tasks
    from flask_migrate import upgrade
    upgrade()

if __name__=='__main__':
    manager.run()