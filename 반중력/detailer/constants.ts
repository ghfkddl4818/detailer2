import { PortfolioCategory, PortfolioItem, ServiceItem, ServiceType } from './types';

// =========================================================================================
// [이미지 경로 설정]
// 1. 로컬 개발 시: "." (기본값)
// 2. 깃허브 호스팅 시: "https://raw.githubusercontent.com/[사용자ID]/[저장소명]/main" 
// =========================================================================================
export const IMAGE_BASE_URL = ".";

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
    title: '번역 + 히어로/썸네일',
    price: '33,000원',
    description: '번역에 더해 첫 화면과 썸네일을 깔끔하게 제작합니다.',
    features: [
      '전체 한국어 번역',
      '최상단 히어로 이미지 제작',
      '판매용 썸네일 이미지 제작',
      '깔끔한 배경/레이아웃 구성'
    ],
    summary: '본문은 유지, 첫인상은 완벽하게.',
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

export const PORTFOLIO_ITEMS: PortfolioItem[] = [
  {
    id: 'p1',
    title: '기본 번역 예시 (15,000원)',
    category: PortfolioCategory.TRANSLATION,
    beforeImage: `${IMAGE_BASE_URL}/원문_한글_번역/PT1/before.jpg`,
    afterImage: `${IMAGE_BASE_URL}/원문_한글_번역/PT1/after.jpg`,
    description: '중국어 원문의 배치를 유지하되 가독성을 높인 기본 번역'
  },
  {
    id: 'p2',
    title: '썸네일 제작 예시 (4,000원)',
    category: PortfolioCategory.TRANSLATION,
    beforeImage: `${IMAGE_BASE_URL}/원문_한글_번역/PT2/PT2_썸네일_원문.png`,
    afterImage: `${IMAGE_BASE_URL}/원문_한글_번역/PT2/PT2_썸네일_제작.png`,
    description: '클릭을 유도하는 깔끔한 한글 썸네일 제작'
  },
  {
    id: 'p3',
    title: '번역 + 히어로/썸네일 (33,000원)',
    category: PortfolioCategory.TRANSLATION,
    beforeImage: `${IMAGE_BASE_URL}/원문_한글_번역/PT3/before.jpg`,
    afterImage: `${IMAGE_BASE_URL}/원문_한글_번역/PT3/PT3_히어로섹션_제작.png`,
    description: '상세페이지의 첫인상을 결정하는 히어로 섹션 디자인'
  },
  {
    id: 'p4',
    title: '상세페이지 전체 제작 (44,000원)',
    category: PortfolioCategory.CREATION,
    afterImage: `${IMAGE_BASE_URL}/제작/full_page.jpg`,
    description: '인트로, 포인트, 디테일 컷까지 흐름을 고려한 전체 제작'
  },
  {
    id: 'p5',
    title: '노블레스 시그니처 필로우 (제작)',
    category: PortfolioCategory.CREATION,
    afterImage: `${IMAGE_BASE_URL}/제작/PT4_상세페이지_제작.png`,
    description: '프리미엄 침구 브랜드의 고급스러운 상세페이지 제작 예시'
  }
];