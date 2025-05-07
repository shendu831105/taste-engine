import React, { useState } from 'react';

interface PreferenceFormProps {
    onSubmit: (input: string) => Promise<void>;
    loading: boolean;
}

const PreferenceForm: React.FC<PreferenceFormProps> = ({ onSubmit, loading }) => {
    const [input, setInput] = useState('');

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!input.trim()) return;
        await onSubmit(input);
    };

    return (
        <form onSubmit={handleSubmit} className="space-y-4">
            <div>
                <label htmlFor="input" className="block text-sm font-medium text-gray-700">
                    描述你的品味偏好
                </label>
                <textarea
                    id="input"
                    rows={4}
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    placeholder="例如：我喜欢带有黑色幽默但结局不那么悲惨的科幻电影"
                    disabled={loading}
                />
            </div>
            <button
                type="submit"
                disabled={loading || !input.trim()}
                className={`w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white 
          ${loading || !input.trim()
                        ? 'bg-indigo-400 cursor-not-allowed'
                        : 'bg-indigo-600 hover:bg-indigo-700'} 
          focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500`}
            >
                {loading ? '生成推荐中...' : '获取推荐'}
            </button>
        </form>
    );
};

export default PreferenceForm; 