from haisya_app.app import create_app, db

def create_tables(event, context):
    app = create_app()
    with app.app_context():
        db.create_all()
        return "Tables created successfully!"
