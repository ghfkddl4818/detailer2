import React from 'react';
import { Check } from 'lucide-react';
import { SERVICES } from '../constants';
import FadeIn from './ui/FadeIn';

const Services: React.FC = () => {
  return (
    <section id="services" className="py-24 relative">
      <div className="container mx-auto px-6 relative z-10">
        <div className="text-center mb-20">
          <FadeIn>
            <h2 className="text-3xl font-bold text-primary mb-4">서비스 안내</h2>
            <div className="w-10 h-1 bg-accent mx-auto rounded-full mb-4 opacity-70"></div>
            <p className="text-gray-500">복잡한 거품을 뺀 담백한 구성</p>
          </FadeIn>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-6xl mx-auto">
          {SERVICES.map((service, index) => (
            <FadeIn key={service.id} delay={index * 150} className="h-full">
              {/* Card Container with Paper/Glass Effect */}
              <div className="bg-white/70 backdrop-blur-md p-8 rounded-3xl shadow-card hover:shadow-xl hover:bg-white/90 transition-all duration-500 h-full flex flex-col relative overflow-hidden group border border-white/50">
                {/* Subtle Watercolor Hover wash */}
                <div className="absolute top-0 right-0 w-32 h-32 bg-accent/20 rounded-full blur-2xl -translate-y-1/2 translate-x-1/2 opacity-0 group-hover:opacity-100 transition-opacity duration-700" />
                
                <div className="relative z-10">
                  <h3 className="text-xl font-bold text-primary mb-2">{service.title}</h3>
                  <div className="mb-6 flex items-baseline gap-1">
                    <span className="text-3xl font-bold text-primary">{service.price}</span>
                  </div>
                  
                  <p className="text-gray-500 mb-8 text-sm leading-relaxed min-h-[60px]">
                    {service.description}
                  </p>

                  <ul className="space-y-4 mb-8 flex-grow">
                    {service.features.map((feature, i) => (
                      <li key={i} className="flex items-start text-sm text-gray-600">
                        <div className="bg-accent/40 rounded-full p-1 mr-3 mt-0.5 text-primary">
                          <Check size={12} strokeWidth={3} />
                        </div>
                        <span>{feature}</span>
                      </li>
                    ))}
                  </ul>

                  <div className="mt-auto pt-6 border-t border-gray-100/50 text-center">
                    <p className="text-xs text-secondary font-medium px-4 py-2 bg-white/50 rounded-full inline-block group-hover:bg-white group-hover:shadow-sm transition-colors border border-transparent group-hover:border-gray-100">
                      {service.summary}
                    </p>
                  </div>
                </div>
              </div>
            </FadeIn>
          ))}
        </div>
      </section>
  );
};

export default Services;