import { useState } from 'react'
import './App.css'
import PreferenceForm from './components/PreferenceForm'
import RecommendationList from './components/RecommendationList'

interface Recommendation {
    title: string;
    description: string;
}

function App() {
    const [recommendations, setRecommendations] = useState<Recommendation[]>([])
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState<string | null>(null)

    const handleSubmit = async (input: string) => {
        setLoading(true)
        setError(null)
        try {
            const response = await fetch('http://localhost:8000/api/recommend', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ input }),
            })

            if (!response.ok) {
                throw new Error('推荐生成失败')
            }

            const data = await response.json()
            setRecommendations(data.recommendations)
        } catch (err) {
            setError(err instanceof Error ? err.message : '发生未知错误')
            console.error('Error:', err)
        } finally {
            setLoading(false)
        }
    }

    return (
        <div className="min-h-screen bg-gray-100 py-6 flex flex-col justify-center sm:py-12">
            <div className="relative py-3 sm:max-w-xl sm:mx-auto">
                <div className="relative px-4 py-10 bg-white shadow-lg sm:rounded-3xl sm:p-20">
                    <div className="max-w-md mx-auto">
                        <div className="divide-y divide-gray-200">
                            <div className="py-8 text-base leading-6 space-y-4 text-gray-700 sm:text-lg sm:leading-7">
                                <h1 className="text-3xl font-bold text-center mb-8">个性化品味引擎</h1>
                                {error && (
                                    <div className="bg-red-50 border-l-4 border-red-400 p-4 mb-4">
                                        <p className="text-red-700">{error}</p>
                                    </div>
                                )}
                                <PreferenceForm onSubmit={handleSubmit} loading={loading} />
                            </div>
                            <RecommendationList recommendations={recommendations} />
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default App 