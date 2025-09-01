import { 
  Bot, 
  Code, 
  Database, 
  Zap, 
  Calendar, 
  Brain, 
  Blocks, 
  Server,
  Globe,
  GitBranch,
  Clock,
  Sparkles
} from "lucide-react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

const About = () => {
  const backendTech = [
    { name: "CrewAI", description: "Multi-agent AI framework for automated content generation", icon: <Bot className="w-5 h-5" /> },
    { name: "FastAPI", description: "High-performance Python web framework for API development", icon: <Zap className="w-5 h-5" /> },
    { name: "Python", description: "Core programming language for AI and backend logic", icon: <Code className="w-5 h-5" /> },
    { name: "PostgreSQL", description: "Robust relational database for storing blog posts and metadata", icon: <Database className="w-5 h-5" /> },
    { name: "Prisma", description: "Next-generation ORM for database management", icon: <Server className="w-5 h-5" /> },
    { name: "APScheduler", description: "Advanced Python scheduler for automated blog generation", icon: <Clock className="w-5 h-5" /> }
  ];

  const frontendTech = [
    { name: "React 18", description: "Modern JavaScript library for building user interfaces", icon: <Globe className="w-5 h-5" /> },
    { name: "TypeScript", description: "Type-safe JavaScript for better development experience", icon: <Code className="w-5 h-5" /> },
    { name: "Vite", description: "Lightning-fast build tool and development server", icon: <Zap className="w-5 h-5" /> },
    { name: "Tailwind CSS", description: "Utility-first CSS framework for rapid UI development", icon: <Sparkles className="w-5 h-5" /> },
    { name: "Shadcn/ui", description: "Beautiful and accessible React component library", icon: <GitBranch className="w-5 h-5" /> },
    { name: "React Router", description: "Declarative routing for React applications", icon: <Globe className="w-5 h-5" /> }
  ];

  const features = [
    {
      title: "Automated Content Generation",
      description: "AI agents collaborate to research, write, and publish high-quality blog posts automatically",
      icon: <Bot className="w-8 h-8 text-primary" />
    },
    {
      title: "Daily Fresh Content",
      description: "New blog posts are generated every day covering the latest developments in AI and blockchain",
      icon: <Calendar className="w-8 h-8 text-accent" />
    },
    {
      title: "Dual Topic Focus",
      description: "Specialized coverage of both Generative AI innovations and Blockchain technology advances",
      icon: <Brain className="w-8 h-8 text-primary" />
    },
    {
      title: "Real-time Research",
      description: "AI agents perform live research to ensure content reflects the most current trends and developments",
      icon: <Zap className="w-8 h-8 text-accent" />
    }
  ];

  return (
    <div className="min-h-screen bg-background">
      {/* Hero Section */}
      <section className="relative py-20 px-4 sm:px-6 lg:px-8 bg-gradient-hero">
        <div className="absolute inset-0 bg-gradient-to-b from-background/90 to-background/70" />
        <div className="relative z-10 max-w-4xl mx-auto text-center">
          <div className="flex justify-center space-x-4 mb-8">
            <div className="p-4 bg-primary/20 rounded-full animate-glow">
              <Bot className="w-10 h-10 text-primary" />
            </div>
            <div className="p-4 bg-accent/20 rounded-full animate-glow">
              <Blocks className="w-10 h-10 text-accent" />
            </div>
          </div>
          
          <h1 className="text-4xl md:text-6xl font-bold bg-gradient-primary bg-clip-text text-transparent mb-6">
            About TechBlog
          </h1>
          <p className="text-xl text-muted-foreground leading-relaxed">
            An intelligent, fully automated blog generation system that delivers fresh insights 
            on Generative AI and Blockchain technology every single day.
          </p>
        </div>
      </section>

      {/* What We Do Section */}
      <section className="py-16 px-4 sm:px-6 lg:px-8 bg-background">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-bold text-foreground mb-4">
              What We Do
            </h2>
            <p className="text-lg text-muted-foreground max-w-3xl mx-auto">
              TechBlog is a cutting-edge automated content platform that leverages advanced AI agents 
              to research, write, and publish high-quality blog posts about the latest developments 
              in artificial intelligence and blockchain technology.
            </p>
          </div>

          <div className="grid md:grid-cols-2 gap-8">
            {features.map((feature, index) => (
              <Card key={index} className="bg-gradient-card border-border hover:shadow-card transition-all duration-300">
                <CardHeader>
                  <div className="flex items-center space-x-3 mb-2">
                    {feature.icon}
                    <CardTitle className="text-xl">{feature.title}</CardTitle>
                  </div>
                </CardHeader>
                <CardContent>
                  <CardDescription className="text-base leading-relaxed">
                    {feature.description}
                  </CardDescription>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section className="py-16 px-4 sm:px-6 lg:px-8 bg-secondary/10">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-bold text-foreground mb-4">
              How It Works
            </h2>
            <p className="text-lg text-muted-foreground">
              Our automated system runs 24/7 to deliver fresh, relevant content
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            <div className="text-center">
              <div className="w-16 h-16 bg-primary/20 rounded-full flex items-center justify-center mx-auto mb-6">
                <Brain className="w-8 h-8 text-primary" />
              </div>
              <h3 className="text-xl font-semibold mb-4">AI Research</h3>
              <p className="text-muted-foreground">
                Our AI agents continuously scan the latest developments in GenAI and Blockchain, 
                identifying trending topics and breakthrough innovations.
              </p>
            </div>

            <div className="text-center">
              <div className="w-16 h-16 bg-accent/20 rounded-full flex items-center justify-center mx-auto mb-6">
                <Bot className="w-8 h-8 text-accent" />
              </div>
              <h3 className="text-xl font-semibold mb-4">Content Generation</h3>
              <p className="text-muted-foreground">
                Multiple specialized AI agents collaborate to create comprehensive, 
                well-researched articles with proper structure and engaging narratives.
              </p>
            </div>

            <div className="text-center">
              <div className="w-16 h-16 bg-primary/20 rounded-full flex items-center justify-center mx-auto mb-6">
                <Calendar className="w-8 h-8 text-primary" />
              </div>
              <h3 className="text-xl font-semibold mb-4">Automated Publishing</h3>
              <p className="text-muted-foreground">
                Every day, new content is automatically generated, processed, 
                and published to keep you updated with the latest insights.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Technology Stack Section */}
      <section className="py-16 px-4 sm:px-6 lg:px-8 bg-background">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-bold text-foreground mb-4">
              Technology Stack
            </h2>
            <p className="text-lg text-muted-foreground">
              Built with cutting-edge technologies for performance, reliability, and scalability
            </p>
          </div>

          <div className="grid lg:grid-cols-2 gap-12">
            {/* Backend Technologies */}
            <div>
              <div className="flex items-center space-x-3 mb-8">
                <div className="p-3 bg-primary/20 rounded-lg">
                  <Server className="w-6 h-6 text-primary" />
                </div>
                <h3 className="text-2xl font-bold text-foreground">Backend & AI</h3>
              </div>
              
              <div className="space-y-4">
                {backendTech.map((tech, index) => (
                  <Card key={index} className="bg-gradient-card border-border">
                    <CardContent className="p-4">
                      <div className="flex items-start space-x-3">
                        <div className="p-2 bg-primary/10 rounded-lg mt-1">
                          {tech.icon}
                        </div>
                        <div>
                          <h4 className="font-semibold text-foreground mb-1">{tech.name}</h4>
                          <p className="text-sm text-muted-foreground">{tech.description}</p>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </div>

            {/* Frontend Technologies */}
            <div>
              <div className="flex items-center space-x-3 mb-8">
                <div className="p-3 bg-accent/20 rounded-lg">
                  <Globe className="w-6 h-6 text-accent" />
                </div>
                <h3 className="text-2xl font-bold text-foreground">Frontend & UI</h3>
              </div>
              
              <div className="space-y-4">
                {frontendTech.map((tech, index) => (
                  <Card key={index} className="bg-gradient-card border-border">
                    <CardContent className="p-4">
                      <div className="flex items-start space-x-3">
                        <div className="p-2 bg-accent/10 rounded-lg mt-1">
                          {tech.icon}
                        </div>
                        <div>
                          <h4 className="font-semibold text-foreground mb-1">{tech.name}</h4>
                          <p className="text-sm text-muted-foreground">{tech.description}</p>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Topics We Cover Section */}
      <section className="py-16 px-4 sm:px-6 lg:px-8 bg-secondary/10">
        <div className="max-w-4xl mx-auto">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-bold text-foreground mb-4">
              Topics We Cover
            </h2>
            <p className="text-lg text-muted-foreground">
              Stay ahead with comprehensive coverage of the most important tech trends
            </p>
          </div>

          <div className="grid md:grid-cols-2 gap-8">
            <Card className="bg-gradient-card border-border">
              <CardHeader>
                <div className="flex items-center space-x-3 mb-2">
                  <div className="p-3 bg-primary/20 rounded-lg">
                    <Brain className="w-8 h-8 text-primary" />
                  </div>
                  <CardTitle className="text-2xl">Generative AI</CardTitle>
                </div>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  <div className="flex flex-wrap gap-2">
                    <Badge variant="secondary">Large Language Models</Badge>
                    <Badge variant="secondary">AI Agents</Badge>
                    <Badge variant="secondary">Multi-modal AI</Badge>
                  </div>
                  <div className="flex flex-wrap gap-2">
                    <Badge variant="secondary">Image Generation</Badge>
                    <Badge variant="secondary">Code Generation</Badge>
                    <Badge variant="secondary">RAG Systems</Badge>
                  </div>
                  <div className="flex flex-wrap gap-2">
                    <Badge variant="secondary">Prompt Engineering</Badge>
                    <Badge variant="secondary">AI Safety</Badge>
                    <Badge variant="secondary">Edge AI</Badge>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card className="bg-gradient-card border-border">
              <CardHeader>
                <div className="flex items-center space-x-3 mb-2">
                  <div className="p-3 bg-accent/20 rounded-lg">
                    <Blocks className="w-8 h-8 text-accent" />
                  </div>
                  <CardTitle className="text-2xl">Blockchain</CardTitle>
                </div>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  <div className="flex flex-wrap gap-2">
                    <Badge variant="outline">DeFi Protocols</Badge>
                    <Badge variant="outline">Smart Contracts</Badge>
                    <Badge variant="outline">Web3 Development</Badge>
                  </div>
                  <div className="flex flex-wrap gap-2">
                    <Badge variant="outline">NFT Innovation</Badge>
                    <Badge variant="outline">Layer 2 Solutions</Badge>
                    <Badge variant="outline">Consensus Mechanisms</Badge>
                  </div>
                  <div className="flex flex-wrap gap-2">
                    <Badge variant="outline">Cryptocurrency</Badge>
                    <Badge variant="outline">DAO Governance</Badge>
                    <Badge variant="outline">Interoperability</Badge>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      {/* Mission Statement */}
      <section className="py-16 px-4 sm:px-6 lg:px-8 bg-background">
        <div className="max-w-4xl mx-auto text-center">
          <div className="bg-gradient-card p-12 rounded-2xl border border-border shadow-card">
            <div className="flex justify-center mb-6">
              <div className="p-4 bg-primary/20 rounded-full">
                <Sparkles className="w-10 h-10 text-primary" />
              </div>
            </div>
            <h2 className="text-2xl md:text-3xl font-bold text-foreground mb-6">
              Our Mission
            </h2>
            <p className="text-lg text-muted-foreground leading-relaxed mb-6">
              To democratize access to cutting-edge technology insights by providing 
              automated, intelligent, and always up-to-date content about the most 
              important developments in AI and blockchain technology.
            </p>
            <p className="text-base text-muted-foreground">
              Every day, our AI-powered system ensures you stay informed about the 
              technologies that are shaping the future of our digital world.
            </p>
          </div>
        </div>
      </section>
    </div>
  );
};

export default About;
