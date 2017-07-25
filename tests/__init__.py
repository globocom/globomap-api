from globomap_api.app import create_app

if __name__ == '__main__':
    app = create_app('tests.config')

    with app.app_context():
        db_inst = DB()
        try:
            db_inst.delete_db(app.config['ARANGO_DB'])
        except Exception:
            # Cleanup datebase
            pass
        finally:
            db_inst.create_db(app.config['ARANGO_DB'])
