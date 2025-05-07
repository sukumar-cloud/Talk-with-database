import { BarChart3, Users, Database as DatabaseIcon, Clock } from 'lucide-react';

export default function Dashboard() {
  const metrics = [
    { icon: Users, label: 'Total Queries', value: '1,234', change: '+12%' },
    { icon: DatabaseIcon, label: 'Databases', value: '5', change: '+1' },
    { icon: Clock, label: 'Avg. Response', value: '0.8s', change: '-0.2s' },
    { icon: BarChart3, label: 'Success Rate', value: '99.9%', change: '+0.5%' }
  ];

  const recentQueries = [
    { query: 'Show active users from last month', type: 'SQL', timestamp: '2 hours ago' },
    { query: 'Find orders with status pending', type: 'MongoDB', timestamp: '5 hours ago' },
    { query: 'Get user registration trends', type: 'API', timestamp: '1 day ago' }
  ];

  return (
    <div className="py-24 px-4">
      <h1 className="text-4xl font-bold mb-2 bg-clip-text text-transparent bg-gradient-to-r from-[#00ff00] to-[#00cc00]">
        Dashboard
      </h1>
      <p className="text-gray-400 mb-8 text-lg">Monitor your database interactions</p>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        {metrics.map(({ icon: Icon, label, value, change }) => (
          <div key={label} className="border border-[#00ff00]/30 rounded-lg p-6 hover-glow transition-all duration-300 bg-black/30">
            <div className="flex items-center justify-between mb-4">
              <Icon className="h-6 w-6 text-[#00ff00]" />
              <span className={`text-sm ${change.startsWith('+') ? 'text-[#00ff00]' : 'text-red-500'}`}>
                {change}
              </span>
            </div>
            <p className="text-gray-400 text-sm">{label}</p>
            <p className="text-2xl font-bold text-white mt-1">{value}</p>
          </div>
        ))}
      </div>

      <div className="border border-[#00ff00]/30 rounded-lg p-6 hover-glow transition-all duration-300 bg-black/30">
        <h2 className="text-xl font-semibold text-[#00ff00] mb-4">Recent Queries</h2>
        <div className="space-y-4">
          {recentQueries.map((item, index) => (
            <div key={index} className="border-b border-[#00ff00]/10 last:border-0 pb-4 last:pb-0">
              <div className="flex items-center justify-between">
                <p className="text-white">{item.query}</p>
                <span className="text-[#00ff00] text-sm px-2 py-1 rounded-full border border-[#00ff00]/30">
                  {item.type}
                </span>
              </div>
              <p className="text-gray-500 text-sm mt-1">{item.timestamp}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}