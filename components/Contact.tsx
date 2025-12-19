import React from 'react';
import { Mail, Clock, ArrowRight } from 'lucide-react';
import { EMAIL_CONTACT } from '../constants';
import FadeIn from './ui/FadeIn';

const Contact: React.FC = () => {
  return (
    <section id="contact" className="py-24 bg-primary text-white relative overflow-hidden">
      {/* Background Artistic Elements */}
      <div className="absolute top-0 right-0 w-[600px] h-[600px] bg-secondary/30 rounded-full blur-[120px] translate-x-1/3 -translate-y-1/3 pointer-events-none" />
      <div className="absolute bottom-0 left-0 w-[500px] h-[500px] bg-black/20 rounded-full blur-[100px] -translate-x-1/3 translate-y-1/3 pointer-events-none" />

      <div className="container mx-auto px-6 relative z-10">
        <div className="flex flex-col md:flex-row items-center justify-between gap-16">
          
          <div className="w-full md:w-1/2">
            <FadeIn>
              <h2 className="text-3xl md:text-4xl font-light mb-6">
                가장 <span className="font-bold">심플하게</span><br/> 
                작업을 시작하세요.
              </h2>
              <p className="text-gray-300 mb-10 leading-relaxed text-lg font-light">
                복잡한 견적서는 없습니다.<br />
                원하시는 상품의 링크만 보내주시면<br />
                가장 알맞은 구성을 제안해 드립니다.
              </p>
              
              <a 
                href={`mailto:${EMAIL_CONTACT}`}
                className="group inline-flex items-center gap-4 bg-white text-primary px-8 py-5 rounded-full font-bold hover:bg-accent hover:text-primary transition-all shadow-lg hover:shadow-xl hover:-translate-y-1"
              >
                <Mail size={22} className="text-primary" />
                <span>이메일 문의하기</span>
                <ArrowRight size={20} className="group-hover:translate-x-1 transition-transform" />
              </a>
              <p className="mt-6 text-sm text-gray-400 font-light ml-2">{EMAIL_CONTACT}</p>
            </FadeIn>
          </div>

          <div className="w-full md:w-5/12">
            <FadeIn delay={200}>
              <div className="bg-white/5 backdrop-blur-md p-10 rounded-3xl border border-white/10 shadow-2xl">
                <div className="flex items-center gap-3 mb-8 text-accent">
                  <Clock size={24} />
                  <span className="text-lg font-bold tracking-wide">예상 소요 시간</span>
                </div>
                <div className="space-y-6">
                  <div className="flex justify-between items-center border-b border-white/10 pb-4">
                    <span className="text-gray-300 font-light">한국어 번역</span>
                    <span className="font-bold text-white text-lg">약 1일</span>
                  </div>
                  <div className="flex justify-between items-center border-b border-white/10 pb-4">
                    <span className="text-gray-300 font-light">번역 + 히어로</span>
                    <span className="font-bold text-white text-lg">약 1일</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-gray-300 font-light">상세페이지 제작</span>
                    <span className="font-bold text-white text-lg">1~2일</span>
                  </div>
                </div>
                <div className="mt-8 text-xs text-gray-400 font-light leading-relaxed">
                  * 주문량이 많을 경우 스케줄이 조정될 수 있습니다.<br/>
                  * 급행 작업은 메일에 별도로 표기해 주세요.
                </div>
              </div>
            </FadeIn>
          </div>

        </div>
      </div>
    </section>
  );
};

export default Contact;