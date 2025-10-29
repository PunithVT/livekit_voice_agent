import { createGlobalStyle } from 'styled-components';

export const GlobalStyle = createGlobalStyle`
  * {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
  }
  
  body {
    background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
    color: #E2E8F0;
    line-height: 1.6;
    min-height: 100vh;
  }
  
  #root {
    min-height: 100vh;
  }
  
  /* Custom Scrollbar */
  ::-webkit-scrollbar {
    width: 8px;
    height: 8px;
  }
  
  ::-webkit-scrollbar-track {
    background: #0F172A;
  }
  
  ::-webkit-scrollbar-thumb {
    background: #334155;
    border-radius: 4px;
    border: 2px solid #0F172A;
    
    &:hover {
      background: #475569;
    }
  }
  
  *::selection {
    background: #10B981;
    color: white;
  }
`;