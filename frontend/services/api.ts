export type Category = "OPEN" | "OBC-NCL" | "SC" | "ST" | "EWS";
export type CollegeType = "IIT" | "NIT" | "IIIT" | "GFTI" | "ALL";
export type Gender = "Gender-Neutral" | "Female-only";

export interface PredictRequest {
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
  priority: number;
}

export interface PredictResponse {
  rank: number;
  category: string;
  college_type: string;
  total_results: number;
  results: CollegeResult[];
}

export async function fetchPredictions(request: PredictRequest): Promise<PredictResponse> {
  const response = await fetch("http://localhost:8000/api/predict", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(request),
  });
  
  if (!response.ok) {
    throw new Error("Failed to fetch predictions");
  }
  
  return response.json();
}
