import ReactMarkdown from 'react-markdown';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { atomDark } from 'react-syntax-highlighter/dist/esm/styles/prism';

export default function Documentation() {
  const documentation = `
# Database Query Assistant Documentation

## Getting Started

Our AI-powered database assistant helps you interact with your databases using natural language. Simply describe what you want to do, and we'll generate the appropriate query.

\`\`\`sql
-- Example: "Show all active users"
SELECT * FROM users WHERE status = 'active';
\`\`\`

## Supported Query Types

1. **SQL Queries**
   - SELECT statements
   - INSERT operations
   - UPDATE records
   - DELETE operations

2. **MongoDB Queries**
   - Find documents
   - Update operations
   - Aggregation pipelines

3. **API Requests**
   - REST endpoints
   - GraphQL queries
   - Custom integrations

## Best Practices

- Be specific in your requests
- Include relevant conditions
- Specify the target database
- Review generated queries before execution
`;

  return (
    <div className="py-24 px-4 max-w-4xl mx-auto">
      <h1 className="text-4xl font-bold mb-2 bg-clip-text text-transparent bg-gradient-to-r from-[#00ff00] to-[#00cc00]">
        Documentation
      </h1>
      <p className="text-gray-400 mb-8 text-lg">Learn how to use the Database Assistant effectively</p>

      <div className="prose prose-invert max-w-none">
        <ReactMarkdown
          components={{
            code({node, inline, className, children, ...props}) {
              const match = /language-(\w+)/.exec(className || '');
              return !inline && match ? (
                <SyntaxHighlighter
                  style={atomDark}
                  language={match[1]}
                  PreTag="div"
                  className="border border-[#00ff00]/30 rounded-lg !bg-black/30"
                  {...props}
                >
                  {String(children).replace(/\n$/, '')}
                </SyntaxHighlighter>
              ) : (
                <code className="bg-black/30 px-1 rounded" {...props}>
                  {children}
                </code>
              );
            }
          }}
        >
          {documentation}
        </ReactMarkdown>
      </div>
    </div>
  );
}