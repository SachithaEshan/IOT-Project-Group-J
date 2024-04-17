const admin = require('firebase-admin');

// Initialize Firebase Admin SDK with your credentials
const serviceAccount = {
  "type": "service_account",
  "project_id": "iot-groupj",
  "private_key_id": "c009da07acdf23917ef36cb3655bb54bb6da50bb",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQChRGR78+iK3PL1\nzCfdlfR06vetMwfj605yDpqTJz8zE1jEtJXcn5sNhTzmytin2uaKqV+RemOFBouy\nmFSF3F4dSbmhh47v6KFlH7LYxOlfZ2/4ANfatehEOUko1+xnYeON7h1koRDIuFeY\nevfCr4eHCfzdyyDeU72jCLDBCFmqkEkNguWp6V/yANk9b6uMko34q3GWGSd5y4ox\nRJWQ0A78TcMIbZQwjyXxNpiqsvYoc6Bcfl6LGusO+MDQzOv1BXX+a6k72OVVvaPz\nSkae3jfQu/UK7SE3tQ6Xpbt/ARYEtCYT3ERz665thdWF0ogl6nysVlS6zZ4KpWtj\nIJu7et9pAgMBAAECggEACLre1K30v/Wril5RpydruxuQKlZZnj85+Scsu3wTqgRp\nWQasmSujtWTp0dWXymhpdAast3+gXQ5oaBPieXefOacozyN7O6YEfKitYhowxvse\nvtZu2PZhezX9raIYuFT+gEusWCr28WK3TTgU6vtdExSZlXkeT6LJYIbDKMP2tKqy\nZNDMz0fZpfNWYxKRJsHOP329D1j74LgXz9Onz0ZlS1IPajty8id7jXdNh90H0xgR\n7+ea3AjCzrHLs1FuQvDztegkv5vqj/aNmYI6fjLcUhdDcS0ddKHWEevRKes2TnJ+\nVtNIGi1TJHDKbakIITwOqWZj9M+qZhxB5xUhXQxUAQKBgQDPeQsjNE8fLrdytmwL\nKSfcmlZma+ZcjrNHwi4pnqsaWiFqPq6ulhc8zYnpHI+siZVXH0Rtyw71fF1c1yow\n6DBXjHAIO0a2wCcptOJmR4bxO8ECbUWCAwyL2i0MN112dCk0ty+Zig4KuP3ACTLR\ndevYg9tDS0tR/n6RNAoL81yhaQKBgQDG/Ksp1qmAZyQ27WkHbNrFxJTmbhQJcm4S\nWJzTLGpd83z8IjQkNh6HD84q4Ucnn/6Og1fd+pzUJgTpZ+b8nYNDJeJl+fmEu20y\nyNFoa02kI4qKYyqP1g44r+Cx5YfctRZeR7jHBbAoGMOyPIg0gzT3SabcT/woTyO7\nAUh/ySaOAQKBgDHJm1mcYOxbupwlmLHo827l/pvfgs1tVSqAN7G3KNpPDLvBRQwS\naosly9WMDBJcheD9WN98Hh/c806nN7G61nb79ZqUFvkeDYfdp4Lh4UkcjMm3TTnQ\n337kIXFQC/a0E3taBmszDQGXuRUPYAmR4cH4inKQrAeGKftQYKTThsQZAoGAaCou\nY7l2g7v6bjJ7j6KBJ5QPqkyneoaHbl0qwzT1/XaPz+EL0ITwGB3C/BlvySNs+ydw\nYMhnPnskiRaWCVlfNFBpop5n6v6+XB5Z2MKLI0hjpqvgxOj2CuCuzBFuvK+jJPmA\nlda5b1P/ZZdgabThji3lBmFsi6FZ//PdAt/GqgECgYA879O4I34RLFfZpVILbkW4\n86n+WY5zZDVk69qFIXnGxFpzTXzg07BfRNS7ycHU7g5Ktvk4v7DCfwaeR9FEKZlo\nnGqlsQkO0cN9c9K9W9B7aaZbiRJ9uHx+VZo9wuA9HttGEA2zpuAxzICiGjJ23vTk\n6g1fdMLMRzG5Zd17MTZdlQ==\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-hnc2f@iot-groupj.iam.gserviceaccount.com",
  "client_id": "100226460112349575571",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-hnc2f%40iot-groupj.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
};

admin.initializeApp({
  credential: admin.credential.cert(serviceAccount),
  databaseURL: "https://iot-groupj-default-rtdb.asia-southeast1.firebasedatabase.app"
});

const db = admin.database();

// Retrieve location data from Firebase Realtime Database
const getLocationData = async () => {
  try {
    const snapshot = await db.ref('drawsiness_events').once('value');
    return snapshot.val();
  } catch (error) {
    console.error('Error retrieving location data:', error);
    throw error;
  }
};

// Perform analysis on location data
const analyzeLocationData = (locationData) => {
  // Perform analysis here
  // For example, calculate total distance traveled, detect patterns, etc.
  console.log('Location data:', locationData);
};

// Main function to retrieve data and perform analysis
const main = async () => {
  try {
    const locationData = await getLocationData();
    if (locationData) {
      analyzeLocationData(locationData);
    } else {
      console.log('No location data found.');
    }
  } catch (error) {
    console.error('Error:', error);
  } finally {
    // Close Firebase Admin app to release resources
    admin.app().delete();
  }
};

// Run the main function
main();
