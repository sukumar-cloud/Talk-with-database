import { Sun, User } from 'lucide-react';
import { useState } from 'react';

export default function Navbar() {
  const [isScrolled, setIsScrolled] = useState(false);

  // Add scroll listener
  if (typeof window !== 'undefined') {
    window.addEventListener('scroll', () => {
      setIsScrolled(window.scrollY > 20);
    });
  }

  return (
    <nav className={`fixed w-full z-50 transition-all duration-300 ${
      isScrolled ? 'glass-effect' : 'bg-transparent'
    }`}>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center group">
            
            
          </div>
          <div className="flex items-center space-x-4">
            <button className="p-2 rounded-lg hover:bg-[#00ff00]/10 transition-all duration-300">
              <Sun className="h-5 w-5 text-[#00ff00]" />
            </button>
            <button className="p-2 rounded-lg hover:bg-[#00ff00]/10 transition-all duration-300">
              <User className="h-5 w-5 text-[#00ff00]" />
            </button>
          </div>
        </div>
      </div>
    </nav>
  );
}