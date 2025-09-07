from app import create_app

app = create_app()

# add route to test /hello reply with hello
@app.route('/hello', methods=['GET'])
def hello():
    return "Hello, World!"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)