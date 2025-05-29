import React, {useState} from 'react';
import {analyzeCodebaseByUrl, analyzeCodebaseByFile} from './services/analyze';
import {ApiLoadingState, Question} from './types/response.types';

const App: React.FC = () => {
    const [searchTerm, setSearchTerm] = useState('');
    const [focus, setFocus] = useState('');
    const [useLLM, setUseLLM] = useState(false);
    const [isLoading, setIsLoading] = useState<ApiLoadingState>();
    const [questions, setQuestions] = useState<Question[]>();
    const [file, setFile] = useState<File | null>(null);
    const [errorMsg, setErrorMsg] = useState<string | null>(null);
    const backendApiUrl = import.meta.env.VITE_BACKEND_API_URL;

    const handleSearch = () => {
        setQuestions([]);
        setIsLoading(true);

        analyzeCodebaseByUrl(backendApiUrl, searchTerm, { llm: useLLM, focus })
            .then(result => {
                if (result && Array.isArray(result.questions)) {
                    setQuestions(result.questions);
                } else if (Array.isArray(result)) {
                    setQuestions(result);
                } else if (result && result.error) {
                    setQuestions([{ question: result.error, answer: '', difficulty: '', component: '', type: '' }]);
                }
            })
            .catch(_ => {
                setQuestions([{ question: 'An error occurred.', answer: '', difficulty: '', component: '', type: '' }]);
            })
            .finally(() => {
                setIsLoading(false);
            });
    };

    const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files && e.target.files.length > 0) {
            setFile(e.target.files[0]);
        }
    };

    const handleFileAnalyze = (e: React.FormEvent) => {
        e.preventDefault();
        if (!file) return;
        setQuestions([]);
        setIsLoading(true);
        analyzeCodebaseByFile(backendApiUrl, file, { llm: useLLM, focus })
            .then(result => {
                if (result && Array.isArray(result.questions)) {
                    setQuestions(result.questions);
                } else if (Array.isArray(result)) {
                    setQuestions(result);
                } else if (result && result.error) {
                    setQuestions([{ question: result.error, answer: '', difficulty: '', component: '', type: '' }]);
                }
            })
            .catch(_ => {
                setQuestions([{ question: 'An error occurred.', answer: '', difficulty: '', component: '', type: '' }]);
            })
            .finally(() => {
                setIsLoading(false);
            });
    };

    return (
        <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100 p-4">
            <h1 className="text-4xl font-bold text-gray-800 mb-6">Interview Question page</h1>
            <form
                className="flex items-center space-x-4 mb-4"
                onSubmit={e => {
                    e.preventDefault();
                    if (searchTerm) {
                        setErrorMsg(null);
                        handleSearch();
                    } else if (file) {
                        setErrorMsg(null);
                        handleFileAnalyze(e);
                    } else {
                        setErrorMsg('Please enter a URL or upload a zip file.');
                    }
                }}
            >
                <input
                    type="text"
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    placeholder="URL to analyze"
                    className="p-3 border border-gray-300 rounded-md w-[400px] bg-white"
                />
                <label htmlFor="file-upload" className="sr-only">Upload</label>
                <input
                    id="file-upload"
                    type="file"
                    accept=".zip"
                    onChange={handleFileUpload}
                    className="hidden"
                />
                <span className="mx-2 text-gray-500 font-semibold">or</span>
                <label htmlFor="file-upload" className="p-3 border border-gray-300 rounded-md w-[220px] bg-white cursor-pointer text-center">
                    {file ? file.name : 'Upload file'}
                </label>
                <label className="flex items-center space-x-2">
                    <input
                        type="checkbox"
                        checked={useLLM}
                        onChange={e => setUseLLM(e.target.checked)}
                    />
                    <span>Use LLM</span>
                </label>
                <input
                    type="text"
                    value={focus}
                    onChange={e => setFocus(e.target.value)}
                    placeholder="Focus (optional)"
                    className={`p-3 border border-gray-300 rounded-md w-[200px] ${useLLM ? 'bg-white' : 'bg-gray-200'}`}
                    disabled={!useLLM}
                />
                <button
                    type="submit"
                    className="bg-blue-500 text-white px-6 py-3 rounded-md hover:bg-blue-600"
                    disabled={isLoading}
                >
                    {isLoading ? 'Analyzing...' : 'Analyze'}
                </button>
            </form>
            {errorMsg && (
                <div className="text-red-600 font-semibold mb-2">{errorMsg}</div>
            )}
            {questions && questions.length > 0 && (
                <div className="bg-white rounded-lg shadow-md p-6 w-full max-w-2xl mt-6">
                    <h2 className="text-2xl font-semibold mb-4">Generated Questions</h2>
                    <ul className="space-y-4">
                        {questions.map((q, idx) => (
                            <li key={idx} className="border-b pb-4 last:border-b-0">
                                <div className="font-bold text-lg text-blue-700 mb-1">{q.question}</div>
                                {q.answer && <div className="text-gray-700 mb-1"><span className="font-semibold">Answer:</span> {q.answer}</div>}
                                <div className="text-sm text-gray-500">Difficulty: {q.difficulty || 'N/A'} | Component: {q.component || 'N/A'} | Type: {q.type || 'N/A'}</div>
                            </li>
                        ))}
                    </ul>
                </div>
            )}
        </div>
    );
};

export default App;
