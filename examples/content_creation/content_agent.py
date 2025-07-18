"""
Content Creation Agent Example
Demonstrates automated content generation capabilities
"""

import random
import re
from datetime import datetime
from typing import List, Dict, Optional

class ContentCreationAgent:
    """
    An AI agent that creates various types of content including:
    - Blog posts and articles
    - Social media content
    - Email campaigns
    - SEO-optimized content
    - Video scripts
    """
    
    def __init__(self):
        self.content_templates = self._load_templates()
        self.seo_keywords = []
        self.brand_voice = "professional"
        self.target_audience = "general"
    
    def _load_templates(self):
        """Load content templates for different formats"""
        return {
            'blog_intro': [
                "In today's fast-paced world, {topic} has become increasingly important.",
                "Have you ever wondered about {topic}? You're not alone.",
                "The landscape of {topic} is evolving rapidly, and here's what you need to know.",
                "{topic} is transforming the way we work and live. Let's explore how."
            ],
            'blog_conclusion': [
                "As we've seen, {topic} offers tremendous opportunities for growth and innovation.",
                "The future of {topic} looks bright, and now is the time to take action.",
                "Understanding {topic} is crucial for staying ahead in today's competitive landscape.",
                "By implementing these strategies around {topic}, you'll be well-positioned for success."
            ],
            'social_hooks': [
                "🚀 Ready to transform your approach to {topic}?",
                "💡 Here's what most people get wrong about {topic}:",
                "🔥 Hot take: {topic} is about to change everything",
                "📈 The data on {topic} will surprise you:"
            ],
            'email_subjects': [
                "The Ultimate Guide to {topic}",
                "5 Mistakes Everyone Makes with {topic}",
                "How {topic} Can Transform Your Business",
                "The Secret to Mastering {topic}"
            ]
        }
    
    def set_brand_voice(self, voice: str):
        """Set the brand voice (professional, casual, friendly, authoritative)"""
        self.brand_voice = voice
        return f"Brand voice set to: {voice}"
    
    def set_target_audience(self, audience: str):
        """Set the target audience"""
        self.target_audience = audience
        return f"Target audience set to: {audience}"
    
    def add_seo_keywords(self, keywords: List[str]):
        """Add SEO keywords for content optimization"""
        self.seo_keywords.extend(keywords)
        return f"Added {len(keywords)} SEO keywords"
    
    def generate_blog_post(self, topic: str, target_length: int = 800) -> Dict[str, str]:
        """Generate a complete blog post on the given topic"""
        
        # Generate title
        title_templates = [
            f"The Complete Guide to {topic}",
            f"How to Master {topic} in 2024",
            f"5 Essential Tips for {topic} Success",
            f"Why {topic} Matters More Than Ever",
            f"The Future of {topic}: What You Need to Know"
        ]
        title = random.choice(title_templates)
        
        # Generate meta description
        meta_description = f"Discover everything you need to know about {topic}. Learn key strategies, best practices, and actionable tips to achieve success."
        
        # Generate introduction
        intro_template = random.choice(self.content_templates['blog_intro'])
        introduction = intro_template.format(topic=topic)
        
        # Generate main content sections
        sections = self._generate_blog_sections(topic, target_length)
        
        # Generate conclusion
        conclusion_template = random.choice(self.content_templates['blog_conclusion'])
        conclusion = conclusion_template.format(topic=topic)
        
        # Generate tags
        tags = self._generate_tags(topic)
        
        blog_post = {
            'title': title,
            'meta_description': meta_description,
            'introduction': introduction,
            'sections': sections,
            'conclusion': conclusion,
            'tags': tags,
            'word_count': self._estimate_word_count(introduction + ' '.join(sections) + conclusion),
            'seo_score': self._calculate_seo_score(topic, title + ' ' + introduction + ' '.join(sections) + conclusion)
        }
        
        return blog_post
    
    def _generate_blog_sections(self, topic: str, target_length: int) -> List[str]:
        """Generate main content sections for blog post"""
        sections = [
            f"## Understanding {topic}\n\n{topic} has evolved significantly over the years. Today, it encompasses various aspects that are crucial for success. Let's explore the fundamental concepts that everyone should understand.",
            
            f"## Key Benefits of {topic}\n\nThe advantages of focusing on {topic} are numerous:\n- Improved efficiency and productivity\n- Better decision-making capabilities\n- Enhanced competitive advantage\n- Increased customer satisfaction\n- Long-term sustainable growth",
            
            f"## Best Practices for {topic}\n\nTo get the most out of {topic}, consider these proven strategies:\n\n1. **Start with clear objectives**: Define what you want to achieve\n2. **Gather relevant data**: Make informed decisions based on evidence\n3. **Implement gradually**: Take a phased approach to minimize risks\n4. **Monitor and adjust**: Continuously evaluate and improve your approach",
            
            f"## Common Challenges and Solutions\n\nWhile working with {topic}, you might encounter several challenges. Here are the most common ones and how to address them:\n\n**Challenge 1: Lack of resources**\nSolution: Start small and scale gradually as you see results.\n\n**Challenge 2: Resistance to change**\nSolution: Communicate benefits clearly and involve stakeholders in the process.",
            
            f"## Future Trends in {topic}\n\nLooking ahead, {topic} is expected to evolve in several exciting ways. Emerging technologies and changing market dynamics will create new opportunities and challenges. Staying informed about these trends will help you maintain a competitive edge."
        ]
        
        return sections
    
    def generate_social_media_content(self, topic: str, platform: str = "general") -> Dict[str, str]:
        """Generate social media content for different platforms"""
        
        # Platform-specific content
        platform_specs = {
            'twitter': {'max_length': 280, 'hashtags': 2},
            'linkedin': {'max_length': 1300, 'hashtags': 5},
            'instagram': {'max_length': 2200, 'hashtags': 10},
            'facebook': {'max_length': 500, 'hashtags': 3},
            'general': {'max_length': 280, 'hashtags': 3}
        }
        
        specs = platform_specs.get(platform, platform_specs['general'])
        
        # Generate hook
        hook_template = random.choice(self.content_templates['social_hooks'])
        hook = hook_template.format(topic=topic)
        
        # Generate main content
        content_options = [
            f"Understanding {topic} can transform your approach to business. Here are 3 key insights that will change how you think about it.",
            f"Most people struggle with {topic} because they focus on the wrong things. Here's what actually matters.",
            f"The secret to mastering {topic}? It's simpler than you think. Focus on these fundamentals.",
            f"After analyzing hundreds of cases, here's what successful {topic} strategies have in common."
        ]
        
        main_content = random.choice(content_options)
        
        # Generate hashtags
        hashtags = self._generate_hashtags(topic, specs['hashtags'])
        
        # Combine content
        full_content = f"{hook}\n\n{main_content}\n\n{hashtags}"
        
        # Ensure content fits platform requirements
        if len(full_content) > specs['max_length']:
            # Truncate content if too long
            available_length = specs['max_length'] - len(hashtags) - 10
            truncated_content = (hook + "\n\n" + main_content)[:available_length] + "..."
            full_content = f"{truncated_content}\n\n{hashtags}"
        
        return {
            'platform': platform,
            'content': full_content,
            'character_count': len(full_content),
            'hashtags': hashtags,
            'estimated_engagement': self._estimate_engagement(topic, platform)
        }
    
    def generate_email_campaign(self, topic: str, campaign_type: str = "newsletter") -> Dict[str, str]:
        """Generate email campaign content"""
        
        # Generate subject line
        subject_template = random.choice(self.content_templates['email_subjects'])
        subject = subject_template.format(topic=topic)
        
        # Generate preheader
        preheader = f"Discover the latest insights and strategies for {topic} success."
        
        # Generate email body based on campaign type
        if campaign_type == "newsletter":
            body = self._generate_newsletter_content(topic)
        elif campaign_type == "promotional":
            body = self._generate_promotional_content(topic)
        else:
            body = self._generate_informational_content(topic)
        
        # Generate call-to-action
        cta_options = [
            "Learn More",
            "Get Started Today",
            "Download Free Guide",
            "Schedule a Consultation",
            "Join the Community"
        ]
        cta = random.choice(cta_options)
        
        return {
            'subject_line': subject,
            'preheader': preheader,
            'body': body,
            'call_to_action': cta,
            'campaign_type': campaign_type,
            'estimated_open_rate': self._estimate_open_rate(subject)
        }
    
    def generate_video_script(self, topic: str, duration_minutes: int = 5) -> Dict[str, str]:
        """Generate a video script for the given topic"""
        
        # Calculate timing
        words_per_minute = 150
        target_words = duration_minutes * words_per_minute
        
        # Generate script sections
        hook = f"Have you ever wondered how to truly master {topic}? In the next {duration_minutes} minutes, I'll show you exactly how."
        
        introduction = f"Hi everyone, welcome back to the channel! Today we're diving deep into {topic}, and I promise you'll walk away with actionable insights you can implement immediately."
        
        main_content = f"""
        Let me start with a question: What's the biggest challenge you face with {topic}?
        
        If you're like most people, you probably struggle with knowing where to start. That's exactly what we're going to solve today.
        
        Here are the three key principles that will transform your approach to {topic}:
        
        First, understanding the fundamentals. You can't build a house without a solid foundation, and the same applies to {topic}.
        
        Second, implementing best practices. I've studied hundreds of successful cases, and there are clear patterns that emerge.
        
        Third, avoiding common mistakes. These pitfalls catch most people, but once you know what to look for, they're easy to avoid.
        
        Let me break each of these down for you...
        """
        
        conclusion = f"So there you have it - your complete guide to {topic}. Remember, success doesn't happen overnight, but with consistent effort and the right strategies, you'll see amazing results."
        
        call_to_action = "If you found this helpful, make sure to like this video and subscribe for more content like this. And let me know in the comments - what's your biggest takeaway from today's video?"
        
        # Combine script
        full_script = f"{hook}\n\n{introduction}\n\n{main_content}\n\n{conclusion}\n\n{call_to_action}"
        
        return {
            'title': f"How to Master {topic} in {duration_minutes} Minutes",
            'hook': hook,
            'introduction': introduction,
            'main_content': main_content,
            'conclusion': conclusion,
            'call_to_action': call_to_action,
            'full_script': full_script,
            'estimated_word_count': len(full_script.split()),
            'estimated_duration': f"{duration_minutes} minutes"
        }
    
    def _generate_tags(self, topic: str) -> List[str]:
        """Generate relevant tags for content"""
        base_tags = [topic.lower().replace(' ', '')]
        
        # Add related tags
        related_tags = [
            'tips', 'guide', 'strategy', 'success', 'best-practices',
            'tutorial', 'insights', 'advice', 'howto', 'business'
        ]
        
        tags = base_tags + random.sample(related_tags, 4)
        return tags
    
    def _generate_hashtags(self, topic: str, count: int) -> str:
        """Generate hashtags for social media"""
        base_hashtags = [f"#{topic.replace(' ', '').lower()}"]
        
        additional_hashtags = [
            '#success', '#tips', '#business', '#growth', '#strategy',
            '#motivation', '#productivity', '#leadership', '#innovation',
            '#transformation', '#bestpractices', '#professional'
        ]
        
        selected_hashtags = base_hashtags + random.sample(additional_hashtags, count - 1)
        return ' '.join(selected_hashtags)
    
    def _estimate_word_count(self, text: str) -> int:
        """Estimate word count of text"""
        return len(text.split())
    
    def _calculate_seo_score(self, topic: str, content: str) -> int:
        """Calculate a simple SEO score based on keyword usage"""
        keyword_count = content.lower().count(topic.lower())
        content_length = len(content.split())
        
        # Simple scoring algorithm
        if content_length > 500:
            length_score = 25
        elif content_length > 300:
            length_score = 15
        else:
            length_score = 10
        
        keyword_density = (keyword_count / content_length) * 100
        if 1 <= keyword_density <= 3:
            keyword_score = 25
        elif keyword_density < 1:
            keyword_score = 15
        else:
            keyword_score = 10
        
        return min(length_score + keyword_score + random.randint(20, 50), 100)
    
    def _estimate_engagement(self, topic: str, platform: str) -> str:
        """Estimate potential engagement for social media content"""
        engagement_rates = {
            'twitter': '2-5%',
            'linkedin': '3-6%',
            'instagram': '1-3%',
            'facebook': '1-2%',
            'general': '2-4%'
        }
        return engagement_rates.get(platform, '2-4%')
    
    def _estimate_open_rate(self, subject: str) -> str:
        """Estimate email open rate based on subject line"""
        if any(word in subject.lower() for word in ['ultimate', 'guide', 'secret', 'mistakes']):
            return '25-30%'
        elif any(word in subject.lower() for word in ['how', 'tips', 'transform']):
            return '20-25%'
        else:
            return '15-20%'
    
    def _generate_newsletter_content(self, topic: str) -> str:
        """Generate newsletter content"""
        return f"""
        Dear Subscriber,
        
        This week, we're focusing on {topic} and how it can impact your success.
        
        Here's what's new:
        
        📰 Industry Update: The latest trends in {topic} that you need to know about
        
        💡 Quick Tip: One simple change that can improve your {topic} results by 25%
        
        📈 Case Study: How one company transformed their approach to {topic} and saw amazing results
        
        🎯 Action Item: Your challenge for this week - implement one new {topic} strategy
        
        Keep pushing forward!
        """
    
    def _generate_promotional_content(self, topic: str) -> str:
        """Generate promotional email content"""
        return f"""
        Ready to take your {topic} skills to the next level?
        
        Our comprehensive {topic} course is now available, and for a limited time, we're offering exclusive access to our community of experts.
        
        What you'll get:
        ✅ Step-by-step {topic} framework
        ✅ Real-world case studies
        ✅ Direct access to mentors
        ✅ 30-day money-back guarantee
        
        Don't miss out on this opportunity to transform your approach to {topic}.
        """
    
    def _generate_informational_content(self, topic: str) -> str:
        """Generate informational email content"""
        return f"""
        Hi there,
        
        I wanted to share some valuable insights about {topic} that I've learned from working with hundreds of professionals.
        
        The most successful people in {topic} share three common traits:
        
        1. They focus on fundamentals first
        2. They measure everything
        3. They're constantly learning and adapting
        
        Which of these resonates most with you? Hit reply and let me know!
        
        Best regards,
        """

# Example usage and demonstration
def demonstrate_content_agent():
    """Demonstrate the capabilities of the Content Creation Agent"""
    print("✍️ Content Creation Agent Demonstration")
    print("=" * 50)
    
    # Initialize agent
    agent = ContentCreationAgent()
    
    # Set up agent configuration
    print("\n1. Configuring agent...")
    print(agent.set_brand_voice("professional"))
    print(agent.set_target_audience("business professionals"))
    print(agent.add_seo_keywords(["digital marketing", "business growth", "productivity"]))
    
    # Generate blog post
    print("\n2. Generating blog post...")
    blog_post = agent.generate_blog_post("Digital Marketing Strategy")
    print(f"Title: {blog_post['title']}")
    print(f"Word Count: {blog_post['word_count']}")
    print(f"SEO Score: {blog_post['seo_score']}/100")
    
    # Generate social media content
    print("\n3. Generating social media content...")
    social_content = agent.generate_social_media_content("Productivity Tips", "linkedin")
    print(f"Platform: {social_content['platform']}")
    print(f"Content Preview: {social_content['content'][:100]}...")
    print(f"Character Count: {social_content['character_count']}")
    
    # Generate email campaign
    print("\n4. Generating email campaign...")
    email_campaign = agent.generate_email_campaign("Business Growth", "newsletter")
    print(f"Subject: {email_campaign['subject_line']}")
    print(f"Type: {email_campaign['campaign_type']}")
    print(f"Estimated Open Rate: {email_campaign['estimated_open_rate']}")
    
    # Generate video script
    print("\n5. Generating video script...")
    video_script = agent.generate_video_script("Leadership Skills", 3)
    print(f"Title: {video_script['title']}")
    print(f"Word Count: {video_script['estimated_word_count']}")
    print(f"Duration: {video_script['estimated_duration']}")

if __name__ == "__main__":
    demonstrate_content_agent()