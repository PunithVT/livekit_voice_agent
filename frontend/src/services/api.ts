// src/services/api.ts

export interface ModuleType {
  id: number;
  title: string;
  slug: string;
  description: string;
  icon_name: string;
  duration: string;
  order: number;
  is_active: boolean;
  created_at: string;
  updated_at: string;
  lessons?: Array<{
    id: number;
    title: string;
    content: string;
    code_snippet: string;
    explanation: string;
    order: number;
    is_exercise: boolean;
    expected_output: string | null;
  }>;
}

interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

const API_BASE_URL = "http://127.0.0.1:8000/api"

export const api = {
  getModules: async (): Promise<ModuleType[]> => {
    try {
      console.log('Fetching modules from:', `${API_BASE_URL}/modules/`);
      const response = await fetch(`${API_BASE_URL}/modules/`, {
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include',
      });
      
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        console.error('API Error:', {
          status: response.status,
          statusText: response.statusText,
          errorData
        });
        throw new Error(`Failed to fetch modules: ${response.status} ${response.statusText}`);
      }

      const data: PaginatedResponse<ModuleType> = await response.json();
      console.log('API Response:', data);
      
      // Return the results array from the paginated response
      return Array.isArray(data.results) ? data.results : [];
    } catch (error) {
      console.error('Error in getModules:', error);
      return [];
    }
  },

  getModule: async (id: number): Promise<ModuleType | null> => {
    try {
      const response = await fetch(`${API_BASE_URL}/modules/${id}/`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return await response.json();
    } catch (error) {
      console.error(`Error fetching module ${id}:`, error);
      return null;
    }
  }
};

export default api;