import { useState } from 'react';
import { Button } from "@/components/ui/button";
import { ArrowRight } from "lucide-react";

const DemoSection = () => {
  const [currentMessage, setCurrentMessage] = useState('');
  const [conversation, setConversation] = useState([
    { sender: 'user', message: 'Show me the status of my OpenStack project.' },
    { sender: 'agent', message: 'Here\'s the current status of your OpenStack project:', details: [
      'Compute: 8/20 instances in use',
      'Memory: 64GB/160GB allocated',
      'Storage: 2TB/5TB provisioned',
      'Networks: 3 networks with 45 active ports',
      'All services are operating normally'
    ]}
  ]);
  
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!currentMessage.trim()) return;
    
    // Add user message
    setConversation([...conversation, { sender: 'user', message: currentMessage }]);
    
    // Simulate AI response based on the input
    setTimeout(() => {
      let response;
      
      if (currentMessage.toLowerCase().includes('create') || currentMessage.toLowerCase().includes('launch')) {
        response = {
          sender: 'agent',
          message: 'I\'ll need your confirmation before proceeding:',
          details: ['Create a new m1.large instance named "web-server-03"?'],
          confirmAction: true
        };
      } else if (currentMessage.toLowerCase().includes('list') || currentMessage.toLowerCase().includes('show')) {
        response = {
          sender: 'agent',
          message: 'Here are your current instances:',
          details: [
            'web-server-01 (m1.large): ACTIVE',
            'web-server-02 (m1.large): ACTIVE',
            'db-server-01 (m2.xlarge): ACTIVE',
            'test-instance (m1.small): SHUTOFF'
          ]
        };
      } else {
        response = {
          sender: 'agent',
          message: 'I\'ve processed your request:',
          details: ['Your query has been logged and processed successfully.']
        };
      }
      
      setConversation(prev => [...prev, response]);
    }, 1000);
    
    setCurrentMessage('');
  };
  
  return (
    <section id="demo" className="py-16 md:py-24 bg-gradient-to-br from-gray-50 to-blue-50">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center max-w-3xl mx-auto mb-16">
          <h2 className="text-3xl md:text-4xl font-bold mb-6">
            <span className="bg-clip-text text-transparent bg-gradient-to-r from-cloud to-ai">
              See It In Action
            </span>
          </h2>
          <p className="text-xl text-gray-600">
            Try our interactive demo to experience how natural language simplifies your cloud management
          </p>
        </div>
        
        <div className="max-w-4xl mx-auto">
          <div className="bg-white rounded-2xl shadow-xl overflow-hidden">
            <div className="bg-gradient-to-r from-cloud to-ai p-4 text-white flex items-center justify-between">
              <div className="flex items-center space-x-3">
                <div className="w-3 h-3 rounded-full bg-white/30"></div>
                <div className="w-3 h-3 rounded-full bg-white/30"></div>
                <div className="w-3 h-3 rounded-full bg-white/30"></div>
              </div>
              <div className="text-sm font-medium">CloudScribe AI Agent Demo</div>
              <div></div>
            </div>
            
            <div className="h-96 overflow-y-auto p-4 space-y-4 bg-gray-50">
              {conversation.map((item, index) => (
                <div key={index} className={`flex ${item.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
                  <div className={`max-w-[80%] rounded-xl p-4 ${
                    item.sender === 'user' 
                      ? 'bg-cloud text-white rounded-br-none' 
                      : 'bg-white shadow-md rounded-bl-none'
                  }`}>
                    <p className={item.sender === 'user' ? 'text-white' : 'text-gray-800'}>
                      {item.message}
                    </p>
                    
                    {item.details && (
                      <ul className={`mt-2 space-y-1 text-sm ${item.sender === 'user' ? 'text-white/90' : 'text-gray-600'}`}>
                        {item.details.map((detail, i) => (
                          <li key={i} className="flex items-baseline">
                            <span className="mr-2">•</span>
                            <span>{detail}</span>
                          </li>
                        ))}
                      </ul>
                    )}
                    
                    {item.confirmAction && (
                      <div className="mt-3 flex space-x-3">
                        <Button size="sm" className="bg-green-600 hover:bg-green-700">
                          Yes, proceed
                        </Button>
                        <Button size="sm" variant="outline" className="border-white text-white hover:bg-white/20">
                          Cancel
                        </Button>
                      </div>
                    )}
                  </div>
                </div>
              ))}
            </div>
            
            <div className="p-4 border-t border-gray-200">
              <form onSubmit={handleSubmit} className="flex items-center space-x-2">
                <input
                  type="text"
                  value={currentMessage}
                  onChange={(e) => setCurrentMessage(e.target.value)}
                  placeholder="Type a command or question..."
                  className="flex-1 py-2 px-4 border border-gray-300 rounded-full focus:outline-none focus:ring-2 focus:ring-cloud focus:border-transparent"
                />
                <Button type="submit" className="rounded-full bg-gradient-to-r from-cloud to-ai p-2">
                  <ArrowRight className="h-5 w-5" />
                </Button>
              </form>
              <div className="mt-2 text-center">
                <p className="text-xs text-gray-500">Try: "Show me my compute instances" or "Create a new VM with 4 CPUs"</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default DemoSection;
