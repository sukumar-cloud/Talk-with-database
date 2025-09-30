import { useState } from 'react';
import { Play, AlertTriangle } from 'lucide-react';
import { Editor } from '@monaco-editor/react';
import { post } from '../lib/api';

export default function SqlQuery() {
  const [input, setInput] = useState(() => {
    // Load saved query from localStorage on mount
    return localStorage.getItem('sqlQueryInput') || '';
  });
  const [generatedQuery, setGeneratedQuery] = useState(() => {
    return localStorage.getItem('sqlQueryGenerated') || '';
  });
  const [results, setResults] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [queryWarning, setQueryWarning] = useState<string | null>(null);

  // Save query to localStorage whenever it changes
  const handleInputChange = (value: string) => {
    setInput(value);
    localStorage.setItem('sqlQueryInput', value);
  };

  // Save generated query to localStorage
  const handleGeneratedQueryChange = (value: string) => {
    setGeneratedQuery(value);
    localStorage.setItem('sqlQueryGenerated', value);
  };

  const checkDangerousQuery = (sql: string): string | null => {
    const upperQuery = sql.trim().toUpperCase();
    
    if (upperQuery.startsWith('DELETE') && !upperQuery.includes('WHERE')) {
      return '⚠️ WARNING: This query will DELETE ALL rows from the table! This action cannot be undone.';
    }
    
    if (upperQuery.startsWith('UPDATE') && !upperQuery.includes('WHERE')) {
      return '⚠️ WARNING: This query will UPDATE ALL rows in the table! This may cause data loss.';
    }
    
    if (upperQuery.includes('TRUNCATE')) {
      return '⚠️ WARNING: TRUNCATE will permanently delete all data from the table! This action cannot be undone.';
    }
    
    if (upperQuery.includes('DROP TABLE') || upperQuery.includes('DROP DATABASE')) {
      return '⚠️ CRITICAL WARNING: DROP will permanently delete the entire table/database! This action cannot be undone.';
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
      if (!input.trim()) {
        throw new Error('Please enter a natural language request.');
      }

      // 1) Inspect schema from backend (MySQL default)
      const schema = await post<{ db_type: string }, any>('/schema/inspect', { db_type: 'mysql' });

      // 2) Generate candidates with Mixtral (server decides provider)
      const gen = await post<any, { candidates: string[]; provider: string }>(
        '/generate',
        {
          text: input,
          db_type: 'mysql',
          schema,
          n_candidates: 5,
        }
      );
      const candidates = gen.candidates || [];
      if (!candidates.length) throw new Error('No candidates generated.');


      // 3) Validate candidates (safety)
      await post<{ candidates: string[]; db_type: string }, any>('/validate', {
        candidates,
        db_type: 'mysql',
      });

      // 4) Rank candidates
      const ranking = await post<any, { ranked: Array<{ query: string; score: number }> }>(
        '/rank',
        {
          text: input,
          candidates,
          schema,
          db_type: 'mysql',
        }
      );
      const best = ranking.ranked?.[0]?.query || candidates[0];
      bestQuery = best;
      handleGeneratedQueryChange(best);
      
      // Check if generated query is dangerous
      const warning = checkDangerousQuery(best);
      if (warning) {
        setQueryWarning(warning);
      }

      // 5) Execute best query
      const execRes = await post<{ query: string; db_type: string }, any>('/execute', {
        query: best,
        db_type: 'mysql',
      });
      setResults(execRes);
      
      // Mark as successful
      querySuccess = true;
      resultCount = execRes.rows?.length || 0;
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
            query_type: 'mysql',
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

  return (
    <div className="py-24 px-4 max-w-4xl mx-auto">
      <h1 className="text-4xl font-bold mb-2 bg-clip-text text-transparent bg-gradient-to-r from-[#00ff00] to-[#00cc00]">
        Text to SQL Query
      </h1>
      <p className="text-gray-400 mb-8 text-lg">Convert natural language to SQL queries</p>

      <div className="space-y-6">
        <div className="border border-[#00ff00]/30 rounded-lg p-6 bg-black/30">
          <textarea
            value={input}
            onChange={(e) => handleInputChange(e.target.value)}
            placeholder="Describe your query in natural language..."
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
            <span>{loading ? 'Processing...' : 'Generate SQL'}</span>
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
                    <strong className="text-red-400">💡 Recommendation:</strong> This query is NOT recommended for production use. Consider adding a WHERE clause to limit which rows are affected, or modify your natural language request to be more specific.
                  </p>
                </div>
              </div>
            </div>
          </div>
        )}

        {generatedQuery && (
          <div className="border border-[#00ff00]/30 rounded-lg overflow-hidden">
            <div className="bg-black/50 px-4 py-2 border-b border-[#00ff00]/30">
              <h3 className="text-[#00ff00] font-semibold">Generated SQL Query</h3>
            </div>
            <Editor
              height="200px"
              defaultLanguage="sql"
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

        {error && (
          <div className="border border-red-500/40 rounded-lg p-4 bg-red-900/20">
            <div className="text-red-400 font-mono text-sm">{error}</div>
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