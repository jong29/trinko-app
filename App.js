import React, { useState } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, AreaChart, Area } from 'recharts';
import { Bell, MessageSquare, User, ChevronDown, LogIn, Mail, Lock, Check, ArrowRight, Award, Users, BarChart2 } from 'lucide-react';

// Sample data for charts
const tradeData = [
  { date: 'Jan 24', price: 85, benchmark: 82 },
  { date: 'Feb 24', price: 88, benchmark: 83 },
  { date: 'Mar 24', price: 90, benchmark: 85 },
  { date: 'Apr 24', price: 85, benchmark: 84 },
  { date: 'May 24', price: 82, benchmark: 86 },
  { date: 'Jun 24', price: 87, benchmark: 85 },
  { date: 'Jul 24', price: 90, benchmark: 84 },
  { date: 'Aug 24', price: 95, benchmark: 86 },
  { date: 'Sep 24', price: 92, benchmark: 88 },
  { date: 'Oct 24', price: 88, benchmark: 86 },
  { date: 'Nov 24', price: 93, benchmark: 89 },
  { date: 'Dec 24', price: 96, benchmark: 90 },
  { date: 'Jan 25', price: 92, benchmark: 91 },
  { date: 'Feb 25', price: 97, benchmark: 92 },
  { date: 'Mar 25', price: 95, benchmark: 90 },
  { date: 'Apr 25', price: 90, benchmark: 89 },
];

const leaderboardData = [
  { id: 1, username: 'cryptomaster', avgReturn: 12.4, sharpeRatio: 1.8, infoRatio: 0.9, profilePic: '/api/placeholder/40/40' },
  { id: 2, username: 'valueinvestor', avgReturn: 9.8, sharpeRatio: 2.1, infoRatio: 1.2, profilePic: '/api/placeholder/40/40' },
  { id: 3, username: 'daytradepro', avgReturn: 15.6, sharpeRatio: 1.5, infoRatio: 0.7, profilePic: '/api/placeholder/40/40' },
  { id: 4, username: 'techstocks', avgReturn: 11.2, sharpeRatio: 1.9, infoRatio: 1.0, profilePic: '/api/placeholder/40/40' },
  { id: 5, username: 'indexfan', avgReturn: 8.5, sharpeRatio: 2.0, infoRatio: 0.8, profilePic: '/api/placeholder/40/40' },
];

// Sample user performance data
const userPerformance = {
  avgReturn: 11.7,
  returns: [8.4, 10.2, 12.4, 9.8, 15.6, 11.2],
  sharpeRatio: 1.8,
  infoRatio: 0.9,
  percentileRank: 72
};

// Sample trading history data
const tradeHistoryData = [
  { id: 1, date: 'Apr 28, 2025', ticker: 'AAPL', position: 'Long', entryPrice: 185.50, currentPrice: 193.30, status: 'Open', return: 4.2 },
  { id: 2, date: 'Apr 15, 2025', ticker: 'BTC-USD', position: 'Long', entryPrice: 58750, currentPrice: 68000, status: 'Open', return: 15.8 },
  { id: 3, date: 'Apr 02, 2025', ticker: 'TSLA', position: 'Short', entryPrice: 175.20, currentPrice: 178.90, status: 'Closed', return: -2.1 },
  { id: 4, date: 'Mar 20, 2025', ticker: 'NVDA', position: 'Long', entryPrice: 920.30, currentPrice: 1000.40, status: 'Closed', return: 8.7 },
];

// Distribution data for visualization
const distributionData = [
  { value: 5, count: 2 },
  { value: 6, count: 5 },
  { value: 7, count: 8 },
  { value: 8, count: 12 },
  { value: 9, count: 18 },
  { value: 10, count: 25 },
  { value: 11, count: 30 },
  { value: 12, count: 25 },
  { value: 13, count: 18 },
  { value: 14, count: 12 },
  { value: 15, count: 8 },
  { value: 16, count: 5 },
  { value: 17, count: 2 },
];

function App() {
  const [currentPage, setCurrentPage] = useState('signup');

  const renderPage = () => {
    switch(currentPage) {
      case 'signup':
        return <SignupPage setCurrentPage={setCurrentPage} />;
      case 'userInfo':
        return <UserInfoPage setCurrentPage={setCurrentPage} />;
      case 'feature01':
        return <Feature01Page setCurrentPage={setCurrentPage} />;
      case 'feature01a':
        return <Feature01aPage setCurrentPage={setCurrentPage} />;
      case 'feature02':
        return <Feature02Page setCurrentPage={setCurrentPage} />;
      case 'feature03':
        return <Feature03Page setCurrentPage={setCurrentPage} />;
      case 'feature04':
        return <Feature04Page setCurrentPage={setCurrentPage} />;
      default:
        return <SignupPage setCurrentPage={setCurrentPage} />;
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {currentPage !== 'signup' && currentPage !== 'userInfo' && (
        <header className="bg-white shadow">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex justify-between items-center h-16">
            <div className="font-bold text-xl text-blue-600">Trinko</div>
            <div className="flex space-x-4">
              <button onClick={() => setCurrentPage('feature01')} className={`px-3 py-2 ${currentPage === 'feature01' ? 'text-blue-600 border-b-2 border-blue-600' : 'text-gray-500'}`}>Submit Trade</button>
              <button onClick={() => setCurrentPage('feature01a')} className={`px-3 py-2 ${currentPage === 'feature01a' ? 'text-blue-600 border-b-2 border-blue-600' : 'text-gray-500'}`}>Trade History</button>
              <button onClick={() => setCurrentPage('feature02')} className={`px-3 py-2 ${currentPage === 'feature02' ? 'text-blue-600 border-b-2 border-blue-600' : 'text-gray-500'}`}>Stats</button>
              <button onClick={() => setCurrentPage('feature03')} className={`px-3 py-2 ${currentPage === 'feature03' ? 'text-blue-600 border-b-2 border-blue-600' : 'text-gray-500'}`}>Leaderboard</button>
              <button onClick={() => setCurrentPage('feature04')} className={`px-3 py-2 ${currentPage === 'feature04' ? 'text-blue-600 border-b-2 border-blue-600' : 'text-gray-500'}`}>Profile</button>
            </div>
            <div className="flex items-center space-x-2">
              <button className="p-2 text-gray-500 hover:text-blue-600">
                <Bell size={20} />
              </button>
              <button className="p-2 text-gray-500 hover:text-blue-600">
                <MessageSquare size={20} />
              </button>
              <button className="flex items-center space-x-2 p-2 text-gray-500 hover:text-blue-600">
                <User size={20} />
                <ChevronDown size={16} />
              </button>
            </div>
          </div>
        </header>
      )}
      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        {renderPage()}
      </main>
    </div>
  );
}

// Feature 0 - Sign Up
function SignupPage({ setCurrentPage }) {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        <div>
          <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">Trinko</h2>
          <p className="mt-2 text-center text-sm text-gray-600">
            Track your trades, analyze performance, and compete with others
          </p>
        </div>
        <div className="mt-8 space-y-6">
          <div className="rounded-md shadow-sm space-y-4">
            <div>
              <label htmlFor="email-address" className="sr-only">Email address</label>
              <div className="flex">
                <span className="inline-flex items-center px-3 rounded-l-md border border-r-0 border-gray-300 bg-gray-50 text-gray-500">
                  <Mail size={16} />
                </span>
                <input id="email-address" name="email" type="email" autoComplete="email" required className="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-r-md focus:outline-none focus:ring-blue-500 focus:border-blue-500 focus:z-10 sm:text-sm" placeholder="Email address" />
              </div>
            </div>
            <div>
              <label htmlFor="password" className="sr-only">Password</label>
              <div className="flex">
                <span className="inline-flex items-center px-3 rounded-l-md border border-r-0 border-gray-300 bg-gray-50 text-gray-500">
                  <Lock size={16} />
                </span>
                <input id="password" name="password" type="password" autoComplete="current-password" required className="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-r-md focus:outline-none focus:ring-blue-500 focus:border-blue-500 focus:z-10 sm:text-sm" placeholder="Password" />
              </div>
            </div>
          </div>

          <div>
            <button onClick={() => setCurrentPage('userInfo')} className="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
              Sign Up with Email
            </button>
          </div>

          <div className="mt-6">
            <div className="relative">
              <div className="absolute inset-0 flex items-center">
                <div className="w-full border-t border-gray-300"></div>
              </div>
              <div className="relative flex justify-center text-sm">
                <span className="px-2 bg-gray-50 text-gray-500">Or continue with</span>
              </div>
            </div>

            <div className="mt-6 grid grid-cols-2 gap-3">
              <div>
                <button className="w-full inline-flex justify-center py-2 px-4 border border-gray-300 rounded-md shadow-sm bg-white text-sm font-medium text-gray-500 hover:bg-gray-50">
                  <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                    <path fillRule="evenodd" d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z" clipRule="evenodd" />
                  </svg>
                </button>
              </div>
              <div>
                <button className="w-full inline-flex justify-center py-2 px-4 border border-gray-300 rounded-md shadow-sm bg-white text-sm font-medium text-gray-500 hover:bg-gray-50">
                  <svg className="w-5 h-5" viewBox="0 0 24 24" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
                    <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#4285F4"/>
                    <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853"/>
                    <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" fill="#FBBC05"/>
                    <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335"/>
                  </svg>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

// Feature 0 - User Information
function UserInfoPage({ setCurrentPage }) {
  return (
    <div className="max-w-lg mx-auto bg-white shadow-md rounded-lg overflow-hidden">
      <div className="px-6 py-4">
        <h2 className="text-2xl font-bold text-center text-gray-800 mb-8">Complete Your Profile</h2>
        
        <div className="space-y-6">
          <div>
            <label className="block text-sm font-medium text-gray-700">Username</label>
            <input type="text" className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500" />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700">Date of Birth</label>
            <input type="date" className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500" />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700">Interested Asset Classes</label>
            <div className="mt-2 grid grid-cols-2 gap-2">
              {['Stocks', 'Bonds', 'Crypto', 'Forex', 'Commodities', 'ETFs'].map((asset) => (
                <div key={asset} className="flex items-center">
                  <input id={asset} type="checkbox" className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded" />
                  <label htmlFor={asset} className="ml-2 block text-sm text-gray-700">{asset}</label>
                </div>
              ))}
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700">Profession</label>
            <input type="text" className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500" />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700">Short Bio</label>
            <textarea className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500" rows="3"></textarea>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700">Profile Picture</label>
            <div className="mt-1 flex items-center">
              <span className="inline-block h-12 w-12 rounded-full overflow-hidden bg-gray-100">
                <svg className="h-full w-full text-gray-300" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M24 20.993V24H0v-2.996A14.977 14.977 0 0112.004 15c4.904 0 9.26 2.354 11.996 5.993zM16.002 8.999a4 4 0 11-8 0 4 4 0 018 0z" />
                </svg>
              </span>
              <button type="button" className="ml-5 bg-white py-2 px-3 border border-gray-300 rounded-md shadow-sm text-sm leading-4 font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">Upload</button>
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700">Investment Style</label>
            <select className="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm rounded-md">
              <option>Value Investing</option>
              <option>Growth Investing</option>
              <option>Momentum Trading</option>
              <option>Swing Trading</option>
              <option>Day Trading</option>
              <option>Dividend Investing</option>
              <option>Index Investing</option>
            </select>
          </div>

          <div className="flex justify-end">
            <button onClick={() => setCurrentPage('feature01')} className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 flex items-center">
              Next
              <ArrowRight size={16} className="ml-2" />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

// Feature 01 - Submit Trade
function Feature01Page({ setCurrentPage }) {
  const [tradeConfidence, setTradeConfidence] = useState(3);
  
  return (
    <div className="max-w-6xl mx-auto">
      <div className="bg-white shadow overflow-hidden sm:rounded-lg">
        <div className="px-6 py-4 border-b border-gray-200">
          <h3 className="text-lg leading-6 font-medium text-gray-900">
            Post New Trade
          </h3>
        </div>
        <div className="px-6 py-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="space-y-6">
              <div>
                <label className="block text-sm font-medium text-gray-700">Asset Name/Ticker</label>
                <input type="text" className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500" placeholder="e.g. AAPL, BTC-USD" />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700">Position Type</label>
                <div className="mt-2 grid grid-cols-2 gap-2">
                  <div className="flex items-center">
                    <input id="long" name="position" type="radio" className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300" />
                    <label htmlFor="long" className="ml-2 block text-sm text-gray-700">Long</label>
                  </div>
                  <div className="flex items-center">
                    <input id="short" name="position" type="radio" className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300" />
                    <label htmlFor="short" className="ml-2 block text-sm text-gray-700">Short</label>
                  </div>
                </div>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700">Entry Type</label>
                <div className="mt-2 grid grid-cols-2 gap-2">
                  <div className="flex items-center">
                    <input id="open" name="entry" type="radio" className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300" />
                    <label htmlFor="open" className="ml-2 block text-sm text-gray-700">Open Position</label>
                  </div>
                  <div className="flex items-center">
                    <input id="close" name="entry" type="radio" className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300" />
                    <label htmlFor="close" className="ml-2 block text-sm text-gray-700">Close Position</label>
                  </div>
                </div>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700">Trade Confidence (0-5)</label>
                <div className="mt-2 flex items-center space-x-2">
                  <input 
                    type="range" 
                    min="0" 
                    max="5" 
                    value={tradeConfidence} 
                    onChange={(e) => setTradeConfidence(parseInt(e.target.value))} 
                    className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
                  />
                  <span className="text-lg font-medium text-blue-600">{tradeConfidence}</span>
                </div>
                <div className="mt-1 text-xs text-gray-500 flex justify-between">
                  <span>Low Certainty</span>
                  <span>High Certainty</span>
                </div>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700">Trade Reason (Optional)</label>
                <textarea className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500" rows="4" placeholder="Explain your reasoning for this trade..."></textarea>
              </div>
            </div>
            
            <div className="bg-gray-50 p-4 rounded-lg">
              <h4 className="text-lg font-medium text-gray-700 mb-4">Trade Performance</h4>
              <div className="h-64">
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={tradeData.slice(-12)}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="date" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Line type="monotone" dataKey="price" stroke="#3B82F6" activeDot={{ r: 8 }} name="Asset Price" />
                    <Line type="monotone" dataKey="benchmark" stroke="#9CA3AF" name="S&P 500" />
                  </LineChart>
                </ResponsiveContainer>
              </div>
              <div className="mt-4 grid grid-cols-2 gap-4">
                <div className="bg-white p-3 rounded-lg shadow-sm">
                  <div className="text-sm text-gray-500">Asset Return</div>
                  <div className="text-lg font-semibold text-green-600">+5.8%</div>
                </div>
                <div className="bg-white p-3 rounded-lg shadow-sm">
                  <div className="text-sm text-gray-500">S&P 500 Return</div>
                  <div className="text-lg font-semibold text-green-600">+3.2%</div>
                </div>
                <div className="bg-white p-3 rounded-lg shadow-sm">
                  <div className="text-sm text-gray-500">Alpha</div>
                  <div className="text-lg font-semibold text-green-600">+2.6%</div>
                </div>
                <div className="bg-white p-3 rounded-lg shadow-sm">
                  <div className="text-sm text-gray-500">Duration</div>
                  <div className="text-lg font-semibold">32 Days</div>
                </div>
              </div>
            </div>
          </div>
          
          <div className="mt-6 flex justify-end">
            <button 
              onClick={() => setCurrentPage('feature01a')} 
              className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 flex items-center"
            >
              Post Trade
              <Check size={16} className="ml-2" />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

// Feature 01a - Trade History
function Feature01aPage({ setCurrentPage }) {
  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-white p-3 rounded shadow-md border border-gray-200">
          <p className="text-sm font-medium">{label}</p>
          <p className="text-sm text-blue-600">{`${payload[0].name}: ${payload[0].value}`}</p>
          <p className="text-sm text-gray-600">{`S&P Return To Date: ${payload[1].value}`}</p>
        </div>
      );
    }
    return null;
  };

  return (
    <div className="max-w-6xl mx-auto">
      <div className="bg-white shadow overflow-hidden sm:rounded-lg">
        <div className="px-6 py-4 border-b border-gray-200">
          <h3 className="text-lg leading-6 font-medium text-gray-900">
            Your Trade History
          </h3>
        </div>
        <div className="px-6 py-6">
          <div className="bg-gray-50 p-4 rounded-lg mb-6">
            <h4 className="text-lg font-medium text-gray-700 mb-4">Trade Performance History</h4>
            <div className="h-64">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={tradeData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="date" />
                  <YAxis />
                  <Tooltip content={<CustomTooltip />} />
                  <Legend />
                  <Line type="monotone" dataKey="price" stroke="#00A3FF" strokeWidth={2} activeDot={{ r: 8 }} name="Your Return To Date" />
                  <Line type="monotone" dataKey="benchmark" stroke="#FF971D" strokeWidth={2} name="S&P Return To Date" />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </div>
          
          <div className="overflow-hidden bg-white rounded-lg border border-gray-200">
            <div className="px-6 py-4 border-b border-gray-200 bg-gray-50 flex justify-between items-center">
              <h4 className="text-lg font-medium text-gray-700">Your Trades</h4>
              <div className="flex items-center space-x-2">
                <span className="text-sm text-gray-500">Sort by:</span>
                <select className="border-gray-300 rounded-md shadow-sm text-sm focus:border-blue-300 focus:ring focus:ring-blue-200 focus:ring-opacity-50">
                  <option>Date (Newest)</option>
                  <option>Date (Oldest)</option>
                  <option>Return (Highest)</option>
                  <option>Return (Lowest)</option>
                </select>
              </div>
            </div>
            
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Date</th>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Asset</th>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Position</th>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Entry Price</th>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Current/Exit Price</th>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Return</th>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                  <th scope="col" className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Action</th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {tradeHistoryData.map((trade) => (
                  <tr key={trade.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{trade.date}</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{trade.ticker}</td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${
                        trade.position === 'Long' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                      }`}>
                        {trade.position}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {typeof trade.entryPrice === 'number' && trade.entryPrice > 1000 
                        ? trade.entryPrice.toLocaleString('en-US', { style: 'currency', currency: 'USD', maximumFractionDigits: 0 })
                        : trade.entryPrice.toLocaleString('en-US', { style: 'currency', currency: 'USD', minimumFractionDigits: 2 })
                      }
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {typeof trade.currentPrice === 'number' && trade.currentPrice > 1000 
                        ? trade.currentPrice.toLocaleString('en-US', { style: 'currency', currency: 'USD', maximumFractionDigits: 0 })
                        : trade.currentPrice.toLocaleString('en-US', { style: 'currency', currency: 'USD', minimumFractionDigits: 2 })
                      }
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                      <span className={trade.return >= 0 ? 'text-green-600' : 'text-red-600'}>
                        {trade.return >= 0 ? '+' : ''}{trade.return}%
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${
                        trade.status === 'Open' ? 'bg-blue-100 text-blue-800' : 'bg-gray-100 text-gray-800'
                      }`}>
                        {trade.status}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                      {trade.status === 'Open' && (
                        <button className="text-blue-600 hover:text-blue-900 bg-blue-50 px-3 py-1 rounded-md">
                          Close Position
                        </button>
                      )}
                      {trade.status === 'Closed' && (
                        <button className="text-gray-600 hover:text-gray-900 bg-gray-50 px-3 py-1 rounded-md">
                          View Details
                        </button>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
            
            <div className="px-6 py-4 bg-gray-50 border-t border-gray-200 flex items-center justify-between">
              <div className="text-sm text-gray-700">
                Showing <span className="font-medium">1</span> to <span className="font-medium">{tradeHistoryData.length}</span> of <span className="font-medium">{tradeHistoryData.length}</span> trades
              </div>
              <div className="flex-1 flex justify-between sm:justify-end">
                <button className="relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50">
                  Previous
                </button>
                <button className="ml-3 relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50">
                  Next
                </button>
              </div>
            </div>
          </div>
          
          <div className="mt-6 flex justify-end space-x-4">
            <button 
              onClick={() => setCurrentPage('feature01')} 
              className="bg-gray-100 text-gray-700 px-4 py-2 rounded-md hover:bg-gray-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500"
            >
              Submit New Trade
            </button>
            <button 
              onClick={() => setCurrentPage('feature02')} 
              className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
            >
              View Stats
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

// Feature 02 - Performance Statistics
function Feature02Page({ setCurrentPage }) {
  // Custom component for distribution chart with vertical line
  const DistributionChart = () => {
    const userValue = userPerformance.avgReturn;
    
    return (
      <ResponsiveContainer width="100%" height="100%">
        <AreaChart data={distributionData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis 
            dataKey="value" 
            label={{ value: 'Average Return (%)', position: 'bottom', offset: 0 }} 
          />
          <YAxis 
            label={{ value: 'Number of Users', angle: -90, position: 'insideLeft' }} 
          />
          <Tooltip />
          <defs>
            <linearGradient id="colorCount" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#3B82F6" stopOpacity={0.8}/>
              <stop offset="95%" stopColor="#3B82F6" stopOpacity={0.2}/>
            </linearGradient>
            <linearGradient id="percentileGradient" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#10B981" stopOpacity={0.2}/>
              <stop offset="95%" stopColor="#10B981" stopOpacity={0.1}/>
            </linearGradient>
          </defs>
          
          {/* Main area chart */}
          <Area 
            type="monotone" 
            dataKey="count" 
            stroke="#3B82F6" 
            fillOpacity={1} 
            fill="url(#colorCount)" 
          />
          
          {/* Percentile shaded area */}
          <Area 
            type="monotone" 
            dataKey={(entry) => (entry.value >= userValue) ? entry.count : 0} 
            stroke="none"
            fillOpacity={1} 
            fill="url(#percentileGradient)" 
          />
          
          {/* Vertical line for user position */}
          <Line 
            type="monotone" 
            dataKey={(entry) => entry.value === userValue ? entry.count : null} 
            stroke="#DC2626" 
            strokeWidth={2} 
            dot={{ r: 6, fill: '#DC2626' }} 
            activeDot={{ r: 8, fill: '#DC2626' }} 
          />
        </AreaChart>
      </ResponsiveContainer>
    );
  };

  return (
    <div className="max-w-6xl mx-auto">
      <div className="bg-white shadow overflow-hidden sm:rounded-lg">
        <div className="px-6 py-4 border-b border-gray-200">
          <h3 className="text-lg leading-6 font-medium text-gray-900">
            Your Performance Statistics
          </h3>
        </div>
        <div className="px-6 py-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <div className="bg-gray-50 p-4 rounded-lg">
                <h4 className="text-lg font-medium text-gray-700 mb-4">Key Performance Metrics</h4>
                <div className="grid grid-cols-2 gap-4">
                  <div className="bg-white p-4 rounded-lg shadow-sm">
                    <div className="flex items-start">
                      <div className="flex-shrink-0">
                        <div className="p-2 bg-blue-100 rounded-md">
                          <BarChart2 className="h-5 w-5 text-blue-600" />
                        </div>
                      </div>
                      <div className="ml-4">
                        <h5 className="text-sm font-medium text-gray-500">Average Returns</h5>
                        <div className="mt-1 text-xl font-semibold text-green-600">+{userPerformance.avgReturn}%</div>
                        <div className="mt-1 text-xs text-gray-500">
                          <span className="text-green-600">Better than {userPerformance.percentileRank}% of users</span>
                        </div>
                      </div>
                    </div>
                  </div>
                  <div className="bg-white p-4 rounded-lg shadow-sm">
                    <div className="flex items-start">
                      <div className="flex-shrink-0">
                        <div className="p-2 bg-blue-100 rounded-md">
                          <BarChart2 className="h-5 w-5 text-blue-600" />
                        </div>
                      </div>
                      <div className="ml-4">
                        <h5 className="text-sm font-medium text-gray-500">Sharpe Ratio</h5>
                        <div className="mt-1 text-xl font-semibold text-blue-600">{userPerformance.sharpeRatio}</div>
                        <div className="mt-1 text-xs text-gray-500">
                          <span className="text-green-600">Better than {userPerformance.percentileRank - 5}% of users</span>
                        </div>
                      </div>
                    </div>
                  </div>
                  <div className="bg-white p-4 rounded-lg shadow-sm">
                    <div className="flex items-start">
                      <div className="flex-shrink-0">
                        <div className="p-2 bg-blue-100 rounded-md">
                          <BarChart2 className="h-5 w-5 text-blue-600" />
                        </div>
                      </div>
                      <div className="ml-4">
                        <h5 className="text-sm font-medium text-gray-500">Information Ratio</h5>
                        <div className="mt-1 text-xl font-semibold text-blue-600">{userPerformance.infoRatio}</div>
                        <div className="mt-1 text-xs text-gray-500">
                          <span className="text-green-600">Better than {userPerformance.percentileRank - 10}% of users</span>
                        </div>
                      </div>
                    </div>
                  </div>
                  <div className="bg-white p-4 rounded-lg shadow-sm">
                    <div className="flex items-start">
                      <div className="flex-shrink-0">
                        <div className="p-2 bg-blue-100 rounded-md">
                          <Award className="h-5 w-5 text-blue-600" />
                        </div>
                      </div>
                      <div className="ml-4">
                        <h5 className="text-sm font-medium text-gray-500">Total Trades</h5>
                        <div className="mt-1 text-xl font-semibold text-gray-800">24</div>
                        <div className="mt-1 text-xs text-gray-500">
                          <span>Last 90 days</span>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
                
                <div className="mt-6">
                  <h5 className="text-sm font-medium text-gray-700 mb-2">Information Ratio Explained</h5>
                  <div className="bg-blue-50 p-3 rounded-lg text-sm text-gray-700">
                    <p>The Information Ratio (IR) measures the risk-adjusted returns of your portfolio compared to a benchmark (S&P 500). It shows how much excess return is generated from the amount of excess risk taken relative to the benchmark.</p>
                    <p className="mt-2">IR = (Portfolio Return - Benchmark Return) / Tracking Error</p>
                    <p className="mt-2">Higher IR indicates better risk-adjusted performance.</p>
                  </div>
                </div>
                
                <div className="mt-6">
                  <h5 className="text-sm font-medium text-gray-700 mb-2">Sharpe Ratio Explained</h5>
                  <div className="bg-blue-50 p-3 rounded-lg text-sm text-gray-700">
                    <p>The Sharpe Ratio measures the performance of an investment compared to a risk-free asset, after adjusting for its risk.</p>
                    <p className="mt-2">Sharpe Ratio = (Average Portfolio Return - Risk Free Rate) / Standard Deviation of Portfolio</p>
                    <p className="mt-2">A higher Sharpe ratio indicates better risk-adjusted performance. A Sharpe ratio greater than 1.0 is considered acceptable, while a ratio greater than 2.0 is considered very good.</p>
                  </div>
                </div>
              </div>
            </div>
            
            <div>
              <div className="bg-gray-50 p-4 rounded-lg">
                <h4 className="text-lg font-medium text-gray-700 mb-4">Distribution Analysis</h4>
                <div className="h-64">
                  <DistributionChart />
                </div>
                <div className="mt-4 text-sm text-gray-600">
                  <div className="flex items-center">
                    <span className="h-3 w-3 bg-blue-600 rounded-full mr-2"></span>
                    <span>All Users' Return Distribution</span>
                  </div>
                  <div className="flex items-center mt-1">
                    <span className="h-3 w-3 bg-red-600 rounded-full mr-2"></span>
                    <span>Your Position ({userPerformance.avgReturn}%)</span>
                  </div>
                  <div className="flex items-center mt-1">
                    <span className="h-3 w-3 bg-green-500 opacity-20 rounded-sm mr-2"></span>
                    <span>Top {100 - userPerformance.percentileRank}% Percentile</span>
                  </div>
                </div>
                <div className="mt-4 bg-blue-50 p-3 rounded-lg text-sm text-gray-700">
                  <p>Your returns are in the top {100 - userPerformance.percentileRank}th percentile of all users.</p>
                </div>
              </div>
            </div>
          </div>
          
          <div className="mt-6 flex justify-end">
            <button 
              onClick={() => setCurrentPage('feature03')} 
              className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
            >
              View Leaderboard
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

// Feature 03 - Leaderboard
function Feature03Page({ setCurrentPage }) {
  return (
    <div className="max-w-6xl mx-auto">
      <div className="bg-white shadow overflow-hidden sm:rounded-lg">
        <div className="px-6 py-4 border-b border-gray-200 flex justify-between items-center">
          <h3 className="text-lg leading-6 font-medium text-gray-900">
            Trader Leaderboard
          </h3>
          <div className="flex items-center">
            <span className="mr-2 text-sm text-gray-500">Sort by:</span>
            <select className="border-gray-300 rounded-md shadow-sm focus:border-blue-300 focus:ring focus:ring-blue-200 focus:ring-opacity-50">
              <option>Avg Return</option>
              <option>Sharpe Ratio</option>
              <option>Information Ratio</option>
            </select>
          </div>
        </div>
        
        <div className="divide-y divide-gray-200">
          <div className="grid grid-cols-10 gap-4 px-6 py-3 bg-gray-50 text-xs font-medium text-gray-500 uppercase tracking-wider">
            <div className="col-span-1 text-center">Rank</div>
            <div className="col-span-3">Trader</div>
            <div className="col-span-2 text-center">Avg Return</div>
            <div className="col-span-2 text-center">Sharpe Ratio</div>
            <div className="col-span-2 text-center">Info Ratio</div>
          </div>
          
          {leaderboardData.map((user, index) => (
            <div key={user.id} className="grid grid-cols-10 gap-4 px-6 py-4 hover:bg-gray-50 cursor-pointer" onClick={() => setCurrentPage('feature04')}>
              <div className="col-span-1 flex justify-center items-center">
                {index === 0 ? (
                  <div className="p-1 bg-yellow-100 rounded-full">
                    <Award className="h-5 w-5 text-yellow-400" />
                  </div>
                ) : (
                  <div className="font-medium text-gray-900">{index + 1}</div>
                )}
              </div>
              <div className="col-span-3 flex items-center">
                <img className="h-10 w-10 rounded-full" src={user.profilePic} alt="" />
                <div className="ml-4">
                  <div className="text-sm font-medium text-gray-900">{user.username}</div>
                  <div className="text-xs text-gray-500">Member since Nov 2024</div>
                </div>
              </div>
              <div className="col-span-2 flex justify-center items-center">
                <div className="text-sm font-medium text-green-600">+{user.avgReturn}%</div>
              </div>
              <div className="col-span-2 flex justify-center items-center">
                <div className="text-sm font-medium text-gray-900">{user.sharpeRatio}</div>
              </div>
              <div className="col-span-2 flex justify-center items-center">
                <div className="text-sm font-medium text-gray-900">{user.infoRatio}</div>
              </div>
            </div>
          ))}
        </div>
        
        <div className="px-6 py-4 bg-gray-50 border-t border-gray-200 flex items-center justify-between">
          <div className="text-sm text-gray-700">
            Showing <span className="font-medium">1</span> to <span className="font-medium">5</span> of <span className="font-medium">122</span> traders
          </div>
          <div className="flex-1 flex justify-between sm:justify-end">
            <button className="relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50">
              Previous
            </button>
            <button className="ml-3 relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50">
              Next
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

// Feature 04 - Profile Section
function Feature04Page({ setCurrentPage }) {
  // Custom component for distribution chart with vertical line
  const DistributionChart = () => {
    const userValue = userPerformance.avgReturn;
    
    return (
      <ResponsiveContainer width="100%" height="100%">
        <AreaChart data={distributionData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis 
            dataKey="value" 
            label={{ value: 'Average Return (%)', position: 'bottom', offset: 0 }} 
          />
          <YAxis 
            label={{ value: 'Number of Users', angle: -90, position: 'insideLeft' }} 
          />
          <Tooltip />
          <defs>
            <linearGradient id="colorCount" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#3B82F6" stopOpacity={0.8}/>
              <stop offset="95%" stopColor="#3B82F6" stopOpacity={0.2}/>
            </linearGradient>
            <linearGradient id="percentileGradient" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#10B981" stopOpacity={0.2}/>
              <stop offset="95%" stopColor="#10B981" stopOpacity={0.1}/>
            </linearGradient>
          </defs>
          
          {/* Main area chart */}
          <Area 
            type="monotone" 
            dataKey="count" 
            stroke="#3B82F6" 
            fillOpacity={1} 
            fill="url(#colorCount)" 
          />
          
          {/* Percentile shaded area */}
          <Area 
            type="monotone" 
            dataKey={(entry) => (entry.value >= userValue) ? entry.count : 0} 
            stroke="none"
            fillOpacity={1} 
            fill="url(#percentileGradient)" 
          />
          
          {/* Vertical line for user position */}
          <Line 
            type="monotone" 
            dataKey={(entry) => entry.value === userValue ? entry.count : null} 
            stroke="#DC2626" 
            strokeWidth={2} 
            dot={{ r: 6, fill: '#DC2626' }} 
            activeDot={{ r: 8, fill: '#DC2626' }} 
          />
        </AreaChart>
      </ResponsiveContainer>
    );
  };

  return (
    <div className="max-w-6xl mx-auto">
      <div className="bg-white shadow overflow-hidden sm:rounded-lg">
        <div className="px-6 py-6 border-b border-gray-200">
          <div className="flex flex-wrap items-center">
            <img className="h-24 w-24 rounded-full mr-6" src="/api/placeholder/100/100" alt="Profile" />
            <div className="flex-1">
              <h2 className="text-2xl font-bold text-gray-900">cryptomaster</h2>
              <p className="text-sm text-gray-500 mt-1">Member since November 2024</p>
              <p className="text-sm text-gray-600 mt-1">Crypto enthusiast and long-term investor focusing on emerging technology. Currently studying computer science and developing trading algorithms.</p>
              <div className="mt-3 flex flex-wrap gap-2">
                <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-blue-100 text-blue-800">
                  Crypto
                </span>
                <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-blue-100 text-blue-800">
                  Tech Stocks
                </span>
                <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-blue-100 text-blue-800">
                  Momentum Trading
                </span>
              </div>
            </div>
            <div className="flex space-x-3">
              <button className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
                <Bell size={16} className="mr-2" />
                Follow
              </button>
              <button className="inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md shadow-sm text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
                <MessageSquare size={16} className="mr-2" />
                Message
              </button>
            </div>
          </div>
        </div>
        
        <div className="px-6 py-6">
          <div className="mb-6">
            <h3 className="text-lg font-medium text-gray-900 mb-4">Performance Summary</h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="bg-gray-50 p-4 rounded-lg">
                <div className="text-sm text-gray-500">Avg Return</div>
                <div className="text-2xl font-bold text-green-600">+12.4%</div>
                <div className="text-xs text-gray-500 mt-1">Better than 72% of users</div>
              </div>
              <div className="bg-gray-50 p-4 rounded-lg">
                <div className="text-sm text-gray-500">Sharpe Ratio</div>
                <div className="text-2xl font-bold text-blue-600">1.8</div>
                <div className="text-xs text-gray-500 mt-1">Better than 65% of users</div>
              </div>
              <div className="bg-gray-50 p-4 rounded-lg">
                <div className="text-sm text-gray-500">Information Ratio</div>
                <div className="text-2xl font-bold text-blue-600">0.9</div>
                <div className="text-xs text-gray-500 mt-1">Better than 58% of users</div>
              </div>
            </div>
          </div>
          
          <div className="mb-6">
            <h3 className="text-lg font-medium text-gray-900 mb-4">Performance History</h3>
            <div className="bg-gray-50 p-4 rounded-lg">
              <div className="h-64">
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={tradeData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="date" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Line type="monotone" dataKey="price" stroke="#00A3FF" strokeWidth={2} name="Portfolio Value" />
                    <Line type="monotone" dataKey="benchmark" stroke="#FF971D" strokeWidth={2} name="S&P 500" />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            </div>
          </div>
          
          <div className="mb-6">
            <h3 className="text-lg font-medium text-gray-900 mb-4">Distribution Analysis</h3>
            <div className="bg-gray-50 p-4 rounded-lg">
              <div className="h-64">
                <DistributionChart />
              </div>
              <div className="mt-4 text-sm text-gray-600">
                <div className="flex items-center">
                  <span className="h-3 w-3 bg-blue-600 rounded-full mr-2"></span>
                  <span>All Users' Return Distribution</span>
                </div>
                <div className="flex items-center mt-1">
                  <span className="h-3 w-3 bg-red-600 rounded-full mr-2"></span>
                  <span>Your Position (12.4%)</span>
                </div>
                <div className="flex items-center mt-1">
                  <span className="h-3 w-3 bg-green-500 opacity-20 rounded-sm mr-2"></span>
                  <span>Top 28% Percentile</span>
                </div>
              </div>
              <div className="mt-4 bg-blue-50 p-3 rounded-lg text-sm text-gray-700">
                <p>Your returns are in the top 28th percentile of all users.</p>
              </div>
            </div>
          </div>
          
          <div>
            <h3 className="text-lg font-medium text-gray-900 mb-4">Recent Trades</h3>
            <div className="overflow-hidden bg-gray-50 rounded-lg">
              <table className="min-w-full divide-y divide-gray-200">
                <thead>
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Date</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Asset</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Position</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Return</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Confidence</th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  <tr>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">Apr 28, 2025</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">AAPL</td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800">Long</span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-green-600">+4.2%</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">4/5</td>
                  </tr>
                  <tr>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">Apr 15, 2025</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">BTC-USD</td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800">Long</span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-green-600">+15.8%</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">5/5</td>
                  </tr>
                  <tr>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">Apr 02, 2025</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">TSLA</td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-red-100 text-red-800">Short</span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-red-600">-2.1%</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">3/5</td>
                  </tr>
                  <tr>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">Mar 20, 2025</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">NVDA</td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800">Long</span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-green-600">+8.7%</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">4/5</td>
                  </tr>
                </tbody>
              </table>
              <div className="px-6 py-4 bg-gray-50 border-t border-gray-200">
                <button className="text-sm text-blue-600 hover:text-blue-500">View all trades →</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;