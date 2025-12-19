import React from 'react';
import FadeIn from './ui/FadeIn';
import Logo from './Logo';

const Hero: React.FC = () => {
  return (
    <section className="relative min-h-screen flex items-center justify-center overflow-hidden pt-20">
      
      {/* Background Blobs (Watercolor effect) */}
      <div className="absolute top-1/4 left-1/2 -translate-x-1/2 w-[500px] h-[500px] bg-accent/30 rounded-full blur-[100px] -z-10 mix-blend-multiply opacity-70 animate-pulse" style={{ animationDuration: '8s' }} />
      <div className="absolute top-1/3 left-1/3 w-[300px] h-[300px] bg-purple-100 rounded-full blur-[80px] -z-10 mix-blend-multiply opacity-60" />
      
      <div className="container mx-auto px-6 text-center relative z-10">
        <FadeIn>
          <div className="mb-10 flex justify-center relative">
             {/* Glow effect behind logo */}
             <div className="absolute inset-0 bg-white/50 blur-xl scale-110 rounded-full z-0"></div>
             <div className="relative z-10 transform hover:scale-105 transition-transform duration-700 ease-out">
               <Logo variant="hero" />
             </div>
          </div>
        </FadeIn>

        <FadeIn delay={100}>
          <h2 className="text-secondary font-medium tracking-[0.2em] text-sm mb-6 uppercase">
            Art of Detail
          </h2>
        </FadeIn>
        
        <FadeIn delay={200}>
          <h1 className="text-4xl md:text-5xl lg:text-6xl font-light text-primary leading-tight md:leading-snug mb-8 word-keep-all tracking-tight">
            필요한 만큼만, <span className="font-bold">투명하게</span><br/>
            상세페이지의 결을 살립니다.
          </h1>
        </FadeIn>
        
        <FadeIn delay={400}>
          <p className="text-gray-500 text-base md:text-lg mb-12 max-w-2xl mx-auto word-keep-all leading-relaxed">
            중국 상세페이지의 거친 느낌을 지우고,<br className="md:hidden" /> 
            한국 소비자의 감성에 스며드는<br className="hidden md:block" /> 
            정갈한 번역과 디자인을 제공합니다.
          </p>
        </FadeIn>
        
        <FadeIn delay={600}>
          <div className="flex flex-col sm:flex-row gap-5 justify-center">
            <a 
              href="#services" 
              className="px-10 py-4 bg-primary text-white font-medium rounded-full hover:bg-secondary transition-all duration-300 shadow-soft hover:shadow-lg hover:-translate-y-1"
            >
              서비스 보기
            </a>
            <a 
              href="#portfolio" 
              className="px-10 py-4 bg-white text-primary border border-gray-100 font-medium rounded-full hover:border-accentDark hover:text-accentDark transition-all duration-300 shadow-sm hover:shadow-md"
            >
              포트폴리오
            </a>
          </div>
        </FadeIn>
      </div>
    </section>
  );
};

export default Hero;