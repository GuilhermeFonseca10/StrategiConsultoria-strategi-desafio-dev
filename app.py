from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

from flask import Flask






app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/heroes.db'
db = SQLAlchemy(app)
with app.app_context():
    class Hero(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(80), unique=True, nullable=False)
        description = db.Column(db.String(250))
        photo = db.Column(db.String(250))
        team = db.Column(db.String(80))

        def __repr__(self):
            return '<Hero %r>' % self.name


    class Team(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(80), unique=True, nullable=False)
        description = db.Column(db.String(200), nullable=False)
        
        def __repr__(self):
            return '<Team %r>' % self.name



    db.create_all()

    @app.route('/')
    def index():
        heroes = Hero.query.all()
        return render_template('index.html', heroes=heroes)

    @app.route('/add', methods=['POST'])
    def add():
        hero = Hero(name=request.form['name'], description=request.form['description'], photo=request.form['photo'])
        db.session.add(hero)
        db.session.commit()
        return redirect(url_for('index'))

    @app.route('/select/<int:id>')
    def select(id):
        hero = Hero.query.get(id)
        hero.team = 'possible_candidate'
        db.session.commit()
        return redirect(url_for('index'))

    @app.route('/deselect/<int:id>')
    def deselect(id):
        hero = Hero.query.get(id)
        hero.team = None
        db.session.commit()
        return redirect(url_for('index'))

    

    @app.route("/edit/<int:id>")
    def edit(id):
        hero = Hero.query.get(id)
        return render_template("edit.html", hero=hero)

    @app.route('/teams', methods=['GET', 'POST'])
    def teams():
        if request.method == 'POST':
            name = request.form['name']
            description = request.form['description']
            team = Team(name=name, description=description)
            db.session.add(team)
            db.session.commit()
            return redirect(url_for('teams'))
        teams = Team.query.all()
        return render_template('teams.html', teams=teams)

@app.route('/assign_team/<int:hero_id>', methods=['GET', 'POST'])
def assign_team(hero_id):
    hero = Hero.query.get(hero_id)
    if request.method == 'POST':
        team_id = request.form['team']
        team = Team.query.get(team_id)
        hero.team = team
        db.session.commit()
        return redirect(url_for('index'))
    teams = Team.query.all()
    return render_template('assign_team.html', hero=hero, teams=teams)


if __name__ == '__main__':
        app.run(debug=True)