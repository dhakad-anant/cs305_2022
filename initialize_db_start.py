from pkg.initialize_db import app


# driver function
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)