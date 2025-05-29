import { describe, it, expect, vi, beforeEach } from 'vitest';
import { analyzeCodebaseByUrl, analyzeCodebaseByFile } from './analyze';

const backendApiUrl = 'http://localhost:3000';
const mockResponseData = { result: 'success', data: { summary: 'Test summary' } };
const mockErrorResponse = { error: 'Something went wrong' };

// Helper to create a mock File object
function createMockFile(filename = 'test.txt', content = 'test content') {
    return new File([content], filename, { type: 'text/plain' });
}

describe('analyzeCodebaseByUrl', () => {
    beforeEach(() => {
        vi.resetAllMocks();
        globalThis.fetch = vi.fn();
    });

    it('sends POST request and returns data on success', async () => {
        (fetch as unknown as ReturnType<typeof vi.fn>).mockResolvedValueOnce({
            ok: true,
            json: async () => mockResponseData,
        });
        const result = await analyzeCodebaseByUrl(backendApiUrl, 'https://github.com/example/repo');
        expect(fetch).toHaveBeenCalledWith(
            `${backendApiUrl}/analyze/url/`,
            expect.objectContaining({
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ url: 'https://github.com/example/repo', llm: false, focus: undefined, openai_api_key: undefined })
            })
        );
        expect(result).toEqual(mockResponseData);
    });

    it('sends options in request body if provided', async () => {
        (fetch as unknown as ReturnType<typeof vi.fn>).mockResolvedValueOnce({
            ok: true,
            json: async () => mockResponseData,
        });
        await analyzeCodebaseByUrl(backendApiUrl, 'https://github.com/example/repo', { llm: true, focus: 'backend', openai_api_key: 'sk-123' });
        expect(fetch).toHaveBeenCalledWith(
            `${backendApiUrl}/analyze/url/`,
            expect.objectContaining({
                body: JSON.stringify({ url: 'https://github.com/example/repo', llm: true, focus: 'backend', openai_api_key: 'sk-123' })
            })
        );
    });

    it('throws error with message from backend on non-ok response', async () => {
        (fetch as unknown as ReturnType<typeof vi.fn>).mockResolvedValueOnce({
            ok: false,
            status: 400,
            json: async () => mockErrorResponse,
        });
        await expect(analyzeCodebaseByUrl(backendApiUrl, 'bad-url')).rejects.toThrow('Error 400: Something went wrong');
    });

    it('throws error on fetch failure', async () => {
        (fetch as unknown as ReturnType<typeof vi.fn>).mockRejectedValueOnce(new Error('Network error'));
        await expect(analyzeCodebaseByUrl(backendApiUrl, 'any')).rejects.toThrow('Network error');
    });
});

describe('analyzeCodebaseByFile', () => {
    beforeEach(() => {
        vi.resetAllMocks();
        globalThis.fetch = vi.fn();
    });

    it('sends POST request with FormData and returns data on success', async () => {
        (fetch as unknown as ReturnType<typeof vi.fn>).mockResolvedValueOnce({
            ok: true,
            json: async () => mockResponseData,
        });
        const file = createMockFile();
        const result = await analyzeCodebaseByFile(backendApiUrl, file);
        expect(fetch).toHaveBeenCalledWith(
            `${backendApiUrl}/analyze/file/`,
            expect.objectContaining({
                method: 'POST',
                body: expect.any(FormData),
            })
        );
        expect(result).toEqual(mockResponseData);
    });

    it('includes options in FormData if provided', async () => {
        (fetch as unknown as ReturnType<typeof vi.fn>).mockResolvedValueOnce({
            ok: true,
            json: async () => mockResponseData,
        });
        const file = createMockFile();
        await analyzeCodebaseByFile(backendApiUrl, file, { llm: true, focus: 'frontend', openai_api_key: 'sk-456' });
        const lastCall = (fetch as unknown as ReturnType<typeof vi.fn>).mock.calls[0][1];
        const formData = lastCall.body as FormData;
        expect(formData.get('llm')).toBe('true');
        expect(formData.get('focus')).toBe('frontend');
        expect(formData.get('openai_api_key')).toBe('sk-456');
    });

    it('throws error with message from backend on non-ok response', async () => {
        (fetch as unknown as ReturnType<typeof vi.fn>).mockResolvedValueOnce({
            ok: false,
            status: 500,
            json: async () => mockErrorResponse,
        });
        const file = createMockFile();
        await expect(analyzeCodebaseByFile(backendApiUrl, file)).rejects.toThrow('Error 500: Something went wrong');
    });

    it('throws error on fetch failure', async () => {
        (fetch as unknown as ReturnType<typeof vi.fn>).mockRejectedValueOnce(new Error('Network error'));
        const file = createMockFile();
        await expect(analyzeCodebaseByFile(backendApiUrl, file)).rejects.toThrow('Network error');
    });
});
