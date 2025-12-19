import React from 'react';
import { EMAIL_CONTACT } from '../constants';
import Logo from './Logo';

const Footer: React.FC = () => {
  return (
    <footer className="relative border-t border-gray-200/60 pt-16 pb-12 overflow-hidden">
        {/* Footer Background wash */}
        <div className="absolute inset-0 bg-white/40 backdrop-blur-sm -z-10"></div>
        
      <div className="container mx-auto px-6 flex flex-col md:flex-row justify-between items-center gap-6">
        <div className="text-center md:text-left">
          <div className="mb-4 flex justify-center md:justify-start">
            <Logo variant="footer" className="opacity-90" />
          </div>
          <p className="text-xs text-gray-400 font-light">
            &copy; {new Date().getFullYear()} DETAILER. All rights reserved.
          </p>
        </div>
        
        <div className="text-center md:text-right">
          <a 
            href={`mailto:${EMAIL_CONTACT}`} 
            className="text-sm font-medium text-gray-500 hover:text-primary transition-colors block mb-2"
          >
            {EMAIL_CONTACT}
          </a>
          <div className="text-xs text-gray-400 flex items-center justify-center md:justify-end gap-3">
            <span className="cursor-pointer hover:text-gray-600 transition-colors">이용약관</span> 
            <span className="w-px h-3 bg-gray-300"></span>
            <span className="cursor-pointer hover:text-gray-600 transition-colors">개인정보처리방침</span>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;