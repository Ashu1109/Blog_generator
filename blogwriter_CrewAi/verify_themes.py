#!/usr/bin/env python3
"""
Theme Verification Script
Comprehensive test to verify both GenAI and Blockchain themes are working properly.
"""

import asyncio
import json
from datetime import datetime


async def verify_all_themes():
    """Comprehensive verification of theme functionality."""
    print("🔍 THEME VERIFICATION REPORT")
    print("=" * 60)
    print(f"Timestamp: {datetime.now().isoformat()}")
    print()

    try:
        from src.blog_generator import blog_generator
        from main import BlogGenerationRequest
        
        # Test 1: Topic Lists
        print("📚 TOPIC INVENTORY")
        print("-" * 30)
        genai_count = len(blog_generator.GENERATIVE_AI_TOPICS)
        blockchain_count = len(blog_generator.BLOCKCHAIN_TOPICS)
        total_count = genai_count + blockchain_count
        
        print(f"GenAI Topics: {genai_count}")
        print(f"Blockchain Topics: {blockchain_count}")
        print(f"Total Topics: {total_count}")
        
        status_1 = "✅ PASS" if genai_count > 0 and blockchain_count > 0 else "❌ FAIL"
        print(f"Status: {status_1}")
        print()

        # Test 2: Random Theme Selection
        print("🎲 RANDOM THEME SELECTION")
        print("-" * 30)
        
        themes_detected = []
        sample_topics = []
        
        for i in range(15):
            topic = blog_generator.generate_dynamic_topic()  # Should be random
            sample_topics.append(topic)
            
            # Detect theme based on content
            blockchain_keywords = [
                'blockchain', 'bitcoin', 'crypto', 'defi', 'nft', 'ethereum', 
                'dao', 'web3', 'smart contract', 'decentralized', 'cbdc',
                'tokenization', 'consensus', 'mining', 'wallet'
            ]
            
            is_blockchain = any(keyword in topic.lower() for keyword in blockchain_keywords)
            theme = 'blockchain' if is_blockchain else 'genai'
            themes_detected.append(theme)

        genai_count = themes_detected.count('genai')
        blockchain_count = themes_detected.count('blockchain')
        
        print(f"Sample Size: 15 topics")
        print(f"GenAI: {genai_count} ({genai_count/15*100:.1f}%)")
        print(f"Blockchain: {blockchain_count} ({blockchain_count/15*100:.1f}%)")
        
        # Show some examples
        print("\nSample Topics:")
        for i, (topic, theme) in enumerate(zip(sample_topics[:5], themes_detected[:5]), 1):
            print(f"  {i}. [{theme:10}] {topic[:60]}...")
        
        status_2 = "✅ PASS" if blockchain_count > 0 and genai_count > 0 else "❌ FAIL"
        print(f"Status: {status_2}")
        print()

        # Test 3: Explicit Theme Selection
        print("🎯 EXPLICIT THEME SELECTION")
        print("-" * 30)
        
        genai_topic = blog_generator.generate_dynamic_topic('genai')
        blockchain_topic = blog_generator.generate_dynamic_topic('blockchain')
        
        print(f"GenAI Topic: {genai_topic[:70]}...")
        print(f"Blockchain Topic: {blockchain_topic[:70]}...")
        
        # Verify themes are correct
        blockchain_keywords = [
            'blockchain', 'bitcoin', 'crypto', 'defi', 'nft', 'ethereum', 
            'dao', 'web3', 'smart contract', 'decentralized', 'cbdc'
        ]
        
        blockchain_correct = any(kw in blockchain_topic.lower() for kw in blockchain_keywords)
        genai_correct = not any(kw in genai_topic.lower() for kw in blockchain_keywords)
        
        status_3 = "✅ PASS" if blockchain_correct and genai_correct else "❌ FAIL"
        print(f"Status: {status_3}")
        print()

        # Test 4: Agent Configuration
        print("🤖 AGENT CONFIGURATION")
        print("-" * 30)
        
        research_role = blog_generator.research_agent.role
        writer_backstory = blog_generator.writer_agent.backstory.lower()
        editor_backstory = blog_generator.editor_agent.backstory.lower()
        
        supports_blockchain = (
            'blockchain' in writer_backstory and 
            'blockchain' in editor_backstory
        )
        
        print(f"Research Agent: {research_role}")
        print(f"Writer supports blockchain: {'blockchain' in writer_backstory}")
        print(f"Editor supports blockchain: {'blockchain' in editor_backstory}")
        
        status_4 = "✅ PASS" if supports_blockchain else "❌ FAIL"
        print(f"Status: {status_4}")
        print()

        # Test 5: API Request Models
        print("🌐 API REQUEST MODELS")
        print("-" * 30)
        
        test_requests = [
            BlogGenerationRequest(),
            BlogGenerationRequest(theme='genai'),
            BlogGenerationRequest(theme='blockchain'),
            BlogGenerationRequest(topic='Custom topic', theme='blockchain')
        ]
        
        print("Request model tests:")
        for i, req in enumerate(test_requests, 1):
            theme_str = req.theme or 'random'
            topic_str = req.topic or 'auto'
            print(f"  {i}. theme={theme_str}, topic={topic_str}")
        
        status_5 = "✅ PASS"
        print(f"Status: {status_5}")
        print()

        # Test 6: Task Creation
        print("📋 TASK CREATION")
        print("-" * 30)
        
        try:
            genai_research = blog_generator.create_research_task('Test AI', 'genai')
            blockchain_research = blog_generator.create_research_task('Test Blockchain', 'blockchain')
            genai_writing = blog_generator.create_writing_task('Test AI', 'genai')
            blockchain_writing = blog_generator.create_writing_task('Test Blockchain', 'blockchain')
            
            # Check if tasks contain appropriate content
            genai_research_ok = 'ai developments' in genai_research.description.lower()
            blockchain_research_ok = 'blockchain' in blockchain_research.description.lower()
            genai_writing_ok = 'ai/ml terminology' in genai_writing.description.lower()
            blockchain_writing_ok = 'blockchain terminology' in blockchain_writing.description.lower()
            
            all_tasks_ok = all([genai_research_ok, blockchain_research_ok, genai_writing_ok, blockchain_writing_ok])
            
            print("Task creation results:")
            print(f"  GenAI research task: {'✓' if genai_research_ok else '✗'}")
            print(f"  Blockchain research task: {'✓' if blockchain_research_ok else '✗'}")
            print(f"  GenAI writing task: {'✓' if genai_writing_ok else '✗'}")
            print(f"  Blockchain writing task: {'✓' if blockchain_writing_ok else '✗'}")
            
            status_6 = "✅ PASS" if all_tasks_ok else "❌ FAIL"
            
        except Exception as e:
            print(f"Task creation error: {e}")
            status_6 = "❌ FAIL"
        
        print(f"Status: {status_6}")
        print()

        # Final Summary
        print("📊 FINAL SUMMARY")
        print("=" * 30)
        
        all_statuses = [status_1, status_2, status_3, status_4, status_5, status_6]
        passed = sum(1 for status in all_statuses if "✅" in status)
        total = len(all_statuses)
        
        print(f"Tests Passed: {passed}/{total}")
        print(f"Overall Status: {'🎉 ALL SYSTEMS GO!' if passed == total else '⚠️ ISSUES DETECTED'}")
        
        if passed == total:
            print("\n✨ Your blog generator is ready to create amazing content")
            print("   on both AI and Blockchain themes in any random order!")
        else:
            print(f"\n🔧 Please review the failed tests above.")
            
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        print("Please ensure all dependencies are installed: pip install -r requirements.txt")
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")


if __name__ == "__main__":
    asyncio.run(verify_all_themes())
