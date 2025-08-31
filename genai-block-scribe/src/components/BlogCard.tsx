import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { CalendarDays, Clock, ArrowRight } from "lucide-react";
import { Link } from "react-router-dom";

interface BlogPost {
  id: string;
  title: string;
  excerpt: string;
  category: "GenAI" | "Blockchain";
  readTime: string;
  publishedAt: string;
  image?: string;
  featured?: boolean;
}

interface BlogCardProps {
  post: BlogPost;
  featured?: boolean;
}

const BlogCard = ({ post, featured = false }: BlogCardProps) => {
  const cardSize = featured ? "lg:col-span-2" : "";

  return (
    <Card className={`group bg-gradient-card backdrop-blur-sm border-border/50 hover:shadow-glow transition-all duration-300 hover:scale-[1.02] h-full flex flex-col ${cardSize}`}>
      {post.image && (
        <div className="relative overflow-hidden rounded-t-lg">
          <img
            src={post.image}
            alt={post.title}
            className={`w-full object-cover transition-transform duration-300 group-hover:scale-105 ${
              featured ? "h-64" : "h-48"
            }`}
          />
          <div className="absolute inset-0 bg-gradient-to-t from-black/50 to-transparent" />
        </div>
      )}
      
      <CardHeader className="space-y-3 flex-grow">
        <div className="flex items-center justify-between flex-wrap gap-2">
          <Badge 
            variant={post.category === "GenAI" ? "default" : "secondary"}
            className={`${
              post.category === "GenAI" 
                ? "bg-primary/90 text-primary-foreground hover:bg-primary" 
                : "bg-accent/90 text-accent-foreground hover:bg-accent"
            } font-medium`}
          >
            {post.category}
          </Badge>
          {post.featured && (
            <Badge variant="outline" className="border-accent/50 text-accent bg-accent/10">
              Featured
            </Badge>
          )}
        </div>
        
        <CardTitle className={`${featured ? "text-2xl" : "text-xl"} leading-tight group-hover:text-primary transition-colors line-clamp-2`}>
          {post.title}
        </CardTitle>
        
        <CardDescription className={`${featured ? "text-base" : "text-sm"} text-muted-foreground line-clamp-3 flex-grow`}>
          {post.excerpt}
        </CardDescription>
      </CardHeader>
      
      <CardContent className="space-y-4 mt-auto">
        <div className="flex items-center text-sm text-muted-foreground space-x-4 pb-2">
          <div className="flex items-center space-x-1">
            <CalendarDays className="w-4 h-4" />
            <span>{post.publishedAt}</span>
          </div>
          <div className="flex items-center space-x-1">
            <Clock className="w-4 h-4" />
            <span>{post.readTime}</span>
          </div>
        </div>
        
        <Link to={`/blog/${post.id}`}>
          <Button className="w-full group/btn bg-gradient-primary hover:shadow-glow transition-all duration-300">
            Read More
            <ArrowRight className="w-4 h-4 ml-2 transition-transform group-hover/btn:translate-x-1" />
          </Button>
        </Link>
      </CardContent>
    </Card>
  );
};

export default BlogCard;