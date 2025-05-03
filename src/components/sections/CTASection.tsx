import { Button } from "@/components/ui/button";
import { ArrowRight } from "lucide-react";

const CTASection = () => {
  return (
    <section className="py-16 md:py-24 bg-gradient-to-br from-cloud-dark to-ai-dark text-white">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-3xl md:text-4xl font-bold mb-6">
            Ready to Transform Your OpenStack Experience?
          </h2>
          <p className="text-xl text-white/80 mb-8 max-w-2xl mx-auto">
            Join the future of cloud management with natural language controls and intuitive AI assistance.
          </p>
          <div className="flex flex-col sm:flex-row justify-center gap-4">
            <Button size="lg" className="bg-white text-cloud-dark hover:bg-white/90 px-8">
              Get Early Access
              <ArrowRight className="ml-2 h-5 w-5" />
            </Button>
            <Button size="lg" variant="outline" className="border-white text-white hover:bg-white/20 px-8">
              Book a Demo
            </Button>
          </div>
        </div>
      </div>
    </section>
  );
};

export default CTASection;
