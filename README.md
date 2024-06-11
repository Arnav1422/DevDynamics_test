# Publisher-Subscriber Notification System

## Overview
This is a simple implementation of a Publisher-Subscriber Notification System using Flask. The system supports subscribing to topics, notifying subscribers, and unsubscribing from topics.

## APIs

### 1. Subscribe
**Endpoint:** `/subscribe`  
**Method:** `POST`  
**Payload:**
```json
{
  "topicId": "topic1",
  "subscriberId": "sub1"
}
```
Description: Subscribes a subscriber to a topic.


### 2. Notify
**Endpoint:** `/notify`
**Method:** `POST`
**Payload:**
```json
{
  "topicId": "topic1"
}
```
Description: Notifies all subscribers of a particular topic.

### 3. Unsubscribe
**Endpoint:** `/unscbscribe`
**Method:** `POST`
**Payload:**
```json
{
  "topicId": "topic1",
  "subscriberId": "sub1"
}
```
Description: Unsubscribes a subscriber from a topic.


**Running the Application**
Prerequisites
Python 3.x
Flask
Requests library
