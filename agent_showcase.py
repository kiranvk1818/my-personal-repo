#!/usr/bin/env python3
"""
🤖 Agent Showcase Demo
A comprehensive demonstration of all agent capabilities
"""

import os
import sys
from datetime import datetime

# Add examples directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'examples'))

def main():
    """Run a comprehensive demo of all agents"""
    print("🤖 AI AGENT CAPABILITIES SHOWCASE")
    print("="*60)
    print(f"Demo started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Import agents
    try:
        from business_analytics.business_agent import BusinessAnalyticsAgent
        from content_creation.content_agent import ContentCreationAgent
        from research.research_agent import ResearchAgent
        from automation.automation_agent import AutomationAgent, TaskStatus, Priority
    except ImportError as e:
        print(f"❌ Error importing agents: {e}")
        print("💡 Please install dependencies: pip install -r examples/requirements.txt")
        return
    
    print("🎯 AGENT SHOWCASE: What Can These Agents Do?")
    print("-"*60)
    
    # 1. Business Analytics Demo
    print("\n📊 1. BUSINESS ANALYTICS AGENT")
    print("   Capabilities: Sales analysis, customer segmentation, KPI tracking")
    
    try:
        business_agent = BusinessAnalyticsAgent()
        business_agent.load_sample_data()
        
        # Quick analysis
        sales_insights = business_agent.analyze_sales_performance()
        print(f"   ✅ Total Sales: {sales_insights['total_sales']}")
        print(f"   ✅ Growth Rate: {sales_insights['sales_growth']}")
        print(f"   ✅ Best Month: {sales_insights['best_month']}")
        
        recommendations = business_agent.generate_recommendations()
        print(f"   ✅ Generated {len(recommendations)} business recommendations")
        
    except Exception as e:
        print(f"   ❌ Error in business analytics: {e}")
    
    # 2. Content Creation Demo
    print("\n✍️ 2. CONTENT CREATION AGENT")
    print("   Capabilities: Blog posts, social media, emails, video scripts")
    
    try:
        content_agent = ContentCreationAgent()
        content_agent.set_brand_voice("professional")
        content_agent.add_seo_keywords(["AI", "productivity", "business"])
        
        # Generate content
        blog_post = content_agent.generate_blog_post("AI in Business", 500)
        social_post = content_agent.generate_social_media_content("AI Productivity", "linkedin")
        email_campaign = content_agent.generate_email_campaign("AI Innovation", "newsletter")
        video_script = content_agent.generate_video_script("AI Future", 2)
        
        print(f"   ✅ Blog Post: '{blog_post['title']}' ({blog_post['word_count']} words)")
        print(f"   ✅ Social Media: {social_post['character_count']} characters for {social_post['platform']}")
        print(f"   ✅ Email Campaign: '{email_campaign['subject_line']}'")
        print(f"   ✅ Video Script: '{video_script['title']}' ({video_script['estimated_word_count']} words)")
        
    except Exception as e:
        print(f"   ❌ Error in content creation: {e}")
    
    # 3. Research Agent Demo
    print("\n🔍 3. RESEARCH AGENT")
    print("   Capabilities: Market research, trend analysis, fact checking")
    
    try:
        research_agent = ResearchAgent()
        research_agent.add_research_source("Industry Reports", "industry", 8.5)
        research_agent.add_research_source("Academic Database", "academic", 9.0)
        
        # Conduct research
        market_research = research_agent.conduct_market_research("Artificial Intelligence", ["machine learning", "automation"])
        news_monitoring = research_agent.monitor_news_and_trends(["AI", "technology"])
        fact_check = research_agent.fact_check_information([
            "AI will transform business operations",
            "Machine learning improves decision making"
        ])
        
        print(f"   ✅ Market Research: {market_research['industry']} industry analysis")
        print(f"   ✅ Market Size: {market_research['market_size']}")
        print(f"   ✅ News Monitoring: {news_monitoring['articles_found']} articles analyzed")
        print(f"   ✅ Fact Check: {len(fact_check['verified_claims'])} claims verified")
        
    except Exception as e:
        print(f"   ❌ Error in research: {e}")
    
    # 4. Automation Agent Demo
    print("\n⚙️ 4. AUTOMATION AGENT")
    print("   Capabilities: Task management, workflow automation, scheduling")
    
    try:
        automation_agent = AutomationAgent()
        
        # Create tasks and workflows
        task1 = automation_agent.create_task(
            title="AI Implementation Project",
            description="Deploy AI agents in business processes",
            priority=Priority.HIGH,
            assigned_to="project.manager",
            estimated_duration=480
        )
        
        # Create automation rule
        rule_id = automation_agent.create_automation_rule(
            name="Project completion notification",
            trigger={"type": "task_completed"},
            action={"type": "send_email", "template": "task_completion"}
        )
        
        # Get recommendations
        recommendations = automation_agent.get_task_recommendations("project.manager")
        
        # Generate report
        productivity_report = automation_agent.generate_productivity_report("project.manager")
        
        print(f"   ✅ Created task: {task1}")
        print(f"   ✅ Automation rule: {rule_id}")
        print(f"   ✅ Task recommendations: {len(recommendations)}")
        print(f"   ✅ Productivity report generated")
        
    except Exception as e:
        print(f"   ❌ Error in automation: {e}")
    
    # Summary
    print("\n🎉 SHOWCASE SUMMARY")
    print("-"*60)
    print("These agents demonstrate the power of AI automation across:")
    print("📈 Business Intelligence & Analytics")
    print("📝 Content Creation & Marketing") 
    print("🔍 Research & Information Gathering")
    print("⚙️ Task Automation & Productivity")
    print()
    print("🚀 Ready to explore more? Check out:")
    print("   📖 AGENT_CAPABILITIES.md - Complete capabilities guide")
    print("   💻 examples/ - Full working code examples")
    print("   🛠️ examples/README.md - Setup and customization guide")
    print()
    print("💡 Next Steps:")
    print("   1. Explore individual agent examples")
    print("   2. Customize agents for your specific needs")
    print("   3. Integrate with your existing systems")
    print("   4. Build your own agent combinations")
    print()
    print(f"Demo completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    # Set matplotlib backend for headless environment
    import os
    os.environ['MPLBACKEND'] = 'Agg'
    
    main()