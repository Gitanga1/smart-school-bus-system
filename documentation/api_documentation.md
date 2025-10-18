**API Documentation - Smart School Bus System**



**Overview**

**RESTful API endpoints for the Smart School Bus System. All endpoints require authentication unless specified.**



**Authentication Endpoints**



**POST /accounts/login/**

**Description: User authentication**

**Access: Public**

**Request:**

**```json**

**{**

    **"username": "string",**

    **"password": "string"**

**}**

**```**

**Response:**

**```json**

**{**

    **"success": true,**

    **"user": {**

        **"username": "driver\_john",**

        **"user\_type": "driver",**

        **"first\_name": "driver",**

        **"last\_name": "john"**

    **}**

**}**

**```**



**GET /accounts/logout/**

**Description: User logout**

**Access: Authenticated users only**

**Response: Redirects to home page**



**Notification Endpoints**



**GET /notifications/**

**Description: List all notifications for current user**

**Access: All authenticated users**

**Response:**

**```json**

**{**

    **"notifications": \[**

        **{**

            **"id": 1,**

            **"title": "Bus Delay Alert",**

            **"message": "Bus SCHOOL-001 is running 15 minutes late",**

            **"notification\_type": "delay",**

            **"created\_at": "2024-10-08T10:30:00Z",**

            **"is\_read": false,**

            **"sender": "admin\_user"**

        **}**

    **]**

**}**

**```**



**POST /notifications/send/**

**Description: Send new notification (Admin/Staff only)**

**Access: Admin and School Staff**

**Request:**

**```json**

**{**

    **"title": "Weather Alert",**

    **"message": "Heavy rain expected today",**

    **"notification\_type": "weather",**

    **"recipients": \[1, 2, 3],**

    **"bus\_id": 1**

**}**

**```**



**POST /notifications/read/{notification\_id}/**

**Description: Mark notification as read**

**Access: Notification recipient**

**Response:**

**```json**

**{**

    **"success": true,**

    **"message": "Notification marked as read"**

**}**

**```**



**Tracking Endpoints**



**POST /tracking/update-location/**

**Description: Update bus GPS location (Driver only)**

**Access: Drivers only**

**Request:**

**```json**

**{**

    **"bus\_id": 1,**

    **"latitude": 40.7128,**

    **"longitude": -74.0060,**

    **"speed": 35.5**

**}**

**```**



**GET /tracking/bus-locations/**

**Description: Get all active bus locations**

**Access: Parents, Staff, Admin**

**Response:**

**```json**

**{**

    **"buses": \[**

        **{**

            **"bus\_number": "SCHOOL-001",**

            **"latitude": 40.7128,**

            **"longitude": -74.0060,**

            **"speed": 35.5,**

            **"timestamp": "2024-10-08T10:30:00Z",**

            **"driver": "driver\_john"**

        **}**

    **]**

**}**

**```**



**Student Endpoints**



**GET /students/my-children/**

**Description: Get parent's children (Parent only)**

**Access: Parents only**

**Response:**

**```json**

**{**

    **"children": \[**

        **{**

            **"student\_id": "STU-001",**

            **"first\_name": "Esther",**

            **"last\_name": "Wangui",**

            **"grade": "5th G-01",**

            **"bus\_assignment": "SCHOOL-001"**

        **}**

    **]**

**}**

**```**



**GET /attendance/today/**

**Description: Get today's attendance for user**

**Access: Parents (their children), Drivers (their bus), Staff/Admin (all)**

**Response:**

**```json**

**{**

    **"attendance": \[**

        **{**

            **"student\_name": "Esther Wangui",**

            **"status": "present",**

            **"check\_in\_time": "2024-10-08T08:15:00Z",**

            **"bus": "SCHOOL-001"**

        **}**

    **]**

**}**

**```**



**Error Responses**



**Common Error Format:**

**```json**

**{**

    **"error": true,**

    **"message": "Detailed error message",**

    **"code": "ERROR\_CODE"**

**}**

**```**



**Common Error Codes:**

**- `AUTH\_REQUIRED` - Authentication required**

**- `PERMISSION\_DENIED` - Insufficient permissions**

**- `NOT\_FOUND` - Resource not found**

**- `VALIDATION\_ERROR` - Invalid input data**



**Usage Examples**



**Example: Sending a Notification**

**```python**

**import requests**



**Login first**

**login\_data = {**

    **"username": "superuser2",**

    **"password": "@qwertyui"**

**}**

**response = requests.post("http://localhost:8000/accounts/login/", data=login\_data)**



**Send notification**

**notification\_data = {**

    **"title": "Emergency Alert",**

    **"message": "School closing early due to weather",**

    **"notification\_type": "emergency",**

    **"recipients": \[1, 2, 3]**

**}**

**response = requests.post("http://localhost:8000/notifications/send/", data=notification\_data)**

**```**



**Example: Getting Bus Locations**

**```python**

**import requests**



**Get bus locations (requires authentication)**

**response = requests.get("http://localhost:8000/tracking/bus-locations/")**

**bus\_data = response.json()**



**for bus in bus\_data\['buses']:**

    **print(f"Bus {bus\['bus\_number']} at {bus\['latitude']}, {bus\['longitude']}")**

**```**



**Testing the API**



**Using curl:**

**```bash**

**Login**

**curl -X POST http://localhost:8000/accounts/login/ \\**

  **-d "username=driver\_john\&password=@zxcvbnm,"**



**Get notifications**

**curl http://localhost:8000/notifications/ \\**

  **-H "Cookie: sessionid=your\_session\_id\_here"**

**```**



**Using Django Test Client:**

**```python**

**from django.test import TestCase**

**from django.urls import reverse**



**class APITestCase(TestCase):**

    **def setUp(self):**

        **self.client.login(username='driver\_john', password='@zxcvbnm,')**

    

    **def test\_get\_notifications(self):**

        **response = self.client.get(reverse('notification\_list'))**

        **self.assertEqual(response.status\_code, 200)**

**```**



**Rate Limiting**

**- Authentication endpoints: 5 attempts per minute**

**- Notification endpoints: 10 requests per minute**

**- Tracking endpoints:30 requests per minute**



**Security Notes**

**- All sensitive data transmitted over HTTPS in production**

**- CSRF protection enabled on all POST endpoints**

**- Session-based authentication**

**- Role-based access control on all endpoints**

**```**



