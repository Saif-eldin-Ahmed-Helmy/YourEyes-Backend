from app import create_app
import os

app = create_app()

# add route to test /hello reply with hello
@app.route('/hello', methods=['GET'])
def hello():
    return "Hello, World!"

if __name__ == "__main__":
    app.run(host=os.environ.get('HOST', '127.0.0.1'), port=5000, debug=False)
