import { useState, useEffect } from "react";
import { useParams, Navigate } from "react-router-dom";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { BlogPost as BlogPostType } from "@/data/blogPosts";
import { CalendarDays, Clock, ArrowLeft, Share2, BookOpen } from "lucide-react";
import { Link } from "react-router-dom";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

const BlogPost = () => {
  const { id } = useParams<{ id: string }>();
  const [post, setPost] = useState<BlogPostType | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchPost = async () => {
      if (!id) return;
      try {
        const response = await fetch(
          `${import.meta.env.VITE_API_URL}/posts/${id}`
        );
        if (!response.ok) {
          throw new Error("Blog post not found");
        }
        const data = await response.json();

        const transformedPost: BlogPostType = {
          id: data.id.toString(),
          title: data.title,
          excerpt:
            data.meta_description ||
            (data.content
              ? data.content.slice(0, 150) + "..."
              : "No excerpt available"),
          content: data.content || "",
          category:
            data.topic === "GenAI" || data.topic === "Blockchain"
              ? data.topic
              : "GenAI",
          readTime: `${Math.ceil((data.word_count || 0) / 200)} min read`,
          publishedAt: new Date(data.created_at).toLocaleDateString("en-US", {
            year: "numeric",
            month: "long",
            day: "numeric",
          }),
          tags: data.tags || [],
        };

        setPost(transformedPost);
      } catch (err) {
        setError(
          err instanceof Error ? err.message : "An unknown error occurred"
        );
      } finally {
        setIsLoading(false);
      }
    };

    fetchPost();
  }, [id]);

  if (isLoading) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <div className="text-2xl">Loading post...</div>
      </div>
    );
  }

  if (error) {
    return <Navigate to="/404" replace />;
  }

  if (!post) {
    return <Navigate to="/blog" replace />;
  }

  // TODO: Implement fetching related posts from the API
  const relatedPosts: BlogPostType[] = [];

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <div className="bg-gradient-card border-b border-border">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <Link to="/blog">
            <Button variant="ghost" className="mb-8 hover:bg-secondary">
              <ArrowLeft className="w-4 h-4 mr-2" />
              Back to Blog
            </Button>
          </Link>

          <div className="space-y-6">
            <div className="flex items-center space-x-4">
              <Badge
                variant={post.category === "GenAI" ? "default" : "secondary"}
                className={`${
                  post.category === "GenAI"
                    ? "bg-primary text-primary-foreground"
                    : "bg-accent text-accent-foreground"
                }`}
              >
                {post.category}
              </Badge>
              {post.featured && (
                <Badge variant="outline" className="border-accent text-accent">
                  Featured
                </Badge>
              )}
            </div>

            <h1 className="text-4xl md:text-5xl font-bold text-foreground leading-tight">
              {post.title}
            </h1>

            <p className="text-xl text-muted-foreground leading-relaxed">
              {post.excerpt}
            </p>

            <div className="flex items-center justify-between pt-6 border-t border-border">
              <div className="flex items-center space-x-6 text-muted-foreground">
                <div className="flex items-center space-x-2">
                  <CalendarDays className="w-5 h-5" />
                  <span>{post.publishedAt}</span>
                </div>
                <div className="flex items-center space-x-2">
                  <Clock className="w-5 h-5" />
                  <span>{post.readTime}</span>
                </div>
                <div className="flex items-center space-x-2">
                  <BookOpen className="w-5 h-5" />
                  <span>Article</span>
                </div>
              </div>

              <Button
                variant="outline"
                size="sm"
                className="hover:bg-secondary"
              >
                <Share2 className="w-4 h-4 mr-2" />
                Share
              </Button>
            </div>
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="prose prose-lg max-w-none prose-invert">
          <ReactMarkdown remarkPlugins={[remarkGfm]}>
            {post.content}
          </ReactMarkdown>
        </div>

        {/* Tags */}
        <div className="mt-12 pt-8 border-t border-border">
          <h3 className="text-lg font-semibold text-foreground mb-4">Tags</h3>
          <div className="flex flex-wrap gap-2">
            {post.tags.map((tag) => (
              <Badge key={tag} variant="secondary" className="text-sm">
                {tag}
              </Badge>
            ))}
          </div>
        </div>

        {/* Related Posts */}
        {relatedPosts.length > 0 && (
          <div className="mt-16 pt-8 border-t border-border">
            <h3 className="text-2xl font-bold text-foreground mb-8">
              Related Articles
            </h3>
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
              {relatedPosts.map((relatedPost) => (
                <Link
                  key={relatedPost.id}
                  to={`/blog/${relatedPost.id}`}
                  className="group"
                >
                  <div className="bg-gradient-card p-6 rounded-lg border border-border hover:shadow-glow transition-all duration-300 hover:scale-[1.02]">
                    <Badge
                      variant={
                        relatedPost.category === "GenAI"
                          ? "default"
                          : "secondary"
                      }
                      className={`mb-3 ${
                        relatedPost.category === "GenAI"
                          ? "bg-primary text-primary-foreground"
                          : "bg-accent text-accent-foreground"
                      }`}
                    >
                      {relatedPost.category}
                    </Badge>
                    <h4 className="font-semibold text-foreground group-hover:text-primary transition-colors line-clamp-2 mb-2">
                      {relatedPost.title}
                    </h4>
                    <p className="text-sm text-muted-foreground line-clamp-3 mb-3">
                      {relatedPost.excerpt}
                    </p>
                    <div className="flex items-center text-xs text-muted-foreground space-x-3">
                      <span>{relatedPost.publishedAt}</span>
                      <span>{relatedPost.readTime}</span>
                    </div>
                  </div>
                </Link>
              ))}
            </div>
          </div>
        )}

        {/* CTA */}
        <div className="mt-16 pt-8 border-t border-border text-center">
          <div className="bg-gradient-card p-8 rounded-xl border border-border">
            <h3 className="text-xl font-bold text-foreground mb-3">
              Enjoyed this article?
            </h3>
            <p className="text-muted-foreground mb-6">
              Subscribe to our newsletter for more insights on AI and Blockchain
            </p>
            <Button className="bg-gradient-primary hover:shadow-glow transition-all duration-300">
              Subscribe Now
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default BlogPost;
