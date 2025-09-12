import { useState } from 'react';
import { Play } from 'lucide-react';
import { Editor } from '@monaco-editor/react';
import { post } from '../lib/api';

export default function SqlQuery() {
  const [input, setInput] = useState('');
  const [generatedQuery, setGeneratedQuery] = useState('');
  const [results, setResults] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    setError(null);
    setGeneratedQuery('');
    setResults(null);
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
      setGeneratedQuery(best);

      // 5) Execute best query
      const execRes = await post<{ query: string; db_type: string }, any>('/execute', {
        query: best,
        db_type: 'mysql',
      });
      setResults(execRes);
    } catch (e: any) {
      console.error('Error:', e);
      setError(e?.message || 'Something went wrong');
    } finally {
      setLoading(false);
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
            onChange={(e) => setInput(e.target.value)}
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