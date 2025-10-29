import React, { useState } from 'react';
import styled from 'styled-components';
import { motion } from 'framer-motion';
import Editor from '@monaco-editor/react';
import { FiCode, FiCopy, FiPlay, FiSave } from 'react-icons/fi';

const EditorContainer = styled(motion.div)`
  display: flex;
  flex-direction: column;
  background: rgba(30, 41, 59, 0.8);
  border-radius: 16px;
  overflow: hidden;
  border: 1px solid rgba(51, 65, 85, 0.3);
  backdrop-filter: blur(10px);
  height: 100%;
  min-height: 500px;
  max-height: 70vh;
  width: 100%;
`;

const EditorHeader = styled.div`
  padding: 1rem 1.5rem;
  background: rgba(15, 23, 42, 0.5);
  border-bottom: 1px solid rgba(51, 65, 85, 0.3);
  display: flex;
  justify-content: space-between;
  align-items: center;
  
  h3 {
    margin: 0;
    color: #E2E8F0;
    font-size: 1rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }
`;

const EditorActions = styled.div`
  display: flex;
  gap: 0.5rem;
`;

const ActionButton = styled(motion.button)`
  background: rgba(51, 65, 85, 0.5);
  border: 1px solid rgba(51, 65, 85, 0.3);
  color: #94A3B8;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.8rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.3s ease;
  
  &:hover {
    background: rgba(16, 185, 129, 0.2);
    color: #10B981;
    border-color: #10B981;
  }

  &.primary {
    background: linear-gradient(135deg, #10B981 0%, #3B82F6 100%);
    color: white;
    border: none;
    
    &:hover {
      background: linear-gradient(135deg, #059669 0%, #2563EB 100%);
      transform: translateY(-2px);
    }
  }
`;

const EditorContent = styled.div`
  flex: 1;
  position: relative;
  width: 100%;
  height: 100%;
  min-height: 400px;
  
  /* Target Monaco Editor container */
  .monaco-editor {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
  }
  
  /* Target the editor's root element */
  .monaco-editor .overflow-guard {
    border-radius: 0 0 16px 16px;
    overflow: hidden;
  }
`;

const LanguageSelector = styled.select`
  background: rgba(15, 23, 42, 0.5);
  border: 1px solid rgba(51, 65, 85, 0.3);
  color: #E2E8F0;
  padding: 0.5rem;
  border-radius: 6px;
  font-size: 0.8rem;
  cursor: pointer;
  margin-right: 1rem;
  
  &:focus {
    outline: none;
    border-color: #10B981;
  }

  option {
    background: #1E293B;
    color: #E2E8F0;
  }
`;

interface CodeEditorProps {
  initialCode?: string;
}

const CodeEditor: React.FC<CodeEditorProps> = ({ initialCode = '' }) => {
  const [code, setCode] = useState<string>(initialCode || `# Welcome to the Code Editor!
# You can write and edit code here in any language.

# Try changing the language from the dropdown above
# and see the syntax highlighting change!

def hello_world():
    print("Hello, World!")
    return "Python is awesome!"

# Call the function
result = hello_world()
print(result)`);

  const [language, setLanguage] = useState('python');

  const languageTemplates = {
    python: `# Welcome to Python!
def greet(name):
    return f"Hello, {name}!"

print(greet("World"))`,

    javascript: `// Welcome to JavaScript!
function greet(name) {
    return \`Hello, \${name}!\`;
}

console.log(greet("World"));`,

    typescript: `// Welcome to TypeScript!
function greet(name: string): string {
    return \`Hello, \${name}!\`;
}

console.log(greet("World"));`,

    java: `// Welcome to Java!
public class Main {
    public static void main(String[] args) {
        System.out.println("Hello, World!");
    }
    
    public static String greet(String name) {
        return "Hello, " + name + "!";
    }
}`,

    cpp: `// Welcome to C++!
#include <iostream>
#include <string>

using namespace std;

string greet(string name) {
    return "Hello, " + name + "!";
}

int main() {
    cout << greet("World") << endl;
    return 0;
}`,

    csharp: `// Welcome to C#!
using System;

class Program {
    static void Main() {
        Console.WriteLine("Hello, World!");
    }
    
    static string Greet(string name) {
        return $"Hello, {name}!";
    }
}`,

    go: `// Welcome to Go!
package main

import "fmt"

func greet(name string) string {
    return fmt.Sprintf("Hello, %s!", name)
}

func main() {
    fmt.Println(greet("World"))
}`,

    rust: `// Welcome to Rust!
fn main() {
    println!("Hello, World!");
}

fn greet(name: &str) -> String {
    format!("Hello, {}!", name)
}`,

    html: `<!-- Welcome to HTML! -->
<!DOCTYPE html>
<html>
<head>
    <title>My Page</title>
</head>
<body>
    <h1>Hello, World!</h1>
    <p>Welcome to my website.</p>
</body>
</html>`,

    css: `/* Welcome to CSS! */
body {
    font-family: Arial, sans-serif;
    background-color: #f0f0f0;
    margin: 0;
    padding: 20px;
}

.container {
    max-width: 800px;
    margin: 0 auto;
    background: white;
    padding: 20px;
    border-radius: 8px;
}`,

    sql: `-- Welcome to SQL!
SELECT * FROM users WHERE age > 18;

-- Create a table
CREATE TABLE users (
    id INT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(255)
);

-- Insert data
INSERT INTO users (id, name, email) 
VALUES (1, 'John Doe', 'john@example.com');`
  };

  const handleCopy = () => {
    navigator.clipboard.writeText(code);
    console.log('Code copied to clipboard!');
  };

  const handleRun = () => {
    try {
      console.log('Running code:', code);
      console.log('Language:', language);
    } catch (error) {
      console.error('Execution error:', error);
    }
  };

  const handleSave = () => {
    console.log('Code saved!');
  };

  const handleEditorChange = (value: string | undefined) => {
    setCode(value || '');
  };

  const handleLanguageChange = (newLanguage: string) => {
    setLanguage(newLanguage);
    setCode(languageTemplates[newLanguage as keyof typeof languageTemplates] || `// Welcome to ${newLanguage}!\n// Start coding here...`);
  };

  return (
    <EditorContainer
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.2 }}
    >
      <EditorHeader>
        <h3>
          <FiCode size={18} />
          Multi-Language Code Editor
        </h3>
        
        <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
          <LanguageSelector 
            value={language} 
            onChange={(e) => handleLanguageChange(e.target.value)}
          >
            <option value="python">Python</option>
            <option value="javascript">JavaScript</option>
            <option value="typescript">TypeScript</option>
            <option value="java">Java</option>
            <option value="cpp">C++</option>
            <option value="csharp">C#</option>
            <option value="go">Go</option>
            <option value="rust">Rust</option>
            <option value="html">HTML</option>
            <option value="css">CSS</option>
            <option value="sql">SQL</option>
          </LanguageSelector>
          
          <EditorActions>
            <ActionButton
              onClick={handleSave}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              <FiSave size={14} />
              Save
            </ActionButton>
            <ActionButton
              onClick={handleCopy}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              <FiCopy size={14} />
              Copy
            </ActionButton>
            <ActionButton
              onClick={handleRun}
              className="primary"
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              <FiPlay size={14} />
              Run
            </ActionButton>
          </EditorActions>
        </div>
      </EditorHeader>
      
      <EditorContent>
        <Editor
          height="100%"
          width="100%"
          language={language}
          value={code}
          onChange={handleEditorChange}
          theme="vs-dark"
          options={{
            minimap: { enabled: true },
            fontSize: 14,
            fontFamily: "'Fira Code', monospace",
            lineNumbers: 'on',
            scrollBeyondLastLine: false,
            automaticLayout: true,
            readOnly: false,
            wordWrap: 'on',
            tabSize: 4,
            insertSpaces: true,
            detectIndentation: true,
            trimAutoWhitespace: true,
            formatOnType: true,
            formatOnPaste: true,
            suggestOnTriggerCharacters: true,
            acceptSuggestionOnEnter: "on",
            cursorBlinking: "smooth",
            scrollbar: {
              vertical: 'auto',
              horizontal: 'auto',
              useShadows: true,
              verticalHasArrows: false,
              horizontalHasArrows: false,
              verticalScrollbarSize: 10,
              horizontalScrollbarSize: 10,
              verticalSliderSize: 10,
              horizontalSliderSize: 10,
            },
            renderLineHighlight: 'all',
            fixedOverflowWidgets: true,
            lineDecorationsWidth: 10,
            overviewRulerBorder: false,
            hideCursorInOverviewRuler: true,
            renderWhitespace: 'selection',
            renderLineHighlightOnlyWhenFocus: true,
            matchBrackets: 'always',
            folding: true,
            foldingHighlight: true,
            showFoldingControls: 'always',
            guides: {
              indentation: true,
              highlightActiveIndentation: true
            }
          }}
          onMount={(editor) => {
            // Force a layout after the editor is mounted
            setTimeout(() => {
              editor.layout();
            }, 0);
          }}
        />
      </EditorContent>
    </EditorContainer>
  );
};

export default CodeEditor;