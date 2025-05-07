import { useState } from 'react';
import { Play } from 'lucide-react';
// import { getCollection } from '../lib/mongodb'; // Removed direct MongoDB usage
import { Editor } from '@monaco-editor/react';

export default function ApiQuery() {
  const [input, setInput] = useState('');
  const [generatedQuery, setGeneratedQuery] = useState('');
  const [results, setResults] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    try {
      setLoading(true);
      
      // Store the query via API
      const query = {
        query_text: input,
        query_type: 'API',
        generated_query: JSON.stringify({
          method: 'GET',
          url: '/api/users',
          params: { days: 7 }
        }, null, 2),
        result: [],
        created_at: new Date()
      };
      await fetch('/api/save-query', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(query)
      });
      setGeneratedQuery(query.generated_query);
      setResults([]);

    } catch (error) {
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="py-24 px-4 max-w-4xl mx-auto">
      <h1 className="text-4xl font-bold mb-2 bg-clip-text text-transparent bg-gradient-to-r from-[#00ff00] to-[#00cc00]">
        Text to API Query
      </h1>
      <p className="text-gray-400 mb-8 text-lg">Convert natural language to API requests</p>

      <div className="space-y-6">
        <div className="border border-[#00ff00]/30 rounded-lg p-6 bg-black/30">
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Describe your API request in natural language..."
            className="w-full h-32 bg-black/50 border border-[#00ff00]/30 rounded-md px-4 py-2
              focus:outline-none focus:ring-2 focus:ring-[#00ff00]/50 text-white
              placeholder:text-gray-500 transition-all duration-300 hover:border-[#00ff00]/50"
          />
          <button
            onClick={handleSubmit}
            disabled={loading}
            className="mt-4 w-full bg-[#00ff00]/10 text-[#00ff00] py-3 px-4 rounded-md 
              hover:bg-[#00ff00]/20 transition-all duration-300 hover-glow
              flex items-center justify-center space-x-2 border border-[#00ff00]/30
              disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <Play className="h-5 w-5" />
            <span>{loading ? 'Processing...' : 'Generate API Request'}</span>
          </button>
        </div>

        {generatedQuery && (
          <div className="border border-[#00ff00]/30 rounded-lg overflow-hidden">
            <div className="bg-black/50 px-4 py-2 border-b border-[#00ff00]/30">
              <h3 className="text-[#00ff00] font-semibold">Generated API Request</h3>
            </div>
            <Editor
              height="200px"
              defaultLanguage="json"
              value={generatedQuery}
              theme="vs-dark"
              options={{
                minimap: { enabled: false },
                readOnly: true,
                fontSize: 14,
              }}
            />
          </div>
        )}

        {results && (
          <div className="border border-[#00ff00]/30 rounded-lg overflow-hidden">
            <div className="bg-black/50 px-4 py-2 border-b border-[#00ff00]/30">
              <h3 className="text-[#00ff00] font-semibold">Results</h3>
            </div>
            <div className="p-4 bg-black/30">
              <pre className="whitespace-pre-wrap text-gray-300 font-mono text-sm">
                {JSON.stringify(results, null, 2)}
              </pre>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}