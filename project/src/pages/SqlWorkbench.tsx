import { useState, useEffect } from 'react';
import { Play, Database, Table2, ChevronRight, ChevronDown, Loader2 } from 'lucide-react';
import { post } from '../lib/api';

interface Column {
  name: string;
  type: string;
  nullable: string;
  key: string;
}

interface SchemaData {
  db: string;
  tables: string[];
  columns: Record<string, Column[]>;
  primary_keys: Record<string, string[]>;
  foreign_keys: any[];
}

export default function SqlWorkbench() {
  const [schema, setSchema] = useState<SchemaData | null>(null);
  const [query, setQuery] = useState(() => {
    // Load saved query from localStorage on mount
    return localStorage.getItem('sqlWorkbenchQuery') || 'SELECT * FROM customers LIMIT 10;';
  });
  const [results, setResults] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [schemaLoading, setSchemaLoading] = useState(false);
  const [error, setError] = useState('');
  const [expandedTables, setExpandedTables] = useState<Set<string>>(new Set());

  // Save query to localStorage whenever it changes
  const handleQueryChange = (value: string) => {
    setQuery(value);
    localStorage.setItem('sqlWorkbenchQuery', value);
  };

  useEffect(() => {
    loadSchema();
  }, []);

  const loadSchema = async () => {
    setSchemaLoading(true);
    try {
      const data = await post<{ db_type: string }, SchemaData>('/schema/inspect', {
        db_type: 'mysql'
      });
      setSchema(data);
      // Auto-expand first table
      if (data.tables.length > 0) {
        setExpandedTables(new Set([data.tables[0]]));
      }
    } catch (err: any) {
      console.error('Failed to load schema:', err);
    } finally {
      setSchemaLoading(false);
    }
  };

  const toggleTable = (tableName: string) => {
    const newExpanded = new Set(expandedTables);
    if (newExpanded.has(tableName)) {
      newExpanded.delete(tableName);
    } else {
      newExpanded.add(tableName);
    }
    setExpandedTables(newExpanded);
  };

  const insertTableName = (tableName: string) => {
    setQuery(prev => prev + ` ${tableName}`);
  };

  const insertColumnName = (tableName: string, columnName: string) => {
    setQuery(prev => prev + ` ${tableName}.${columnName}`);
  };

  const isDangerousQuery = (sql: string): { dangerous: boolean; reason: string } => {
    const upperQuery = sql.trim().toUpperCase();
    
    // Check for DELETE without WHERE
    if (upperQuery.startsWith('DELETE') && !upperQuery.includes('WHERE')) {
      return { dangerous: true, reason: 'DELETE without WHERE clause will delete ALL rows!' };
    }
    
    // Check for UPDATE without WHERE
    if (upperQuery.startsWith('UPDATE') && !upperQuery.includes('WHERE')) {
      return { dangerous: true, reason: 'UPDATE without WHERE clause will modify ALL rows!' };
    }
    
    // Check for TRUNCATE
    if (upperQuery.includes('TRUNCATE')) {
      return { dangerous: true, reason: 'TRUNCATE will permanently delete all data from the table!' };
    }
    
    // Check for DROP
    if (upperQuery.includes('DROP TABLE') || upperQuery.includes('DROP DATABASE')) {
      return { dangerous: true, reason: 'DROP will permanently delete the entire table/database!' };
    }
    
    return { dangerous: false, reason: '' };
  };

  const executeQuery = async () => {
    if (!query.trim()) return;
    
    // Check if query is dangerous
    const dangerCheck = isDangerousQuery(query);
    if (dangerCheck.dangerous) {
      const confirmed = window.confirm(
        `⚠️ DANGEROUS OPERATION WARNING!\n\n${dangerCheck.reason}\n\nThis action cannot be undone.\n\nAre you absolutely sure you want to execute this query?\n\nQuery: ${query.trim().substring(0, 100)}...`
      );
      
      if (!confirmed) {
        return; // User canceled
      }
    }
    
    const startTime = performance.now();
    let querySuccess = false;
    let resultCount = 0;
    let errorMessage = '';
    
    setLoading(true);
    setError('');
    setResults(null);

    try {
      const result = await post<{ query: string; db_type: string }, any>('/execute', {
        query: query.trim(),
        db_type: 'mysql'
      });

      if (result.error) {
        errorMessage = result.error;
        setError(result.error);
      } else {
        setResults(result);
        querySuccess = true;
        resultCount = result.rows?.length || 0;
      }
    } catch (err: any) {
      errorMessage = err.message || 'Failed to execute query';
      setError(errorMessage);
    } finally {
      setLoading(false);
      
      // Calculate execution time
      const executionTime = performance.now() - startTime;
      
      // Save to history
      try {
        await post('/history/save', {
          query_text: `Direct SQL: ${query.trim().substring(0, 100)}...`,
          generated_sql: query.trim(),
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
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
      e.preventDefault();
      executeQuery();
    }
  };

  return (
    <div className="flex bg-gradient-to-br from-gray-900 via-black to-gray-900" style={{ height: 'calc(100vh - 4rem)' }}>
      {/* Left Sidebar - Schema Browser */}
      <div className="w-80 bg-gray-900 border-r border-green-500/30 flex flex-col shadow-lg">
        <div className="p-4 border-b border-green-500/30 bg-gray-800/50">
          <h2 className="text-lg font-semibold text-green-400 flex items-center gap-2">
            <Database className="w-5 h-5 text-green-500" />
            {schema?.db || 'Database'}
          </h2>
          <p className="text-xs text-gray-400 mt-1">
            {schema?.tables.length || 0} tables
          </p>
        </div>

        <div className="flex-1 overflow-y-auto">
          {schemaLoading ? (
            <div className="flex items-center justify-center p-8">
              <Loader2 className="w-6 h-6 animate-spin text-green-500" />
            </div>
          ) : (
            <div className="p-2">
              {schema?.tables.map((tableName) => {
                const isExpanded = expandedTables.has(tableName);
                const columns = schema.columns[tableName] || [];
                const primaryKeys = schema.primary_keys[tableName] || [];

                return (
                  <div key={tableName} className="mb-1">
                    <button
                      onClick={() => toggleTable(tableName)}
                      onDoubleClick={() => insertTableName(tableName)}
                      className="w-full flex items-center gap-2 px-2 py-1.5 text-sm hover:bg-green-500/10 rounded transition-colors text-left"
                      title="Click to expand, double-click to insert"
                    >
                      {isExpanded ? (
                        <ChevronDown className="w-4 h-4 text-gray-400" />
                      ) : (
                        <ChevronRight className="w-4 h-4 text-gray-400" />
                      )}
                      <Table2 className="w-4 h-4 text-green-500" />
                      <span className="font-medium text-gray-200">{tableName}</span>
                    </button>

                    {isExpanded && (
                      <div className="ml-8 mt-1 space-y-0.5">
                        {columns.map((col) => (
                          <button
                            key={col.name}
                            onDoubleClick={() => insertColumnName(tableName, col.name)}
                            className="w-full flex items-center justify-between px-2 py-1 text-xs hover:bg-green-500/20 rounded transition-colors text-left group"
                            title="Double-click to insert"
                          >
                            <div className="flex items-center gap-2">
                              <span className={`font-medium ${
                                primaryKeys.includes(col.name) 
                                  ? 'text-yellow-400' 
                                  : 'text-gray-300'
                              }`}>
                                {col.name}
                              </span>
                              {primaryKeys.includes(col.name) && (
                                <span className="text-[10px] bg-yellow-500/20 text-yellow-400 px-1 rounded">PK</span>
                              )}
                            </div>
                            <span className="text-gray-500">{col.type}</span>
                          </button>
                        ))}
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
          )}
        </div>

        <div className="p-3 border-t border-green-500/30 text-xs text-gray-400 bg-gray-800/30">
          <p className="flex items-center gap-1"><span className="text-green-500">💡</span> Double-click tables/columns to insert</p>
          <p className="mt-1 flex items-center gap-1"><span className="text-green-500">⌨️</span> Ctrl+Enter to execute</p>
        </div>
      </div>

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col">
        {/* Query Editor */}
        <div className="bg-gray-800 border-b border-green-500/30 p-4">
          <div className="flex items-center justify-between mb-2">
            <div className="flex items-center gap-3">
              <h3 className="text-sm font-semibold text-green-400">Query Editor</h3>
              {isDangerousQuery(query).dangerous && (
                <span className="text-xs px-2 py-1 bg-red-500/20 text-red-400 border border-red-500/50 rounded flex items-center gap-1">
                  ⚠️ Dangerous Query - Confirmation Required
                </span>
              )}
            </div>
            <button
              onClick={executeQuery}
              disabled={loading || !query.trim()}
              className="flex items-center gap-3 px-5 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:bg-gray-600 disabled:cursor-not-allowed transition-colors shadow-lg shadow-green-500/20"
            >
              {loading ? (
                <>
                  <Loader2 className="w-4 h-4 animate-spin" />
                  <span>Executing...</span>
                </>
              ) : (
                <>
                  <Play className="w-4 h-4" />
                  <span>Run Query</span>
                </>
              )}
            </button>
          </div>
          
          <textarea
            value={query}
            onChange={(e) => handleQueryChange(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Enter your SQL query here... (Ctrl+Enter to execute)"
            className="w-full h-32 p-3 bg-gray-900 border border-green-500/30 rounded-lg font-mono text-sm text-gray-200 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-green-500 resize-none"
          />
        </div>

        {/* Results Panel */}
        <div className="flex-1 overflow-auto p-4 bg-gradient-to-br from-gray-900 via-black to-gray-900">
          {error && (
            <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg mb-4">
              <p className="font-semibold">Error</p>
              <p className="text-sm mt-1">{error}</p>
            </div>
          )}

          {results && !error && (
            <div className="bg-gray-800 rounded-lg shadow-lg border border-green-500/30">
              <div className="p-4 border-b border-green-500/30 bg-gray-900/50">
                <h3 className="text-sm font-semibold text-green-400">
                  Results {results.rows ? `(${results.rows.length} rows)` : ''}
                </h3>
              </div>

              {results.rows && results.rows.length > 0 ? (
                <div className="overflow-x-auto">
                  <table className="w-full text-sm">
                    <thead className="bg-gray-900 border-b border-green-500/30">
                      <tr>
                        {Object.keys(results.rows[0]).map((key) => (
                          <th
                            key={key}
                            className="px-4 py-3 text-left font-semibold text-green-400 whitespace-nowrap"
                          >
                            {key}
                          </th>
                        ))}
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-green-500/20">
                      {results.rows.map((row: any, idx: number) => (
                        <tr key={idx} className="hover:bg-green-500/10 transition-colors">
                          {Object.values(row).map((value: any, colIdx: number) => (
                            <td
                              key={colIdx}
                              className="px-4 py-3 text-gray-300 whitespace-nowrap"
                            >
                              {value === null ? (
                                <span className="text-gray-500 italic">NULL</span>
                              ) : typeof value === 'object' ? (
                                JSON.stringify(value)
                              ) : (
                                String(value)
                              )}
                            </td>
                          ))}
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              ) : results.row_count !== undefined ? (
                <div className="p-8 text-center text-gray-400">
                  <p>Query executed successfully.</p>
                  <p className="text-sm mt-1 text-green-400">Rows affected: {results.row_count}</p>
                </div>
              ) : (
                <div className="p-8 text-center text-gray-500">
                  <p>No results to display</p>
                </div>
              )}
            </div>
          )}

          {!results && !error && !loading && (
            <div className="flex items-center justify-center h-full text-gray-500">
              <div className="text-center">
                <Database className="w-16 h-16 mx-auto mb-4 opacity-30 text-green-500" />
                <p className="text-lg text-gray-400">Enter a query and click Run to see results</p>
                <p className="text-sm mt-2 text-gray-500">or press <span className="text-green-500">Ctrl+Enter</span></p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
