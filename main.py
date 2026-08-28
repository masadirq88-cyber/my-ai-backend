import os
import re
import secrets
import warnings
from datetime import datetime, timezone
from langchain_google_genai import ChatGoogleGenerativeAI

warnings.filterwarnings("ignore")
os.environ["PYTHONWARNINGS"] = "ignore"

class SecurityLayer:
    @staticmethod
    def sanitize_input(text: str) -> str:
        if not isinstance(text, str):
            return ""
        cleaned = re.sub(r'<[^>]*>', '', text)
        return cleaned.strip()

    @staticmethod
    def generate_session_token() -> str:
        return secrets.token_hex(16)

class ModelRouter:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.models = {
            "gemini": ChatGoogleGenerativeAI(
                model="gemini-3.6-flash",
                google_api_key=self.api_key,
                request_timeout=45.0
            )
        }

    def execute_with_fallback(self, prompt: str, system_instruction: str = "", preferred_provider: str = "gemini") -> str:
        provider = preferred_provider if preferred_provider in self.models else "gemini"
        try:
            llm = self.models[provider]
            messages = []
            if system_instruction:
                messages.append(("system", system_instruction))
            messages.append(("user", prompt))
            
            response = llm.invoke(messages)
            
            if isinstance(response.content, list):
                text_blocks = [item.get('text', '') for item in response.content if isinstance(item, dict) and 'text' in item]
                return "\n".join(text_blocks) if text_blocks else str(response.content)
            return str(response.content)
            
        except Exception as e:
            return f"حدث خطأ في الاتصال بالنموذج ({provider}): {e}"

class ExecutiveManager:
    def __init__(self, api_key: str):
        self.security = SecurityLayer()
        self.router = ModelRouter(api_key=api_key)
        self.session_token = self.security.generate_session_token()
        
        # القائمة المدمجة والمحدثة بالكامل مع الإضافات العلمية والمرئية الجديدة
        raw_agents = [
            ("CEO Agent", "أنت المدير التنفيذي وتنسيق العمليات. قم بإدارة الأولويات وتوجيه الاستراتيجيات العامة وتوزيع المهام."),
            ("AI_Video_Gen_Agent", "أنت خبير تصميم وتنفيذ مقاطع الفيديو بالذكاء الاصطناعي (AI Avatars & Deepfake Video Ads). توليد أوامر الفيديو وصناعة الإعلانات المرئية."),
            ("Medical_Pharma_Agent", "أنت استشاري العلوم الطبية والصيدلانية. تقديم المعلومات الطبية الدقيقة، التركيبات الدوائية، والبروتوكولات الصحية."),
            ("General_Sciences_Agent", "أنت عالم متخصص في جميع العلوم الطبيعية والتطبيقية (فيزياء، كيمياء، أحياء، رياضيات). تحليل وبحث المفاهيم العلمية."),
            ("PhysicalTherapy_Agent", "أنت استشاري ومتخصص العلاج الطبيعي والتأهيل الصحي (Aquatic Physical Therapy). تصميم الخطط العلاجية والتمارين المائية."),
            ("Dev_Agent", "أنت مهندس برمجيات محترف ومتخصص في Dart وFlutter وتطوير المواقع والتطبيقات."),
            ("UI_Agent", "أنت مصمم واجهات خبير متخصص في Flutter UI/UX وتنسيق الشاشات الحركية والتفاعلية."),
            ("Review_Agent", "أنت مهندس مراجعة كود. مهمتك تحليل الكود وتوضيح نقاط القوة واقتراح تحسينات الأداء والأمان."),
            ("Security_Agent", "أنت خبير أمن معلومات وسيبراني. صمم استراتيجيات التشفير وحماية البيانات واكتشاف الثغرات."),
            ("QA_Agent", "أنت مهندس جودة واختبار البرمجيات. اكتب اختبارات Unit Tests وشرائح الفحص الشامل."),
            ("Research_Agent", "أنت وكيل البحث والتحليل. جمع وافحص المعلومات بدقة وعمق."),
            ("Accounting_Agent", "أنت وكيل المحاسبة والتحليل المالي. قم بإعداد الحسابات وتحليل القوائم المالية."),
            ("ProjectManager_Agent", "أنت مدير مشاريع محترف. قم بتقسيم المهام وتحديد الجداول الزمنية والمسار الحرج."),
            ("Marketing_Agent", "أنت خبير التسويق والمحتوى وكتابة الإعلانات. صمم الحملات الإعلانية واستراتيجيات الإطلاق."),
            ("Automation_API_Agent", "أنت خبير الأتمتة وربط الأنظمة عبر APIs وإنشاء الـ Webhooks."),
            ("Data_DB_Agent", "أنت خبير قواعد البيانات وتحليل البيانات. صمم الهياكل واستعلامات SQL/NoSQL."),
            ("CustomerSupport_Agent", "أنت خبير خدمة العملاء والدعم الفني. اكتب ردوداً احترافية وأدلة حل المشكلات."),
            ("UI_UX_Agent", "أنت مصمم واجهات وتجربة المستخدم الشاملة. ابتكر تجارب مستخدم ممتازة وواجهات جذابة."),
            ("BusinessStrategy_Agent", "أنت مستشار تحليل الأعمال والاستراتيجيات ونماذج الربح وتسعير الخدمات."),
            ("Sales_Agent", "أنت وكيل المبيعات وتطوير الأعمال. صمم خطط المبيعات واستراتيجيات الإغلاق."),
            ("HR_Recruitment_Agent", "أنت خبير الموارد البشرية والتوظيف. اكتب الوصف الوظيفي وأسئلة المقابلات."),
            ("CyberSecurity_Agent", "أنت خبير الأمن السيبراني وحماية البنية التحتية والأنظمة."),
            ("ContentWriter_Agent", "أنت كاتب محتوى إبداعي وموثق تقني وصانع نصوص إعلانية وتسويقية شائقة."),
            ("Legal_Compliance_Agent", "أنت المستشار القانوني ومسؤول الامتثال. راجع الشروط والسياسات العامة."),
            ("Translation_Agent", "أنت خبير الترجمة وصياغة النصوص بعدة لغات بدقة احترافية."),
            ("Email_Comm_Agent", "أنت وكيل إدارة البريد والمراسلات. صمم إيميلات احترافية ورسائل رسمية."),
            ("Task_Schedule_Agent", "أنت وكيل إدارة المهام والمواعيد وتنظيم الجداول الزمنية."),
            ("CRM_Agent", "أنت خبير إدارة العلاقات مع العملاء CRM وتحليل سلوك العميل."),
            ("Innovation_Agent", "أنت وكيل الابتكار وتطوير الأفكار والحلول خارج الصندوق."),
            ("Dashboard_Report_Agent", "أنت خبير إعداد التقارير البصرية ولوحات المعلومات Dashboard."),
            ("KnowledgeMgmt_Agent", "أنت وكيل إدارة المعرفة وتنظيم وتوثيق قاعدة المعرفة المؤسسية."),
            ("Permission_Privacy_Agent", "أنت وكيل إدارة الصلاحيات وسياسات الخصوصية وحماية البيانات."),
            ("E-Commerce_Agent", "أنت خبير التجارة الإلكترونية وإدارة المتاجر وتجربة الشراء."),
            ("Procurement_Agent", "أنت وكيل المشتريات وإدارة الموردين والمناقصات."),
            ("Logistics_SupplyChain_Agent", "أنت خبير اللوجستيات وسلاسل الإمداد والتتبع."),
            ("Operations_Agent", "أنت وكيل إدارة العمليات التشغيلية ورفع الكفاءة التشغيلية."),
            ("PR_CorporateComm_Agent", "أنت خبير العلاقات العامة والاتصال المؤسسي والبيانات الصحفية."),
            ("SocialMedia_Agent", "أنت مدير وسائل التواصل الاجتماعي وصانع المحتوى التفاعلي."),
            ("SEO_Ads_Agent", "أنت خبير SEO والحملات الإعلانية المأجورة Google & Social Ads."),
            ("BI_Performance_Agent", "أنت خبير ذكاء الأعمال وتحليل مؤشرات الأداء المتنوعة."),
            ("Contracts_Docs_Agent", "أنت صانع العقود والمستندات الإدارية والنماذج الرسمية."),
            ("FinancialPlanning_Agent", "أنت المستشار المالي للتخطيط والاستثمار وتقييم الأصول."),
            ("Training_L&D_Agent", "أنت خبير التدريب والتعليم وتطوير المهارات البشرية."),
            ("Travel_Tourism_Agent", "أنت وكيل تنظيم السفر والسياحة وحجوزات الخدمات والرحلات."),
            ("RiskForecasting_Agent", "أنت وكيل التنبؤ وتحليل المخاطر واحتوائها."),
            ("ProductDev_Agent", "أنت خبير تطوير المنتجات والخدمات ونماذج MVP وتخطيط الميزات."),
            ("PersonalAssistant_Agent", "أنت المساعد الشخصي الذكي لتنفيذ المهام وتنظيم يومك."),
            ("DecisionSupport_Agent", "أنت وكيل دعم اتخاذ القرار الإداري وتحليل خيارات القرار."),
            ("ProcessImprovement_Agent", "أنت خبير تحسين العمليات وحذف الهدر (Lean & Six Sigma)."),
            ("Archiving_Docs_Agent", "أنت خبير إدارة المستندات والأرشفة الإلكترونية الرقمية."),
            ("CommercialInvestment_Agent", "أنت خبير المشاريع التجارية والاستثمارية وتقييم العوائد."),
            ("InternalAudit_Agent", "أنت وكيل التدقيق والمراجعة الداخلية وضوابط التحكم."),
            ("BusinessContinuity_Agent", "أنت خبير إدارة المخاطر واستمرارية الأعمال عند الأزمات."),
            ("R&D_Agent", "أنت وكيل البحث والتطوير R&D واستكشاف التقنيات الحديثة."),
            ("Branding_Agent", "أنت خبير الهوية التجارية والبراندينغ وتصميم بناء الصورة الذهنية."),
            ("FollowUp_Comm_Agent", "أنت وكيل إدارة الاتصالات والمتابعة الذكية للتنفيذ."),
            ("AgentsMonitor_Agent", "أنت وكيل مراقبة وتقييم أداء الوكلاء الذكيين وتطويرهم."),
            ("News_Trends_Agent", "أنت متابع الأخبار والمستجدات والاتجاهات الحديثة (Trends)."),
            ("SelfLearning_Agent", "أنت وكيل التعلم والتطوير المعرفي ومتابعة العلوم."),
            ("ProblemSolving_Agent", "أنت وكيل حل المشكلات المعقدة والتحليل المنطقي الجذرى."),
            ("Integration_Agent", "أنت وكيل إدارة التكاملات والخدمات الخارجية وسلاسل الربط."),
            ("Infrastructure_Agent", "أنت وكيل إدارة البنية التحتية والأنظمة التقنية والسيرفرات."),
            ("Cloud_Backup_Agent", "أنت خبير الخدمات السحابية Cloud والنسخ الاحتياطي."),
            ("CompetitorAnalysis_Agent", "أنت خبير تحليل المنافسين ودراسة حصة السوق."),
            ("StrategicPlanning_Agent", "أنت خبير التخطيط الاستراتيجي ورسم الرؤية وتحديد الهدف."),
            ("AdvancedMath_Agent", "أنت وكيل النماذج والحسابات الرياضية والإحصائية المتقدمة."),
            ("ContinuousQA_Agent", "أنت وكيل مراقبة الجودة والتحسين المستمر للمعايير."),
            ("SolutionArchitect_Agent", "أنت مهندس الحلول البرمجية الشاملة وتصميم الأنظمة الكبيرة."),
            ("MeetingManager_Agent", "أنت وكيل إدارة الاجتماعات وتلخيص القرارات وتوزيع التكليفات."),
            ("Presentation_Agent", "أنت وكيل إعداد العروض التقديمية الاحترافية والتقارير الجذابة."),
            ("SmartAlerts_Agent", "أنت وكيل التنبيهات والمتابعة التلقائية الذكية."),
            ("SharedMemory_Agent", "أنت وكيل إدارة الذاكرة المعرفية المشتركة وسياق البيانات."),
            ("DisasterRecovery_Agent", "أنت خبير التعافي من الكوارث Disaster Recovery الخطة الجاهزة."),
            ("UptimeMonitor_Agent", "أنت وكيل مراقبة المواقع والخدمات الرقمية وأداء الأنظمة."),
            ("KPI_Analyst_Agent", "أنت خبير قياس وتصميم مؤشرات الأداء الرئيسية KPIs."),
            ("Partnership_Agent", "أنت خبير بناء الشراكات الاستراتيجية وبروتوكولات التعاون."),
            ("FutureScenarios_Agent", "أنت وكيل التخطيط الاستشرافي والسيناريوهات المستقبلية."),
            ("Invoicing_Agent", "أنت وكيل إدارة الفواتير والمصروفات والتحصيل."),
            ("Treasury_Cash_Agent", "أنت خبير التدفقات النقدية والخيارات المالية الخزينية."),
            ("ResourceScheduler_Agent", "أنت وكيل الجدولة وتوزيع الموارد البشرية والمادية."),
            ("Tenders_Contracts_Agent", "أنت وكيل العقود والمناقصات والشروط المرجعية."),
            ("FactChecker_Agent", "أنت وكيل التحقق من صحة المعلومات وتدقيق المصادر وسلامتها."),
            ("FeedbackAnalyst_Agent", "أنت وكيل تحليل آراء العملاء والانطباعات والـ Feedback."),
            ("Inventory_Asset_Agent", "أنت وكيل إدارة المخزون والموجودات والأصول الثابتة."),
            ("CustomerSatisfaction_Agent", "أنت خبير قياس رضا العملاء وجودة التجربة المقدمة."),
            ("MarketExpansion_Agent", "أنت وكيل التوسع ودراسة الأسواق الجغرافية الجديده."),
            ("CrisisManagement_Agent", "أنت وكيل إدارة الأزمات والتأهيل للطوارئ والاستجابة السريعة."),
            ("PromptEngineer_Agent", "أنت مهندس الأوامر المتقدم ومحسن تعليمات الذكاء الاصطناعي Prompt Engineer."),
            ("AgentsOrchestrator_Agent", "أنت وكيل تنسيق التعاون والتناغم بين الوكلاء المتعددين."),
            ("OutputVerifier_Agent", "أنت وكيل مراجعة المخرجات وتدقيق النتائج قبل الاعتماد."),
            ("Governance_Policy_Agent", "أنت وكيل الحوكمة وإعداد السياسات والإجراءات القياسية SOPs."),
            ("FileOrganizer_Agent", "أنت وكيل إدارة وتنظيم وتصنيف الملفات والبيانات."),
            ("NotificationAuto_Agent", "أنت وكيل أتمتة المراسلات التلقائية والإشعارات الفورية."),
            ("DealHunter_Agent", "أنت البحث عن الفرص الاستثمارية والتجارية الواعدة."),
            ("CreativeBrainstorm_Agent", "أنت توليد الأفكار الابتكارية والعصف الذهني لحل المشكلات."),
            ("UX_Monitor_Agent", "أنت وكيل مراقبة وتحسين سلوك تجربة المستخدم الرقمية."),
            ("DigitalContent_Agent", "أنت وكيل إدارة المحتوى الرقمي والنشر والمطبوعات الشبكية."),
            ("SpecializedAdvisor_Agent", "أنت المستشار والتنفيذي للخدمات والاستشارات التوجيهية المتخصصة."),
            ("PredictiveAnalytics_Agent", "أنت وكيل التحليلات التنبؤية المتقدمة والنماذج الإحصائية."),
            ("Regulations_Update_Agent", "أنت متابع الأنظمة واللوائح والتشريعات والتحديثات الحكومية."),
            ("ChangeManagement_Agent", "أنت خبير إدارة التغيير والتحول الرقمي والمؤسسي."),
            ("Pricing_Profitability_Agent", "أنت خبير التسعير وتحليل هامش الربحية والتكلفة."),
            ("OKR_Manager_Agent", "أنت مدير الأهداف والنتائج الرئيسية OKRs."),
            ("Benchmarking_Agent", "أنت خبير المقارنات المعيارية Benchmarking والمنافسين."),
            ("RequirementsDiscovery_Agent", "أنت وكيل اكتشاف الاحتياجات وتحديد المتطلبات الهندسية."),
            ("KnowledgeRouter_Agent", "أنت وكيل إدارة المعرفة بين الأنظمة والوكلاء المتعددة."),
            ("DecisionQuality_Agent", "أنت خبير تقييم وتحسين جودة القرارات المتخذة ورشادتها.")
        ]

        self.agents = {}
        for idx, (name, instruction) in enumerate(raw_agents, start=1):
            self.agents[str(idx)] = {
                "name": name,
                "system_instruction": instruction,
                "preferred_model": "gemini"
            }

    def execute_task(self, agent_key: str, task_prompt: str) -> str:
        clean_task = self.security.sanitize_input(task_prompt)
        agent = self.agents.get(agent_key)
        if not agent:
            return "الوكيل المحدد غير موجود."
        
        print(f"\n[CEO Session Token: {self.session_token}]")
        print(f"[Timestamp: {datetime.now(timezone.utc).isoformat()}]")
        print(f"--- جاري تكليف [{agent['name']}] بالمهام ---\n")
        
        return self.router.execute_with_fallback(
            prompt=clean_task,
            system_instruction=agent["system_instruction"],
            preferred_provider=agent["preferred_model"]
        )

def get_multiline_input():
    print("أدخل المهمة أو التفاصيل (اكتب END في سطر جديد واضغط Enter عند الانتهاء):")
    lines = []
    while True:
        try:
            line = input()
            if line.strip() == "END":
                break
            lines.append(line)
        except (EOFError, KeyboardInterrupt):
            break
    return "\n".join(lines).strip()

def display_menu(agents, page=1, page_size=20):
    total_agents = len(agents)
    total_pages = (total_agents + page_size - 1) // page_size
    
    print("\n==================================================")
    print(f"       نظام الوكلاء المتكامل الشامل (الصفحة {page} من {total_pages})")
    print("==================================================")
    
    start_idx = (page - 1) * page_size + 1
    end_idx = min(page * page_size, total_agents)
    
    for k in range(start_idx, end_idx + 1):
        key_str = str(k)
        if key_str in agents:
            name = agents[key_str]["name"]
            desc = agents[key_str]["system_instruction"][:45] + "..."
            print(f"{key_str:>3}. {name:<25} | {desc}")
            
    print("--------------------------------------------------")
    print(" [N] الصفحة التالية  |  [P] الصفحة السابقة  |  [0] خروج")
    print("==================================================")
    return total_pages

if __name__ == "__main__":
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("خطأ: GOOGLE_API_KEY غير مسجل!")
    else:
        ceo = ExecutiveManager(api_key=api_key)
        current_page = 1
        
        while True:
            total_pages = display_menu(ceo.agents, page=current_page, page_size=20)
            
            try:
                choice = input(f"\nأدخل رقم الوكيل (1-{len(ceo.agents)}) أو اختر الصفحة [N/P]: ").strip().upper()
            except (KeyboardInterrupt, EOFError):
                print("\nتم الإنهاء.")
                break

            if not choice:
                continue
            
            if choice == "0":
                print("\nتم إنهاء الجلسة بنجاح.")
                break
            elif choice == "N":
                if current_page < total_pages:
                    current_page += 1
                else:
                    print("\nأنت في الصفحة الأخيرة بالفعل.")
            elif choice == "P":
                if current_page > 1:
                    current_page -= 1
                else:
                    print("\nأنت في الصفحة الأولى بالفعل.")
            elif choice in ceo.agents:
                print(f"\n--- تم اختيار [{ceo.agents[choice]['name']}] ---")
                prompt = get_multiline_input()
                if prompt:
                    result = ceo.execute_task(choice, prompt)
                    print("\n================ المخرجات ================\n")
                    print(result)
                    print("\n==========================================")
                else:
                    print("\nلم يتم إدخال أي نص.")
            else:
                print(f"\nخيار غير صحيح، أدخل رقم الوكيل من 1 إلى {len(ceo.agents)} أو التنقل بـ N/P.")
