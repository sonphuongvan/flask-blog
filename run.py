from flaskblog import create_app, db

app = create_app()

if __name__ == '__main__':
    db.create_all(app=create_app())
    app.run(debug=True, host='0.0.0.0')