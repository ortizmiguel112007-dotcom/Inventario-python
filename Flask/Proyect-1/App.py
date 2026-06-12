from flask import Flask

from src.routers.aprendizRouter import aprendiz_router
from src.routers.homeRouter import home

App = Flask(__name__)

App.register_blueprint(aprendiz_router, url_prefix="/aprendiz")
App.register_blueprint(home)

if __name__ == '__main__':
    App.run(host="0.0.0.0", port=5000, debug=True)
