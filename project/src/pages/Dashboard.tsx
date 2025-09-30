import { BarChart3, Users, Database as DatabaseIcon, Clock, TrendingUp, Loader2 } from 'lucide-react';
import { useState, useEffect } from 'react';

interface HistoryItem {
  id: number;
  query_text: string;
  query_type: string;
  status: string;
  result_count: number;
  execution_time_ms: number;
  created_at: string;
}

interface Stats {
  total_queries: number;
  success_rate: number;
  avg_execution_time: number;
  mysql_count: number;
  mongodb_count: number;
}

export default function Dashboard() {
  const [stats, setStats] = useState<Stats | null>(null);
  const [recentQueries, setRecentQueries] = useState<HistoryItem[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadDashboardData();
    // Refresh every 30 seconds
    const interval = setInterval(loadDashboardData, 30000);
    return () => clearInterval(interval);
  }, []);

  const loadDashboardData = async () => {
    try {
      // Fetch history
      const historyResponse = await fetch('http://localhost:8000/history');
      const historyData = await historyResponse.json();
      
      // Calculate stats
      const total = historyData.length;
      const successful = historyData.filter((q: HistoryItem) => q.status === 'success').length;
      const successRate = total > 0 ? (successful / total) * 100 : 0;
      
      const avgTime = total > 0 
        ? historyData.reduce((sum: number, q: HistoryItem) => sum + (q.execution_time_ms || 0), 0) / total
        : 0;
      
      const mysqlCount = historyData.filter((q: HistoryItem) => q.query_type === 'mysql').length;
      const mongodbCount = historyData.filter((q: HistoryItem) => q.query_type === 'mongodb').length;
      
      setStats({
        total_queries: total,
        success_rate: successRate,
        avg_execution_time: avgTime,
        mysql_count: mysqlCount,
        mongodb_count: mongodbCount
      });
      
      // Get recent 5 queries
      setRecentQueries(historyData.slice(0, 5));
      
    } catch (error) {
      console.error('Failed to load dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  const formatTimeAgo = (timestamp: string) => {
    const date = new Date(timestamp);
    const now = new Date();
    const seconds = Math.floor((now.getTime() - date.getTime()) / 1000);
    
    if (seconds < 60) return 'just now';
    if (seconds < 3600) return `${Math.floor(seconds / 60)} min ago`;
    if (seconds < 86400) return `${Math.floor(seconds / 3600)} hours ago`;
    return `${Math.floor(seconds / 86400)} days ago`;
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <Loader2 className="w-8 h-8 animate-spin text-green-500" />
      </div>
    );
  }

  const metrics = [
    { icon: Users, label: 'Total Queries', value: stats?.total_queries.toString() || '0', change: '' },
    { icon: DatabaseIcon, label: 'MySQL Queries', value: stats?.mysql_count.toString() || '0', change: '' },
    { icon: DatabaseIcon, label: 'MongoDB Queries', value: stats?.mongodb_count.toString() || '0', change: '' },
    { icon: Clock, label: 'Avg. Response', value: `${(stats?.avg_execution_time || 0).toFixed(0)}ms`, change: '' },
    { icon: BarChart3, label: 'Success Rate', value: `${(stats?.success_rate || 0).toFixed(1)}%`, change: '' },
    { icon: TrendingUp, label: 'Active Today', value: recentQueries.length.toString(), change: '' }
  ];

  return (
    <div className="py-24 px-4">
      <h1 className="text-4xl font-bold mb-2 bg-clip-text text-transparent bg-gradient-to-r from-[#00ff00] to-[#00cc00]">
        Dashboard
      </h1>
      <p className="text-gray-400 mb-8 text-lg">Monitor your database interactions</p>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-8">
        {metrics.map(({ icon: Icon, label, value }) => (
          <div key={label} className="border border-[#00ff00]/30 rounded-lg p-6 hover-glow transition-all duration-300 bg-black/30">
            <div className="flex items-center justify-between mb-4">
              <Icon className="h-6 w-6 text-[#00ff00]" />
            </div>
            <p className="text-gray-400 text-sm">{label}</p>
            <p className="text-2xl font-bold text-white mt-1">{value}</p>
          </div>
        ))}
      </div>

      <div className="border border-[#00ff00]/30 rounded-lg p-6 hover-glow transition-all duration-300 bg-black/30">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-xl font-semibold text-[#00ff00]">Recent Queries</h2>
          <button 
            onClick={loadDashboardData}
            className="text-xs text-gray-400 hover:text-green-400 flex items-center gap-1"
          >
            <Loader2 className="w-3 h-3" />
            Refresh
          </button>
        </div>
        <div className="space-y-4">
          {recentQueries.length > 0 ? (
            recentQueries.map((item) => (
              <div key={item.id} className="border-b border-[#00ff00]/10 last:border-0 pb-4 last:pb-0">
                <div className="flex items-center justify-between gap-4">
                  <p className="text-white truncate flex-1">{item.query_text}</p>
                  <div className="flex items-center gap-2">
                    <span className={`text-xs px-2 py-1 rounded-full border ${
                      item.status === 'success' 
                        ? 'text-green-400 border-green-500/30 bg-green-500/10' 
                        : 'text-red-400 border-red-500/30 bg-red-500/10'
                    }`}>
                      {item.status}
                    </span>
                    <span className="text-[#00ff00] text-sm px-2 py-1 rounded-full border border-[#00ff00]/30">
                      {item.query_type.toUpperCase()}
                    </span>
                  </div>
                </div>
                <div className="flex items-center gap-4 mt-2">
                  <p className="text-gray-500 text-xs">{formatTimeAgo(item.created_at)}</p>
                  <p className="text-gray-500 text-xs">⚡ {item.execution_time_ms}ms</p>
                  {item.result_count > 0 && (
                    <p className="text-gray-500 text-xs">📊 {item.result_count} results</p>
                  )}
                </div>
              </div>
            ))
          ) : (
            <p className="text-gray-500 text-center py-4">No queries yet. Start querying to see history!</p>
          )}
        </div>
      </div>
    </div>
  );
}