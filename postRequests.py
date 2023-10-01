from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/your-endpoint', methods=['POST'])
def receive_notification():
    # Handle the eBay notification data here
    data = request.json  # Assuming eBay sends JSON data
    # Process the data as needed

    # Send a response to eBay to acknowledge the notification
    return jsonify({'message': 'Notification received and acknowledged'}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)