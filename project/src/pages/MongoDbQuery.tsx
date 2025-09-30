import { useState } from 'react';
import { Play, AlertTriangle, Zap } from 'lucide-react';
import { Editor } from '@monaco-editor/react';
import { post } from '../lib/api';

interface MongoDBResult {
  operation: string;
  count?: number;
  documents?: any[];
  inserted_id?: string;
  acknowledged?: boolean;
  matched_count?: number;
  modified_count?: number;
  deleted_count?: number;
}

export default function MongoDbQuery() {
  const [input, setInput] = useState(() => {
    return localStorage.getItem('mongoQueryInput') || '';
  });
  const [generatedQuery, setGeneratedQuery] = useState(() => {
    return localStorage.getItem('mongoQueryGenerated') || '';
  });
  const [results, setResults] = useState<MongoDBResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [executing, setExecuting] = useState(false);
  const [queryWarning, setQueryWarning] = useState<string | null>(null);

  // Save input to localStorage
  const handleInputChange = (value: string) => {
    setInput(value);
    localStorage.setItem('mongoQueryInput', value);
  };

  // Save generated query to localStorage
  const handleGeneratedQueryChange = (value: string) => {
    setGeneratedQuery(value);
    localStorage.setItem('mongoQueryGenerated', value);
  };

  const checkDangerousQuery = (query: string): string | null => {
    const lowerQuery = query.toLowerCase();
    
    if (lowerQuery.includes('deleteMany({})') || lowerQuery.includes('remove({})')) {
      return '⚠️ WARNING: This query will DELETE ALL documents from the collection! This action cannot be undone.';
    }
    
    if (lowerQuery.includes('updateMany({})')) {
      return '⚠️ WARNING: This query will UPDATE ALL documents in the collection! This may cause data loss.';
    }
    
    if (lowerQuery.includes('drop()')) {
      return '⚠️ CRITICAL WARNING: DROP will permanently delete the entire collection! This action cannot be undone.';
    }
    
    return null;
  };

  const handleSubmit = async () => {
    setError(null);
    handleGeneratedQueryChange('');
    setResults(null);
    setQueryWarning(null);
    
    const startTime = performance.now();
    let querySuccess = false;
    let resultCount = 0;
    let errorMessage = '';
    let bestQuery = '';
    
    try {
      setLoading(true);

      // 1) Get schema
      const schema = await post<{ db_type: string }, any>('/mongodb/inspect', {
        db_type: 'mongodb'
      });

      // 2) Generate MongoDB query candidates
      const genResult = await post<any, any>('/mongodb/generate', {
        text: input,
        db_schema: schema,
        n_candidates: 1
      });

      const candidates = genResult.candidates || [];
      if (candidates.length === 0) {
        throw new Error('No MongoDB queries generated');
      }

      const best = candidates[0];
      bestQuery = best;
      handleGeneratedQueryChange(best);
      
      // Check if generated query is dangerous
      const warning = checkDangerousQuery(best);
      if (warning) {
        setQueryWarning(warning);
      }

      // Mark as successful
      querySuccess = true;
      resultCount = 0; // MongoDB results vary
    } catch (e: any) {
      console.error('Error:', e);
      errorMessage = e?.message || 'Something went wrong';
      setError(errorMessage);
    } finally {
      setLoading(false);
      
      // Calculate execution time
      const executionTime = performance.now() - startTime;
      
      // Save to history
      if (bestQuery) {
        try {
          await post('/history/save', {
            query_text: input,
            generated_sql: bestQuery,
            query_type: 'mongodb',
            status: querySuccess ? 'success' : 'error',
            result_count: resultCount,
            error_message: errorMessage || null,
            execution_time_ms: Math.round(executionTime)
          });
        } catch (historyError) {
          console.error('Failed to save to history:', historyError);
        }
      }
    }
  };

  const handleExecute = async () => {
    if (!generatedQuery) return;

    setExecuting(true);
    setError(null);
    setResults(null);

    try {
      // Parse the MongoDB query
      const match = generatedQuery.match(/db\.(\w+)\.(find|findOne|insertOne|updateOne|deleteOne|aggregate)\((.*)\)/s);
      
      if (!match) {
        throw new Error('Could not parse MongoDB query format');
      }

      const collection = match[1];
      const operation = match[2];
      let queryObj = {};

      try {
        // Try to parse the query parameter
        const queryStr = match[3].trim();
        if (queryStr && queryStr !== '') {
          queryObj = JSON.parse(queryStr);
        }
      } catch (parseError) {
        throw new Error('Invalid query format. Please ensure valid JSON.');
      }

      // Execute the query
      const response = await fetch('http://localhost:8000/mongodb/execute', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          db_name: 'mydb',
          collection_name: collection,
          query: queryObj,
          operation: operation === 'findOne' ? 'find' : operation,
          document: ['insertOne', 'updateOne'].includes(operation) ? queryObj : null
        })
      });

      const data = await response.json();

      if (response.ok) {
        setResults(data);
      } else {
        setError(data.detail || 'Failed to execute query');
      }
    } catch (err: any) {
      setError(err.message || 'Failed to execute query');
    } finally {
      setExecuting(false);
    }
  };

  return (
    <div className="py-24 px-4 max-w-4xl mx-auto">
      <h1 className="text-4xl font-bold mb-2 bg-clip-text text-transparent bg-gradient-to-r from-[#00ff00] to-[#00cc00]">
        Text to MongoDB Query
      </h1>
      <p className="text-gray-400 mb-8 text-lg">Convert natural language to MongoDB queries</p>

      <div className="space-y-6">
        <div className="border border-[#00ff00]/30 rounded-lg p-6 bg-black/30">
          <textarea
            value={input}
            onChange={(e) => handleInputChange(e.target.value)}
            placeholder="Describe your query in natural language...&#10;Examples:&#10;• Find all active users&#10;• Get products with price greater than 100&#10;• Show orders from last month"
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
            <span>{loading ? 'Processing...' : 'Generate MongoDB Query'}</span>
          </button>
        </div>

        {queryWarning && (
          <div className="border border-red-500/50 rounded-lg bg-red-900/20 p-5 animate-pulse">
            <div className="flex items-start gap-3">
              <AlertTriangle className="w-8 h-8 text-red-500 flex-shrink-0" />
              <div className="flex-1">
                <h3 className="text-red-400 font-bold text-lg mb-2 flex items-center gap-2">
                  Dangerous Query Detected!
                </h3>
                <p className="text-red-200 font-semibold mb-2">{queryWarning}</p>
                <div className="bg-red-950/50 border border-red-500/30 rounded p-3 mt-3">
                  <p className="text-red-300 text-sm">
                    <strong className="text-red-400">💡 Recommendation:</strong> This query is NOT recommended for production use. Consider adding filter criteria to limit which documents are affected, or modify your natural language request to be more specific.
                  </p>
                </div>
              </div>
            </div>
          </div>
        )}

        {generatedQuery && (
          <div className="border border-[#00ff00]/30 rounded-lg overflow-hidden">
            <div className="bg-black/50 px-4 py-2 border-b border-[#00ff00]/30 flex items-center justify-between">
              <h3 className="text-[#00ff00] font-semibold">Generated MongoDB Query</h3>
              <button
                onClick={handleExecute}
                disabled={executing}
                className="bg-[#00ff00]/10 text-[#00ff00] px-4 py-1.5 rounded-md hover:bg-[#00ff00]/20 
                  transition-all duration-300 flex items-center gap-2 border border-[#00ff00]/30
                  disabled:opacity-50 disabled:cursor-not-allowed text-sm"
              >
                <Zap className="w-4 h-4" />
                {executing ? 'Executing...' : 'Execute Query'}
              </button>
            </div>
            <Editor
              height="200px"
              defaultLanguage="javascript"
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
          <div className="border border-[#00ff00]/30 rounded-lg overflow-hidden bg-black/30">
            <div className="bg-black/50 px-4 py-3 border-b border-[#00ff00]/30">
              <h3 className="text-[#00ff00] font-semibold">Query Results</h3>
              <p className="text-xs text-gray-400 mt-1">
                {results.documents ? `${results.documents.length} documents found` : 'Query executed successfully'}
              </p>
            </div>
            <div className="p-4 max-h-96 overflow-auto">
              {results.documents && results.documents.length > 0 ? (
                <pre className="text-sm text-gray-300">
                  {JSON.stringify(results.documents, null, 2)}
                </pre>
              ) : (
                <div className="text-center py-8">
                  <p className="text-gray-400">
                    {results.count !== undefined && `Count: ${results.count}`}
                    {results.matched_count !== undefined && `Matched: ${results.matched_count}, Modified: ${results.modified_count}`}
                    {results.deleted_count !== undefined && `Deleted: ${results.deleted_count} documents`}
                  </p>
                </div>
              )}
            </div>
          </div>
        )}

        {error && (
          <div className="border border-red-500/30 rounded-lg p-4 bg-red-900/20">
            <h3 className="text-red-400 font-semibold mb-2">Error</h3>
            <p className="text-red-300">{error}</p>
          </div>
        )}

        {!generatedQuery && !error && !loading && (
          <div className="border border-[#00ff00]/20 rounded-lg p-8 text-center bg-black/20">
            <p className="text-gray-400 text-lg mb-2">Enter a question above to generate MongoDB query</p>
            <p className="text-gray-500 text-sm">Try asking: "Find all active users" or "Get products above $100"</p>
          </div>
        )}
      </div>
    </div>
  );
}
