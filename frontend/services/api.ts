export type Category = "OPEN" | "OBC-NCL" | "SC" | "ST" | "EWS";
export type CollegeType = "IIT" | "NIT" | "IIIT" | "GFTI" | "ALL";
export type Gender = "Gender-Neutral" | "Female-only";

export type ExamType = "JEE_MAIN" | "JEE_ADVANCED";

export interface PredictRequest {
  exam_type?: ExamType;
  rank: number;
  category: Category;
  college_type: CollegeType;
  gender: Gender;
  home_state?: string | null;
  include_five_year: boolean;
}

export interface CollegeResult {
  institute: string;
  program: string;
  branch: string;
  program_type: string;
  college_type: string;
  quota: string;
  seat_type: string;
  gender: string;
  opening_rank: number;
  closing_rank: number;
  rank_gap: number;
  chance_category: string;
  branch_priority: number;
  priority: number;
}

export interface PredictResponse {
  rank: number;
  category: string;
  college_type: string;
  total_results: number;
  results: CollegeResult[];
  developed_by?: string;
  linkedin?: string;
}

/**
 * Using your live Render backend URL.
 * If you run locally, it will prioritize the environment variable if set.
 */
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "https://smartcounsellor.onrender.com";

export async function fetchPredictions(request: PredictRequest): Promise<PredictResponse> {
  const response = await fetch(`${API_BASE_URL}/api/predict`, {
    method: "POST",
    headers: { 
      "Content-Type": "application/json",
    },
    body: JSON.stringify(request),
  });
  
  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.message || "Failed to fetch predictions from the server");
  }
  
  return response.json();
}
