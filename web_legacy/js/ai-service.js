/**
 * AI Service for handling responses and recommendations
 */
class AIService {
    constructor() {
        this.responses = {
            greeting: [
                "안녕하세요! 😊 무엇을 도와드릴까요?",
                "반갑습니다! 프로젝트에 대해 궁금한 점이 있으신가요?",
                "안녕하세요! Joy입니다. 어떤 도움이 필요하신가요?"
            ],
            projectStructure: [
                "프로젝트 구조는 다음과 같이 구성하는 것을 추천드립니다:\n\n1. css/ - 스타일시트 (variables, components, layout)\n2. js/ - 자바스크립트 모듈\n3. images/ - 이미지 및 에셋\n4. index.html - 메인 진입점\n\n이렇게 분리하면 유지보수가 훨씬 쉬워집니다!",
                "좋은 프로젝트 구조는 확장성과 유지보수성을 고려해야 합니다.\n\n기능별로 폴더를 나누고, 특히 CSS와 JS를 역할별로 분리하는 것이 좋습니다.\n\n현재 프로젝트 구조도 아주 좋네요! 👍"
            ],
            codeReview: [
                "코드 리뷰를 도와드리겠습니다! 📝\n\n다음 사항들을 확인해보세요:\n- 코드 가독성\n- 성능 최적화\n- 에러 핸들링\n- 보안 취약점\n\n구체적인 코드를 보여주시면 더 자세히 도와드릴 수 있습니다!",
                "코드 리뷰는 코드 품질 향상에 매우 중요합니다.\n\n변수명이 명확한가요? 함수가 단일 책임 원칙을 따르나요? 중복 코드는 없나요?\n\n코드를 공유해주시면 구체적인 피드백을 드리겠습니다!"
            ],
            debugging: [
                "버그를 해결하는 방법:\n\n1. 에러 메시지를 자세히 읽기\n2. console.log()로 변수 값 확인\n3. 브라우저 개발자 도구 활용\n4. 단계별로 코드 실행 추적\n\n어떤 에러가 발생했나요?",
                "디버깅은 체계적으로 접근하는 것이 중요합니다.\n\n에러가 발생하는 정확한 위치를 파악하고, 예상되는 값과 실제 값을 비교해보세요.\n\n구체적인 에러 내용을 알려주시면 더 도움을 드릴 수 있습니다!"
            ],
            technology: [
                "최신 기술 트렌드를 따라가는 것도 중요하지만, 프로젝트에 적합한 기술을 선택하는 것이 더 중요합니다.\n\n어떤 기술 스택을 고민하고 계신가요?",
                "기술 선택 시 고려사항:\n- 프로젝트 요구사항\n- 팀의 기술 숙련도\n- 커뮤니티 지원\n- 장기적인 유지보수\n\n구체적으로 어떤 기술에 대해 궁금하신가요?"
            ],
            help: [
                "제가 도와드릴 수 있는 것들:\n\n💡 프로젝트 아이디어 및 구조 제안\n🔍 코드 리뷰 및 최적화\n🐛 버그 디버깅 지원\n📚 기술 학습 가이드\n🚀 베스트 프랙티스 공유\n\n무엇이 필요하신가요?",
                "언제든지 편하게 질문해주세요!\n\n코딩, 디자인, 아키텍처, 배포 등 프로젝트의 모든 단계에서 도움을 드릴 수 있습니다. 😊"
            ],
            thanks: [
                "천만에요! 😊 더 궁금한 점이 있으시면 언제든 물어보세요!",
                "도움이 되었다니 기쁩니다! 프로젝트 진행하시면서 막히는 부분이 있으면 언제든 찾아주세요!",
                "별말씀을요! 함께 멋진 프로젝트 만들어가요! 🚀"
            ],
            default: [
                "흥미로운 질문이네요! 🤔\n\n좀 더 구체적으로 설명해주시면 더 정확한 답변을 드릴 수 있습니다.",
                "그 부분에 대해 함께 고민해볼까요?\n\n프로젝트의 맥락을 조금 더 알려주시면 더 도움이 될 것 같습니다!",
                "좋은 질문입니다!\n\n어떤 방향으로 접근하고 싶으신지 말씀해주시면 구체적인 조언을 드리겠습니다.",
                "제가 도와드릴 수 있도록 조금 더 자세히 설명해주시겠어요? 😊"
            ]
        };
    }

    generateResponse(userMessage) {
        const lowerMessage = userMessage.toLowerCase();
        
        // Determine response category
        if (lowerMessage.match(/안녕|하이|hello|hi|헬로/)) {
            return this.randomChoice(this.responses.greeting);
        } else if (lowerMessage.match(/프로젝트 구조|폴더 구조|디렉토리|structure/)) {
            return this.randomChoice(this.responses.projectStructure);
        } else if (lowerMessage.match(/코드 리뷰|리뷰|review|피드백/)) {
            return this.randomChoice(this.responses.codeReview);
        } else if (lowerMessage.match(/버그|에러|오류|디버그|debug|error/)) {
            return this.randomChoice(this.responses.debugging);
        } else if (lowerMessage.match(/기술|스택|프레임워크|라이브러리|tech|framework/)) {
            return this.randomChoice(this.responses.technology);
        } else if (lowerMessage.match(/도움|help|뭐|what|어떻게/)) {
            return this.randomChoice(this.responses.help);
        } else if (lowerMessage.match(/감사|고마|thanks|thank/)) {
            return this.randomChoice(this.responses.thanks);
        } else {
            return this.randomChoice(this.responses.default);
        }
    }
    
    randomChoice(array) {
        return array[Math.floor(Math.random() * array.length)];
    }
}

export default new AIService();
