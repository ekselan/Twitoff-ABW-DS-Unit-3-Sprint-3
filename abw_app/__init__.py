# web_app/__init__.py

from flask import Flask

from abw_app.routes.home_routes import home_routes
from abw_app.routes.book_routes import book_routes
from abw_app.routes.user_routes import user_routes
from abw_app.routes.tweet_routes import tweet_routes
from abw_app.routes.twitter_routes import twitter_routes
from abw_app.models import db, migrate

# DATABASE_URI = "sqlite:///web_app_99.db" # using relative filepath
# using absolute filepath on Mac (recommended)
# DATABASE_URI = "sqlite:////Users/ekselan/Documents/GitHub/33_Repo_DS14_Twitoff/Twitoff-ABW-DS-Unit-3-Sprint-3/twitoff_dev_14.db"
DATABASE_URI = "sqlite:////Users/ekselan/Documents/GitHub/33_Repo_DS14_Twitoff/Twitoff-ABW-DS-Unit-3-Sprint-3/twitoff_II.db"
# DATABASE_URI =
# "sqlite:///C:\\Users\\Username\\Desktop\\your-repo-name\\web_app_99.db"
# # using absolute filepath on Windows (recommended) h/t:
# https://stackoverflow.com/a/19262231/670433


def create_app():
    app = Flask(__name__)

    # For use with database
    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(home_routes)
    app.register_blueprint(book_routes)
    app.register_blueprint(user_routes)
    app.register_blueprint(tweet_routes)
    app.register_blueprint(twitter_routes)
    return app


if __name__ == "__main__":
    my_app = create_app()
    my_app.run(debug=True)
