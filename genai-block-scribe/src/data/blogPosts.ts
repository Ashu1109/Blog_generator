export interface BlogPost {
  id: string;
  title: string;
  excerpt: string;
  content: string;
  category: "GenAI" | "Blockchain";
  readTime: string;
  publishedAt: string;
  image?: string;
  featured?: boolean;
  tags: string[];
}

export const blogPosts: BlogPost[] = [
  {
    id: "future-of-generative-ai",
    title: "The Future of Generative AI: Transforming Creative Industries",
    excerpt: "Exploring how generative AI is revolutionizing content creation, from text to images, and its impact on creative professionals worldwide.",
    content: `
      <h2>Introduction</h2>
      <p>Generative AI has emerged as one of the most transformative technologies of our time, fundamentally changing how we approach creativity and content generation...</p>
      
      <h2>Impact on Creative Industries</h2>
      <p>The creative landscape is experiencing unprecedented changes as AI tools become more sophisticated and accessible...</p>
      
      <h2>Challenges and Opportunities</h2>
      <p>While generative AI presents exciting opportunities, it also raises important questions about originality, copyright, and the future role of human creativity...</p>
      
      <h2>Conclusion</h2>
      <p>As we move forward, the key lies in finding the right balance between human creativity and AI assistance...</p>
    `,
    category: "GenAI",
    readTime: "8 min read",
    publishedAt: "Dec 15, 2024",
    featured: true,
    tags: ["AI", "Creativity", "Technology", "Future"]
  },
  {
    id: "blockchain-scalability-solutions",
    title: "Blockchain Scalability: Layer 2 Solutions and Beyond",
    excerpt: "A comprehensive look at the current state of blockchain scalability, examining Layer 2 solutions, sharding, and emerging technologies.",
    content: `
      <h2>The Scalability Challenge</h2>
      <p>Blockchain technology faces significant challenges when it comes to scalability, with traditional networks like Bitcoin and Ethereum processing limited transactions per second...</p>
      
      <h2>Layer 2 Solutions</h2>
      <p>Layer 2 scaling solutions have emerged as promising approaches to address blockchain's scalability limitations...</p>
      
      <h2>Sharding and Beyond</h2>
      <p>Beyond Layer 2, innovative approaches like sharding are being implemented to increase blockchain throughput...</p>
      
      <h2>Future Outlook</h2>
      <p>The future of blockchain scalability looks promising with multiple solutions being developed and tested...</p>
    `,
    category: "Blockchain",
    readTime: "12 min read",
    publishedAt: "Dec 12, 2024",
    featured: true,
    tags: ["Blockchain", "Scalability", "Layer2", "Technology"]
  },
  {
    id: "llm-training-efficiency",
    title: "Optimizing Large Language Model Training: Efficiency Techniques",
    excerpt: "Deep dive into advanced techniques for training LLMs more efficiently, including gradient accumulation, mixed precision, and distributed training.",
    content: `
      <h2>Training Challenges</h2>
      <p>Training large language models requires enormous computational resources and sophisticated optimization techniques...</p>
      
      <h2>Efficiency Techniques</h2>
      <p>Several techniques have been developed to make LLM training more efficient and accessible...</p>
      
      <h2>Implementation Strategies</h2>
      <p>Implementing these optimization techniques requires careful consideration of hardware constraints and model architecture...</p>
    `,
    category: "GenAI",
    readTime: "10 min read",
    publishedAt: "Dec 10, 2024",
    tags: ["LLM", "Training", "Optimization", "AI"]
  },
  {
    id: "defi-protocols-security",
    title: "DeFi Security: Analyzing Common Vulnerabilities",
    excerpt: "An in-depth analysis of security vulnerabilities in DeFi protocols and best practices for building secure decentralized applications.",
    content: `
      <h2>DeFi Security Landscape</h2>
      <p>Decentralized Finance has grown exponentially, but with growth comes increased security risks and attack vectors...</p>
      
      <h2>Common Vulnerabilities</h2>
      <p>Understanding the most common vulnerabilities in DeFi protocols is crucial for developers and users alike...</p>
      
      <h2>Best Practices</h2>
      <p>Implementing security best practices from the ground up can prevent many common attacks...</p>
    `,
    category: "Blockchain",
    readTime: "9 min read",
    publishedAt: "Dec 8, 2024",
    tags: ["DeFi", "Security", "Smart Contracts", "Blockchain"]
  },
  {
    id: "multimodal-ai-applications",
    title: "Multimodal AI: Bridging Text, Vision, and Audio",
    excerpt: "Exploring the latest advances in multimodal AI systems that can understand and generate content across different modalities.",
    content: `
      <h2>The Rise of Multimodal AI</h2>
      <p>Multimodal AI represents a significant leap forward in artificial intelligence, enabling systems to process and understand multiple types of data...</p>
      
      <h2>Applications and Use Cases</h2>
      <p>From autonomous vehicles to content creation, multimodal AI is finding applications across numerous industries...</p>
      
      <h2>Technical Challenges</h2>
      <p>Building effective multimodal systems requires solving complex technical challenges related to data alignment and fusion...</p>
    `,
    category: "GenAI",
    readTime: "11 min read",
    publishedAt: "Dec 5, 2024",
    tags: ["Multimodal", "AI", "Vision", "Audio"]
  },
  {
    id: "web3-identity-solutions",
    title: "Decentralized Identity: Web3's Answer to Privacy",
    excerpt: "How blockchain-based identity solutions are revolutionizing digital identity management and user privacy protection.",
    content: `
      <h2>Identity in the Digital Age</h2>
      <p>Traditional digital identity systems rely on centralized authorities, creating privacy and security concerns...</p>
      
      <h2>Blockchain-Based Solutions</h2>
      <p>Web3 identity solutions leverage blockchain technology to give users control over their digital identities...</p>
      
      <h2>Implementation Challenges</h2>
      <p>While promising, decentralized identity systems face several implementation and adoption challenges...</p>
    `,
    category: "Blockchain",
    readTime: "7 min read",
    publishedAt: "Dec 3, 2024",
    tags: ["Web3", "Identity", "Privacy", "Decentralization"]
  }
];