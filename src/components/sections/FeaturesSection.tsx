import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Check, Code, Clock, Link, Search } from "lucide-react";

const FeaturesSection = () => {
  const features = [
    {
      icon: <Search className="h-10 w-10 text-cloud" />,
      title: "Natural Language Processing",
      description: "Simply type your request in plain English, and our AI will understand what you need and map it to the right API calls."
    },
    {
      icon: <Code className="h-10 w-10 text-ai" />,
      title: "OpenStack API Integration",
      description: "Seamlessly interfaces with OpenStack Compute (Nova), Network (Neutron), and Block-Storage (Cinder) APIs."
    },
    {
      icon: <Check className="h-10 w-10 text-cloud" />,
      title: "Safety Confirmation",
      description: "Before making any significant changes, the agent asks for your explicit confirmation to prevent unintended actions."
    },
    {
      icon: <Link className="h-10 w-10 text-ai" />,
      title: "Secure Communication",
      description: "All communications with OpenStack APIs are secured through TLS encryption, keeping your infrastructure safe."
    },
    {
      icon: <Clock className="h-10 w-10 text-cloud" />,
      title: "Request History",
      description: "Maintains a database of all user requests, making it easy to track changes and audit system interactions."
    }
  ];

  return (
    <section id="features" className="py-16 md:py-24 bg-gray-50">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center max-w-3xl mx-auto mb-16">
          <h2 className="text-3xl md:text-4xl font-bold mb-6">
            <span className="bg-clip-text text-transparent bg-gradient-to-r from-cloud to-ai">
              Powerful Features
            </span> 
            <span className="block mt-2">Designed for Cloud Engineers</span>
          </h2>
          <p className="text-xl text-gray-600">
            CloudScribe combines the power of AI with OpenStack's comprehensive APIs to streamline your cloud infrastructure management.
          </p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          {features.map((feature, index) => (
            <Card key={index} className="border border-gray-200 hover:shadow-md transition-shadow overflow-hidden">
              <div className="h-1 bg-gradient-to-r from-cloud to-ai"></div>
              <CardHeader>
                <div className="mb-4">{feature.icon}</div>
                <CardTitle className="text-xl">{feature.title}</CardTitle>
              </CardHeader>
              <CardContent>
                <CardDescription className="text-gray-600 text-base">
                  {feature.description}
                </CardDescription>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </section>
  );
};

export default FeaturesSection;
