import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import App from './App';
import { analyzeCodebaseByUrl, analyzeCodebaseByFile } from './services/analyze';

vi.mock('./services/analyze', () => ({
    analyzeCodebaseByUrl: vi.fn(),
    analyzeCodebaseByFile: vi.fn(),
}));

describe('App Component', () => {
    beforeEach(() => {
        vi.stubEnv('VITE_BACKEND_API_URL', 'http://mockapi.com');
    });

    afterEach(() => {
        vi.unstubAllGlobals();
        vi.resetAllMocks();
    });

    it('renders all main UI elements', () => {
        render(<App />);
        expect(screen.getByText('Interview Question page')).toBeInTheDocument();
        expect(screen.getByPlaceholderText('URL to analyze')).toBeInTheDocument();
        expect(screen.getByPlaceholderText('Focus (optional)')).toBeInTheDocument();
        expect(screen.getByRole('checkbox', { name: /Use LLM/i })).toBeInTheDocument();
        expect(screen.getByRole('button', { name: /Analyze/i })).toBeInTheDocument();
        expect(screen.getByLabelText(/Use LLM/i)).toBeInTheDocument();
    });

    it('updates input fields and checkbox', () => {
        render(<App />);
        const urlInput = screen.getByPlaceholderText('URL to analyze');
        const focusInput = screen.getByPlaceholderText('Focus (optional)');
        const llmCheckbox = screen.getByRole('checkbox', { name: /Use LLM/i });
        fireEvent.change(urlInput, { target: { value: 'https://github.com/test/repo' } });
        fireEvent.change(focusInput, { target: { value: 'auth' } });
        fireEvent.click(llmCheckbox);
        expect(urlInput).toHaveValue('https://github.com/test/repo');
        expect(focusInput).toHaveValue('auth');
        expect(llmCheckbox).toBeChecked();
    });

    it('shows error message if neither URL nor file is provided', () => {
        render(<App />);
        fireEvent.click(screen.getByRole('button', { name: /Analyze/i }));
        expect(screen.getByText('Please enter a URL or upload a zip file.')).toBeInTheDocument();
    });

    it('calls analyzeCodebaseByUrl and displays loading state', async () => {
        vi.mocked(analyzeCodebaseByUrl).mockResolvedValue({ questions: [{ question: 'Q1', answer: 'A1', difficulty: '', component: '', type: '' }] });
        render(<App />);
        const urlInput = screen.getByPlaceholderText('URL to analyze');
        fireEvent.change(urlInput, { target: { value: 'https://github.com/test/repo' } });
        fireEvent.click(screen.getByRole('button', { name: /Analyze/i }));
        expect(screen.getByRole('button')).toBeDisabled();
        expect(screen.getByRole('button')).toHaveTextContent('Analyzing...');
        await waitFor(() => {
            expect(analyzeCodebaseByUrl).toHaveBeenCalled();
            expect(screen.getByText('Generated Questions')).toBeInTheDocument();
            expect(screen.getByText('Q1')).toBeInTheDocument();
            expect(screen.getByText(/Answer:/)).toBeInTheDocument();
        });
    });

    it('calls analyzeCodebaseByFile and displays loading state', async () => {
        vi.mocked(analyzeCodebaseByFile).mockResolvedValue([{ question: 'Q2', answer: 'A2', difficulty: '', component: '', type: '' }]);
        render(<App />);
        const fileInput = screen.getByLabelText(/upload/i);
        const file = new File(['dummy content'], 'test.zip', { type: 'application/zip' });
        fireEvent.change(fileInput, { target: { files: [file] } });
        fireEvent.click(screen.getByRole('button', { name: /Analyze/i }));
        expect(screen.getByRole('button')).toBeDisabled();
        expect(screen.getByRole('button')).toHaveTextContent('Analyzing...');
        await waitFor(() => {
            expect(analyzeCodebaseByFile).toHaveBeenCalled();
            expect(screen.getByText('Q2')).toBeInTheDocument();
        });
    });

    it('displays error message on API error', async () => {
        vi.mocked(analyzeCodebaseByUrl).mockRejectedValue(new Error('API error'));
        render(<App />);
        const urlInput = screen.getByPlaceholderText('URL to analyze');
        fireEvent.change(urlInput, { target: { value: 'https://github.com/test/repo' } });
        fireEvent.click(screen.getByRole('button', { name: /Analyze/i }));
        await waitFor(() => {
            expect(screen.getByText('An error occurred.')).toBeInTheDocument();
        });
    });
});
