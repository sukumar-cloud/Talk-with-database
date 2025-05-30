import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Sidebar from './components/Sidebar';
import Home from './pages/Home';
import Dashboard from './pages/Dashboard';
import History from './pages/History';
import Chatbot from './pages/Chatbot';
import Documentation from './pages/Documentation';
import Settings from './pages/Settings';
import SqlQuery from './pages/SqlQuery';
import ApiQuery from './pages/ApiQuery';
import MongoDbQuery from './pages/MongoDbQuery';

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-black text-white">
        <Navbar />
        <div className="flex">
          <Sidebar />
          <main className="flex-1 pl-64 transition-all duration-300">
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/dashboard" element={<Dashboard />} />
              <Route path="/history" element={<History />} />
              <Route path="/chatbot" element={<Chatbot />} />
              <Route path="/docs" element={<Documentation />} />
              <Route path="/settings" element={<Settings />} />
              <Route path="/sql-query" element={<SqlQuery />} />
              <Route path="/api-query" element={<ApiQuery />} />
              <Route path="/mongodb-query" element={<MongoDbQuery />} />
            </Routes>
          </main>
        </div>
      </div>
    </Router>
  );
}

export default App;