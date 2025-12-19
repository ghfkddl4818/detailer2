import { PortfolioCategory, PortfolioItem, ServiceItem, ServiceType } from './types';

export const EMAIL_CONTACT = "detailer4818@gmail.com";

export const SERVICES: ServiceItem[] = [
  {
    id: 'basic',
    title: '한국어 번역',
    price: '15,000원',
    description: '중국 상세페이지를 한국 판매용 한국어로 번역합니다.',
    features: [
      '중국어 → 한국어 번역',
      '자연스러운 판매 문구로 정리',
      '원본 구성 유지',
      '수정 1회 포함'
    ],
    summary: '구조는 그대로, 텍스트만 한국어로.',
    type: ServiceType.TRANSLATION
  },
  {
    id: 'standard',
    title: '한국어 번역 + 상단 히어로 1장',
    price: '33,000원',
    description: '번역에 더해 첫 화면을 정리해 제작합니다.',
    features: [
      '전체 한국어 번역',
      '최상단 히어로 이미지 1장 제작',
      '제품명 및 핵심 문구 배치',
      '깔끔한 배경/레이아웃 구성'
    ],
    summary: '본문은 유지, 첫인상만 새로.',
    type: ServiceType.PARTIAL
  },
  {
    id: 'premium',
    title: '상세페이지 제작',
    price: '44,000원',
    description: '번역을 포함해 바로 사용할 수 있는 상세페이지를 제작합니다.',
    features: [
      '전체 한국어 번역',
      '상세페이지 전체 디자인 정리',
      '문구 배치 및 흐름 정리',
      '이미지 구성 최적화'
    ],
    summary: '바로 업로드할 수 있는 완성본.',
    type: ServiceType.FULL
  }
];

// Note: For production build, ensure images are in the public folder
export const PORTFOLIO_ITEMS: PortfolioItem[] = [
  {
    id: 'p1',
    title: '생활용품 번역 예시',
    category: PortfolioCategory.TRANSLATION,
    beforeImage: './p1_before.jpg',
    afterImage: './p1_after.jpg',
    description: '중국어 원문의 배치를 유지하되 가독성을 높인 번역'
  },
  {
    id: 'p2',
    title: '전자기기 번역 예시',
    category: PortfolioCategory.TRANSLATION,
    beforeImage: './p2_before.jpg',
    afterImage: './p2_after.jpg',
    description: '기술적 용어를 자연스러운 한국어 표현으로 변경'
  },
  {
    id: 'p3',
    title: '의류 번역 예시',
    category: PortfolioCategory.TRANSLATION,
    beforeImage: './p3_before.jpg',
    afterImage: './p3_after.jpg',
    description: '감성적인 뉘앙스를 살린 의류 상세페이지 번역'
  },
  {
    id: 'p4',
    title: '캠핑용품 상세페이지 제작',
    category: PortfolioCategory.CREATION,
    afterImage: './p4_after.jpg',
    description: '인트로, 포인트, 디테일 컷까지 흐름을 고려한 전체 제작'
  }
];