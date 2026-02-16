# Banjara Translator - Backend Setup Guide

## Overview
Your Banjara Language Translator now has a complete Node.js/Express backend with a dictionary system integrated with the frontend.

## Files Created

### Backend Files:
1. **server.js** - Express server with translation API endpoints
2. **package.json** - Node.js dependencies configuration
3. **banjara-dictionary.json** - Banjara language dictionary with 15+ words

### Updated Frontend Files:
1. **translate.html** - Text-to-text translator connected to backend
2. **speech-translate.html** - Speech translator connected to backend

## Installation & Setup

### Step 1: Install Node.js Dependencies
Open PowerShell in your project directory and run:
```powershell
npm install
```

This will install:
- express (web framework)
- cors (cross-origin requests)
- body-parser (JSON parsing)

### Step 2: Start the Backend Server
In PowerShell, run:
```powershell
npm start
```

You should see:
```
Banjara Translator Backend is running on http://localhost:5000
```

### Step 3: Open Frontend in Browser
1. Open `translate.html` in your browser
2. Select source and target languages
3. Type text and click "Translate" - it will now use the backend API

## API Endpoints

### 1. Translate Text
**POST** `/api/translate`
```json
{
  "text": "hello",
  "fromLanguage": "English",
  "toLanguage": "Banjara"
}
```
Response:
```json
{
  "originalText": "hello",
  "translatedText": "नमस्ते",
  "fromLanguage": "English",
  "toLanguage": "Banjara",
  "matchedEntry": {...}
}
```

### 2. Get Dictionary
**GET** `/api/dictionary`
Returns all 15 dictionary entries with English, Banjara, pronunciation, examples, and categories.

### 3. Search Dictionary
**GET** `/api/dictionary/search?query=water&language=English`
Searches for words in the dictionary.

### 4. Get Pronunciation (Text-to-Speech)
**POST** `/api/speak`
```json
{
  "text": "hello",
  "language": "English"
}
```

### 5. Get Categories
**GET** `/api/categories`
Returns all word categories (greeting, noun, verb, etc.)

## Supported Languages
- **English**
- **Banjara**

## Current Dictionary (15 words)
The dictionary includes common words organized by category:
- **Greetings**: hello, goodbye
- **Politeness**: thank you, please, sorry
- **Common Nouns**: water, food, family, home, day, night, morning
- **Verbs**: love
- **Responses**: yes, no

## Expanding the Dictionary

To add more words, edit `banjara-dictionary.json`:

```json
{
  "id": 16,
  "english": "water",
  "banjara": "पानी",
  "pronunciation": "paani",
  "example_en": "I need water",
  "example_bn": "मुझे पानी चाहिए",
  "category": "noun"
}
```

Then restart the server with `npm start`.

## Features

### Text-to-Text Translation
- Translate between English and Banjara
- Copy translated text to clipboard
- Swap source/target languages
- Character counter (500 character limit)
- Real-time error handling

### Speech-to-Text Translation
- Speech recognition using Web Speech API
- Real-time translation from speech
- Select source and target languages
- Shows original speech and translation

## Troubleshooting

### Backend won't start
- Make sure Node.js is installed: `node --version`
- Delete `node_modules` folder and run `npm install` again
- Check if port 5000 is already in use

### CORS Error in Browser
- Make sure backend is running on `http://localhost:5000`
- Check browser console for error details

### Translation returns "No translation found"
- Word may not be in the dictionary
- Check `banjara-dictionary.json` for available words
- Add new words to expand the dictionary

### Microphone not working
- Allow browser microphone permission
- Use Chrome, Firefox, or Edge (Safari has limited support)
- Check Web Speech API support: https://caniuse.com/speech-recognition

## File Locations
```
c:\Users\pgane\OneDrive\Desktop\Major Project\
├── server.js
├── package.json
├── banjara-dictionary.json
├── translate.html
├── speech-translate.html
├── index.html
├── login.html
├── signup.html
├── styles.css
└── script.js
```

## Production Deployment

For production use:
1. Update API_BASE_URL in HTML files to your production server
2. Use environment variables for configuration
3. Add authentication and rate limiting
4. Deploy on platforms like Heroku, AWS, or DigitalOcean

## Support
For issues or to add more dictionary entries, check the API logs in PowerShell when running the server.
