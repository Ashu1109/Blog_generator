import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import BlogCard from "@/components/BlogCard";
import { BlogPost } from "@/data/blogPosts";
import { ArrowRight, Sparkles, Blocks } from "lucide-react";
import { Link } from "react-router-dom";
import heroImage from "@/assets/hero-bg.jpg";

const Home = () => {
  const [latestPosts, setLatestPosts] = useState<BlogPost[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  // We can add an error state if needed, but for the homepage,
  // we might just show an empty state or a simple message.

  useEffect(() => {
    const fetchLatestPosts = async () => {
      try {
        // Fetch the 3 most recent posts
        const response = await fetch(
          `${import.meta.env.VITE_API_URL}/posts?limit=3`
        );
        if (!response.ok) {
          throw new Error("Failed to fetch posts");
        }
        const data = await response.json();

        // Clean up markdown content by removing markdown code block wrapper
        const cleanContent = (content: string) => {
          if (content.startsWith("```markdown\n")) {
            return content.replace(/^```markdown\n/, "").replace(/\n```$/, "");
          }
          return content;
        };

        const transformedPosts: BlogPost[] = data.posts.map((post: any) => ({
          id: post.id.toString(),
          title: post.title,
          excerpt:
            post.meta_description ||
            (post.content
              ? cleanContent(post.content).slice(0, 150) + "..."
              : "No excerpt available"),
          content: cleanContent(post.content || ""),
          category:
            post.topic === "GenAI" || post.topic === "Blockchain"
              ? post.topic
              : "GenAI",
          readTime: `${Math.ceil((post.word_count || 0) / 200)} min read`,
          publishedAt: new Date(post.created_at).toLocaleDateString("en-US", {
            year: "numeric",
            month: "long",
            day: "numeric",
          }),
          tags: post.tags || [],
        }));

        setLatestPosts(transformedPosts);
      } catch (err) {
        console.error("Error fetching latest posts:", err);
        // Handle error gracefully, e.g., setLatestPosts([])
      } finally {
        setIsLoading(false);
      }
    };

    fetchLatestPosts();
  }, []);

  // For now, featured posts can be derived from latest or be empty
  const featuredPosts = latestPosts.slice(0, 2);

  return (
    <div className="min-h-screen bg-background">
      {/* Hero Section */}
      <section className="relative min-h-[90vh] flex items-center justify-center overflow-hidden bg-gradient-hero">
        <div
          className="absolute inset-0 bg-cover bg-center bg-no-repeat opacity-20"
          style={{ backgroundImage: `url(${heroImage})` }}
        />
        <div className="absolute inset-0 bg-gradient-to-b from-background/90 to-background/70" />

        <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <div className="space-y-8 animate-fade-in">
            <div className="flex justify-center space-x-4 mb-8">
              <div className="p-3 bg-primary/20 rounded-full animate-glow">
                <Sparkles className="w-8 h-8 text-accent" />
              </div>
              <div className="p-3 bg-accent/20 rounded-full animate-glow">
                <Blocks className="w-8 h-8 text-primary" />
              </div>
            </div>

            <h1 className="text-4xl md:text-6xl lg:text-7xl font-bold bg-gradient-primary bg-clip-text text-transparent leading-tight">
              Exploring the Future of
              <br />
              <span className="text-accent">AI & Blockchain</span>
            </h1>

            <p className="text-lg md:text-xl text-muted-foreground max-w-3xl mx-auto leading-relaxed">
              Dive deep into the latest developments in Generative AI and
              Blockchain technology. Stay ahead with cutting-edge insights and
              expert analysis.
            </p>

            <div className="flex flex-col sm:flex-row gap-4 justify-center items-center pt-4">
              <Link to="/blog">
                <Button
                  size="lg"
                  className="bg-gradient-primary hover:shadow-glow transition-all duration-300 px-8 py-6"
                >
                  Explore Articles
                  <ArrowRight className="w-5 h-5 ml-2" />
                </Button>
              </Link>

              <Button
                variant="outline"
                size="lg"
                className="border-accent text-accent hover:bg-accent hover:text-accent-foreground px-8 py-6"
              >
                Subscribe to Newsletter
              </Button>
            </div>
          </div>
        </div>
      </section>

      {/* Featured Posts */}
      <section className="py-16 px-4 sm:px-6 lg:px-8 bg-background">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-bold text-foreground mb-4">
              Featured Articles
            </h2>
            <p className="text-lg text-muted-foreground">
              Our most popular and impactful pieces
            </p>
          </div>

          <div className="grid lg:grid-cols-2 gap-6 items-stretch">
            {featuredPosts.map((post) => (
              <BlogCard key={post.id} post={post} featured />
            ))}
          </div>
        </div>
      </section>

      {/* Latest Posts */}
      <section className="py-16 px-4 sm:px-6 lg:px-8 bg-secondary/10">
        <div className="max-w-7xl mx-auto">
          <div className="flex justify-between items-center mb-12">
            <div>
              <h2 className="text-3xl md:text-4xl font-bold text-foreground mb-4">
                Latest Articles
              </h2>
              <p className="text-lg text-muted-foreground">
                Stay updated with our newest content
              </p>
            </div>

            <Link to="/blog">
              <Button
                variant="outline"
                className="border-accent text-accent hover:bg-accent hover:text-accent-foreground"
              >
                View All Posts
                <ArrowRight className="w-4 h-4 ml-2" />
              </Button>
            </Link>
          </div>

          {isLoading ? (
            <div className="text-center text-lg">
              Loading latest articles...
            </div>
          ) : (
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6 items-stretch">
              {latestPosts.map((post) => (
                <BlogCard key={post.id} post={post} />
              ))}
            </div>
          )}
        </div>
      </section>

      {/* Newsletter CTA */}
      <section className="py-16 px-4 sm:px-6 lg:px-8 bg-background">
        <div className="max-w-4xl mx-auto text-center">
          <div className="bg-gradient-card p-12 rounded-2xl border border-border shadow-card">
            <h2 className="text-2xl md:text-3xl font-bold text-foreground mb-4">
              Stay Ahead of the Curve
            </h2>
            <p className="text-lg text-muted-foreground mb-8">
              Get the latest insights on AI and Blockchain delivered to your
              inbox weekly
            </p>
            <div className="flex flex-col sm:flex-row gap-4 max-w-md mx-auto">
              <input
                type="email"
                placeholder="Enter your email"
                className="flex-1 px-4 py-3 bg-background border border-border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
              />
              <Button className="bg-gradient-primary hover:shadow-glow transition-all duration-300 px-8">
                Subscribe
              </Button>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Home;
