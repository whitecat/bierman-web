export interface Questions {
    questions: Question[];
}

export interface Question {
    question: string;
    answer: string;
    difficulty: string;
    component: string;
    type: string;
}

export type ApiResponse = Questions | { error: string };
export type ApiLoadingState = boolean;
