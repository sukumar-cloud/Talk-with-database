import { Calendar, Search } from 'lucide-react';

export default function History() {
  const historyItems = [
    {
      query: "Find all users who made a purchase in the last month",
      timestamp: "2024-03-15 14:30",
      type: "SQL",
      status: "success"
    },
    {
      query: "Get products with stock less than 10",
      timestamp: "2024-03-14 09:15",
      type: "MongoDB",
      status: "success"
    },
    {
      query: "Fetch user activity logs",
      timestamp: "2024-03-13 16:45",
      type: "API",
      status: "error"
    }
  ];

  return (
    <div className="py-24 px-4">
      <h1 className="text-4xl font-bold mb-2 bg-clip-text text-transparent bg-gradient-to-r from-[#00ff00] to-[#00cc00]">
        Query History
      </h1>
      <p className="text-gray-400 mb-8 text-lg">View and manage your past queries</p>

      <div className="mb-6 flex space-x-4">
        <div className="relative flex-1">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
          <input
            type="text"
            placeholder="Search queries..."
            className="w-full pl-10 pr-4 py-2 bg-black/50 border border-[#00ff00]/30 rounded-md
              focus:outline-none focus:ring-2 focus:ring-[#00ff00]/50 text-white
              placeholder:text-gray-500 transition-all duration-300 hover:border-[#00ff00]/50"
          />
        </div>
        <button className="px-4 py-2 bg-[#00ff00]/10 text-[#00ff00] rounded-md hover:bg-[#00ff00]/20 
          transition-all duration-300 hover-glow border border-[#00ff00]/30 flex items-center">
          <Calendar className="h-5 w-5 mr-2" />
          Filter Date
        </button>
      </div>

      <div className="space-y-4">
        {historyItems.map((item, index) => (
          <div key={index} 
            className="border border-[#00ff00]/30 rounded-lg p-6 hover-glow 
              transition-all duration-300 bg-black/30">
            <div className="flex items-center justify-between mb-2">
              <span className="text-[#00ff00] text-sm px-2 py-1 rounded-full border border-[#00ff00]/30">
                {item.type}
              </span>
              <div className="flex items-center space-x-2">
                <span className={`px-2 py-1 rounded-full text-sm
                  ${item.status === 'success' ? 'bg-green-500/20 text-green-400' : 'bg-red-500/20 text-red-400'}`}>
                  {item.status}
                </span>
                <span className="text-gray-400">{item.timestamp}</span>
              </div>
            </div>
            <p className="text-white">{item.query}</p>
          </div>
        ))}
      </div>
    </div>
  );
}