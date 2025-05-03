import { Card, CardContent } from "@/components/ui/card";

const HowItWorksSection = () => {
  const steps = [
    {
      number: "01",
      title: "Ask in Natural Language",
      description: "Type your request as if you were talking to a colleague. For example, 'Show me all my compute instances' or 'Create a new VM with 4 CPUs and 8GB RAM'."
    },
    {
      number: "02",
      title: "AI Processing",
      description: "The agent parses your request, identifies your intent, and maps it to the appropriate OpenStack API calls."
    },
    {
      number: "03",
      title: "Confirmation (if needed)",
      description: "For any actions that create, modify, or delete resources, the agent will ask for your explicit confirmation."
    },
    {
      number: "04",
      title: "Execution & Feedback",
      description: "Once confirmed, the agent executes the necessary API calls and provides clear feedback on the results."
    }
  ];

  return (
    <section id="how-it-works" className="py-16 md:py-24">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center max-w-3xl mx-auto mb-16">
          <h2 className="text-3xl md:text-4xl font-bold mb-6">
            <span className="bg-clip-text text-transparent bg-gradient-to-r from-cloud to-ai">
              How It Works
            </span>
          </h2>
          <p className="text-xl text-gray-600">
            CloudScribe's agentic AI simplifies cloud management through a conversational interface
          </p>
        </div>

        <div className="relative">
          {/* Connection line */}
          <div className="absolute left-1/2 top-0 bottom-0 w-0.5 bg-gradient-to-b from-cloud to-ai hidden md:block" style={{ transform: 'translateX(-50%)' }}></div>
          
          <div className="space-y-12 md:space-y-0">
            {steps.map((step, index) => (
              <div key={index} className="flex flex-col md:flex-row md:items-center">
                <div className={`md:w-1/2 ${index % 2 === 0 ? 'md:pr-16' : 'md:order-2 md:pl-16'}`}>
                  <Card className={`border-t-4 ${index % 2 === 0 ? 'border-t-cloud' : 'border-t-ai'} shadow-lg`}>
                    <CardContent className="pt-6">
                      <div className="mb-4 flex items-baseline">
                        <span className={`text-4xl font-bold mr-4 ${index % 2 === 0 ? 'text-cloud' : 'text-ai'}`}>
                          {step.number}
                        </span>
                        <h3 className="text-xl font-semibold">{step.title}</h3>
                      </div>
                      <p className="text-gray-600">{step.description}</p>
                    </CardContent>
                  </Card>
                </div>
                
                {/* Circle connector */}
                <div className="hidden md:flex items-center justify-center md:w-0">
                  <div className={`w-8 h-8 rounded-full ${index % 2 === 0 ? 'bg-cloud' : 'bg-ai'} flex items-center justify-center z-10`}>
                    <div className="w-3 h-3 rounded-full bg-white"></div>
                  </div>
                </div>
                
                <div className={`md:w-1/2 ${index % 2 === 0 ? 'md:order-2' : 'md:pr-16'} hidden md:block`}>
                  {/* Empty space for alternating layout */}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
};

export default HowItWorksSection;
