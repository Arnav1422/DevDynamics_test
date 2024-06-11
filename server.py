from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory data structures
topics = {}

def validate_subscription_data(data):
    if not data:
        return "Request body is empty", False
    if 'topicId' not in data or not isinstance(data['topicId'], str) or not data['topicId']:
        return "Invalid or missing 'topicId'", False
    if 'subscriberId' not in data or not isinstance(data['subscriberId'], str) or not data['subscriberId']:
        return "Invalid or missing 'subscriberId'", False
    if len(data['topicId']) > 1000 or len(data['subscriberId']) > 1000:
        return "Parameters 'topicId' or 'subscriberId' are too large", False
    return "", True

@app.route('/')
def index():
    return "Welcome ! This code is written by Arnav Shah. This Publisher-Subscriber Notification System API. Use /subscribe, /notify, and /unsubscribe endpoints."

@app.route('/subscribe', methods=['POST'])
def subscribe():
    data = request.json
    error_message, is_valid = validate_subscription_data(data)
    if not is_valid:
        return jsonify({"error": error_message}), 400
    
    topic_id = data['topicId']
    subscriber_id = data['subscriberId']
    
    if topic_id not in topics:
        topics[topic_id] = set()
    topics[topic_id].add(subscriber_id)
    
    return jsonify({"message": f"Subscriber {subscriber_id} subscribed to topic {topic_id}"}), 200

@app.route('/notify', methods=['POST'])
def notify():
    data = request.json
    if not data or 'topicId' not in data or not isinstance(data['topicId'], str) or not data['topicId']:
        return jsonify({"error": "Invalid or missing 'topicId'"}), 400
    if len(data['topicId']) > 1000:
        return jsonify({"error": "Parameter 'topicId' is too large"}), 400

    topic_id = data['topicId']
    
    if topic_id in topics:
        subscribers = list(topics[topic_id])
        return jsonify({"subscribers": subscribers}), 200
    else:
        return jsonify({"message": f"No subscribers for topic {topic_id}"}), 404

@app.route('/unsubscribe', methods=['POST'])
def unsubscribe():
    data = request.json
    error_message, is_valid = validate_subscription_data(data)
    if not is_valid:
        return jsonify({"error": error_message}), 400

    topic_id = data['topicId']
    subscriber_id = data['subscriberId']
    
    if topic_id in topics and subscriber_id in topics[topic_id]:
        topics[topic_id].remove(subscriber_id)
        if not topics[topic_id]:
            del topics[topic_id]
        return jsonify({"message": f"Subscriber {subscriber_id} unsubscribed from topic {topic_id}"}), 200
    else:
        return jsonify({"message": f"Subscriber {subscriber_id} not found in topic {topic_id}"}), 404

def driver():
    import requests
    
    base_url = 'http://127.0.0.1:5000'
    
    # Subscribe to topics
    response = requests.post(f'{base_url}/subscribe', json={"topicId": "topic1", "subscriberId": "sub1"})
    print(response.json())
    
    response = requests.post(f'{base_url}/subscribe', json={"topicId": "topic1", "subscriberId": "sub2"})
    print(response.json())
    
    # Notify subscribers
    response = requests.post(f'{base_url}/notify', json={"topicId": "topic1"})
    print(response.json())
    
    # Unsubscribe from topic
    response = requests.post(f'{base_url}/unsubscribe', json={"topicId": "topic1", "subscriberId": "sub1"})
    print(response.json())
    
    # Notify subscribers again
    response = requests.post(f'{base_url}/notify', json={"topicId": "topic1"})
    print(response.json())

if __name__ == '__main__':
    from threading import Thread
    
    # Run the Flask app in a separate thread
    Thread(target=app.run).start()
    
    # Run the driver function
    driver()
