import { Button } from "@/components/ui/button";
import { ArrowRight } from "lucide-react";

const HeroSection = () => {
  return (
    <section className="pt-24 pb-16 md:pt-32 md:pb-24 overflow-hidden">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex flex-col lg:flex-row items-center">
          {/* Left Column - Text Content */}
          <div className="lg:w-1/2 lg:pr-8 mb-10 lg:mb-0">
            <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold leading-tight mb-6">
              <span className="bg-clip-text text-transparent bg-gradient-to-r from-cloud to-ai">
                Intelligent Cloud Management
              </span> 
              <span className="block mt-2">through Natural Language</span>
            </h1>
            <p className="text-lg md:text-xl text-gray-600 mb-8 max-w-lg">
              Simply ask, and our AI agent will handle your OpenStack resources. No complex commands or API calls needed.
            </p>
            <div className="flex flex-col sm:flex-row gap-4">
              <Button className="bg-gradient-to-r from-cloud to-ai hover:opacity-90 transition-opacity px-8 py-6 text-lg">
                Get Started
                <ArrowRight className="ml-2 h-5 w-5" />
              </Button>
              <Button variant="outline" className="border-gray-300 px-8 py-6 text-lg">
                View Demo
              </Button>
            </div>
          </div>
          
          {/* Right Column - Interactive Illustration */}
          <div className="lg:w-1/2 relative">
            <div className="relative z-10">
              <div className="bg-white rounded-xl shadow-xl p-5 max-w-md mx-auto">
                <div className="flex items-center space-x-3 mb-4">
                  <div className="w-3 h-3 rounded-full bg-red-500"></div>
                  <div className="w-3 h-3 rounded-full bg-yellow-500"></div>
                  <div className="w-3 h-3 rounded-full bg-green-500"></div>
                  <div className="ml-2 text-sm text-gray-600">CloudScribe Agent</div>
                </div>
                
                <div className="bg-gray-50 rounded-lg p-4 mb-4">
                  <p className="text-gray-700 mb-2">
                    <span className="text-gray-400">User:</span> Show me all available compute instances in my project
                  </p>
                </div>
                
                <div className="bg-gradient-to-r from-blue-50 to-purple-50 rounded-lg p-4 mb-4">
                  <p className="text-gray-700 mb-2">
                    <span className="text-ai">CloudScribe:</span> I found 3 compute instances in your project:
                  </p>
                  <ul className="list-disc list-inside text-gray-600 text-sm ml-2">
                    <li>web-server-01 (Running) - 4 vCPUs, 8GB RAM</li>
                    <li>db-server-01 (Running) - 8 vCPUs, 16GB RAM</li>
                    <li>test-instance (Stopped) - 2 vCPUs, 4GB RAM</li>
                  </ul>
                </div>
                
                <div className="relative">
                  <input 
                    type="text" 
                    placeholder="Type your request..." 
                    className="w-full border border-gray-200 rounded-full py-2 px-4 focus:outline-none focus:ring-2 focus:ring-cloud"
                  />
                  <div className="absolute right-2 top-1/2 transform -translate-y-1/2 bg-gradient-to-r from-cloud to-ai rounded-full p-1">
                    <ArrowRight className="h-4 w-4 text-white" />
                  </div>
                </div>
              </div>
            </div>
            
            {/* Background decorations */}
            <div className="absolute -top-10 -right-10 w-64 h-64 bg-gradient-to-r from-cloud-light/30 to-ai-light/30 rounded-full filter blur-3xl animate-pulse-slow"></div>
            <div className="absolute -bottom-10 -left-10 w-64 h-64 bg-gradient-to-r from-ai-light/30 to-cloud-light/30 rounded-full filter blur-3xl animate-pulse-slow animation-delay-1000"></div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default HeroSection;
