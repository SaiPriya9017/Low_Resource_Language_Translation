const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');
const dictionary = require('./banjara-dictionary.json');

const app = express();
const PORT = process.env.PORT || 5000;

// Middleware
app.use(cors());
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

// Serve static files from the current directory (for frontend access)
app.use(express.static(__dirname));

// Health check endpoint
app.get('/api/health', (req, res) => {
  res.json({ status: 'Backend is running' });
});

// Translate text endpoint
app.post('/api/translate', (req, res) => {
  const { text, fromLanguage, toLanguage } = req.body;

  if (!text || !fromLanguage || !toLanguage) {
    return res.status(400).json({ 
      error: 'Missing required fields: text, fromLanguage, toLanguage' 
    });
  }

  const textLower = text.toLowerCase().trim();
  let translation = null;
  let matchedEntry = null;

  if (fromLanguage === 'English' && toLanguage === 'Banjara') {
    // Search for English to Banjara translation
    matchedEntry = dictionary.dictionary.find(
      entry => entry.english.toLowerCase() === textLower
    );
    
    if (matchedEntry) {
      translation = matchedEntry.banjara;
    } else {
      // If no exact match, try to find partial matches
      const partialMatch = dictionary.dictionary.find(
        entry => entry.english.toLowerCase().includes(textLower) ||
                 textLower.includes(entry.english.toLowerCase())
      );
      translation = partialMatch ? partialMatch.banjara : `No translation found for "${text}"`;
    }
  } else if (fromLanguage === 'Banjara' && toLanguage === 'English') {
    // Search for Banjara to English translation
    matchedEntry = dictionary.dictionary.find(
      entry => entry.banjara === text
    );
    
    if (matchedEntry) {
      translation = matchedEntry.english;
    } else {
      translation = `No translation found for "${text}"`;
    }
  } else {
    translation = 'Language pair not supported';
  }

  res.json({
    originalText: text,
    translatedText: translation,
    fromLanguage,
    toLanguage,
    matchedEntry: matchedEntry || null
  });
});

// Get dictionary entries endpoint
app.get('/api/dictionary', (req, res) => {
  const category = req.query.category;
  
  if (category) {
    const filtered = dictionary.dictionary.filter(
      entry => entry.category === category
    );
    return res.json(filtered);
  }
  
  res.json(dictionary.dictionary);
});

// Search dictionary endpoint
app.get('/api/dictionary/search', (req, res) => {
  const { query, language } = req.query;

  if (!query) {
    return res.status(400).json({ error: 'Query parameter is required' });
  }

  const queryLower = query.toLowerCase();
  let results = [];

  if (language === 'English' || !language) {
    results = dictionary.dictionary.filter(
      entry => entry.english.toLowerCase().includes(queryLower) ||
               entry.english.toLowerCase().startsWith(queryLower)
    );
  } else if (language === 'Banjara') {
    results = dictionary.dictionary.filter(
      entry => entry.banjara.includes(query)
    );
  }

  res.json({
    query,
    language: language || 'English',
    resultsCount: results.length,
    results
  });
});

// Text-to-Speech endpoint (returns pronunciation and audio info)
app.post('/api/speak', (req, res) => {
  const { text, language } = req.body;

  if (!text) {
    return res.status(400).json({ error: 'Text is required' });
  }

  const textLower = text.toLowerCase().trim();
  let entry = null;

  if (language === 'Banjara' || !language) {
    entry = dictionary.dictionary.find(
      e => e.banjara === text || e.english.toLowerCase() === textLower
    );
  } else if (language === 'English') {
    entry = dictionary.dictionary.find(
      e => e.english.toLowerCase() === textLower
    );
  }

  if (entry) {
    res.json({
      text,
      language,
      pronunciation: entry.pronunciation,
      banjara: entry.banjara,
      english: entry.english,
      example: language === 'Banjara' ? entry.example_bn : entry.example_en
    });
  } else {
    res.json({
      text,
      language,
      pronunciation: 'Pronunciation not available',
      message: 'Word not found in dictionary'
    });
  }
});

// Get all categories
app.get('/api/categories', (req, res) => {
  const categories = [...new Set(dictionary.dictionary.map(entry => entry.category))];
  res.json({ categories });
});

// Error handling middleware
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({ error: 'Internal server error' });
});

// Start server
app.listen(PORT, () => {
  console.log(`Banjara Translator Backend is running on http://localhost:${PORT}`);
  console.log(`API Documentation:`);
  console.log(`  POST /api/translate - Translate text`);
  console.log(`  GET /api/dictionary - Get all dictionary entries`);
  console.log(`  GET /api/dictionary/search - Search dictionary`);
  console.log(`  POST /api/speak - Get pronunciation`);
  console.log(`  GET /api/categories - Get all categories`);
});
