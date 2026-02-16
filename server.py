from flask import Flask, request, jsonify
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

# Load dictionary
with open('banjara-dictionary.json', 'r', encoding='utf-8') as f:
    dictionary_data = json.load(f)

# Health check
@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'Backend is running'})

# Translate endpoint
@app.route('/api/translate', methods=['POST'])
def translate():
    data = request.json
    text = data.get('text', '').strip()
    from_lang = data.get('fromLanguage', '')
    to_lang = data.get('toLanguage', '')
    
    if not text or not from_lang or not to_lang:
        return jsonify({'error': 'Missing required fields'}), 400
    
    text_lower = text.lower()
    translation = None
    matched_entry = None
    
    if from_lang == 'English' and to_lang == 'Banjara':
        for entry in dictionary_data['dictionary']:
            if entry['english'].lower() == text_lower:
                translation = entry['banjara']
                matched_entry = entry
                break
        
        if not translation:
            for entry in dictionary_data['dictionary']:
                if entry['english'].lower() in text_lower or text_lower in entry['english'].lower():
                    translation = entry['banjara']
                    matched_entry = entry
                    break
        
        if not translation:
            translation = f'No translation found for "{text}"'
    
    elif from_lang == 'Banjara' and to_lang == 'English':
        for entry in dictionary_data['dictionary']:
            if entry['banjara'] == text:
                translation = entry['english']
                matched_entry = entry
                break
        
        if not translation:
            translation = f'No translation found for "{text}"'
    
    else:
        translation = 'Language pair not supported'
    
    return jsonify({
        'originalText': text,
        'translatedText': translation,
        'fromLanguage': from_lang,
        'toLanguage': to_lang,
        'matchedEntry': matched_entry
    })

# Get dictionary
@app.route('/api/dictionary', methods=['GET'])
def get_dictionary():
    category = request.args.get('category')
    
    if category:
        filtered = [e for e in dictionary_data['dictionary'] if e['category'] == category]
        return jsonify(filtered)
    
    return jsonify(dictionary_data['dictionary'])

# Search dictionary
@app.route('/api/dictionary/search', methods=['GET'])
def search_dictionary():
    query = request.args.get('query', '').lower()
    language = request.args.get('language', 'English')
    
    if not query:
        return jsonify({'error': 'Query parameter is required'}), 400
    
    results = []
    
    if language == 'English' or not language:
        results = [e for e in dictionary_data['dictionary'] 
                   if query in e['english'].lower() or e['english'].lower().startswith(query)]
    elif language == 'Banjara':
        results = [e for e in dictionary_data['dictionary'] if query in e['banjara']]
    
    return jsonify({
        'query': query,
        'language': language or 'English',
        'resultsCount': len(results),
        'results': results
    })

# Pronunciation endpoint
@app.route('/api/speak', methods=['POST'])
def speak():
    data = request.json
    text = data.get('text', '').strip()
    language = data.get('language', '')
    
    if not text:
        return jsonify({'error': 'Text is required'}), 400
    
    text_lower = text.lower()
    entry = None
    
    if language == 'Banjara' or not language:
        for e in dictionary_data['dictionary']:
            if e['banjara'] == text or e['english'].lower() == text_lower:
                entry = e
                break
    elif language == 'English':
        for e in dictionary_data['dictionary']:
            if e['english'].lower() == text_lower:
                entry = e
                break
    
    if entry:
        return jsonify({
            'text': text,
            'language': language,
            'pronunciation': entry['pronunciation'],
            'banjara': entry['banjara'],
            'english': entry['english'],
            'example': entry['example_bn'] if language == 'Banjara' else entry['example_en']
        })
    else:
        return jsonify({
            'text': text,
            'language': language,
            'pronunciation': 'Pronunciation not available',
            'message': 'Word not found in dictionary'
        })

# Get categories
@app.route('/api/categories', methods=['GET'])
def get_categories():
    categories = list(set(e['category'] for e in dictionary_data['dictionary']))
    return jsonify({'categories': categories})

if __name__ == '__main__':
    print('Banjara Translator Backend is running on http://localhost:5000')
    print('API Endpoints:')
    print('  POST /api/translate - Translate text')
    print('  GET /api/dictionary - Get all dictionary entries')
    print('  GET /api/dictionary/search - Search dictionary')
    print('  POST /api/speak - Get pronunciation')
    print('  GET /api/categories - Get all categories')
    app.run(debug=True, port=5000)
