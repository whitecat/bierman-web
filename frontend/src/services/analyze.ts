export const analyzeCodebaseByUrl = async (
    backendApiUrl: string,
    url: string,
    options?: { llm?: boolean; focus?: string; openai_api_key?: string }
) => {
    const endpoint = '/analyze/url/';
    const response = await fetch(`${backendApiUrl}${endpoint}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            url,
            llm: options?.llm ?? false,
            focus: options?.focus,
            openai_api_key: options?.openai_api_key,
        }),
    });
    if (!response.ok) {
        const errorBody = await response.json();
        throw new Error(`Error ${response.status}: ${errorBody.error}`);
    }
    return await response.json();
};

export const analyzeCodebaseByFile = async (
    backendApiUrl: string,
    file: File,
    options?: { llm?: boolean; focus?: string; openai_api_key?: string }
) => {
    const endpoint = '/analyze/file/';
    const formData = new FormData();
    formData.append('file', file);
    if (options?.llm !== undefined) formData.append('llm', String(options.llm));
    if (options?.focus) formData.append('focus', options.focus);
    if (options?.openai_api_key) formData.append('openai_api_key', options.openai_api_key);
    const response = await fetch(`${backendApiUrl}${endpoint}`, {
        method: 'POST',
        body: formData,
    });
    if (!response.ok) {
        const errorBody = await response.json();
        throw new Error(`Error ${response.status}: ${errorBody.error}`);
    }
    return await response.json();
};
